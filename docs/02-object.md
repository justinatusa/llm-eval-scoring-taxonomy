# 对象 O：判的是什么东西

同一个判官，可以判模型给一段文本的概率，也可以判它写出来的代码、它改过的数据库，或者一整段真实对话。对象这条轴把这些分开。预训练评测和后训练评测的差别主要在这条轴上：前者常常只读概率（O1），后者让模型生成后再判（O2、O3、O4），判官和合并方式可以完全一样。

| 代号 | 名称 | 怎么认出来 | 例子 | 清单里在用的行数 |
|---|---|---|---|---|
| O1 | 概率 | 不让模型生成，直接读它给某段文本或某个选项的概率，需要 logprob | OLMo 3 Base Easy、Uncheatable Eval、RewardBench 2（读奖励模型给 4 个回答的分） | 3 |
| O2 | 短答案 | 一个数、一个选项、一个实体、一个集合、一个网格，可以抽出来逐个比 | HLE、CritPt、AA-LCR、GraphWalks、ARC-AGI-2 | 76 |
| O3 | 产物 | 长回答、代码或补丁、文件、报告、证明、CAD，甚至训好的模型权重 | SWE-bench Pro、GDP.pdf、GDPval-AA、PostTrainBench | 94 |
| O4 | 环境终态 | 做完以后数据库、文件系统、虚拟机、账户余额、对局结果变成什么样 | Terminal-Bench、τ²-bench、AutomationBench、OSWorld、Vending-Bench 2 | 32 |
| O5 | 过程 | 推理步骤、动作序列、动作数；结果相同、过程不同，分数就不同 | ARC-AGI-3（动作数）、ProcessBench、CoT-pass@k | 6 |
| O6 | 真实会话 | 一整段真实用户和模型的交互，没有预设题目 | Agent Arena、Arena Alignment Index、OpenRouter | 3 |

两条固定搭配：读概率只能靠计算，所以 O1 的判官总是 J1a；用户行为 J5 只会出现在真实会话 O6 上。

---

<a id="o1"></a>
## O1 概率

基座模型往往还不会好好答题，所以预训练阶段大量用"不生成、只算概率"的打分方式。

### 困惑度和每字节比特数（BPB）

把一段标准文本喂给模型，看它对每个下一个 token 平均有多意外。文本切成 $T$ 个 token，总负对数似然（自然对数，单位 nats）是

$$
\mathrm{NLL}=-\sum_{t=1}^{T}\ln p(x_t\mid x_{<t})
$$

$$
\text{token 级困惑度}=\exp\!\Big(\frac{\mathrm{NLL}}{T}\Big),\qquad
\mathrm{BPB}=\frac{\mathrm{NLL}}{B\cdot\ln 2}
$$

$B$ 是这段文本的 UTF-8 字节数。

例子：同一段 100 字节的英文，模型 A 和模型 B 的总 NLL 都是 46 nats。A 的分词器切出 25 个 token，困惑度 $e^{46/25}=6.30$；B 切出 40 个，困惑度 $e^{46/40}=3.16$。两者 BPB 都是 $46/(100\ln 2)=0.664$。困惑度差了一倍，只是因为分母是 token 数；BPB 的分母是字节数，和分词器无关。再换一组数：44 字节的句子，10 个 token、每个 2.3 nats，BPB = 0.7541；换一个分词器切成 20 个 token、每个 1.15 nats，BPB 还是 0.7541。所以跨分词器只能比 BPB（或每字符比特数），不能比 token 级困惑度。

在哪用：DeepSeek-V3 在 Pile-test 上用 BPB；OLMo 3 的 Base Easy 套件算答案部分的 BPB；Microsoft 的 MAI-Thinking-1（2026）用约 40 个 NLL 基准做训练目标，在 4 个保留任务上用 BPB 对比 DS-V4-Pro、Kimi-K2、Gemma4-31B 等基座；Uncheatable Eval（2026-09）用新语料上的压缩率给 80 个模型排名，新语料可以避开训练集污染。

坑：lm-eval 的 `bits_per_byte` 先在全集上加总再除（加权平均），和逐条平均再除结果不同；评测文本进过训练集，困惑度会虚低；困惑度只能比同一份文本。

### 用对数似然做选择题：CF、MCF、acc 和 acc_norm

不让模型写答案，把每个选项分别接在题干后面，看模型觉得哪个最顺，选最顺的；选对记 1。两种问法（OLMES 的叫法）：

- CF（完形填空式）：题干后直接接选项原文，比较 $\ln P(\text{选项原文}\mid\text{题干})$。
- MCF（字母选项式）：A/B/C/D 都列在题里，最后写 "Answer:"，只比较 " A"、" B" 这几个单 token 的概率。

CF 的麻烦是选项长短不一，长选项 token 多，对数概率天然更小，于是有几种归一化：

