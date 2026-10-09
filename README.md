# 大模型测评的最后一步：分数是怎么算出来的

这个仓库讲模型输出交上来以后，判分、合并、换算成榜单数字的每一步，用一套五轴分类给 2025 年以后仍在用的 236 个测评编码，并给每个术语配上算得出来的例子。

核对日期：2026-10-09。所有时间按北京时间。

<a id="classes"></a>
## 三类入口

Justin 最初把测评分成三类。这三类仍然是最好用的入口，五条轴是把每一类拆开以后的样子。

| 类 | 一句话 | 在五条轴上的位置 | 怎么认 |
|---|---|---|---|
| 1. 单模型直接出分 | 一道题自己就能出分，不需要别的被测模型在场。verifier、LLM 判官、pass@k、maj@k、预训练和 SFT 阶段的评测都在这里 | 参照是 [R1 预设标准](docs/04-reference.md)、[R2 评分细则](docs/04-reference.md)，加上 [R7 自身参照](docs/04-reference.md#r7)（MASK、政治中立性、NoLiMa） | 新模型上榜，老模型的分不变；有"对"或"满足细则"的概念 |
| 2. 多模型比较 | 先让一批模型都跑一遍，再比谁好 | 参照是 [R6 对手池](docs/04-reference.md#r6)，合并用 [G3b 对池拟合](docs/07-g3-item-set.md) | 新模型上榜，老模型的分会变 |
| 3. 其他 | 前两类装不下的 | [R4 固定参照产出](docs/04-reference.md)、[R5 人类标尺](docs/04-reference.md)、[R3 开放量](docs/04-reference.md)；真实使用（[J5](docs/01-judge.md#j5) / [O6](docs/02-object.md)）；跨 bench 指数（[G4](docs/08-g4-cross-bench.md)）；[元评测](docs/01-judge.md#meta)（被评的是判官） | 对手固定、单位是人类的量、没有满分、没有题集、只合并别人的分，或被评者是判官 |

三点补充：

- 第 2 类里的 Elo、BT 只是合并工具，和判官是谁无关。人（Arena）、LLM（GDPval-AA）、程序（Kaggle 国际象棋）都能当第 2 类的判官。
- "比较"可以发生在判分时（判官同时看两份输出，信号是 [S4 偏好](docs/03-signal.md#s4)），也可以发生在合并时（各自先打绝对分，再换算成谁赢谁，例如 FrontierSWE v1 和 AA-Briefcase 的细则路）。见[比较发生在判分时还是合并时](docs/03-signal.md#when-compare)。
- R3 开放量（经营余额、优化分）不需要对手，这一点像第 1 类；但它没有"答对"，单位也没有上限，清单里归第 3 类。

拿到一个榜，三步定位：

1. 新模型上榜后，老模型的分会变吗？会，就是第 2 类。
2. 不会，但它是在和一份固定产出比，或者单位是人类的耗时、步数、名次，或者分数没有上限？是，就是第 3 类。再看它是不是没有题集（真实使用）、是不是只合并别人的分（指数）、被评的是不是判官（元评测）。
3. 都不是，就是第 1 类。

清单里在用的 208 行，按入口：第 1 类 169 行，第 2 类 11 行，第 3 类 26 行（其中指数 7、元评测 4、真实使用 3），跨两类的 2 行（FrontierSWE v1 属第 2 类、v2 属第 3 类；Remote Labor Index 的自动化率属第 3 类、AI 之间的 Elo 属第 2 类）。

<a id="axes"></a>
## 五条轴

任何一个榜单数字，都能用五个问题描述：

```
模型输出 ─判官 J─ 对象 O ─→ 原子信号 S ─按参照 R 解读─→ G1 题内 → G2 多次采样 → G3 题集 → G4 跨 bench ─→ 榜单数字
```

| 轴 | 问的问题 | 取值 | 章节 |
|---|---|---|---|
| J 判官 | 谁来判这次输出 | J1a 抽取比对、J1b 执行与环境、J1c 形式化验证、J2 LLM 判官、J3 学来的打分器、J4 人工评判、J5 用户行为 | [01](docs/01-judge.md) |
| O 对象 | 判的是什么东西 | O1 概率、O2 短答案、O3 产物、O4 环境终态、O5 过程、O6 真实会话 | [02](docs/02-object.md) |
| S 信号 | 一次判定吐出什么 | S1 二值、S2 有序多档、S3 连续量、S4 偏好 | [03](docs/03-signal.md) |
| R 参照 | 拿什么当尺子 | R1 预设标准、R2 评分细则、R3 开放量、R4 固定参照产出、R5 人类标尺、R6 对手池、R7 自身参照 | [04](docs/04-reference.md) |
| G1 题内 | 一次作答里的多个信号怎么合成题分 | 单信号、全过、比例、加权、层级树、集合（F1、全召回精度、精确）、阈值、门控、归一化、判官合并（平均占比、多数、一致、重复众数、单侧覆盖、抽一个） | [05](docs/05-g1-within-item.md) |
| G2 采样 | 同一道题跑多次怎么合 | 单次、平均、pass@k、pass^k、worst@k、best@k、maj@k、选择器 | [06](docs/06-g2-sampling.md) |
| G3 题集 | 所有题怎么变成一个 bench 分 | G3a 平均类、G3b 对池拟合、G3c 对标尺换算、G3d 累计量、G3e 潜变量补题、G3f 按名次 | [07](docs/07-g3-item-set.md) |
| G4 跨 bench | 多个 bench 怎么合成指数 | G4a 固定权重、G4b 等权平均、G4c 联合统计拟合、G4d 按名次、G4e 并列不合并 | [08](docs/08-g4-cross-bench.md) |

会改变数字、但不属于"怎么判分"的东西（题集版本、思考档位、框架、用户模拟器、谁来跑、偏差修正、误差条、锚点和版本）写在数字旁边，不进五条轴，见[第 09 章](docs/09-conditions-corrections-uncertainty.md)。

最重要的一条轴是参照 R：只有 R6 会让新模型改变老模型的分。

## 目录

| 文件 | 内容 |
|---|---|
| [docs/01-judge.md](docs/01-judge.md) | 判官：答案抽取、数学等价、单元测试、环境终态、形式化验证、LLM 判官的三种用法和偏差、人工、用户行为、元评测 |
| [docs/02-object.md](docs/02-object.md) | 对象：logprob 评测（CF、MCF、BPB）、短答案、产物、环境终态、过程、真实会话 |
| [docs/03-signal.md](docs/03-signal.md) | 信号：二值、多档、连续量、偏好，Plackett–Luce，比较发生在哪一层 |
| [docs/04-reference.md](docs/04-reference.md) | 参照：七种尺子，对手池为什么会改老分，锚点和冻结 |
| [docs/05-g1-within-item.md](docs/05-g1-within-item.md) | 题内合并：全过和比例、加权和负分、集合指标、阈值、门控、归一化、判官合并 |
| [docs/06-g2-sampling.md](docs/06-g2-sampling.md) | 采样合并：pass@k 无偏估计、pass^k、maj@k、选择器 |
| [docs/07-g3-item-set.md](docs/07-g3-item-set.md) | 题集合并：错答扣分、校准、在线 Elo、BT、平局、Crowd-BT、合成对局、风格控制、IPS、TrueSkill、对基线胜率、METR、Codeforces、IRT、按名次 |
| [docs/08-g4-cross-bench.md](docs/08-g4-cross-bench.md) | 跨 bench：AA 指数手算、等权、ECI 和 pooled BT、按名次的三个冠军、帕累托 |
| [docs/09-conditions-corrections-uncertainty.md](docs/09-conditions-corrections-uncertainty.md) | 出分条件、用户模拟器、偏差修正、私测选优、标准误、配对和聚类、bootstrap、版本断代 |
| [docs/leaderboards.md](docs/leaderboards.md) | 配方卡：AA 指数及组件、GDPval-AA、AA-Briefcase、Harvey LAB-AA、LMArena、Agent Arena、Vals、SEAL、MathArena、LiveBench、METR、ECI、ARC-AGI-3、FrontierSWE、HealthBench、SWE-bench Pro、Kaggle |
| [docs/bench-list.md](docs/bench-list.md) | 236 行测评清单，按领域分组，每行五轴编码和一手来源 |
| [data/bench-master.csv](data/bench-master.csv) | 清单的原始数据（UTF-8 带 BOM，Excel 可直接打开） |
| [scripts/](scripts/) | 文中所有数值例子的计算脚本 |

每章里每个术语按同一个顺序写：一句白话定义，一个能手算的例子，真实榜单怎么用，读数时的坑。

## 测评清单

共 236 行：在用 208 行，仅作机制解释 19 行，评分不可核实 9 行。"在用"指 2025 年以后仍有厂商发布页、模型卡或第三方榜单在报分，而且评分方式能从公开材料确认。按领域分 23 组，最大的几组是代码/软件工程 31、代理/经营/博弈 22、专业领域 17、多模态理解 17。分组明细、各轴取值计数和简称表见 [docs/bench-list.md](docs/bench-list.md)。

## 脚本

只用 Python 3 标准库，不需要安装任何包。在仓库根目录运行：

```bash
python3 scripts/basics.py        # 采样合并、在线 Elo 和 BT、风格控制、Crowd-BT、IPS、IRT、METR、跨 bench 合并、误差条
python3 scripts/mechanisms.py    # Plackett–Luce 和平局模型、合成对局、支配分、Codeforces、判官合并、集合指标、用户模拟器、效率、BPB
python3 scripts/bench_list.py    # 从 CSV 重新生成 docs/bench-list.md 并打印总数；加 --check 只核对
```

`basics.out.txt` 和 `mechanisms.out.txt` 是一次运行的输出，正文里的数字都能在里面找到。用到随机模拟的段落固定了随机种子。
