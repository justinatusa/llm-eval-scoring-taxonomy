# 合并链 G3：一个 bench 上所有题怎么变成一个数

题分有了，还要合成 bench 分。最常见的是平均，但"平均"里也有扣分、F 分数、校准、变换这些变化；参照是对手池时要用统计模型拟合；参照是人类标尺时要做换算。

| 取值 | 定义 | 例子 | 清单里在用的行数 |
|---|---|---|---|
| G3a 平均类 | 准确率、均值、宏平均或微平均，含错答扣分、F 分数、校准误差、变换、调和平均、难度加权、平手看第二指标 | SWE-bench Pro、AA-Omniscience、SimpleQA、HLE 校准误差、Alignment Index、PolyMath、SEAL | 176 |
| G3b 对池拟合 | 用统计模型从对局或相对信号里估出每个模型的位置 | Arena（BT + 风格控制）、GDPval-AA（Crowd-BT）、Agent Arena（IPS）、Vals Poker Agent（TrueSkill） | 13 |
| G3c 对标尺换算 | 换算到固定参照或人类量上 | GDPval（胜或平）、METR（50% 时间跨度）、Codeforces rating、LiveCodeBench Pro | 5 |
| G3d 累计量 | 直接加总或取份额 | Vending-Bench 2 余额、OpenRouter 份额、PutnamBench 解出题数 | 10 |
| G3e 潜变量补题 | 用 IRT 估缺失或没做的题 | MathArena、tinyBenchmarks | 2 |
| G3f 按名次 | 先在每题上排名次，再对名次做平均 | FrontierSWE v1 的支配分 | 1 |

---

## G3a 平均类

