# 判官 J：谁来判这一次输出

判官只回答一个问题：模型这一次交出来的东西，好还是不好。它吐出的结果叫原子信号（一个对错、一个档位、一个分数或一次"谁更好"）。原子信号之后怎么一层层合成榜单数字，归[合并链 G1–G4](05-g1-within-item.md)管，和判官是谁无关。

| 代号 | 名称 | 怎么认出来 | 例子 | 清单里在用的行数 |
|---|---|---|---|---|
| J1a | 抽取比对 | 程序从输出里抠出答案，做精确匹配、数学等价、约束检查、相似度或集合匹配；不运行产物 | CritPt（官方评分服务器）、IFBench（58 个约束函数）、MRCR v2（文本相似度）、MathArena | 65 |
| J1b | 执行与环境 | 要真的运行点什么才知道对错：跑隐藏测试、查数据库终态、结算对局或经营结果，或者把产物再送去跑一轮评测 | SWE-bench Pro、Terminal-Bench 4.0、AutomationBench、Kaggle 国际象棋、PostTrainBench | 71 |
| J1c | 形式化验证 | 证明检查器（Lean 等）判证明是否成立，题目可以没有已知答案 | PutnamBench、Vals ProofBench、FrontierMath: Open Problems | 3 |
| J2 | LLM 判官 | 通用语言模型按提示词判：等价判定、逐条细则、两份谁更好 | HLE、GDP.pdf、Harvey LAB-AA、GDPval-AA | 86 |
| J3 | 学来的打分器 | 专门为打分训练的模型：奖励模型、过程奖励模型、偏好代理模型 | Arena AutoEval | 1 |
| J4 | 人工评判 | 被请来评分的人，知道自己在评分 | Arena 成对投票、GDPval 原版、Remote Labor Index | 8 |
| J5 | 用户行为 | 用户在办自己的事时留下的信号：点批准、表扬或抱怨、用量 | Agent Arena、OpenRouter Rankings | 2 |

行数来自 [data/bench-master.csv](../data/bench-master.csv) 里状态为"在用"的 208 行，一行同时用两种判官时各计一次。

