# 合并链 G1：一次作答里的多个信号怎么合成题分

一个分数从原子信号走到榜单数字，最多经过四层合并：

```
原子信号 → G1 题内 → G2 多次采样 → G3 题集 → G4 跨 bench → 榜单数字
```

每层都可能不存在（编码里记"—"）。这一章讲第一层：一次作答被判出很多个信号（很多个测试、很多条细则、很多个判官的判定）时，怎么合成这一次作答的分。细则类 bench 的头条数字主要由这一层决定，同一份判定换个合法口径，可以从 0.75 变成 0。

| 取值 | 定义 | 例子 | 清单里在用的行数 |
|---|---|---|---|
| 单信号 | 一次作答只有一个信号 | HLE、ScreenSpot-Pro | 110 |
| 全过 | 所有测试、细则、维度都过才算 1；多个二值维度相乘也是全过 | SWE-bench、Terminal-Bench、APEX-Agents、GDP.pdf 头条 | 37 |
| 比例 | 过了几成给几成 | OSWorld partial、GDP.pdf 的 Mean Pass | 22 |
| 加权 | 每条有分值，可以有负分 | HealthBench、ARC-AGI-3 | 20 |
| 层级树 | 子目标逐层加权平均 | PaperBench | 1 |
| 集合:F1 / 集合:全召回精度 / 集合:精确 | 答案是集合，按命中情况算分 | DeepSearchQA、ITBench-AA、VoiceCodeBench | 5 / 1 / 2 |
| 阈值 | 连续或比例分过线才算通过 | MCP Atlas（覆盖率 ≥0.75） | 13 |
| 门控 | 某个条件一触发，整题清零 | AutomationBench、Harvey LAB-AA | 11 |
| 归一化 | 把题分换算到"最弱基线 = 0、某参照 = 固定值"的刻度上 | MLS-Bench-Lite、Vals RSI Index | 2 |
| 判官:平均占比 / 多数 / 一致 / 重复众数 / 单侧覆盖 / 抽一个 | 多个判官或同一判官多次判，怎么合成一个判定 | Harvey、MLCR-AA、IMO 2026、Vals、AA-AnalystAgent、GDPval-AA | 3 / 4 / 3 / 1 / 1 / 2 |

一行可以叠用几种，比如 Harvey LAB-AA 是"判官:平均占比 + 全过 + 门控"。

---

<a id="all-pass"></a>
## 全过和比例

一道题有很多个二值信号时，最直接的两种合法：全部通过才给 1（全过），或者按通过的比例给分（比例）。再往上一层（题集）还要选：把所有细则摊平了平均（micro，微平均），还是先在每题内平均、再在题之间平均（macro，宏平均）。

$$
\text{micro}=\frac{\sum_t\sum_{c\in t}y_{tc}}{\sum_t\lvert t\rvert},\qquad
\text{macro}=\frac{1}{T}\sum_t\frac{1}{\lvert t\rvert}\sum_{c\in t}y_{tc},\qquad
\text{全过}=\frac{1}{T}\sum_t\prod_{c\in t}y_{tc}
$$

算一遍：两个任务，任务 1 有 10 条细则过了 9 条，任务 2 有 2 条过了 0 条。

| 口径 | 计算 | 结果 |
|---|---|---|
| micro | 9/12 | 0.75 |
| macro | (0.9+0)/2 | 0.45 |
| 全过 | (0+0)/2 | 0 |

同一份判定，从 0.75 到 0。（`python3 scripts/basics.py` §11）

真实榜单：

- GDP.pdf（AA 版）：头条 All-pass 是 500 次作答（100 题 × 5 次）里每条细则都通过的比例，次指标 Mean Pass 是任务宏平均的细则通过率。
- Legal Research Bench（Vals）：同一张榜上 all-pass 55.29、加权通过率 90.58。
- Vals Finance Agent v2 同时报 partial credit 和 all-pass，两种口径下名次会翻转。
- Harvey LAB：Grok 4.7 发布页报 19.6%（全过口径），Kimi K3 报逐条通过率 94.6。这两个数来自不同模型，量级差距主要来自口径。只看厂商表格，读者分不出用的是哪种。
- SWE-bench 的 FULL、τ²-bench 的 DB × COMMUNICATE、IFEval 的 prompt 级都是全过；SWE-bench 的 PARTIAL（报告时不计）、OSWorld partial、IFEval 的 instruction 级是比例。

坑：全过很陡，非常依赖判官在边界情况上的判断。报全过时应同时给出比例口径，否则读者分不清"差一点"和"差很多"。全过和比例排出来的名次可以不同。

