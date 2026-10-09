# 写在数字旁边的东西：出分条件、修正、误差和时间

有些东西会改变分数，但不属于"怎么判分"：用的是哪个版本的题、模型开了多大的思考强度、谁来跑、做过哪些偏差修正、误差条多宽、锚点是什么时候定的。它们不进五条轴，但要和数字写在一起，否则两个数字没法比。

---

## A. 出分条件

同一个 bench、同一套评分规则，下面任何一项不同，数字就不能直接比。

- 题集：版本（Terminal-Bench 2.0、2.1、3.0、4.0 同时有人在报）、子集（公开、私有、保留、商业）、题源（固定、滚动更新、真实流量）。HLE 全集和 AA 用的纯文本 2158 题是两份题。
- 问法：MCF 还是 CF，0-shot 还是 5-shot，有没有思维链（见 [O1](02-object.md#o1)）。
- 抽取规则：strict 还是 flexible，boxed 还是最后一个数字（见 [J1a](01-judge.md#j1a)）。
- 判官身份和版本（见 [J2 的坑](01-judge.md#j2-pitfalls)）。
- 用户模拟器的模型、版本、提示词（见下文）。
- 采样设置：温度、最大输出长度、思考档位、工具开关。
- agent 设置：框架（harness）、步数上限、上下文压缩、输入条件（视频理解各家帧数不同）。
- 资源：硬件、时间预算（PostTrainBench 的 GPU 和 10 小时，ExploitGym 的 2 小时 / 6 小时并按 TPS 归一化）。
- 谁来跑：厂商自测、第三方代跑、直接引用对手自报的数。
- 失败怎么记：超时、API 错误、抽取失败、判官格式错误分别记 0、重试，还是从分母里去掉；fallback（任务降级给别的模型）算谁的：Fable 5 的榜单条目里有 35%（SWE-Marathon）或 40%（ALE）的任务降级到其他模型；Vals 对 Opus 5 分别给了"含 fallback"和"fallback 记失败"两个分。
- 方向：越高越好还是越低越好（攻击成功率、幻觉率）。
- 被评者：被测模型，还是判官本身（[元评测](01-judge.md#meta)）。

几个实际的设置差异：

| 设置 | 怎么影响 | 例子 |
|---|---|---|
| 温度 / top-p | 推理模型贪心解码会重复、卡死 | DeepSeek-R1 用 0.6 / 0.95；AA 对非推理模型用 0、推理模型用 0.6（除非厂商另有推荐） |
| 最大输出长度 | 截断 = 没写完 = 抽取失败 = 0 分 | Qwen3 一般 32,768 token，AIME 放宽到 38,912；AA 对推理模型用厂商公布的最大值 |
| 思考档位 | 同一模型不同档位就是不同的被测对象 | OpenAI 发布页常写"任一强度下的最高分"；AA 连判官的档位也标出来 |
| agent 框架 | 不属于评分，却算进同一个数字 | Terminal-Bench 2.0 论文：Gemini 2.5 Pro 配 Terminus 2 比配 OpenHands 解决率相对高 17%；AA 的 Terminal-Bench 4.0 用 mini-swe-agent |
| API 失败 | 失败算 0 还是重试 | AA 最多重试 30 次，仍失败的人工检查 |
| 取最好成绩 | 不同来源混在一张表里 | Llama 3 报告对非 Llama 模型"取公开报告和自行复现中的最好成绩" |

<a id="user-simulator"></a>
### 用户模拟器

τ 系列 bench 里的"用户"由另一个 LLM 扮演。它说错话、泄露答案或不配合，都会直接改变被测 agent 的分数。判分的仍是数据库终态（J1b / O4），模拟器是环境的一部分，和判官一样要写清模型和版本。

观测到的成功率可以写成

$$
\hat p=\sum_u\pi(u)\,p(\text{agent},u)
$$

$u$ 是模拟器的行为类型（正常、说错、带偏），$\pi(u)$ 由模拟器模型和提示词决定。换模拟器等于换 $\pi$，也就等于换题。模拟器让同一题的失败相关时，pass^k 不再等于 $p^k$：

$$
\text{pass}^k=\mathbb{E}_{\text{任务}}\big[p_{\text{任务}}^{k}\big]\ \ge\ \big(\mathbb{E}\,p_{\text{任务}}\big)^{k}
$$

真实数据：

- Lost in Simulation：同一个 GPT-4o agent 在 τ-bench retail 上（115 题，每种 3 次）换 4 个用户模型，成功率 67.8、67.0、75.9、71.3，极差 8.9 个点，模型间标准差 4.06；同一个用户模型重跑的标准差只有 1.2–3.5。换模拟器的影响大于重跑噪声。真人用户的成功率是 45.2%，远低于模拟器；只改模拟器的"礼貌"提示，18 个任务里有 11 个换了难度档。（[arXiv 2601.17087](https://arxiv.org/abs/2601.17087)）
- τ² 论文（模拟器是 gpt-4.1）：致命错误率 airline 13%、retail 12%、telecom 6%。如果这些对话都被判失败，分数最多被低估约 13、12、6 个点。这只是上界，实际低估多少没有测。（[arXiv 2506.07982](https://arxiv.org/abs/2506.07982)）
- 相关失败的影响：$p=0.7$ 且各次独立时，pass^k（k = 1、2、4、8）是 0.7、0.49、0.24、0.058；如果模拟器把 10% 的任务系统性带偏（这部分成功率 0.2），同时保持 pass^1 = 0.7，pass^k 变成 0.7、0.518、0.293、0.096，k 越大差越多。（`python3 scripts/mechanisms.py` §7）

怎么控制：τ²-bench 提供 No-User 模式（agent 控制全部工具）和 Oracle Plan 模式，把模拟器和沟通的影响拆出来，从 no-user 改成双控制，pass^1 降约 20%。τ³ 的 τ-Knowledge 用"基于流程、以当前环境状态为条件"的模拟器，论文批评以往的模拟器会不自觉地泄露未来状态。τ-Banking 有 698 份文档，最好的 GPT-5.2 high pass^1 约 25.52%，直接给黄金文档也只有 39.69%。AA 的 τ³-Banking 页面没写用户模拟器用的是哪个模型。（[τ-Knowledge](https://arxiv.org/abs/2603.04370)、[Sierra 博客](https://sierra.ai/blog/bench-advancing-agent-benchmarking-to-knowledge-and-voice)）

坑：模拟器错误可能让 agent 白丢分（说错需求），也可能白得分（泄露答案），两个方向不能简单相减。

---

<a id="corrections"></a>
## B. 修正

在某一层扣掉已知偏差。报分时要写明在哪一层做的修正。

| 偏差 | 修正 | 在哪一层 | 例子 |
|---|---|---|---|
| 位置偏差 | 换位判两次 | 判官（J） | Arena-Hard v2 |
| 长度和格式偏差 | 长度回归、风格特征、长度惩罚阈值 | 题集拟合（G3） | AlpacaEval LC、LMArena 风格控制、WildBench 的 K、HealthBench Professional 的长度校正 |
| 自偏好 | 多家判官、排除自评 | 判官 | AA 的三判官评审团、Arena-Hard 创意写作的集成判官 |
| 判官随机噪声 | 可靠度参数 $\eta$ | G3b | Crowd-BT |
| 事实错误 | 事实性对局混入偏好票 | G3b | LMArena 事实性复合 BT |
| 对局分配不均 | 频率重加权、先均衡后主动配对、逆倾向权重、时间衰减 | G3b | LMArena（2025-07-23 起）、GDPval-AA、Agent Arena |
| 作弊 | 作弊试次记 0、污染退回基座分、反作弊判官 | G1 | AA Coding Agent Index、FrontierSWE、PostTrainBench、NL2Repo、SWE-Marathon |
| 效率 | 按 TPS 或成本归一化 | G1 或 G4 | ExploitGym、ARC-AGI-3 |

这些修正的公式分别在 [G3b 风格控制](07-g3-item-set.md#style)、[Crowd-BT](07-g3-item-set.md#crowd-bt)、[IPS](07-g3-item-set.md#ips) 和 [对固定基线的胜率](07-g3-item-set.md#baseline-winrate)。

<a id="leaderboard-illusion"></a>
### 谁能决定送什么进来

Leaderboard Illusion（2025-04）指出，竞技场分数是"机制 + 参赛者行为"的共同产物：厂商可以在公开前私测很多变体，只留最好的（论文举例 Meta 在 Llama 4 发布前测了 27 个私有变体）；少数大厂拿到的对战数据比例远高于开源模型；大量模型被静默下架，破坏了比较图的连通性。

只公开最好的那个为什么会抬分：设 N 个变体真实实力完全相同，各自分数估计误差独立、标准差为 SE，取最大值的期望约为 $\text{SE}\times\mathbb{E}[\max_{i\le N}Z_i]$。$N=10$ 时 $\mathbb{E}[\max Z]\approx 1.54$，SE = 10 分时平均白涨约 15 分，真实能力一分没涨。（`python3 scripts/basics.py` §5、[arXiv 2504.20879](https://arxiv.org/abs/2504.20879)）

BT 的计算本身没错，出问题的是送进 BT 的数据。读竞技场类榜单时，要查清楚谁能决定送哪些模型进来、各送多少次。

---

<a id="error-bars"></a>
## C. 误差条和时间

### 标准误

题库是从"所有可能的题"里抽的一份样本，分数自带抽样误差：

$$
\mathrm{SE}=\sqrt{\frac{\widehat{\operatorname{Var}}(s_i)}{n}},\qquad \text{二值时}\ \mathrm{SE}=\sqrt{\frac{p(1-p)}{n}}
$$

$n=200$、准确率 0.70 时，95% 区间是 ±6.35 个百分点，200 题的榜上差 5 个点也不算稳。Llama 3 报告用 $1.96\sqrt{S(1-S)/N}$：$S=0.30$ 时，$N=30$（AIME 一年的题量）是 ±16.4 个点，$N=500$ 是 ±4.0。（Miller，[arXiv 2411.00640](https://arxiv.org/abs/2411.00640)）

### 配对和聚类

两个模型做同一批题时，题目难度让两者正相关，比较差值时应该用配对标准误：

$$
\operatorname{Var}(\bar a-\bar b)=\frac{\operatorname{Var}(a)+\operatorname{Var}(b)-2\operatorname{Cov}(a,b)}{n}
$$

模拟 200 题：A 0.705、B 0.580，非配对 SE 0.0476，配对 SE 0.0419。

题目成组出现时（同一篇文章出几道题、同一任务族出几个任务），组内结果相关，要用聚类标准误：

$$
\mathrm{SE}_{\text{聚类}}=\frac1n\sqrt{\sum_c\Big(\sum_{i\in c}(s_i-\bar s)\Big)^2}
$$

模拟 50 篇文章 × 每篇 4 题：均值 0.575，朴素 SE 0.0350，聚类 SE 0.0476，是 1.36 倍。忽略聚类会让区间偏窄，制造虚假的显著差异。（`python3 scripts/basics.py` §13）METR 对任务族、任务、运行做分层 bootstrap，Kaggle 扑克按 100 手分块 bootstrap，都是同一个思路。

想检出 $\Delta$ 的差，大约需要 $n\approx(z_{1-\alpha/2}+z_{1-\beta})^2\sigma_d^2/\Delta^2$ 道题。

### bootstrap 和 sandwich

拟合类分数（BT、Crowd-BT）的区间有两种算法。bootstrap 是把对局有放回重抽很多次、每次重拟合，取分位数；闭式做法用最大似然的渐近正态性，sandwich 估计 $\Sigma=H^{-1}\big(\sum_t g_tg_t^{\top}\big)H^{-1}$ 在模型设定不完美时更稳健。玩具数据 30 场时，A 的 95% bootstrap 区间约 [1018, 1606]；同样比例的 300 场时约 [1172, 1301]。锚点模型的区间恒为一个点。

在用：LMArena 2025-12 开源 Arena-Rank，改用闭式区间，整体提速 30 倍以上；GDPval-AA v2.1 用 sandwich；Arena-Hard v2 用 100 次 bootstrap 的 5% 和 95% 分位，得到的是 90% 区间，和别家的 95% 区间放在一起时要注意。

坑：两个区间重叠不等于没有差别，不重叠也只是粗判，应该看差值的区间；一次比 50 个模型，总会有几对"显著"；榜单的区间大多只算了题目或对局抽样，没算判官换版本、提示模板、采样温度带来的变异。

### 时间：锚点、冻结、断代

- 锚点和冻结：见 [R6 锚点](04-reference.md#anchors)。
- 版本断代：AA 指数 v4.1 和 v4.3 不可比（各版本变化见 [G4a](08-g4-cross-bench.md#g4a)）；METR TH1 到 TH1.1；Video-MME v1 到 v2；MCP Atlas 2026-04 重判；AA-LCR v1.0 到 v1.1；GDPval-AA v2 到 v2.1；Harvey LAB-AA v1.0 到 v1.1。

LMArena 的机制变化：

| 日期 | 变化 |
|---|---|
| 2024-01-09 | 在线 Elo 改为 Bradley–Terry |
| 2024-08 | 引入风格控制 |
| 2025-05-16 | 风格控制成为 Text、Vision 默认视图，调整 offset 让两种视图同刻度 |
| 2025-07-23 | 按对局频率重加权 |
| 2025-12-18 | 开源 Arena-Rank，闭式区间取代 bootstrap |
| 2026-06-04 | Agent Arena：因果 IPS 取代两两投票 |
| 2026-07-14 | 事实性复合 BT（默认权重 25%，非默认开关） |
| 2026-07-30 | AutoEval 软票 |
| 2026-09-30 | 12 个 LLM 判官的自偏好研究 |
| 2026-10-08 | Alignment Index 预览 |

（[HF leaderboard-dataset](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset)、[Arena-Rank](https://arena.ai/blog/arena-rank)）
