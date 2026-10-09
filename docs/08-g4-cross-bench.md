# 合并链 G4：多个 bench 怎么合成一个指数

指数不出题，只合并别人的分数。它的五轴编码记"继承"（继承各组件自己的判法），只有 G4 这一层是它自己的。权重、归一化和合并方法都是编辑的选择，换一种选择，冠军就可能换人。

| 取值 | 定义 | 例子 | 清单里在用的行数 |
|---|---|---|---|
| G4a 固定权重 | 编辑决定的权重，或按规则定的权重，通常先归一化 | AA Intelligence Index v4.3.2、Vals Index（按行业 GDP 占比） | 6 |
| G4b 等权平均 | 子项或能力簇等权 | AA Coding Agent Index、AA Cyber Index、OlmoBaseEval、Agent Arena 的五个信号 | 10 |
| G4c 联合统计拟合 | 所有 bench 和模型放进一个统计模型一起拟合 | Epoch ECI、Kaggle 统一榜（pooled BT）、ONEBench（PL） | 2 |
| G4d 按名次 | 平均名次、平均胜率 | HELM 2025-03 以前的 mean win rate | 0 |
| G4e 并列不合并 | 两个指标并排，画成二维图，或按第二个指标排序 | ARC-AGI（分数 × 每任务成本）、PutnamBench、Vals ProofBench、FrontierSWE v2、Vals Finance Agent | 5 |

行数包括单个 bench 内部用到这一层的情况（例如 RewardBench 2 的 6 个领域等权）。

---

<a id="g4a"></a>
## G4a 固定权重

$$
\text{Index}=100\times\sum_k w_k\,x_k,\qquad \sum_k w_k=1
$$

AA Intelligence Index v4.3.2（2026-09 起）四类十项：

| 类别（类权重） | 组件（指数权重）和评分方式 |
|---|---|
| Agents 30% | AA-Briefcase v1.1（15%，合成对局 + 两两比较，Crowd-BT Elo）；GDPval-AA v2.1（10%，判官池两两比较，Crowd-BT）；AutomationBench-AA（5%，碰护栏整题 0 分） |
| Coding 20% | Terminal-Bench 4.0（10%，66 题，3 次，pass@1）；SciCode（10%，288 个子问题，3 次，pass@1） |
| General 30% | AA-Omniscience（15% = 准确率 10% + 1−幻觉率 5%）；GDP.pdf（10%，100 题 × 5 次，全过）；AA-LCR v1.1（5%，100 题，3 次） |
| Scientific Reasoning 20% | HLE（10%，2158 题，等价判定）；CritPt（10%，70 题，5 次，官方评分服务器） |

Elo 类组件先映射到 0–1：

$$
\operatorname{norm}(\text{Elo})=\operatorname{clamp}\Big(\frac{\text{Elo}-500}{2000},\,0,\,1\Big)
$$