$$
\text{none: }\ln P(a_i\mid q)\qquad
\text{token: }\frac{\ln P(a_i\mid q)}{\#\text{tokens}(a_i)}\qquad
\text{char: }\frac{\ln P(a_i\mid q)}{\#\text{chars}(a_i)}\qquad
\text{pmi: }\ln\frac{P(a_i\mid q)}{P(a_i\mid \text{"Answer:"})}
$$

例子：题干"把水在一个标准大气压下加热到 100°C，水会"，正确答案是 B。

| 选项 | 字符数 | 总对数概率 | 按字符归一化 |
|---|---|---|---|
| A `" freeze."` | 8 | −3.0 | −0.375 |
| B `" start to boil and turn into steam."` | 35 | −6.1 | −0.174 |
| C `" boil."` | 6 | −3.2 | −0.533 |

不归一化选总对数概率最大的 A，0 分；按字符归一化选 B，1 分。整套题的分数就是这样逐题 0/1 再平均。

同一个名字，不同框架指的东西不同：

| 含义 | lm-eval | OLMES | lighteval |
|---|---|---|---|
| 不归一化 | `acc` | `acc_raw` | `LoglikelihoodAcc()` |
| 按字符数 | `acc_norm` | `acc_per_char` | `LogProbCharNorm` |
| 按 token 数 | — | `acc_per_token` | `LogProbTokenNorm` |
| 按字节数 | `acc_bytes` | （用 `bits_per_byte` 取最小） | — |
| PMI | `acc_mutual_info` | `acc_uncond` | `LogProbPMINorm` |

lm-eval 的 `acc_norm` 是按字符数归一化（代码里是 `lls / completion_len`，`completion_len` 是选项字符串长度），OLMES 文档里却把 `acc_norm` 叫作按 token 归一化。看到 `acc_norm` 先看是哪个框架。（[lm-eval task.py](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/api/task.py#L1489-L1560)、[OLMES metric.py](https://github.com/allenai/olmes/blob/5a51f502d463b8cdc4a2dcad7d7096c41ff1197e/oe_eval/metrics/metric.py#L186-L320)、[lighteval normalizations.py](https://github.com/huggingface/lighteval/blob/7fa19dc6f53a713ba8bb6541e7ed66dad2e24fd7/src/lighteval/metrics/normalizations.py#L470-L535)）

OLMES（AI2，2024）为了可复现定了规矩：超过 1500 条就固定种子抽 1000 条；固定人工挑的 5-shot 示例；每个任务规定归一化方式；MCF 和 CF 都跑，取高的。理由是弱模型做 MCF 接近随机，强模型做 CF 会被选项长短的噪声拖累。OLMES 举的例子：Llama-3 8B 的"25-shot ARC-Challenge"，Meta 报的 MCF 是 78.6%，Open LLM Leaderboard 的 CF 是 60.2%，名字相同，差 18 个点。（[OLMES](https://arxiv.org/abs/2406.08446)）

坑：MCF 里 `"A"` 和 `" A"` 在很多分词器里是不同 token；闭源推理模型常常不给 logprob，只能改成生成式。

### 涌现：离散指标把渐变压成台阶

一道题要连续写对 $L$ 个 token 才算对，每个 token 写对的概率是 $p$，精确匹配准确率约为 $p^{L}$。$L=10$ 时：

| 每 token 正确率 $p$ | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|
| 精确匹配 $p^{10}$ | 0.107 | 0.349 | 0.599 | 0.904 |

$p$ 只从 0.80 涨到 0.99，精确匹配从 0.1 跳到 0.9，看起来像"突然学会"。换成正确答案的对数概率这类连续指标，曲线是平滑的。所以训练中常用连续代理：DataDecide 的 CORRECT PROB（正确选项平均概率）、OLMES 的 `bits_per_byte_corr`（正确答案的 BPB）；Llama 3 先拟合"训练算力 → 正确答案的归一化负对数似然"，再拟合"负对数似然 → 准确率"。DataDecide 报告用这类连续指标在小规模实验里判断"哪个数据配方在 1B 规模更好"，准确率超过 80%，只用 0.01% 的算力。BPB 低不代表生成出来的答案能被抽出来判对，所以它适合同一条训练线上的比较，不适合当最终能力汇报。（[Schaeffer 等](https://arxiv.org/abs/2304.15004)、[DataDecide](https://arxiv.org/abs/2504.11393)）

### 信噪比：这个 bench 适不适合在训练中看

训练中每隔一段存一个检查点去评测，要的是"分数变化能反映真实差别"。AI2 的 Signal and Noise（2025）定义：

$$
\text{噪声}=\frac{\operatorname{sd}(\text{最后 } n \text{ 个检查点的分数})}{\text{这些分数的均值}},\qquad
\text{信号}=\frac{\max_{j,k}\lvert M_j-M_k\rvert}{\bar M},\qquad
\mathrm{SNR}=\frac{\text{信号}}{\text{噪声}}
$$

论文观察到 1B 模型在 ARC-Challenge 上，最后 30 个检查点之间准确率波动有 1.7 个点；两个数据配方如果只差 1–2 个点，在这个 bench 上分不出好坏。OLMo 3 按 SNR 删掉了噪声大的任务（CruxEval 移出平均），并对生成式代码题增大 pass@k 的采样数 n。（[arXiv 2508.13144](https://arxiv.org/abs/2508.13144)）

### DS-V4 的基座表

DS-V4 基座表有 24 项（AGIEval、BBH、C-Eval、HellaSwag、MMLU、WinoGrande 等），表上只标 "EM"，没有说明是生成式还是按困惑度。DeepSeek-V3 报告明确写了 HellaSwag、WinoGrande、MMLU、MMLU-Pro、C-Eval 等用基于困惑度的评测，TriviaQA、MATH、GSM8K、HumanEval 等用生成式。所以 DS-V4 基座表的对象只能编成"O2 或 O1，未说明"。（[DeepSeek-V3](https://arxiv.org/abs/2412.19437)、[DS-V4](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)）

---

## O2 短答案

### few-shot 生成加精确匹配

给几道带答案的示例题，让模型照着格式写答案，再用正则抠出来逐字比。lm-eval 的 GSM8K 有两套抽取口径，标准答案 `18`，模型输出：

```
She sells 16 - 3 - 4 = 9 eggs, earning 9 * 2 = $18 per day.
Question: ...（模型接着编了一道新题，里面有 "#### 7"）
```

`strict-match` 用正则 `#### (\-?[0-9\.\,]+)` 取第一个匹配，抓到 7，0 分。`flexible-extract` 取最后一个数字，也可能抓到后面编出来的数。lm-eval 的 GSM8K 配置用 `until: ["Question:", ...]` 截断生成，就是为了防止"接着编下一题"；截断设置不同，同一个模型分数就不同。只写"GSM8K 8-shot"不写抽取口径，数字没法比。（[gsm8k.yaml](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/tasks/gsm8k/gsm8k.yaml)）

### 集合和网格

答案可以是一组实体（GraphWalks 的节点集合、ITBench-AA 的根因集合、DeepSearchQA 的答案列表），也可以是一个网格（ARC-AGI-2）。集合怎么算分见 [G1 集合匹配](05-g1-within-item.md#set)。

---

## O3 产物

需要整体检查或运行才能判的东西：长回答、代码或补丁、文件交付物、报告、证明、CAD 模型。PostTrainBench 的产物是一个训好的模型，判官要再拿它去跑 bench（见 [J1b 嵌套评测](01-judge.md#nested)）。O3 是清单里最多的对象（94 行），这些 bench 的头条数字主要由 [G1 怎么合并细则](05-g1-within-item.md)决定。

## O4 环境终态

只看做完以后世界的状态，不看说了什么、走了哪条路。判法见 [J1b 环境终态](01-judge.md#env-state)。

---

<a id="o5"></a>
## O5 过程

结果一样、过程不同，分数就不同。

过程奖励模型（PRM）给每一步打一个"这一步正确"的概率，整条解答的分是各步概率的乘积：

$$
\operatorname{score}(\text{解答})=\prod_{t=1}^{T}P(\text{第 } t \text{ 步正确})
$$

例子：4 步，各步正确概率 0.95、0.9、0.3、0.95，乘积 0.244。第 3 步大概率有错，这条解答在 best-of-N 里排不上去，即使最终答案碰巧对了。（[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)）

其他过程类做法：

- CoT-pass@k：推理过程和答案都对才算对。在这个口径下，RL 后的模型在各个 k 上都比基座好；只看答案时，基座模型在大 k 上常靠"推理错但蒙对"追上来。（[arXiv 2506.14245](https://arxiv.org/abs/2506.14245)）
- ARC-AGI-3：看通关用了多少个改变环境的动作，和人类首玩的动作数比（公式见 [G1 加权](05-g1-within-item.md#weighted)）。
- τ²-bench 的 ACTION 奖励：要求调用过某些工具，只在少数 banking 任务里用。
- ProcessBench：被评者找出最早出错的那一步，这是元评测（见[判官一章](01-judge.md#meta)）。

2026 年的厂商发布页和技术报告里，没有找到用过程分当头条的例子。FrontierSWE v2 用"加权指令数"衡量产物的运行效率，评的是代码跑得快不快，和 agent 的过程无关，所以不算 O5。过程分需要步骤切分和步骤标注，成本远高于结果分；Qwen 团队还发现，用蒙特卡洛续写合成的步骤标签效果不如 LLM 判官或人工标注。（[arXiv 2501.07301](https://arxiv.org/abs/2501.07301)）

## O6 真实会话

一整段真实用户和模型的交互，没有预设题目。Agent Arena 和 OpenRouter 的判法见 [J5](01-judge.md#j5)。LMArena 的 Alignment Index（2026-10-08 预览）也读真实会话，但判官是按细则检测"越权行动、错误归因、谎报完成"三类事件的 LLM，计算方法见 [G3a 变换](07-g3-item-set.md#transform)。