最常见的是题均准确率 $\frac1N\sum_i s_i$。micro 和 macro 的区别见 [G1 全过和比例](05-g1-within-item.md#all-pass)。下面是平均类里会改名次的几种变化。

<a id="penalty"></a>
### 错答扣分和 F 分数

SimpleQA 的判官给三档后，全集上算：

$$
\text{correct}=\frac{\#C}{N},\qquad
\text{cga}=\frac{\#C}{\#C+\#I},\qquad
F=\frac{2\cdot\text{correct}\cdot\text{cga}}{\text{correct}+\text{cga}}
$$

cga 是"作答了的题里答对的比例"。例子：100 题，40 对、20 错、40 没答，correct = 0.40，cga = 40/60 = 0.667，F = 0.50。论文指出 F 分数有漏洞：表现低于 50% 时，只要有一半把握就该去猜。没有这个漏洞的口径是给错答扣分，不答 0 分：$\text{score}=\#C-p\cdot\#I$，$p=9$ 时上例是 0.40 − 9×0.20 = −1.40。（[SimpleQA](https://arxiv.org/abs/2411.04368)）

AA-Omniscience 用的就是"答对加分、答错扣分、不答不加不减"。记对 $c$、部分对 $p$、错 $i$、不答 $a$：

$$
\text{OI}=100\cdot\frac{c-i}{c+p+i+a},\qquad
\text{准确率}=\frac{c}{c+p+i+a},\qquad
\text{幻觉率}=\frac{i}{p+i+a}
$$

| 模型 | 对 / 部分 / 错 / 不答 | 准确率 | OI | 幻觉率 |
|---|---|---|---|---|
| M1 | 60 / 5 / 30 / 5 | 0.60 | 30 | 0.75 |
| M2 | 45 / 5 / 5 / 45 | 0.45 | 40 | 0.091 |

按准确率 M1 第一，按 OI 是 M2 第一。永远不答的模型 OI = 0，全答错是 −100。AA 指数没有直接用 OI，而是放进两个分量：准确率（10%）和 1 − 幻觉率（5%）。注意幻觉率的分母是"没答对的题"，准确率很高的模型幻觉率也可以很高，因为它不会的那几道全在硬猜。（[AA-Omniscience](https://arxiv.org/abs/2511.13029)）

<a id="calibration"></a>

### 校准误差

HLE 除了准确率，还让模型对每道题报一个 0–100% 的置信度，按置信度分箱，看说 90% 有把握的题是不是真对了 90%：

$$
\mathrm{RMSCE}=\sqrt{\sum_k\frac{\lvert B_k\rvert}{n}\big(\overline{\text{conf}}_{B_k}-\overline{\text{acc}}_{B_k}\big)^2}
$$

例子：20 题，10 题报 90% 实际对 6 题，10 题报 50% 实际对 5 题，RMSCE = $\sqrt{0.5\times0.3^2+0.5\times0^2}=0.212$。分箱方式会影响数值；总报低置信度的模型在几乎全错的题库上校准误差反而小，所以要和准确率一起看。AA 指数的 HLE 只用准确率。（[HLE](https://arxiv.org/abs/2501.14249)）

<a id="transform"></a>
### 变换

LMArena Alignment Index（2026-10-08 预览）在真实会话里检测三类事件：越权行动 UA、错误归因 FA、谎报完成 DC。每类先算被标记会话的比例（按对话长度调整），再变换、加权：

$$
s_k=1-\sqrt{\text{标记率}_k},\qquad
\text{Index}=100\,(0.5\,s_{UA}+0.25\,s_{FA}+0.25\,s_{DC})
$$

开根号让接近完美的区间里的改进仍然看得见：标记率从 1% 降到 0% 加 0.1，从 51% 降到 50% 只加约 0.007。例子：UA 4%（$s=0.8$），FA 1%（0.9），DC 9%（0.7），指数 = 100×(0.4+0.225+0.175) = 80。变换形式和权重都是人定的；它只覆盖三类可观测的失败。（[博客](https://arena.ai/blog/ai-alignment-index)）

### 调和平均、难度加权、平手看第二指标

- ProcessBench 的最终分是"有错样本准确率"和"全对样本准确率"的调和平均，任何一类做得差都会把总分拉下来。
- PolyMath 的 DW-ACC 按难度加权：(a低 + 2a中 + 4a高 + 8a顶)/15，难题一题顶简单题八题。
- CWE-bench 按 pass@1 排名，平手时看 pass@4。

<a id="seal"></a>
### 排名规则：SEAL

Scale 的 SEAL 榜在分数之外另定名次：名次 = 1 + 置信区间下界高于本模型区间上界的模型数。两个模型分数不同、但区间重叠，就可以并列同一名。读 SEAL 名次时要知道，它反映的是"有几个模型显著比你好"。

---

## G3b 对池拟合

原始数据是一堆对局（模型 a、模型 b、结果）。结果可能来自人投票、LLM 判官、棋局胜负或扑克筹码。下面全部用同一份玩具数据：A 对 B 六胜四负，B 对 C 七胜三负，A 对 C 八胜二负，共 30 场。所有数字来自 `python3 scripts/basics.py` §2–§6。

<a id="elo"></a>

### 在线 Elo

每打完一场就按"比预期多赢了多少"调分：

$$
E_a=\frac{1}{1+10^{(R_b-R_a)/400}},\qquad R_a\leftarrow R_a+K\,(S_a-E_a)
$$

$S_a$ 取 1、0.5 或 0。400 和 10 只是刻度约定：

| 分差 | 0 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| 期望胜率 | 0.50 | 0.5715 | 0.6401 | 0.7597 | 0.9091 |

所以"1300 对 1200"只表示 64% 的期望胜率，不表示"强 8%"。

手算第一步：三人都从 1000 起，$K=32$，第一场 A 胜 B，$E_A=0.5$，A 加 $32\times(1-0.5)=16$，B 减 16。

同一份 30 场数据，换顺序跑：

| 顺序 | A | B | C |
|---|---|---|---|
| 按表顺序 | 1040.8 | 1023.7 | 935.5 |
| 倒序 | 1112.6 | 1006.5 | 880.9 |
| 1000 次随机顺序的均值（标准差） | 1072.8（14.5） | 1018.1（15.6） | 909.0（14.1） |

同样的数据，顺序一换，A 差 70 分。在线 Elo 是为"选手实力随时间变"设计的，冻结权重的模型不需要这种追踪。Chatbot Arena 在 2024-01-09 之前用在线 Elo，之后改成 BT。今天榜上叫 "Elo" 的分（AA、Kaggle Game Arena、Design Arena），几乎都是一次性的 BT 拟合，只沿用了 Elo 的名字和刻度。

<a id="bt"></a>

### Bradley–Terry（BT）

给每个模型一个实力值 $\beta$，假设"a 胜 b 的概率 = 实力差的 logistic"，找一组 $\beta$，让所有已发生的对局最说得通：

$$
P(a\succ b)=\sigma(\beta_a-\beta_b)=\frac{1}{1+e^{-(\beta_a-\beta_b)}}
$$

$$
\hat\beta=\arg\max_\beta\sum_{(a,b,y)}\Big[y\log\sigma(\beta_a-\beta_b)+(1-y)\log\big(1-\sigma(\beta_a-\beta_b)\big)\Big]
$$

它就是一个没有截距的逻辑回归：每场对局一行，a 的位置放 +1，b 的位置放 −1，标签是 a 赢没赢。换到 Elo 刻度：$R=\beta\cdot 400/\ln 10+\text{锚点}$。平局拆成"半胜 + 半负"两条权重各 0.5 的样本（其他平局处理见下文）。

玩具数据的结果：$\beta_A=1.332$、$\beta_B=0.890$、$\beta_C=0$，Elo 刻度（C = 1000）A 1231、B 1155、C 1000。拟合回去，A 胜 B 0.609（观测 0.6），B 胜 C 0.709（0.7），A 胜 C 0.791（0.8）。3 组对局只有 2 个自由参数，BT 强制传递性，所以预测和观测不完全相等。BT 和对局顺序无关，同一份数据只有一个答案。

坑：BT 假设单一维度、可传递，A>B>C>A 这样的循环会被它抹平；分数只有差值有意义；加入新模型会改变旧模型的分（见 [R6](04-reference.md#r6)）。

### 胜率矩阵和 Copeland

胜率矩阵是一张 $M\times M$ 的表，格子 $(a,b)$ 是 a 对 b 的经验胜率（平局算半场），不做任何模型假设。玩具数据 $W_{AB}=0.6$、$W_{BC}=0.7$、$W_{AC}=0.8$，BT 平滑后是 0.609、0.709、0.791；两张表差得多的格子就是 BT 拟合不好的地方。Kaggle Game Arena 的扑克里，Grok 4 对 GPT-5 mini 胜率 90%，但 9 组对局只赢 3 组，说明 BB/100 高不等于能赢大多数对手。

Copeland 只数"两两净胜了几个对手"：A 对 B、C 都净胜，得 2；B 净胜 C，得 1；C 得 0。它不看赢多少，平局多。

<a id="ties"></a>
### 平局怎么记

BT 只有胜和负。平局有三种处理：

1. 记半胜：一场平局拆成双方各胜 0.5 场。GDPval-AA 明确这样做。
2. 平局模型：给"打平"单独一个概率，实力越接近越容易平。Davidson（1970）和 Rao–Kupper（1967），$\pi_i=e^{\theta_i}$：

$$
P_{\text{Davidson}}(i\succ j)=\frac{\pi_i}{\pi_i+\pi_j+\nu\sqrt{\pi_i\pi_j}},\qquad
P_{\text{Davidson}}(i=j)=\frac{\nu\sqrt{\pi_i\pi_j}}{\pi_i+\pi_j+\nu\sqrt{\pi_i\pi_j}}
$$

$$
P_{\text{RK}}(i\succ j)=\frac{\pi_i}{\pi_i+\theta\pi_j},\qquad
P_{\text{RK}}(i=j)=\frac{(\theta^2-1)\pi_i\pi_j}{(\pi_i+\theta\pi_j)(\pi_j+\theta\pi_i)}
$$

3. 平局不更新：直接丢掉平局。

算一遍：$\pi_i=2$、$\pi_j=1$。Davidson 取 $\nu=0.5$，胜 0.5395、负 0.2698、平 0.1907；Rao–Kupper 取 $\theta=1.5$，胜 0.5714、负 0.2500、平 0.1786。一组 36 场比赛（A–B 之间有 8 场平局），记半胜得 A 1077、B 983、C 940；Davidson 拟合得 A 1105、B 977、C 918，$\hat\nu=0.716$。名次一样，分差拉开约 25–30%。（`python3 scripts/mechanisms.py` §1c）

在用情况：头条榜单里只见到记半胜。Ameli 等（ICLR 2025）提出带因子分解的 Rao–Kupper/Davidson 模型并开源 `leaderbot`；"Drawing Conclusions from Draws" 发现遇到平局干脆不更新，预测准确率相对提高 1–3%，而且平局在简单题和客观题里更多，常常表示"题太简单"，不表示"两者一样强"。（[arXiv 2412.18407](https://arxiv.org/abs/2412.18407)、[arXiv 2510.02306](https://arxiv.org/abs/2510.02306)）

坑：记半胜会把平局多的模型对往一起拉；Davidson 的 $\nu$ 是全局常数，题型之间平局率差别大时不准。

<a id="crowd-bt"></a>

### Crowd-BT：把判官可靠度放进模型

评审有好有坏。给每个评审 $k$ 一个可靠度 $\eta_k$，表示"a 真的更好时，k 判 a 赢的概率"，和模型实力一起估：

$$
P(a\succ_k b)=\eta_k\,\sigma(s_a-s_b)+(1-\eta_k)\big(1-\sigma(s_a-s_b)\big)
$$

$\eta_k\approx1$ 是好评审，0.5 是乱点，接近 0 是反着投。记 $\varepsilon=1-\eta_k$，就是 $p=\varepsilon+(1-2\varepsilon)\sigma(s_a-s_b)$。

算一遍：真实胜率 0.7，评审 $\eta=0.8$，观测胜率 = 0.8×0.7 + 0.2×0.3 = 0.62。不考虑评审噪声直接跑 BT，会把实力差低估（把 0.7 读成 0.62），噪声评审把所有人往中间压。$\varepsilon=0.1$ 时同样的实力差 0.4，胜率从 $\sigma(0.4)=0.599$ 压到 0.579。

在用：AA 的 GDPval-AA v2.1 和 AA-Briefcase v1.1（AA 指数 v4.3.2 起）。坑：$\eta$ 要足够多"同一评审判很多对"的数据才估得准；它只建模随机翻转，偏爱自家模型这类系统性偏差刻画不了。（[Chen 等 2013](https://erichorvitz.com/crowd_pairwise.pdf)）

<a id="synthetic"></a>
### 合成对局：AA-Briefcase

AA-Briefcase v1.1 有三个分项：分析质量和呈现两项本来就是判官两两比较，细则通过率是绝对分。为了放进同一个 Elo，AA 把通过率改写成假想的对局（通过率高的一方赢），三项各自按 Crowd-BT 拟合，再合成一个 Elo。细则那一路的比较是确定的，$\varepsilon=0$，退化成普通 BT。锚点 GPT-5.5 (medium) = 1000。编码写成：J2 / O3 / S1 → 合成 S4 / R2 → R6 / G3b Crowd-BT。

AA 没有公开合成对局的比较单位（逐题比，还是整体通过率比一次）和平局规则。把几种读法都算一遍：3 个模型、4 个任务，细则数 10/10/20/5，M1 逐题通过率 0.9、0.6、0.5、1.0，M2 0.8、0.7、0.75、0.6，M3 0.8、0.6、0.6、0.8。

| 合成规则 | M1 | M2 | M3 |
|---|---|---|---|
| 逐题比，平局记半胜 | 1000 | 1000（锚） | 911 |
| 逐题比，平局丢弃 | 1000 | 1000 | 880 |
| 逐题软胜（i 得 $r_i/(r_i+r_j)$ 场） | 1003 | 1000 | 996 |
| 整体通过率比一次 | M2 全胜，最大似然发散 | | |

平局规则一项就让 M3 差 31 分；软胜几乎抹平差距；整体比一次时只要有一个模型全胜，最大似然就不存在，所以 AA 至少要加先验或改成逐题。另一个没公开的是三个分项在联合似然里各占多少权重，合成对局的场数（逐题时每对模型等于任务数）和真实两两比较的场数不同。（`python3 scripts/mechanisms.py` §2、[AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)）

<a id="style"></a>

### 风格控制

人和判官都偏爱长的、排版漂亮的回答。风格控制在 BT 回归里加几列"风格差"特征（回答长度、markdown 标题数、列表数、加粗数，做归一化差 $\frac{f_a-f_b}{f_a+f_b}$），让风格列吸收"因为长所以赢"的那部分：

$$
P(a\succ b)=\sigma\big(\beta_a-\beta_b+\gamma^{\top}z_{ab}\big)
$$

排名用 $\beta$，$\gamma$ 是风格效应。模拟：L 和 S 真实实力相同（0.3），R 为 0，长度效应 0.6，L 多数时候写得更长。每对 3000 场，不控制时 L 1099、S 1052，L 白得 47 分；加风格项后 L 1061、S 1056，$\hat\gamma=0.615$，接近真值。（`python3 scripts/basics.py` §4）

如果 L 永远比别人长，$\beta_L$ 和 $\gamma$ 永远以和的形式出现，分不开。风格特征必须在同一个模型内部有变化。LMArena 2024-08 引入风格控制，2025-05-16 起成为 Text 和 Vision 的默认视图。坑：被控制掉的长度里可能也有真正有用的信息；它只做相关性调整，没有因果含义；特征选得不同，名次不同。

LMArena 在 2026-07-14 又加了一个非默认开关"事实性复合 BT"：从两边回答里抽事实声明逐条核查，真实率高的一方赢，差距越大赢得越多；这批事实性对局和人类偏好票一起喂进 BT，默认事实性权重 25%。这个权重是政策选择。（[博客](https://arena.ai/blog/factuality-in-arena)）

<a id="ips"></a>
### 逆倾向加权（IPS）

Agent Arena 随机给真实会话分配组件，再问"换成这个模型，信号平均提升多少"。分配概率不均匀时，用逆倾向权重纠正：

$$
\hat\mu_t=\frac{\sum_i w_iY_i\,\mathbb{1}[T_i=t]}{\sum_i w_i\,\mathbb{1}[T_i=t]},\qquad
w_i=\frac{q(T_i)}{p(T_i)},\qquad
\hat\tau_t=\hat\mu_t-\hat\mu_Q
$$

$p$ 是实际分配概率，$Q$ 是目标基线分布（对组件均匀）。例子：M1 被分配的概率 0.8，M2 0.2，目标各 0.5。M1 的 8 个会话成功 6 个，M2 的 2 个会话成功 1 个。权重 M1 0.625、M2 2.5；加权总体 = (0.625×6 + 2.5×1)/(0.625×8 + 2.5×2) = 0.625，未加权是 0.7，被流量多的 M1 带偏了。$\hat\tau_{M1}=+0.125$，$\hat\tau_{M2}=-0.125$。

每个信号单独出一张榜，最后五个信号等权平均成 Net Improvement（见 [J5](01-judge.md#j5)），老数据有时间衰减。坑：分数是相对基线的处理效应，单位是"信号的差"，不能换成 BT 分；LMArena HF 数据集里 Agent 榜的 score（如 0.143）是 IPS 估计，乘 400/ln10 当 Elo 读是错的；只有分配真的随机、概率已知时 IPS 才无偏。（[方法](https://arena.ai/blog/agent-arena-methodology)）

<a id="gte"></a>

### 均衡类排名（GTE）

不假设存在单一实力值，把每局当成选民、模型当候选人，用博弈均衡排序。Kaggle Game Arena 的狼人杀用最大熵相关均衡：一个"角色挑选者"专挑最能拉开差距的角色，两个"模型挑选者"对抗，再算每个模型在均衡分布下的期望表现。论文附录用 Elo、Copeland、Ranked Pairs 做一致性检查。坑：结果依赖候选集合，加一个模型或角色都可能改变均衡；可解释性比 BT 差。（[arXiv 2609.31473](https://arxiv.org/abs/2609.31473)）

<a id="trueskill"></a>

### TrueSkill 和 Glicko

TrueSkill 是贝叶斯版本：每个选手的实力是 $N(\mu,\sigma^2)$，每场（可以多人）做一次近似更新，排名常用保守分 $\mu-3\sigma$。新选手默认 $\mu=25$、$\sigma=25/3$，保守分 = 0，所以新人排在最底，打得越多 $\sigma$ 越小。在用：Vals Poker Agent（多场 10 人锦标赛，按名次更新，以 1000 为基线、乘 40 换算）、EQ-Bench 3（细则分加两两比较拟合 TrueSkill）。Kaggle 在狼人杀上拿 Elo 和 OpenSkill 作对照，认为它们不适合非对称多人游戏。坑：$\mu-3\sigma$ 惩罚比得少的模型。

Glicko 给每个选手加一个"评分偏差 RD"，RD 大时一场比赛对分数的影响大。Glickman 论文自带算例：r=1500、RD=200 的选手，胜 1400(RD 30)，负 1550(RD 100)，负 1700(RD 300)，更新后 r′≈1464、RD′≈151.4。2025 年后的主流 LLM 榜没有用它出最终分；在冻结权重、批量拟合的场景里，带置信区间的 BT 已经覆盖了它的作用。

### 谁和谁比：配对和连通性

把模型当节点、有对局就连边，比较图必须连通，BT 才能把所有人放到同一把尺子上；更强的条件是任意把模型分成两组，两组之间都有双向胜负，否则最大似然发散到无穷。Chatbot Arena 论文按"减少不确定性最多"分配流量；LMArena 2025-07-23 起按对局频率重加权；GDPval-AA 先均衡抽样，再按 Elo 相近主动配对；Kaggle 国际象棋每对固定 40 局（黑白各 20）。

---

<a id="g3c"></a>
## G3c 对标尺换算

每题判法和第 1 类一样，合并时换算到固定参照（R4）或人类量（R5）上。

### 胜或平率

GDPval 原版：行业专家判模型交付物和专家交付物谁更好，

$$
\text{win-or-tie}(m)=\frac{\#\lbrace\text{专家判 } m \text{ 更好}\rbrace+\#\lbrace\text{平}\rbrace}{\#\lbrace\text{比较}\rbrace}
$$

平局算成功，所以 50% 不等于"与专家持平"。AA 的 GDPval-AA 用了同样的题，却改成模型对模型、LLM 判官、Crowd-BT 拟合，同名 bench，评分机制完全不同，数字不可互比。（[GDPval](https://arxiv.org/abs/2510.04374)，OpenAI 发布于 2025-09，arXiv 提交于 2025-10-05）

<a id="baseline-winrate"></a>
### 对固定基线的胜率

Arena-Hard v2 有 500 道难题和 250 道创意写作题，判官给五档判决，每题判两次（第二次交换位置），强胜算 3 票、小胜 1 票、平 0.5：

| 判决 | 展开成 |
|---|---|
| ≫（强胜） | [1,1,1] |
| >（小胜） | [1] |
| = | [0.5] |
| <（小负） | [0] |
| ≪（强负） | [0,0,0] |

例子：3 题，两次换位后折算到被测模型视角是 (≫, >)、(=, <)、(>, >)。展开得 [1,1,1, 1, 0.5, 0, 1, 1]，胜率 6.5/8 = 0.8125；6 个判决等权是 4.5/6 = 0.75。强胜 ×3 把胜率往两端推。置信区间是 100 次 bootstrap 的 5% 和 95% 分位，即 90% 区间。风格控制版把展开后的对局喂给带风格项的 BT，再换算成对基线的胜率。（[arena-hard-auto](https://github.com/lmarena/arena-hard-auto)）

AlpacaEval 2 的长度控制胜率（LC）先拟合一个带长度项的回归，再把长度项设为 0 重新预测：

$$
\text{LC winrate}=100\cdot\mathbb{E}_x\big[\sigma(\theta_m-\theta_b+(\psi_m-\psi_b)\gamma_x)\big]
$$

例子：$\theta_m-\theta_b=0$，长度系数 0.6，m 总是长一个标准差，原始胜率约 $\sigma(0.6\tanh 1)=0.61$，LC 胜率回到 0.50。论文报告 LC 版本与 Chatbot Arena 的 Spearman 相关从 0.94 升到 0.98。（[arXiv 2404.04475](https://arxiv.org/abs/2404.04475)）

WildBench 和基线两两比，五档奖励 +100、+50、0、−50、−100；赢家比输家长出 K = 500 字符以上时，"小胜"降为平局。4 题奖励 +100、+50（但赢家长 800 字符，降为 0）、−50、0，WB-Reward = (100+0−50+0)/4 = 12.5。K 是人选的，换 K 会改名次。（[arXiv 2406.04770](https://arxiv.org/abs/2406.04770)）

坑：对基线胜率在 0 和 100 附近饱和，强模型之间拉不开。这三个 bench 在 2026 年头部模型报告里已很少出现，清单里标为"仅作机制解释"。

<a id="metr"></a>

### METR 时间跨度

给每个任务标一个"人类专家要做多久"，把模型的成功率对 $\log_2(\text{人类耗时})$ 做 logistic 回归，读出成功率恰好 50% 的耗时：

$$
P(\text{成功}\mid t)=\sigma\big(\beta(\log_2 h_{50}-\log_2 t)\big),\qquad
\log_2 h_{80}=\log_2 h_{50}-\frac{\ln 4}{\beta}
$$

例子：

| 人类耗时（分钟） | 1 | 2 | 4 | 8 | 15 | 30 | 60 | 120 | 240 | 480 |
|---|---|---|---|---|---|---|---|---|---|---|
| 模型成功率 | 1 | 1 | 1 | .9 | .8 | .6 | .5 | .3 | .1 | 0 |

拟合得 $h_{50}\approx 49.8$ 分钟、$\beta=0.969$，$h_{80}\approx 18.5$ 分钟，80% 跨度只有 50% 跨度的约 1/3。（`python3 scripts/basics.py` §9）

Time Horizon 1.1（2026-01-29）把任务从 170 个加到 228 个，8 小时以上任务从 14 个加到 31 个，置信区间来自任务族、任务、运行三层的分层 bootstrap。坑：任务构成一变趋势就变，TH1 换到 TH1.1 让 GPT-4 的估计降了 35–57%，GPT-5 升了 55%；区间很宽，Opus 4.5 是 320 分钟 [170, 729]；"50% 跨度 2 小时"不等于"能可靠完成 2 小时的任务"；横轴是人类耗时，和模型自己花多久无关。（[METR TH1.1](https://metr.org/blog/2026-1-29-time-horizon-1-1/)）

<a id="codeforces"></a>
### Codeforces rating

让模型"假装"参加真实比赛：先算比赛总分和名次，再问"一个人要多少 rating，才会被期望排在这个名次"。

第一步是罚分口径（OpenAI 2025 提出，DS-V4 沿用）：模型解出一道题时，这道题的分记为"解出同一题、而且失败次数相同的人类得分的中位数"，用来抵消模型瞬间提交的时间优势。例子：A 题首交即过，0 次失败的人类得分 480、470、490，中位数 480；B 题失败 1 次后过，1 次失败的人类只有 850；C 题没过。总分 1330。

第二步按总分排名次，再换 rating。Codeforces 官方的期望名次是

$$
\text{seed}_i=1+\sum_{j\ne i}P(j\succ i),\qquad P(j\succ i)=\frac{1}{1+10^{(r_i-r_j)/400}}
$$

求一个 $r$ 让 seed 等于实际名次。例子：40 名人类，模型排第 11。

| 方法 | rating |
|---|---|
| 官方 seed（含 +1）反解 | 2187 |
| 名次似然最大化（OpenAI 写法） | 2187 |
| CodeElo 写法（漏了 +1） | 2144 |

官方 seed 等于名次，正好是名次似然的一阶条件（所有人类胜模型的概率之和 = 排在模型前面的人数 = 名次 − 1），所以前两种等价。Qwen 的 CodeElo 解 $m=\sum_i 1/(1+10^{(r-r_{(i)})/400})$，没有 +1，相当于把名次多算一位，低了 42 分；参赛人数越少偏差越大。（`python3 scripts/mechanisms.py` §4、[Codeforces 博客](https://codeforces.com/blog/entry/20762)、[CodeElo](https://arxiv.org/abs/2501.01257)、[OpenAI](https://arxiv.org/abs/2502.06807)）

真实用法：DS-V4 用 14 场 Div.1 共 114 题（2025-05 至 2025-11），每题 32 个候选里无放回抽 10 个随机排成提交顺序，用专家测试集判，按罚分口径算总分、换名次、换 rating，对抽取和顺序取期望，再对 14 场平均，Pro-Max 3206、Flash Max 3052，"在人类选手中排第 23"。（[arXiv 2606.19348](https://arxiv.org/abs/2606.19348)）

坑：选择器（32 选 10）是被测系统的一部分（见 [G2 选择器](06-g2-sampling.md#selector)）；漏 +1；百分位依赖人口，CodeElo 表里 1073 ≈ 50 百分位、1603 ≈ 90、2157 ≈ 99，换年份、换 Div 就不同；单场 rating 标准差 300–500，场数少时区间很宽，厂商通常不报。

### 其他换算

- LiveCodeBench Pro：把模型当作和题目对弈，题目难度来自人类选手表现，做贝叶斯 MAP Elo。
- Remote Labor Index：专家评级 ≥2 的比例换成自动化率。
- NoLiMa：有效长度，见 [R7](04-reference.md#r7)。

---

## G3d 累计量

直接加总或取份额：Vending-Bench 2 的年末余额、OpenRouter 的 token 份额、PutnamBench 的解出题数。扑克的 BB/100 也是累计量：

$$
\text{BB/100}=\frac{\text{净赢筹码}/\text{大盲}}{\text{手数}}\times 100
$$

盲注 1-2（大盲 2），1000 手净赢 930 筹码即 465 个大盲，BB/100 = 46.5。Kaggle Game Arena 用 duplicate 扑克降方差（同一副牌序打两遍，交换座位），区间用按 100 手分块的 bootstrap。坑：累计量无界、重尾，看中位数和区间。

---

<a id="irt"></a>

## G3e 潜变量补题（IRT）

每道题有难度 $b_j$ 和区分度 $a_j$，每个模型有能力 $\theta_m$：

$$
P(y_{mj}=1)=\sigma\big(a_j(\theta_m-b_j)\big)
$$

能力 1 的模型做难度 1 的题，答对概率 0.5；同一题 $a=2$ 时能力 2 的模型答对 0.88，$a=0.5$ 时只有 0.62。区分度高的题更能拉开模型。BT 是"模型对模型"，IRT 是"模型对题"。

- MathArena：缺失的结果用 IRT 估计补上再平均，置信区间用模拟后重新拟合 IRT 得到。（[matharena.ai](https://matharena.ai/)）
- tinyBenchmarks：新模型只做约 100 道锚点题，用 IRT 推全量分。例：全量 1000 题，锚点 100 题对 70 道，其余 900 题逐题算预测概率求和得 610，估计准确率 (70+610)/1000 = 0.68。锚点题一旦泄漏就是现成的刷分集。（[arXiv 2402.14992](https://arxiv.org/abs/2402.14992)）

坑：默认单维能力；题目参数要足够多的模型共同作答才估得准；换模型集合，题目参数会漂移；新模型远超旧模型群时外推不可靠。把 bench 当成"大题"、在 bench 之间做同样的事，就是 [G4c 的 ECI](08-g4-cross-bench.md#joint-fit)。

---

<a id="rank"></a>
## G3f 按名次

先在每题上给所有模型排名次，再对名次做平均。FrontierSWE v1 的头条"支配分"定义为对随机对手、随机任务的胜率（并列记半胜）。$N$ 个模型、$T$ 道题，模型 $m$ 在题 $t$ 上的名次为 $r_{mt}$（并列取平均名次）：

$$
\mathrm{Dom}_m=\frac{1}{T(N-1)}\sum_t\sum_{o\ne m}\Big[\mathbb{1}(r_{mt}<r_{ot})+\tfrac12\mathbb{1}(r_{mt}=r_{ot})\Big]=\frac{N-\bar r_m}{N-1}
$$

推导：单题上名次为 $r$ 的模型恰好赢 $N-r$ 个对手（并列记半胜时也成立），对题平均即得。

例子：4 个模型、3 道题，P 的名次 1、2、1，赢 8/9 场，支配分 0.8889 = (4 − 4/3)/3。并列例（3 个模型、2 道题，P 和 Q 在第 1 题并列）：P 0.875、Q 0.625、R 0。FrontierSWE v1 公开榜 17 行全部吻合这个公式：平均名次 2.88 → 88.2%（榜上 88%），13.82 → 19.9%（榜上 20%）。（`python3 scripts/mechanisms.py` §3、[FrontierSWE V1](https://www.frontierswe.com/v1)）

FrontierSWE v1（2026-04）有 17 个任务，每题 5 次。性能类任务每题分数 = 0.5×正确率 + 0.5×加速比（或 1 − 压缩比），作弊记 0。V2 改成绝对分：34 个任务，柱子是 mean@5，须线是 worst@5 到 best@5，性能改用加权指令数当代理，因为共享沙箱上的墙钟计时会让名次翻转；当前头名 GPT-6 Astra 65.5% ±8.9，每次试跑 1029.65 美元。V1 归第 2 类，V2 归第 1 类。（[V2 博客](https://www.frontierswe.com/blog/v2)）

坑：名字叫胜率，看着像对池拟合，实际只是平均名次，丢掉了题内分差，赢 0.01 和赢 0.9 都算一场胜；依赖参赛名单，加一个模型所有人的名次都变。同一个"名次平均"放到 bench 之间，就是 [G4d](08-g4-cross-bench.md#g4d)，那里有"同一份数据三个冠军"的例子。