主判官和辅助判官同时出现时写成"主+辅"，比如 ITBench-AA 是 J1a+J2（程序做集合匹配，LLM 先把实体名归一），Agent Arena 是 J5+J1b。辅助判官往往只能朝一个方向改结果，这类规则放在 [G1 的判官合并](05-g1-within-item.md#judge-merge)里讲。

判官单独成一条轴，是因为同一种判官在 Justin 的三类里都会出现。J1b 判 SWE-bench（第 1 类），也判 Kaggle 国际象棋的胜负（第 2 类），还判 METR 的任务成败（第 3 类）。J2 判 HLE 的等价（第 1 类），也判 GDPval-AA 的两两比较（第 2 类）。

---

<a id="j1a"></a>

## J1a 抽取比对

程序先从一大段输出里把"最终答案"抠出来，再和标准答案比。比法有精确匹配、数学等价、约束检查、文本相似度和集合匹配几种。

### 答案抽取

常见的抽取规则有三种：找最后一个 `\boxed{...}`，找 "Answer: X" 这样的标记（OpenAI simple-evals 和 AA 的选择题都用正则），或者干脆取输出里的最后一个数字（lm-eval 的 GSM8K flexible-extract）。

同一组输出用两种规则抽，标准答案是 $\tfrac12$：

| 模型输出 | "最后一个数字"抽到 | 判定 | Math-Verify 抽到 | 判定 |
|---|---|---|---|---|
| `... so the answer is \boxed{\frac{1}{2}}` | `2` | 错（对的被判错） | `1/2` | 对 |
| `The probability is 0.5.` | `0.5` | 看比较方式 | `0.5` | 对 |
| `Therefore the answer is $\dfrac{2}{4}$` | `4` | 错（对的被判错） | `1/2` | 对 |
| `Final Answer: 1/3` | `3` | 错 | `1/3` | 错（本来就错） |
| `I think it's one half` | 无 | 错（对的被判错） | 无 | 错（对的被判错） |

判定规则写成公式就是

$$
s=\mathbb{1}\big[\operatorname{norm}(\operatorname{extract}(y))=\operatorname{norm}(y^{*})\big]
$$

其中 extract 是抽取规则，norm 是规范化（去逗号、去货币符号、转小写）。

真实事故：Hugging Face 的 Open LLM Leaderboard 原来在 MATH-Hard 上要求答案写成 "Final answer is [ANSWER]. I hope it is correct." 再交给 SymPy。2025 年 2 月改用 Math-Verify 重评了 3751 个模型，平均每个模型多对 61 题（+4.66 分），Qwen 系列分数翻了一倍多，DeepSeek 系列接近原来的三倍，因为它们习惯把答案写进 `\boxed{}`，旧规则抓不到。前 20 名几乎全部换了位置。（[HF 博客](https://huggingface.co/blog/math_verify_leaderboard)）

几个坑：

- 抽取失败默认记 0 分，和"答错"混在一起。报告里应该单独给出抽取失败率。
- 取第一个还是最后一个匹配，差别很大。推理模型常常先写一个试探答案再改。
- 要求固定格式，会把"格式遵循"混进"数学能力"。AA 的原则是不因为模型照着提示词作答而扣分，所以用宽松的抽取和灵活的等价判定。
- Huang 等（[arXiv 2505.22203](https://arxiv.org/abs/2505.22203)）测了数学数据集上的规则判定器：精确率高，召回率平均只有 86%，也就是 14% 的正确回答被判错；生成模型越强，答案写法越多样，这个比例越高。

### 数学等价判定

`2/4` 和 `\frac{1}{2}` 字符串不同，数学上相等。等价判定把两边都转成 SymPy 表达式，再做符号比较，或者在容差内做数值比较：

$$
s=\mathbb{1}\big[\operatorname{sympy}(\hat a)\equiv\operatorname{sympy}(a^{*})\big]
\quad\text{或}\quad
s=\mathbb{1}\big[\lvert\hat a-a^{*}\rvert\le\epsilon\big]
$$

Math-Verify 判 `{1,3} ∪ {2,4}` 等于 `{1,2,3,4}`，判 `k = 1` 等于 `1`，判 `1/3` 等于 `0.333333`（旧排行榜判不等）。坑有三个：`verify(gold, answer)` 的参数顺序有意义，标准答案要放前面；容差要看题目，题目要求"精确到 4 位小数"时就不该接受 `0.333`（AA-AnalystAgent 的判官提示就这样规定）；复杂 LaTeX 会让解析器卡死，需要单独进程加超时。（[Math-Verify README](https://github.com/huggingface/Math-Verify/blob/ba3d3aaff23b3f4cac7a14672b4f6e293d97c98b/README.md)）

### 约束检查：strict 和 loose

IFEval、IFBench 一类题给每条可机检的要求配一个检查函数（"全文小写""以某句话结尾"）。strict 口径直接对原始回复跑检查；loose 口径先对回复做 8 种变换（去掉 markdown 的 `*`、去掉第一行、去掉最后一行，以及组合和不变换），任何一种变换后通过就算过：

$$
\operatorname{loose}(r,i)=\bigvee_{t=1}^{8}\operatorname{check}_i\big(\operatorname{transform}_t(r)\big)
$$

例子：两条要求"全文小写"和"以 `P.S. I do like the cake` 结尾"，回复第一行是 `Sure, here it is:`，最后一行是 `P.S. **I do like the cake**`。strict 下两条都不过（第一行有大写，结尾多了 `**`），prompt 级 0、instruction 级 0/2；loose 下"去第一行 + 去 markdown"之后两条都过，prompt 级 1、instruction 级 2/2。prompt 级要求一道题所有要求都满足，instruction 级按条平均，这是 [G1 的全过和比例](05-g1-within-item.md#all-pass)。IFEval 论文自己说 loose 会减少假阴性，也可能放进假阳性。（[IFEval](https://arxiv.org/abs/2311.07911)、[IFBench](https://arxiv.org/abs/2507.02833)）

### 训练用的判定器和测评用的判定器

强化学习里的可验证奖励（RLVR）和测评经常用同一套代码。Tülu 3 的训练数据就叫 `RLVR-IFeval`；OLMo 3 的数学奖励是 SymPy 比对，代码奖励是跑测试，指令遵循奖励是逐条约束检查。两边的要求不同：训练最怕被钻空子，常给部分分让梯度不稀疏，而且必须快；测评最怕误判改名次，一般只认全对，可以慢、可以复核。Huang 等发现，把规则判定器换成模型判定器后召回率从 84% 升到 92%，但在训练中会被策略模型钻空子，只输出一个 `{` 这样的简单模式就能骗到奖励。一个 bench 的判定器被拿去训练以后，这个 bench 的分数就有一部分在测"适配这个判定器"。（[Tülu 3](https://arxiv.org/abs/2411.15124)、[OLMo 3](https://arxiv.org/abs/2512.13961)）

---

<a id="j1b"></a>

## J1b 执行与环境

要知道对不对，必须真的运行点什么。

### 单元测试和隐藏测试

模型写的代码放进沙箱跑一组测试，全部通过才算这次对：

$$
s=\prod_{j=1}^{m}\mathbb{1}[\text{测试 } j \text{ 通过}]
$$

一道题 10 个测试过了 9 个，HumanEval 式口径记 0，不记 0.9。隐藏测试是题面只给几个示例、打分用更多不公开的测试，防止模型针对示例硬写答案。坑：超时、内存上限、沙箱缺包都会被记成失败，和能力无关；测试太弱会放过错误代码（EvalPlus 就是给 HumanEval、MBPP 补测试）。

### SWE-bench 的 FAIL_TO_PASS 和 PASS_TO_PASS

修一个 GitHub issue，看两组测试。`FAIL_TO_PASS` 是修之前失败、修好后应该通过的测试，证明"修好了"；`PASS_TO_PASS` 是修之前就通过、修完不能坏的测试，证明"没弄坏别的"。

$$
\text{F2P 率}=\frac{\#\text{F2P 通过}}{\#\text{F2P}},\qquad \text{P2P 率}=\frac{\#\text{P2P 通过}}{\#\text{P2P}}
$$

两者都等于 1 记 `RESOLVED_FULL`；F2P 部分通过而 P2P 全过记 `RESOLVED_PARTIAL`；其他记 `RESOLVED_NO`。报出来的 "% Resolved" 只数 FULL。

例子：F2P 有两个测试，P2P 有三个老测试。补丁让两个 F2P 都过了，却弄坏一个老测试，F2P 率 1、P2P 率 2/3，结果 `RESOLVED_NO`，0 分。SWE-bench Pro（1865 题，含不公开的保留集和商业代码库）沿用同样的规则。不稳定的测试和装不上的环境会被算成模型失败，所以 harness 里专门有 `infra_failure.py`。（[grading.py](https://github.com/SWE-bench/SWE-bench/blob/02e7a74ffd0b707aab73d203fe87bdc7c76afc8e/swebench/harness/grading.py#L285-L330)、[SWE-bench Pro](https://arxiv.org/abs/2509.16941)）

<a id="env-state"></a>

### 环境终态

代理类题目看做完以后世界变成了什么样，不看说了什么、走了哪条路。

τ²-bench 的奖励默认是两项相乘。DB 项把标准动作序列在全新环境里重放出目标数据库，再比 agent 跑完后的数据库哈希；COMMUNICATE 项检查必须告诉用户的关键信息有没有出现在 agent 的消息里：

$$
r=\mathbb{1}[\text{DB 哈希一致}]\times\mathbb{1}[\text{所有必须告知的信息都说了}]
$$

例子：用户要改签航班，agent 改签对了（DB = 1），但没告诉用户要补 120 美元差价（COMMUNICATE = 0），这次得 0 分。

Terminal-Bench 每题有容器、指令、测试和参考解，测试全过才算通过；AA 把测试放在和 agent 隔离的验证容器里跑，验证超时算失败。OSWorld 每题有一个基于执行的评测脚本，从虚拟机里取文件、设置或网页状态再判断，全集用了 134 个不同的评测函数。EnterpriseOps-Gym 在终态 SQLite 上跑 SQL 验证器，查目标、约束、权限流程和副作用。AutomationBench 把断言分成"目标"和"护栏"，碰了护栏整题 0 分（见 [G1 门控](05-g1-within-item.md#gate)）。

坑：终态检查只能查写了验证器的地方，agent 在没查的地方搞破坏不会扣分，所以要有 PASS_TO_PASS、护栏、"无副作用"这类检查；有的任务有多个合理终态，验证器只写一种就会误判。τ² 系列的"用户"由另一个 LLM 扮演，它属于环境，不属于判官，影响见[出分条件里的用户模拟器](09-conditions-corrections-uncertainty.md#user-simulator)。

<a id="nested"></a>

### 嵌套评测

PostTrainBench 让模型去后训练一个小模型，交上来的产物是模型权重，判官再拿这个小模型跑 7 个 bench，按权重合成一个分；如果判定污染了训练数据，就退回基座模型的分。污染判定要 3 次判官运行里有 2 次同意才成立。（[PostTrainBench](https://posttrainbench.com/)）

---

## J1c 形式化验证

题目写成 Lean 之类的形式化命题，模型交证明，证明检查器编译通过就算解出。它不需要已知答案，所以能出"人类也没解过"的题。

- PutnamBench：Lean 4 题 672 道（另有 Isabelle 640 道、Rocq 412 道），分"给答案"和"不给答案"两个变体，后者要模型自己推出 346 道题里的答案。按解出题数排名，提交时要注明 commit、改动和答案是否忠实于原题。2026 年已有多家 672/672，精选排名改成"全部解出者里每题平均成本最低的排前"，每题平均成本从 0.17 美元到 74 美元不等。（[榜单](https://trishullab.github.io/PutnamBench/leaderboard.html)）
- Vals ProofBench v1.1：Lean 4，100 题，编译通过或不通过，没有部分分。截至 2026-10-07 有 4 个模型并列 100%，页面并报每任务成本。（[页面](https://www.vals.ai/benchmarks/proof_bench)）
- DS-V4：Putnam-200 是 PutnamBench 的固定随机子集，报 Pass@8；Putnam-2025 用形式化加非形式化混合推理报 120/120。（[arXiv 2606.19348](https://arxiv.org/abs/2606.19348)）
- FrontierMath: Open Problems：编译通过即解出。

坑：形式化命题写得和原题不一致时，证明再对也是在证另一件事，所以 PutnamBench 要求审查答案忠实性。题目被做满以后，排名改按成本，bench 测的东西从能力换成了效率，这属于 [G4e 并列不合并](08-g4-cross-bench.md#side-by-side)。

---

## J2 LLM 判官

一个或一组通用语言模型按提示词判，常见三种用法：等价判定、逐条细则、两两比较。

### 等价判定

有标准答案，但答案是自由文本，规则写不全（"Wout Weghorst" 和"韦霍斯特"），就让模型判"这个回答和标准答案是不是一回事"，判官不自己解题。HLE 的判官要输出抽到的最终答案（抽不到写 None）、理由、`correct: yes/no` 和回答里给出的置信度，也就是同时做了抽取和等价判定两步。SimpleQA 的判官给三档：CORRECT、INCORRECT、NOT_ATTEMPTED。AA 的 HLE、AA-LCR、AA-Omniscience 的判官都是 GPT-5.6 Luna (medium)（v4.1.1 起）。（[HLE](https://arxiv.org/abs/2501.14249)、[SimpleQA](https://arxiv.org/abs/2411.04368)）

### 逐条细则

开放式任务由专家给每道题写一组可打勾的条目，判官逐条判"满足没有"。AA 的 GDP.pdf 由单个判官 GPT-5.6 Luna (medium) 判，每次调用只看任务、回答和一条细则，看不到原 PDF，也不知道是哪个模型写的；每条细则都有判定才接受这次评分。（[AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)）

### 两两比较

判官同时看两份输出，说哪份更好。GDPval-AA v2.1 每场从三个判官（Claude Opus 5、GPT-5.6 Sol、Gemini 3.8 Flash）里抽一个盲评两份交付物。这种信号是 [S4 偏好](03-signal.md#s4)。

### 怎么验证判官

拿一批人工标好的样本，比判官和人的一致程度，再和人与人的一致程度比。

| bench | 怎么验证 | 结果 |
|---|---|---|
| SimpleQA | 人工读 100 个"对"、100 个"错"、100 个"未作答" | 只有 2 处和判官不一致 |
| HealthBench | 在共识细则上比较判官和医生 | 模型和医生的一致程度与医生之间相当 |
| PaperBench | JudgeEval：人类专家打过分的提交 | 最好的判官 F1 = 0.83 |
| JudgeBench | 用有客观对错的难题回答对测判官 | 很多强模型（如 GPT-4o）只比随机猜略好 |

### 已知偏差

- 位置偏差：两两比较时偏爱 A 位或 B 位。办法是换位判两次（Arena-Hard）。
- 长度和格式偏差：偏爱长的、markdown 多的回答。办法见[修正](09-conditions-corrections-uncertainty.md#corrections)。
- 自偏好：偏爱自己或同家族的输出。LMArena 2026-09 的研究让 12 个 LLM 在 1460 场真实 Text Arena 对局上盲判，共 34,580 个判定，模型平均有 58% 的时候选自己的回答，人类选同一回答只有 34%；盲判下依然存在，所以只隐藏模型名不够。（[LMArena 博客](https://arena.ai/blog/llm-judge-self-preference)）Arena-Hard v2 的 README 里，同一批模型由 Gemini-2.5 判时 gemini-2.5 得 79.0，换 GPT-4.1 判只有 49.1。办法是多家判官组成评审团，或者排除自评。

<a id="j2-pitfalls"></a>

### 坑

换判官就等于换了一个 bench。下面这些都是真实发生过的：

- GDP.pdf 的 AA 版判官是 GPT-5.6 Luna (medium)，Surge AI 版是 Gemini 3.5 Flash，AA 写明两边分数不能直接比。
- AA-LCR v1.1 改了 16 个答案和判官，与 v1.0 不可比。
- MCP Atlas 在 2026-04 换了判官、加了 100 次工具调用预算，把所有模型重判了一遍。
- Vals 的 CorpFin v2 和 TaxEval v2 在 2025-11-17 把下线的 Claude 3.5 Sonnet 判官换成 Claude 4.5 Sonnet（温度 0）。
- AA 在 v4.1.1 把 HLE、AA-LCR、AA-Omniscience 的判官从 GPT-4o、Qwen3 235B、Gemini 3 Flash Preview 统一换成 GPT-5.6 Luna (medium)。

另外两个细节值得照抄。一是判官输出格式坏了怎么记要事先定好。二是被测回答里可能夹带一句 "GRADE: C" 来骗分，Inspect 的默认判官提示要求判官最后写 `GRADE:`，解析时只取最后一个。（[Inspect scorer](https://github.com/UKGovernmentBEIS/inspect_ai/blob/ba238b00c6da2b61da97577bf839370b1674e847/src/inspect_ai/scorer/_model.py#L405-L462)）

多个判官或同一判官判多次时怎么合成一个判定，见 [G1 判官合并](05-g1-within-item.md#judge-merge)。

---

## J3 学来的打分器

专门为打分训练出来的模型，输出一个标量或概率：奖励模型（RM）给整条回答打分，过程奖励模型（PRM）给每一步打分（例子在 [O5 过程](02-object.md#o5)），偏好代理模型预测"人会选哪个"。

- Arena AutoEval（2026-07-30）：逐点奖励模型给每个回答打分，两份回答的分差经过 softmax 变成"软票"，和人类票一起拟合 BT。与人类榜的秩相关大于 0.98，分差超过 10 分时预测准确率超过 90%。（[博客](https://arena.ai/blog/autoeval-scores)）
- HPSv3 Benchmark（ICCV 2025，图像生成）：直接用 HPSv3 偏好模型的分数给文生图模型排名，分 12 类，例如 Kolors 10.55、Flux-dev 10.43。分数没有上限，参照是开放量 R3。（[arXiv 2508.03789](https://arxiv.org/abs/2508.03789)）

2025 年以后的文本模型厂商报告里，没有找到用 RM 或 PRM 分数当头条的例子，RM 只以"选择器"身份出现，见 [G2 选择器](06-g2-sampling.md#selector)。坑和训练判定器一样：学来的打分器能被针对性地骗分，而且它自己的准确率需要单独评（见本页末尾的元评测）。

---

## J4 人工评判

被请来评分的人。两种主要形式：众包用户盲投（Arena 成对投票，用户看两个匿名回答选一个），以及领域专家盲评（GDPval 让行业专家比较模型交付物和另一位专家的交付物；Remote Labor Index 由 3 人评级取多数，评级 ≥2 算达标）。Anthropic 在 IMO 2026 证明题上用"模型写细则、3 个判官必须一致"再加人工抽查，Opus 5 得 42/42，人工在这里是复核。

坑：贵，样本少，置信区间宽；众包票的来源可以被策略性地操纵，见[修正](09-conditions-corrections-uncertainty.md#leaderboard-illusion)。

---

<a id="j5"></a>

## J5 用户行为

用户在真实使用中留下的痕迹。用户在办自己的事，并没有在打分。

Agent Arena（2026-06-04 上线）随机给真实会话分配编排模型等组件，从会话轨迹里挖五个信号（确认成功、表扬与抱怨、工具幻觉、bash 错误恢复等），每个信号算出相对均匀分配基线的净提升，再五个等权平均成头条 Net Improvement。2026-10-02 的榜上，Claude Fable 5.1 (Max) 的 Net Improvement 是 14.31% ±1.90%，它的 Confirmed Success 一栏是 17.64% ±2.82%；五个信号 (17.64+32.19+8.84+12.39+0.48)/5 = 14.31。统计方法见 [G3b 的 IPS](07-g3-item-set.md#ips)。（[榜单](https://arena.ai/leaderboard/agent)、[方法](https://arena.ai/blog/agent-arena-methodology)）

OpenRouter Rankings 按 token 用量份额排名。用量受价格、速度、免费额度和集成默认值影响，不能读成质量。

坑：没有固定题集，被测的会话分布随时间和用户群变化；只有分配真的随机、分配概率已知时，比较才有因果含义。

---

<a id="meta"></a>
## 被评的是判官时：元评测

判官本身也要被评。这类 bench 的五轴照样能编码，只是被评者换成了判官或打分器，入口归第 3 类（元评测）。

- RewardBench 2：每道题 4 个回答只有 1 个对，奖励模型给对的那个打分最高才算对，随机基线 25%（旧版两两比较是 50%）。6 个领域先各算准确率再不加权平均；Ties 子集看奖励模型能否让所有正确答案都高于所有错误答案。（[arXiv 2506.01937](https://arxiv.org/abs/2506.01937)）
- ProcessBench：被评者要指出最早出错的那一步，或判断全对；最终分是"有错样本准确率"和"全对样本准确率"的调和平均。（[arXiv 2412.06559](https://arxiv.org/abs/2412.06559)）
- JudgeBench：用有客观对错标签的回答对测判官，换位判两次须一致才算判对。（[arXiv 2410.12784](https://arxiv.org/abs/2410.12784)）
- SAGE（Vals）：被评者是"当判官的模型"，报类别平衡准确率。（[页面](https://www.vals.ai/benchmarks/sage)）
- IMO-GradingBench 上的低成本证明评分研究（2026-05）：三判官一致通过的精确率最高（0.855），多数票召回率最高（0.912），一致规则在 4 次重跑里最稳；作者说明这个规则是事后选的。（[arXiv 2608.00004](https://arxiv.org/abs/2608.00004)）