Elo 1100 → 0.30，1600 → 0.55，2200 → 0.85，2600 → 1（截断）。而且 Elo 在模型加入指数时冻结（见 [R6 锚点](04-reference.md#anchors)）。

手算一个虚构模型：

| 组件 | 原始分 | 归一后 | 权重 |
|---|---|---|---|
| AA-Briefcase | Elo 1300 | 0.40 | 0.15 |
| GDPval-AA | Elo 1600 | 0.55 | 0.10 |
| AutomationBench | 0.50 | 0.50 | 0.05 |
| Terminal-Bench | 0.40 | 0.40 | 0.10 |
| SciCode | 0.45 | 0.45 | 0.10 |
| Omniscience 准确率 | 0.50 | 0.50 | 0.10 |
| Omniscience 1−幻觉率 | 0.60 | 0.60 | 0.05 |
| GDP.pdf | 0.30 | 0.30 | 0.10 |
| AA-LCR | 0.70 | 0.70 | 0.05 |
| HLE | 0.30 | 0.30 | 0.10 |
| CritPt | 0.10 | 0.10 | 0.10 |

加权和 0.41，指数 41。（`python3 scripts/basics.py` §10）

坑：

- 权重是编辑决策，AA 写明"权重偏重 agentic"，换权重名次就可能变。
- 归一化区间决定组件的有效权重：Elo 每涨 100 只加 $0.05\times w$；大量模型被截到 1 时，这个组件就没有区分力了。
- 版本号一变，分数就不能跨版本比。v4.1（2026-06 至 08）把 GDPval-AA 升级到 v2（三判官评审团、人类专家锚 1000）、去掉 IFBench、用 τ³-Banking 换掉 τ²-Bench Telecom；v4.1.1 把 HLE、AA-LCR、AA-Omniscience 的判官换成 GPT-5.6 Luna (medium)；v4.2 加入 AA-Briefcase 和 GDP.pdf、去掉 GPQA Diamond；v4.3 用 AutomationBench-AA 换掉 τ³-Banking、用 Terminal-Bench 4.0 换掉 2.1；v4.3.1 把两两比较判官池换成 Claude Opus 5、GPT-5.6 Sol、Gemini 3.8 Flash；v4.3.2 把 GDPval-AA 改锚 DeepSeek V4.1 Flash (max) = 1600 并改用 Crowd-BT，AA-Briefcase 锚点不变，各分项改用 Crowd-BT。厂商发布页引用的 AA 指数常常是更早的版本，要看清版本号。（[AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)）

其他固定权重的例子：Vals Index 按各行业占美国 GDP 的比例加权，权重直接表达了一种价值观；AA-WER v2 先按音频时长加权，再按 50/25/25 跨数据集合并；PostTrainBench 内部把 7 个 bench 加权。

## G4b 等权平均

子项或能力簇等权：

- AA Coding Agent Index：3 个组件等权，每个组件取 3 次 pass@1 的平均，作弊试次记 0。
- AA Cyber Index：3 个组件等权，拒答记 0。
- OlmoBaseEval：按能力把任务聚类，簇内平均后再对簇宏平均。
- HELM Capabilities：2025-03 起顶层改用平均分。
- Agent Arena：五个信号的净提升等权平均。

坑：等权不等于等信息，不同组件的噪声大小不同；平均分要求各组件刻度可比，否则方差大的组件主导。

<a id="joint-fit"></a>
## G4c 联合统计拟合

### Epoch ECI

把每个 bench 当成一道"大题"，有难度 $D_b$ 和斜率 $\alpha_b$，每个模型有能力 $C_m$：

$$
\text{score}(m,b)=\sigma\big(\alpha_b(C_m-D_b)\big)
$$

只要模型之间在某些 bench 上有重叠，就能把所有 bench 和模型放到同一把尺子上，某个 bench 已经饱和、新模型没测过也能比。例子：3 个模型 × 3 个 bench，$C=(0,1,2.5)$、$D=(-1,1,3)$、$\alpha=(2,1.5,1)$。模型 1 在 bench 1 上 $\sigma(1.5\times 0)=0.5$；模型 0 没测过 bench 2，预测 $\sigma(1\times(0-3))=0.047$；模型 2 没测过 bench 0，预测 $\sigma(2\times 3.5)=0.999$，已饱和。同样的能力差，在不同 bench 上对应完全不同的分数差。

ECI 再线性缩放到 Claude 3.5 Sonnet = 130、GPT-5 = 150，至少 4 个 bench 才给分。当前最高是 Opus 5.5，167。FAQ 说上线时约 5 个 ECI 点相当于 METR 时间跨度翻一倍。坑：分数没有绝对含义；新数据会让旧模型的分轻微变化；Elo 类 bench 放不进来，因为必须是 0–1 分数；厂商自报分有挑选偏差。（[Epoch ECI](https://epoch.ai/benchmarks/eci)、[arXiv 2512.00193](https://arxiv.org/abs/2512.00193)）

### Kaggle 统一榜（pooled BT）

国际象棋的 Elo、扑克的 BB/100、狼人杀的均衡胜率单位都不同，没法平均。Kaggle 把所有游戏的对局都化成两两胜负，一起喂给一个 BT，每个游戏除以自己的对局总数，让每个游戏的总权重相同：

$$
\max_\beta\sum_{g}\frac{1}{N_g}\sum_{(a,b,y)\in g}\ell\big(y;\sigma(\beta_a-\beta_b)\big)
$$

狼人杀每轮约 377,000 个 episode，国际象棋约 2,200，不除以 $N_g$ 狼人杀会淹没一切。坑：假设每个模型只有一个技能、跨游戏可传递；狼人杀化成两两胜负丢掉了联盟结构；扑克从"赢多少"变成"赢没赢"。（[Kaggle 博客](https://www.kaggle.com/blog/unified-game-arena-leaderboard)）

### ONEBench

用 Plackett–Luce（见 [S4](03-signal.md#pl)）把样本级的排序合成模型排名，不同 bench 的样本放进同一个似然。（[arXiv 2412.06745](https://arxiv.org/abs/2412.06745)）

<a id="g4d"></a>
## G4d 按名次：同一份数据，三个冠军

$$
\bar s_m=\frac1B\sum_b s_{mb},\qquad
\bar r_m=\frac1B\sum_b\operatorname{rank}_b(m),\qquad
\mathrm{MWR}_m=\frac{1}{B(M-1)}\sum_b\sum_{m'\ne m}\Big(\mathbb{1}[s_{mb}>s_{m'b}]+\tfrac12\mathbb{1}[s_{mb}=s_{m'b}]\Big)
$$

| 模型 | bench1 | bench2 | bench3 | 平均分 | 各 bench 名次 | 平均名次 | 平均胜率 |
|---|---|---|---|---|---|---|---|
| X | 90 | 50 | 52 | 64.0（第 1） | 1, 3, 3 | 2.33 | 0.333 |
| Y | 60 | 60 | 60 | 60.0 | 2, 2, 2 | 2.00 | 0.500 |
| Z | 59 | 61 | 61 | 60.33 | 3, 1, 1 | 1.67（第 1） | 0.667（第 1） |

平均分让偏科的 X 靠一门 90 分夺冠；平均名次和平均胜率让 Z 夺冠，它在 bench2、bench3 只比 Y 高 1 分，却拿满了名次分。再加一个模型 W = (58, 62, 62)：平均分里 X、Y、Z 都不变，平均胜率变成 Z 0.556、Y 0.444、W 0.667，Z 从第一掉到第二，自己一分没变。（`python3 scripts/basics.py` §10）

HELM Capabilities 在 2025-03 把顶层聚合从 mean win rate 改成平均分，理由正是这两点：它依赖参与比较的模型集合，而且对微小差异过敏。2025 年以后几乎没人在跨 bench 层用名次类，在题集层还有 FrontierSWE v1（[G3f](07-g3-item-set.md#rank)）。

<a id="side-by-side"></a>
## G4e 并列不合并

两个指标并排，不硬合成一个数。效率进入评测有四种方式，这里放在一起比：

| 做法 | 例子 |
|---|---|
| 并进单题分 | ARC-AGI-3 的平方动作比（见 [G1 加权](05-g1-within-item.md#weighted)） |
| 准确率做满后按成本排 | PutnamBench 精选排名：Lean 672 题全部解出者，每题平均成本最低的排前；Vals ProofBench 4 个模型并列 100%，页面并报每任务成本，直说满分已分不开头部 |
| 并列画图 | ARC-AGI 榜（每任务成本 × 分数，只显示成本低于 10,000 美元的系统）、Vals Finance Agent（成本帕累托曲线）、FrontierSWE v2（成本、运行时间、token 帕累托） |
| 单独列价格和速度 | AA：混合价、Cost per Task、Cost to Run、四种速度指标 |

AA 的混合价按"缓存命中 : 输入 : 输出 = 7 : 2 : 1"加权：

$$
p_{\text{混合}}=\frac{7p_{\text{缓存}}+2p_{\text{输入}}+p_{\text{输出}}}{10}
$$

缓存 0.3、输入 3、输出 15（美元/百万 token）时，混合价 = (2.1+6+15)/10 = 2.31 美元/百万 token。

帕累托前沿：模型 $m$ 在前沿上，当且仅当没有另一个模型成本不高于 $m$、分数不低于 $m$（至少一项严格）。6 个点（成本美元, 分数）：A(0.5, 40)、B(1.2, 55)、C(2, 52)、D(4, 70)、E(9, 71)、F(12, 69)，前沿是 A、B、D、E。硬并成一个数时，"分数 / 美元"让 A 排第一（80.0），"分数 − 10·log10(成本)"让 D 排第一（64.0）。并法不同，冠军不同。（`python3 scripts/mechanisms.py` §8）

坑：成本依赖价格表和缓存命中率，换供应商或调价成本就变；"只显示低于 10,000 美元"这类过滤会改变前沿形状；做满后改按成本排，这个 bench 测的就从能力变成了效率。
