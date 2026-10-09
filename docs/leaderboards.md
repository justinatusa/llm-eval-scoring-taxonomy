# 榜单配方卡

每张卡用同一个格式写一个榜的头条数字：五轴编码、出分步骤、出分条件、修正、误差与时间、读数时的坑。轴和术语的解释在各章，卡里只链接过去。

编码的写法：判官 / 对象 / 信号 / 参照 / G1 → G2 → G3 → G4。"—"表示这一层不做事。

目录：
[AA Intelligence Index v4.3.2](#aa-index) ·
[AA 指数组件](#aa-components) ·
[AA 附加评测](#aa-extra) ·
[GDPval-AA v2.1](#gdpval-aa) ·
[AA-Briefcase v1.1](#briefcase) ·
[Harvey LAB-AA v1.1](#harvey) ·
[LMArena Text](#lmarena) ·
[Agent Arena](#agent-arena) ·
[Vals](#vals) ·
[SEAL](#seal) ·
[MathArena](#matharena) ·
[LiveBench](#livebench) ·
[METR Time Horizon](#metr) ·
[Epoch ECI](#eci) ·
[ARC-AGI-3](#arc) ·
[FrontierSWE V2](#frontierswe) ·
[HealthBench Professional](#healthbench) ·
[SWE-bench Pro](#swe-pro) ·
[Kaggle Game Arena](#kaggle)

---

<a id="aa-index"></a>
## AA Intelligence Index v4.3.2

| 项 | 内容 |
|---|---|
| 编码 | 继承 10 个组件 / G4a 固定权重 |
| 出分步骤 | 每个组件按自己的配方出分 → Elo 类组件（GDPval-AA、AA-Briefcase）冻结后按 clamp((Elo−500)/2000, 0, 1) 换到 0–1 → 按权重加权求和 ×100 |
| 权重 | Agents 30%（Briefcase 15、GDPval-AA 10、AutomationBench 5）；Coding 20%（Terminal-Bench 4.0 10、SciCode 10）；General 30%（Omniscience 准确率 10 + 1−幻觉率 5、GDP.pdf 10、AA-LCR 5）；Scientific Reasoning 20%（HLE 10、CritPt 10） |
| 出分条件 | 温度：非推理模型 0，推理模型 0.6（厂商另有推荐时从厂商）；推理模型用厂商公布的最大输出长度；API 失败最多重试 30 次 |
| 修正 | 各组件内部各自修正（判官评审团、Crowd-BT 的 η、AutomationBench 碰护栏记 0） |
| 误差与时间 | 2026-09 起；版本号决定可比性，v4.1、v4.2、v4.3 分数互不可比 |
| 坑 | 厂商发布页引用的常是旧版本（OpenAI 2026-09 发布页引用的是 v4.1.1）；权重是编辑决策 |
| 详解 | [G4a](08-g4-cross-bench.md#g4a)（含手算例子和版本变化） |
| 来源 | [AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |

<a id="aa-components"></a>
## AA 指数组件

| 组件 | 规模和次数 | 编码 | 要点 |
|---|---|---|---|
| Terminal-Bench 4.0 | 66 题 × 3 次 | J1b / O4 / S1 / R1 / 全过 → 平均 → G3a | mini-swe-agent 框架 |
| SciCode | 288 个子问题 × 3 次 | J1b / O3 / S1 / R1 / 全过 → 平均 → G3a | 评分超时 v4.2 起从 60 秒放宽到 300 秒，重判记为 v1.0.1 |
| AA-Omniscience | 6,000 题 × 1 次，私有 | J2 / O2 / S2 / R1 / 单信号 → 单次 → G3a 错答扣分 | 准确率和 1−幻觉率分作两个组件；判官 GPT-5.6 Luna (medium)；见 [错答扣分](07-g3-item-set.md#penalty) |
| GDP.pdf | 100 题、10 个领域 × 5 次 | J2 / O2 / S1 / R2 / 全过 → 平均 → G3a | 头条是全过率，另报任务宏平均的 Mean Pass；AA 用单判官 GPT-5.6 Luna (medium) 逐条判，Surge 原版用 Gemini 3.5 Flash，两版不可比 |
| AA-LCR v1.1 | 100 题 × 3 次 | J2 / O2 / S1 / R1 / 单信号 → 平均 → G3a | 等价判定，判官 GPT-5.6 Luna (medium) |
| HLE | 2,158 题（纯文本）× 1 次 | J2 / O2 / S1 / R1 / 单信号 → 单次 → G3a | 等价判定，判官 GPT-5.6 Luna (medium)；HLE 官方另报校准误差，见 [校准误差](07-g3-item-set.md#calibration) |
| CritPt | 70 题 × 5 次 | J1a / O2 + O3 / S1 / R1 / 单信号 → 平均 → G3a | 官方评分服务器做数值、SymPy 和函数测试判定 |
| AutomationBench-AA | 657 题 | J1b / O4 / S1 / R1 / 门控 + 比例 → 单次 → G3a | 碰护栏整题记 0，否则按目标完成比例给分，见 [门控](05-g1-within-item.md#gate) |
| GDPval-AA v2.1、AA-Briefcase v1.1 | 见下面两张卡 | | |

<a id="aa-extra"></a>
## AA 附加评测（不进指数）

| 评测 | 规模和次数 | 头条口径 | 编码要点 |
|---|---|---|---|
| τ³-Banking | 97 题 × 5 次 | 数据库终态判定，pass@1（5 次平均） | τ-bench 原版报 pass^k，同一 bench 换了采样合并口径，见 [pass^k](06-g2-sampling.md#passk)；AA 页面没写用户模拟器用的模型 |
| Harvey LAB-AA v1.1 | 120 题 × 1 次，私有 | 幻觉门控全过率 | 见下面的卡 |
| APEX-Agents-AA | 452 题 × 3 次 | 细则判定，pass@1 | Mercor 公开 480 题，AA 用其中 452 题；判官 Gemini 3 Flash (low)；全部细则通过才算 |
| AA-AnalystAgent | 80 题、14 个领域 × 5 次 | pass^5 | LLM 判官二元判对错，数值预检单向覆盖判官（只会改判为过），见 [判官合并](05-g1-within-item.md#judge-merge) |
| ITBench-AA | 59 个场景 × 3 次 | 全召回精度 | 见 [集合匹配](05-g1-within-item.md#set) |
| EnterpriseOps-Gym-AA | 1,117 题 × 3 次 | SQL 状态验证，严格 pass@1 | |
| IFBench | 294 题 × 5 次 | 规则抽取判定，pass@1 | v4.1 起移出指数 |
| MLCR-AA | 60 题 × 3 次 | 简洁性门控 + 三判官多数票 | 见 [门控](05-g1-within-item.md#gate) |
| Global-MMLU-Lite、MMMU Pro | 约 6,000 题、1,730 题 × 1 次 | 正则抽取，pass@1 | Global-MMLU-Lite 是 AA 多语言指数的来源 |

<a id="gdpval-aa"></a>
## GDPval-AA v2.1

| 项 | 内容 |
|---|---|
| 编码 | J2 判官池抽一 / O3 / S4 / R6 / 单信号 → 单次 → G3b Crowd-BT → 进指数时冻结并 clamp |
| 出分步骤 | 220 题；两个模型的交付物配成一场 → 每场从三判官池（Claude Opus 5、GPT-5.6 Sol、Gemini 3.8 Flash）里抽一个盲评 → 平局各算半胜 → Crowd-BT 最大似然（带判官可靠度 η）→ 锚定 DeepSeek V4.1 Flash (max) = 1600 |
| 出分条件 | Stirrup 框架；v2 起最多 250 轮，可以提前结束 |
| 修正 | 匿名；判官可靠度 η；先均衡抽样，再按 Elo 相近主动配对 |
| 误差与时间 | 95% 区间用 sandwich 估计；v2 锚人类专家 = 1000，v2.1 改锚 1600 并改用 Crowd-BT，两版不可比（DeepSeek-V4 报的 1554 是 v2 的数） |
| 坑 | 每场只有一个判官，判官池的组成就是题的一部分；分数依赖对手池 |
| 详解 | [S4](03-signal.md#s4)、[R6](04-reference.md#r6)、[Crowd-BT](07-g3-item-set.md#crowd-bt)、[平局](07-g3-item-set.md#ties) |
| 来源 | [AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |

GDP.pdf 用单判官 GPT-5.6 Luna (medium)，HLE、AA-LCR、AA-Omniscience 的等价判定也用它；GDPval-AA 用三判官池、每场抽一个。两者容易混。

<a id="briefcase"></a>
## AA-Briefcase v1.1

| 项 | 内容 |
|---|---|
| 编码 | J2 / O3 / 细则路 S1 → S4，另两路 S4 / 细则路 R2 → R6，另两路 R6 / 判官:抽一个 + 比例 → 单次 → G3b 合成对局 + Crowd-BT |
| 出分步骤 | 91 题、4 个场景；分析质量、呈现两路是判官两两比较；细则一路由三判官团里抽一个判（同一条细则固定同一个判官），细则通过率再转成合成对局 → 按 scope 分别拟合 Crowd-BT → 锚 GPT-5.5 (medium) = 1000 |
| 修正 | 合成对局的比较不含随机性，该 scope 的 η = 1 |
| 坑 | 合成对局的比较单位（按题还是按细则）和平局规则 AA 没有公开；细则分本来是绝对的，转成对局后依赖对手池 |
| 详解 | [合成对局](07-g3-item-set.md#synthetic)（含两种比较单位的数值对比） |

<a id="harvey"></a>
## Harvey LAB-AA v1.1

| 项 | 内容 |
|---|---|
| 编码 | J2 三判官团 / O3 / S1 / R2 / 判官:平均占比 + 全过 + 门控 → 单次 → G3a 任务宏平均 |
| 出分步骤 | 120 个私有任务、24 个法律业务领域；每题细则 44–90 条（中位数 55）→ 三个判官（GPT-6 Sol、Grok 4.7、Claude Opus 5.5，均 medium）各自逐条判 → 每个判官看自己是否判了全部细则通过，每题分 = 判全过的判官占比（0、⅓、⅔、1）→ 有实质幻觉的题记 0 → 对任务等权平均 |
| 幻觉检查 | 两步：列举判官列出疑似虚假陈述并引证，怀疑判官 GPT-6 Sol (high) 对照材料逐条维持、驳回或合并；只有实质幻觉进门控，轻微幻觉只报不扣 |
| 其他指标 | 逐条通过率（三判官平均后在所有细则上摊平，微平均，门控前）；Near-Pass（允许漏 1 条、2 条）；每题幻觉数 |
| 出分条件 | Stirrup 框架、最多 200 轮、上下文压缩；文件名必须精确匹配；判官能看到完整任务说明（Harvey 原版只给标题）；Harvey 原版单判官、温度 0 |
| 误差与时间 | v1.1 和 v1.0 不可比；按业务领域细分时每格只有 5 题，只能按 1/15 的步长变化 |
| 坑 | 全过率和逐条通过率量级差很远。Grok 4.7 发布页报 19.6%（全过口径），Kimi K3 报逐条通过率 94.6，两个数来自不同模型，也来自不同口径 |
| 详解 | [全过和比例](05-g1-within-item.md#all-pass)、[门控](05-g1-within-item.md#gate)、[判官合并](05-g1-within-item.md#judge-merge) |
| 来源 | [AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)、[Harvey 公开样例](https://github.com/harveyai/harvey-labs) |

<a id="lmarena"></a>
## LMArena Text

| 项 | 内容 |
|---|---|
| 编码 | J4 众包 / O3 / S4 / R6 / 单信号 → 单次 → G3b BT + 风格控制 |
| 出分步骤 | 用户提问，两个匿名模型回答，用户投票 → 平局拆成两个半场 → BT 拟合，换到 Elo 刻度 → 默认视图带风格控制 |
| 出分条件 | 题源是用户实时提问，分布随时间变 |
| 修正 | 风格控制（2025-05-16 起成为默认视图）；按对局频率重加权（2025-07-23 起）；事实性复合 BT 是非默认开关 |
| 误差与时间 | 2025-12 起用闭式区间（Arena-Rank）；机制变化时间表见 [时间](09-conditions-corrections-uncertainty.md#error-bars) |
| 坑 | 私测多个变体只公开最好的会抬分，见 [谁能决定送什么进来](09-conditions-corrections-uncertainty.md#leaderboard-illusion)；"Elo"这个名字沿用下来，背后是 BT |
| 详解 | [BT](07-g3-item-set.md#bt)、[风格控制](07-g3-item-set.md#style) |
| 来源 | [排行榜](https://lmarena.ai/leaderboard)、[Arena-Rank](https://arena.ai/blog/arena-rank)、[HF 数据集](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset) |

<a id="agent-arena"></a>
## Agent Arena

| 项 | 内容 |
|---|---|
| 编码 | J5 + J1b / O6 / S1 + S3 / R6（相对均匀分配基线）/ 单信号 → 单次 → G3b IPS → 五个信号 G4b 等权 |
| 出分步骤 | 真实会话随机分配编排模型 → 挖五个信号 → 每个信号用逆倾向加权算相对基线的净提升 → 五个等权平均成 Net Improvement |
| 修正 | 逆倾向权重、时间衰减 |
| 误差与时间 | 95% 区间；并报每任务成本 |
| 读数 | 2026-10-02 的榜：Claude Fable 5.1 (Max) 的 Net Improvement 14.31% ±1.90%，Confirmed Success 17.64% ±2.82% |
| 坑 | 头条是五个信号的平均，引用"成功率"要看 Confirmed Success 一栏；IPS 分数不能乘 400/ln10 当 Elo 读 |
| 详解 | [J5](01-judge.md#j5)、[IPS](07-g3-item-set.md#ips) |
| 来源 | [榜单](https://arena.ai/leaderboard/agent)、[方法](https://arena.ai/blog/agent-arena-methodology) |

<a id="vals"></a>
## Vals

Vals 维护约 30 个 bench 和一个指数，各 bench 的配方差别很大。

| 榜 | 编码要点 | 读数时注意 |
|---|---|---|
| Vals Index | 继承 / G4a，按各行业占美国 GDP 的比例加权 | 权重本身表达价值观 |
| Finance Agent v2 | J2 判 3 次取众数 / R2 / 判官:重复众数，部分分和全过两种口径 | 两种口径排名会翻转；并列画成本帕累托曲线 |
| Legal Research Bench | J2 单判官 GPT-5.4 逐条判 / R2 / 全过（主）vs 加权通过率 | 同一模型 55.29 vs 90.58 |
| ProofBench v1.1 | J1c Lean 4 编译 / 100 题 / 只能提交一次 | 2026-10-07 有 4 个模型并列 100%，页面并报每任务成本 |
| Poker Agent | J1b 牌局结算 / R6 / G3b TrueSkill | 1000 基线归一 |
| 各 bench 通用 | fallback 分开报：对 Opus 5 给了"含 fallback"和"fallback 记失败"两个分 | 见 [出分条件](09-conditions-corrections-uncertainty.md) |

来源：[vals.ai](https://www.vals.ai/benchmarks)、[Finance Agent](https://www.vals.ai/benchmarks/finance_agent)、[ProofBench](https://www.vals.ai/benchmarks/proof_bench)、[Legal Research](https://www.vals.ai/benchmarks/legal_research)。

<a id="seal"></a>
## SEAL（Scale）

| 项 | 内容 |
|---|---|
| 共同点 | 每个 bench 自己出分，榜上的名次另有规则：名次 = 1 + 置信区间下界高于本模型区间上界的模型数，区间重叠的模型可以并列 |
| HSS（Humanity's Sixth Sense） | J2 Claude Opus 5 逐条判 / R2 / 每题 3 次，pass@1 取平均 / 95% 区间按题 bootstrap / 522 题（288 图像、234 视频），人类基线 93.1% |
| MCP Atlas | J2 逐条判要点 1、0.5、0 / 阈值：覆盖率 ≥ 0.75 算通过 / 2026-04 换判官重判 |
| HiL-Bench | ASK-F1（提问精确率和阻塞召回率的调和平均）+ Pass@3 |
| 坑 | 名次反映"有几个模型显著比你好"，分数高一点不一定名次高；不同 bench 的判官各不相同 |
| 详解 | [SEAL 排名规则](07-g3-item-set.md#seal)、[阈值](05-g1-within-item.md#threshold) |
| 来源 | [HSS 论文](https://labs.scale.com/papers/humanitys-sixth-sense)、[MCP Atlas](https://scale.com/leaderboard/mcp_atlas) |

<a id="matharena"></a>
## MathArena

| 项 | 内容 |
|---|---|
| 编码 | J1a / O2 / S1 / R1 / 单信号 → 平均（每题 4 次）→ G3a，缺格用 G3e IRT 补；证明题另见清单里的 IMO-ProofBench 行 |
| 出分步骤 | 新竞赛题出来后尽快测，降低污染 → 每题跑 4 次取平均 → 没跑到的模型和比赛组合用 IRT 估计补上再平均 |
| 误差 | 置信区间用模拟后重新拟合 IRT 得到 |
| 坑 | 补出来的格子是统计模型的预测值；AIME、HMMT 每届只有 30 题左右，误差条很宽 |
| 详解 | [IRT](07-g3-item-set.md#irt)、[标准误](09-conditions-corrections-uncertainty.md#error-bars) |
| 来源 | [matharena.ai](https://matharena.ai/) |

<a id="livebench"></a>
## LiveBench

| 项 | 内容 |
|---|---|
| 编码 | J1a + J1b / O2 + O3 / S1 / R1 / 单信号 → 单次 → G3a，类别内平均再对类别平均 |
| 原则 | 只用客观答案，不用 LLM 判官；定期换新题以降低污染 |
| 时间 | 2024-06 起滚动更新，2026-06-25 仍有新版本 |
| 坑 | 版本之间题目不同，跨版本比要看版本日期 |
| 来源 | [livebench.ai](https://livebench.ai/) |

<a id="metr"></a>
## METR Time Horizon 1.1

| 项 | 内容 |
|---|---|
| 编码 | J1b / O4 / S1 / R5 人类耗时 / 单信号 → 多次平均 → G3c logistic 读 50% 点 |
| 出分步骤 | 228 个任务，每个任务有人类完成耗时 → 对"成功率 ~ log(人类耗时)"拟合 logistic → 读成功率 50% 处的人类耗时 |
| 误差与时间 | 任务族、任务、运行三层分层 bootstrap；TH1 到 TH1.1 断代 |
| 详解 | [METR 时间跨度](07-g3-item-set.md#metr) |

<a id="eci"></a>
## Epoch ECI

| 项 | 内容 |
|---|---|
| 编码 | 继承 / G4c 联合拟合 |
| 出分步骤 | 每个 bench 一个难度和斜率，每个模型一个能力，联合拟合 → 线性缩放到 Claude 3.5 Sonnet = 130、GPT-5 = 150；至少 4 个 bench 才给分 |
| 详解 | [G4c](08-g4-cross-bench.md#joint-fit) |
| 来源 | [epoch.ai/benchmarks/eci](https://epoch.ai/benchmarks/eci) |

<a id="arc"></a>
## ARC-AGI-3

| 项 | 内容 |
|---|---|
| 编码 | J1b / O5 动作数 / S3 / R5 人类基线 / 加权（权重是关卡号，关分是人类动作数和 AI 动作数之比的平方）→ 单次 → G3a → G4e 并报成本 |
| 坑 | 测的主要是效率；文档写的上限和公式算出来的值不一致，见 [加权](05-g1-within-item.md#weighted) |
| 来源 | [方法](https://docs.arcprize.org/methodology)、[榜单](https://arcprize.org/leaderboard) |

<a id="frontierswe"></a>
## FrontierSWE V2

| 项 | 内容 |
|---|---|
| 编码 | J1b / O3 / S3 / R3 / 加权 → mean@5（须线 worst@5 到 best@5）→ G3a → G4e 成本、运行时间、token 帕累托 |
| 出分条件 | 34 题，每题 5 次，每次 20 小时预算 |
| 坑 | V1 的头条是支配分（按名次），V1 和 V2 不能比，见 [G3f](07-g3-item-set.md#rank) |
| 来源 | [frontierswe.com](https://www.frontierswe.com/) |

<a id="healthbench"></a>
## HealthBench Professional

| 项 | 内容 |
|---|---|
| 编码 | J2 / O3 / S1 每条细则 / R2 含负分 / 加权 → 单次（另报 worst-at-k）→ 全集平均后裁到 [0,1] |
| 出分条件 | 判官 GPT-5.4；OpenAI 测对手时也用自己的判官重跑 |
| 修正 | 长度校正 |
| 详解 | [加权](05-g1-within-item.md#weighted) |

<a id="swe-pro"></a>
## SWE-bench Pro

| 项 | 内容 |
|---|---|
| 编码 | J1b / O3 补丁 / S1 / R1 / 全过（F2P 和 P2P 测试都过）→ 单次 → G3a |
| 出分条件 | 公开、保留、商业子集分开报；框架不同分数不同 |
| 详解 | [SWE-bench 的测试判定](01-judge.md#j1b) |
| 来源 | [arXiv 2509.16941](https://arxiv.org/abs/2509.16941) |

<a id="kaggle"></a>
## Kaggle Game Arena 统一榜

| 项 | 内容 |
|---|---|
| 编码 | J1b 游戏结算 / O4 / S4 化成两两胜负 / R6 / 单信号 → 单次 → G3b pooled BT，每个游戏按对局数倒数加权 |
| 坑 | 扑克的"赢多少"变成"赢没赢"；狼人杀的联盟结构被拆掉 |
| 详解 | [G4c](08-g4-cross-bench.md#joint-fit) |
| 来源 | [Kaggle 博客](https://www.kaggle.com/blog/unified-game-arena-leaderboard) |
