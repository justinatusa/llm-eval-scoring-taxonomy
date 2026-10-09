# 第 7 章 读懂几个主流榜单

前六章按机制讲，这一章倒过来，从读者最常看到的榜单出发，看每个头条数字背后走了哪几步。每个榜单一段，涉及的机制都在前面讲过，这里只指回去。

<a id="7-1"></a>

## 7.1 Artificial Analysis

AA 的智能指数是十个组件的加权和（第 5 章）。Agents 类占 30%，编程占 20%，通用占 30%，科学推理占 20%；两个 Elo 类组件在模型进入指数时冻结，再用 clamp((Elo − 500)/2000) 压到 0 到 1。各组件自己出分：Terminal-Bench 4.0 是 66 道题各跑 3 次、用 mini-swe-agent 框架、全部测试通过才算对；SciCode 是 288 个子问题各跑 3 次；HLE 和 AA-LCR 让 GPT-5.6 Luna (medium) 做等价判定；AA-Omniscience 有 6000 道私有题，准确率和"1 − 幻觉率"拆成两个组件；GDP.pdf 是 100 道题各跑 5 次，同样由 GPT-5.6 Luna 逐条判细则，全部通过才算；CritPt 交给官方评分服务器；AutomationBench-AA 有 657 道题，碰了护栏整题记 0。温度方面，非推理模型用 0，推理模型用 0.6，API 失败最多重试 30 次。指数的小版本之间不可比，厂商发布页引用的常常是更早的版本（[AA 方法页](https://artificialanalysis.ai/methodology/intelligence-benchmarking)）。

GDPval-AA 用 GDPval 的 220 道题，模型在 Stirrup 框架里最多跑 250 轮，交出文件。两个模型的交付物配成一场，每场从三个判官（Claude Opus 5、GPT-5.6 Sol、Gemini 3.8 Flash）里抽一个盲评，平局各算半胜，再用 Crowd-BT 拟合，锚定 DeepSeek V4.1 Flash (max) = 1600，95% 区间用 sandwich 估计。配对先均衡抽样，再让分数相近的模型多比。这里的判官和 GDP.pdf 的单一判官 GPT-5.6 Luna 不是一回事，两者容易混。第二版锚的是人类专家 = 1000，所以 DeepSeek-V4 报告里的 1554 只能和第二版的数比（3.8 节）。

AA-Briefcase 有 91 道题、4 个场景。分析质量和呈现两项是判官两两比较；细则一项由三判官里抽一个判，同一条细则固定由同一个判官判，再把通过率改写成假想的对局。三项分别拟合 Crowd-BT，锚定 GPT-5.5 (medium) = 1000。细则分本来是绝对的，改写成对局以后，也会随对手池变化（3.7 节）。

Harvey LAB-AA 不进指数，却是"全过"和"比例"差距最大的例子。120 个私有法律任务，每题有 44 到 90 条细则。三个判官（GPT-6 Sol、Grok 4.7、Claude Opus 5.5）各自逐条判，每题的分是"判了全部细则通过的判官占比"，只能取 0、⅓、⅔、1（2.2 节）。有实质性幻觉的题直接记 0，幻觉由一个判官列举、另一个判官 GPT-6 Sol (high) 对照材料逐条复核。同一套评测还报逐条通过率，同一份判定在两个口径下可以差出几倍（2.1 节）。

<a id="7-2"></a>

## 7.2 LMArena 和 Agent Arena

LMArena 的文本榜由用户实时提问，两个匿名模型作答，用户投票，平局拆成两个半场，用 BT 拟合，换到 Elo 刻度（3.3 节）。默认视图带风格控制，对局按频率重新加权，事实性对局是一个默认关闭的开关（3.5 节），区间用 Arena-Rank 的闭式算法。题目分布随用户群变化，私测变体只公开最好的会抬分（6.2 节）。

Agent Arena 来自同一家，机制完全不同。它在真实编程会话里随机分配编排模型，从会话中挖五个信号，每个信号用逆倾向加权算出相对均匀分配的净提升，五个等权平均，就是头条的 Net Improvement（第 4 章）。10 月 2 日的榜上，Claude Fable 5.1 (Max) 的 Net Improvement 是 14.31% ±1.90%，Confirmed Success 一栏是 17.64% ±2.82%。两个数都是相对均匀分配基线的提升，单位是百分点，不能当成功率引用（[榜单](https://arena.ai/leaderboard/agent)）。

<a id="7-3"></a>

## 7.3 Vals

Vals 维护约 30 个 bench 和一个按行业 GDP 加权的指数，各 bench 的做法差别很大。Finance Agent 让判官 GPT-5.2 判三次取众数，部分分和全过两种口径的排名会翻转，页面还画了成本的帕累托曲线。Legal Research Bench 用单个判官逐条判细则，同一个模型全过口径 55.29、加权通过率 90.58。ProofBench 用 Lean 4 编译判定证明，100 道题只能提交一次，已经有 4 个模型并列满分，页面另报每任务成本。扑克榜用 TrueSkill，以 1000 为基线。Vals 还把降级到其他模型的任务分开报，给 Claude Opus 5 报了"含降级"和"降级记失败"两个分（6.1 节，[vals.ai](https://www.vals.ai/benchmarks)）。

<a id="7-4"></a>

## 7.4 Scale SEAL

SEAL 的每个 bench 自己出分，名次另有规则：名次等于 1 加上"区间下界高于本模型区间上界"的模型数，区间重叠就可以并列（2.4 节）。Humanity's Sixth Sense 有 522 道题，其中 288 道图像、234 道视频，Claude Opus 5 逐条判细则，每题跑 3 次取平均，按题做 bootstrap 得 95% 区间，人类基线是 93.1%（[论文](https://labs.scale.com/papers/humanitys-sixth-sense)）。MCP Atlas 的判官给每个要点 1、0.5 或 0 分，覆盖率达到 0.75 算通过。HiL-Bench 报提问精确率和阻塞召回率的调和平均，再报 Pass@3。

<a id="7-5"></a>

## 7.5 MathArena 和 LiveBench

这两个榜都靠换新题对付污染。MathArena 在新竞赛题公布后尽快测，每题跑 4 次取平均，用程序比对最终答案；没跑到的模型和比赛组合用项目反应理论补上再平均，区间也用模拟后重新拟合得到（[matharena.ai](https://matharena.ai/)）。补出来的格子是统计模型的预测，AIME、HMMT 每届只有 30 道左右的题，区间很宽（6.3 节）。LiveBench 只用有客观答案的题，不用 LLM 判官，定期换题，类别内平均后再对类别平均，跨版本比较时要看版本日期（[livebench.ai](https://livebench.ai/)）。

<a id="7-6"></a>

## 7.6 METR 和 Epoch

METR 时间跨度 1.1 版有 228 个任务，每个任务标有人类完成耗时，对成功率和人类耗时的对数拟合逻辑回归，读出成功率 50% 处的耗时，区间来自任务族、任务、运行三层的 bootstrap（1.6 节）。和 1.0 版的数字不能直接比。Epoch 的 ECI 把每个 bench 当成一道大题，联合拟合所有模型的能力，线性缩放到 Claude 3.5 Sonnet = 130、GPT-5 = 150，至少有 4 个 bench 的成绩才给分，当前最高的是 Claude Opus 5.5，167（第 5 章，[epoch.ai](https://epoch.ai/benchmarks/eci)）。

<a id="7-7"></a>

## 7.7 ARC-AGI-3 和 FrontierSWE

ARC-AGI-3 的每关分是人类首玩动作数和 AI 动作数之比的平方，按关卡号加权成游戏分，游戏分不超过已通关卡的权重占比，所以分数由通关多少和效率共同决定；榜单同时把每任务成本画出来（1.6 节，[方法](https://docs.arcprize.org/methodology)）。FrontierSWE 第二版有 34 个工程任务，每题跑 5 次、每次 20 小时预算，柱子画平均，须线从最差画到最好，再画成本、运行时间和 token 的帕累托前沿；当前头名 GPT-6 Astra 是 65.5% ±8.9。第一版的头条是按名次算的支配分，两版不能比（3.7 节，[frontierswe.com](https://www.frontierswe.com/)）。

<a id="7-8"></a>

## 7.8 HealthBench Professional 和 SWE-bench Pro

HealthBench Professional 用 GPT-5.4 当判官，按医生写的带正负分值的细则逐条判，题分可以是负的，在全集平均之后才裁到 0 到 1，另报最差一次的 worst-at-k，并做了长度校正（2.1 节）。OpenAI 测别家模型时也用自己的判官重跑。SWE-bench Pro 让模型提交补丁，原本失败的测试要通过、原本通过的测试不能坏，两组都过才算解决；公开、保留、商业三个子集分开报，用的 agent 框架不同，分数也不同（1.2 节，[arXiv 2509.16941](https://arxiv.org/abs/2509.16941)）。

<a id="7-9"></a>

## 7.9 Kaggle Game Arena

Kaggle 的统一榜把国际象棋、扑克、狼人杀的对局都化成两两胜负，放进同一个 BT，每个游戏除以自己的对局总数，让三个游戏的总权重相同（第 5 章）。代价是扑克只剩"赢没赢"、不再计较赢了多少，狼人杀的阵营结构也被拆掉了（[Kaggle 博客](https://www.kaggle.com/blog/unified-game-arena-leaderboard)）。各游戏自己的榜各有算法：国际象棋每对模型下 40 局、最弱者记 0，扑克用每 100 手赢多少个大盲，狼人杀用博弈均衡排名（3.6 节、1.7 节）。