<a id="weighted"></a>
## 加权

每条细则有分值，可以为负，题分 = 满足条目的分值和 ÷ 正分值总和：

$$
s_i=\frac{\sum_c \mathrm{pts}_c\cdot\mathbb{1}[\mathrm{met}_c]}{\sum_{c:\,\mathrm{pts}_c>0}\mathrm{pts}_c},\qquad
\text{总分}=\operatorname{clip}_{[0,1]}\Big(\frac{1}{N}\sum_i s_i\Big)
$$

HealthBench 式例子：五条细则 +5（满足）、+3（满足）、+2（未满足）、−4（触发了）、−2（未触发）。分子 5+3−4 = 4，分母 5+3+2 = 10，题分 0.40；如果没触发那条 −4，题分是 0.80。另一个例子：+5 "建议立即就医"、+3 "询问症状持续多久"、+2 "表达简洁"、−4 "给出具体处方剂量"，回答满足了 +5、+2，也犯了 −4，题分 (5+2−4)/(5+3+2) = 0.3。单题分可以是负数，HealthBench 在全集平均之后才裁到 [0,1]；裁剪放在哪一层，会改均值。（[HealthBench](https://arxiv.org/abs/2505.08775)）

ARC-AGI-3 的 RHAE 也是加权，权重是关卡号，而且每关的分来自人类标尺：

$$
\text{关分}_\ell=\min\Big(1.15,\ \Big(\frac{h_\ell}{a_\ell}\Big)^{2}\Big),\qquad
\text{游戏分}=\frac{\sum_\ell \ell\cdot\text{关分}_\ell}{\sum_{\ell=1}^{L}\ell}
$$

$h_\ell$ 是人类首次游玩者动作数的"上中位数"，$a_\ell$ 是 AI 的动作数，没通的关记 0，总分是各游戏分的平均。

例 1：3 关游戏，人类基线 10、20、30 步；AI 第 1 关 10 步，第 2 关 40 步，第 3 关没过。关分 1、$(20/40)^2=0.25$、0，游戏分 = (1×1+2×0.25+3×0)/6 = 0.25，已通关卡的权重上限是 (1+2)/6 = 0.5。多用一倍动作，那一关只剩 1/4 分。

例 2：5 关，人类基线 10、12、20、25、30，AI 只通了前 4 关，动作数 10、24、18、50。关分 1、0.25、1.15、0.25，游戏分 = (1·1+2·0.25+3·1.15+4·0.25)/15 = 0.3967，已通关卡的权重上限 10/15 = 0.6667。如果 AI 前 4 关都比人快很多（每关 1.15），按公式得 0.7667，超过官方文档"无论多高效也不超过已完成关卡权重占比"的说法。官方实现里应另有一道截断，文档没写。（[ARC-AGI-3 方法](https://docs.arcprize.org/methodology)）

坑：平方让效率惩罚很陡，ARC-AGI-3 测的主要是效率；只数改变环境的动作，内部推理和工具调用不计。

Video-MME v2（2026-04）也是组内非线性：一组 4 题答对 N 题记 $(N/4)^2$，推理组从第一道错题起截断，所以 v1 和 v2 的数字不能混着比。

## 层级树

把任务拆成子目标，叶子是可以判过或不过的具体要求，父节点分数 = 子节点的加权平均。PaperBench 让模型复现 ICML 论文，每篇论文一棵评分树，共 8316 个叶子。

例子：根节点下三个子节点 A（权重 3）、B（权重 1）、C（权重 2）。A 的两个叶子一过一不过，A = 0.5；B = 1；C 的两个叶子（权重 2、1）只过了权重 1 的那个，C = 1/3。根 = (3×0.5 + 1×1 + 2×1/3)/6 = 0.528。（[PaperBench](https://arxiv.org/abs/2504.01848)）

<a id="set"></a>
## 集合匹配

答案是一组东西时，有三种算法。提交集合记 $S$，标准集合记 $G$：

$$
P=\frac{\lvert S\cap G\rvert}{\lvert S\rvert},\qquad R=\frac{\lvert S\cap G\rvert}{\lvert G\rvert},\qquad F_1=\frac{2PR}{P+R}
$$

- 集合:F1：漏报和多报都扣分，有召回就有分。DeepSearchQA 每题算 F1 再平均当主排名指标（单答案题的 F1 就是精确匹配），同时报 Fully Correct、Fully Incorrect、Correct with Extraneous 三类。GraphWalks 也用集合 F1。HiL-Bench 的 ASK-F1（提问精确率和阻塞召回率的调和平均）、WANDR 的逐题 P/R/F1（分 soft 和 hard）也归这里。
- 集合:全召回精度：漏一个就是 0，不漏时才看精确率 $TP/(TP+FP)$。ITBench-AA 用这个。
- 集合:精确：$S=G$ 才算对。VoiceCodeBench 要求一段录音里所有实体都对。

ITBench-AA 的例子：两个根因组 {svc-a, pod-a-1}（pod-a-1 是 svc-a 的别名）和 {db}，另有一个非根因 svc-b。同一组里报多个成员只算一次，没匹配上的和映射到非根因的都算误报。

| 提交 | F1 | 全召回精度 |
|---|---|---|
| 只报 svc-a | 0.667 | 0 |
| svc-a、db | 1 | 1 |
| svc-a、pod-a-1、db（多报一个别名） | 0.800（不做别名合并时） | 1 |
| svc-a、db、svc-b | 0.800 | 0.667 |
| 撒网报 6 个 | 0.500 | 0.333 |

（`python3 scripts/mechanisms.py` §6）

全召回精度专门惩罚少报；报全以后，它对多报的惩罚比 F1 更重，因为召回率为 1 时 $F_1=2P/(P+1)\ge P$。ITBench-AA 有 59 个场景（40 个公开、19 个私有），每个跑 3 次，GPT-5.5 medium 负责实体归一化。AA 汇总表里把它叫 "average precision at full recall"，这里的 average 指对任务和重复取平均，和信息检索里按排序累计的 Average Precision 不是一回事。实体归一化由 LLM 做，等于在程序判官里又嵌了一个 LLM 判官。（[AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)、[ITBench](https://arxiv.org/abs/2502.05352)、[DeepSearchQA](https://arxiv.org/abs/2601.20975)）

<a id="threshold"></a>
## 阈值

连续分或比例分过了某条线才算通过，相当于把 S3 变回 S1：

$$
s=\mathbb{1}[x\ge\tau]
$$

例子：MCP Atlas 每个要点 1/0.5/0，覆盖率 ≥0.75 算通过，另报平均覆盖率；ProgramBench 有 100% 和 ≥95% 两条线；Remote Labor Index 评级 ≥2 算达标；LifeSciBench ≥70%；`$OneMillion-Bench` ≥0.7；FrontierScience Research ≥7/10；Claw-Eval ≥0.75；DrugDiscoveryBench 必须 100 分；MysteryMechanism 要求归一化误差低于噪声阈值。

坑：线放在哪是人定的，同一组连续分，线一挪名次就变；离线很近的模型被硬切成 0 和 1。

<a id="gate"></a>
## 门控

某个条件一触发，整题清零，不管其他部分做得多好：

$$
s=\mathbb{1}[\text{没触发}]\times s_{\text{原}}
$$

- AutomationBench（AA 指数 5%）：断言分成目标和护栏，碰了任何护栏整题 0 分，否则按完成的目标比例给分。
- Harvey LAB-AA：有实质性幻觉的题记 0。检查分两步：一个"列举判官"列出疑似虚假陈述并引证，一个"怀疑判官"（GPT-6 Sol high）对照同一份材料逐条维持、驳回或合并，并重新定严重程度；只有实质性幻觉才清零。
- MRCR v2：缺哈希前缀记 0。MLCR-AA：回答超过参考答案 5 倍长直接记 0。
- FrontierCode：任一 blocker 不过直接 0；v1.1 起违规联网的试跑记 0。Code Migration：作弊直接 0。
- Claw-Eval：安全分做乘法门控，安全 × (0.8·完成 + 0.2·鲁棒)。Tax Agent Bench：全过以后再乘引用质量。
- SHADE-Arena、LinuxArena：副任务完成、而且监控给的可疑分低于阈值，才算"隐蔽成功"。

坑：和全过一样陡。门控条件本身常由另一个判官判，这个判官的错误会直接变成整题 0 分。

## 归一化

把题分换到一个以基线为零点的刻度上：

$$
s=\frac{x-x_{\text{基线}}}{x_{\text{参照}}-x_{\text{基线}}}\times\text{参照对应的分}
$$

- MLS-Bench-Lite：最弱基线 = 0，人类 SOTA 作参考，理论上界 = 100。
- Vals RSI Index：起点 = 0，参考 = 0.5，最优 = 1，在对数尺度上换算。
- AA Endpoint Accuracy Index：服务商端点的分 ÷ 自托管参考端点的分。

坑：基线和参照选谁，决定了 0 和满分落在哪里，换基线等于换尺子。这和 [G4a](08-g4-cross-bench.md#g4a) 里 AA 把 Elo 映射到 0–1 是同一类操作，只是发生在题内。

---

<a id="judge-merge"></a>
## 判官合并

同一条细则有多个判官，或同一个判官判了多次，要先合成一个判定。判官 $k=1..K$ 对细则 $c$ 给出 $v_{kc}\in\lbrace 0,1\rbrace$，六种真实在用的做法：

| 子值 | 公式 | 谁在用 |
|---|---|---|
| 平均占比 | $s_c=\frac1K\sum_k v_{kc}$ | Harvey LAB-AA（每条细则取 3 判官通过占比：0、⅓、⅔、1）；FACTS Grounding 事实分是 3 个判官分数的平均 |
| 多数 | $s_c=\mathbb{1}\big[\sum_k v_{kc}>K/2\big]$ | MLCR-AA（3 判官对准确性、完整性分别多数表决）；FORTRESS；PoLL（二值题用多数，1–5 分用平均） |
| 一致 | $s_c=\prod_k v_{kc}$ | Anthropic IMO 2026（3 判官须一致）；FACTS Grounding 取消资格要 3 个判官都认为不合格；JudgeBench 换位判两次须一致 |
| 重复众数 | 同一判官判 3 次取众数 | Vals Finance Agent（判官 GPT-5.2）；PostTrainBench 污染判定 3 次里 2 次同意才成立 |
| 单侧覆盖 | $s_c=\max(v^{\text{LLM}}_c,\ v^{\text{程序}}_c)$ | AA-AnalystAgent：Gemini 3 Flash 判，再加程序数值预检，预检只能把错改成对，永远不把判过的改成不过 |
| 抽一个 | 每条细则或每场对局从判官池抽一个，Crowd-BT 的可靠度吸收判官差异 | GDPval-AA v2.1、AA-Briefcase v1.1（同一条细则永远由同一个判官判） |

Harvey 的头条在合并顺序上还有讲究：它是"每个判官先看自己是否判全部细则通过，再对判官取占比"，

$$
s_{\text{题}}=\frac1K\sum_k\prod_c v_{kc}
$$

先乘后平均，和"逐条多数后再全过"不同。

### 同一份判定，六种合法

一个任务、5 条细则、3 个判官。判官 1 判 [1,1,1,0,1]，判官 2 判 [1,1,0,1,1]，判官 3 判 [1,1,1,1,1]。

| 规则 | 逐条结果 | 这一题算全过吗 |
|---|---|---|
| 平均占比 | [1, 1, ⅔, ⅔, 1]，逐条通过率 0.867 | — |
| 多数 | [1,1,1,1,1] | 1 |
| 一致 | [1,1,0,0,1] | 0 |
| Harvey 式（判官内全过再取占比） | 只有判官 3 全过 | ⅓ |
| 抽一个判官 | 期望 ⅓，但单次只能是 0 或 1 | 0 或 1 |
| 单侧覆盖（另一例：LLM [0,1,0,1]，程序预检 [1,0,0,1]） | [1,1,0,1] | — |

同一份答卷，"全过"可以是 1、0 或 ⅓。（`python3 scripts/mechanisms.py` §5）

### 对方差和偏差的影响

模拟：100 题，真实通过率 0.60，每个判官独立以 15% 的概率判错，重复 4000 次。

| 规则 | 均值 | 标准差 | 理论期望 |
|---|---|---|---|
| 单判官 | 0.569 | 0.0357 | 0.570 |
| 三判官平均 | 0.570 | 0.0205 | 0.570 |
| 多数 | 0.588 | 0.0238 | 0.588 |
| 一致 | 0.369 | 0.0379 | 0.370 |

平均和单判官的偏差一样，标准差小了近一半；多数票偏差最小；一致规则在判官对称犯错时严重偏低。一致规则只在"判官更容易错放、不容易错杀"时有意义，它用召回率换精确率，IMO 证明评分研究里一致规则精确率 0.855、多数票召回率 0.912（见[元评测](01-judge.md#meta)）。

坑：

- 先合并还是先全过要写清楚。Harvey 式和"逐条多数后全过"在上例里差 ⅓ 和 1。
- 重复众数是对判定投票，maj@k 是对被测模型的答案投票，两者在同一组数据上可以给出 0 和 1（见 [G2 maj@k](06-g2-sampling.md#maj)）。
- 抽一个判官时，必须固定"同一条细则同一判官"，否则跨模型比较时混进了判官噪声。
- Arena-Hard v2 的"换位判两次"是为了抵消位置偏差，归在[修正](09-conditions-corrections-uncertainty.md#corrections)里讲。
