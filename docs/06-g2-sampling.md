# 合并链 G2：同一道题跑多次怎么合

同一道题让模型做 $n$ 次，其中 $c$ 次判对。把这 $n$ 个结果变成这道题的一个数，有好几种算法，它们回答的是不同的问题。

| 取值 | 回答的问题 | 例子 | 清单里在用的行数 |
|---|---|---|---|
| 单次 | — | 多数 AA 单次评测 | 148 |
| 平均（pass@1、avg@k、mean@k） | 随手问一次答对的概率 | AA 的 Terminal-Bench 4.0（3 次）、CritPt（5 次）、FrontierSWE v2 mean@5 | 44 |
| pass@k | 给 k 次机会至少对一次：上限、覆盖面 | ARC-AGI-2（pass@2）、ZeroBench（pass@5） | 10 |
| pass^k | k 次全对：稳不稳 | τ²-bench、AA-AnalystAgent（pass^5） | 5 |
| worst@k / best@k | k 次里最差或最好那次，适合连续分 | HealthBench worst-at-k、FrontierSWE v2 的须线 | 1 / 4 |
| maj@k | 先对 k 个答案投票，再判众数对不对 | DeepSeek-R1 的 cons@64 | 1 |
| 选择器 | 生成 N 个，由奖励模型、测试或规则挑一个再判 | DS-V4 的 Codeforces（32 个候选里排出 10 次提交） | 1 |

贯穿全章的例子：一道题，标准答案 `1/2`，采样 10 次，3 次答对（$n=10$，$c=3$）。所有数字由 `python3 scripts/basics.py` §1 算出。

---

## 平均：pass@1

每题跑 $n$ 次，算对了几成，再在所有题上平均：

$$
\text{pass@1}=\frac{1}{N}\sum_{i=1}^{N}\frac{c_i}{n}
$$

例子里这道题 pass@1 = 3/10 = 0.3。三道题分别 9/10、3/10、0/10 对，pass@1 = (0.9+0.3+0)/3 = 0.40。

AA 的写法相同：多次重复的 pass@1 把所有重复里的每次尝试都当一个实例平均。DeepSeek-R1 也叫它 pass@1，有人叫 avg@k。DeepSeek-R1 说贪心解码评测长推理模型会导致重复和检查点之间大幅波动，所以用温度 0.6、top-p 0.95，AIME 和 GPQA 每题采 64 次再平均。

坑：重复次数不改变期望，只降低方差。名字都叫 pass@1，"采 1 次"和"采 64 次取平均"期望相同，抖动幅度差很多。AIME 每年 30 题，单次运行的标准差可达 5–15 个百分点（"A Sober Look"，2025）。重复只能消掉模型采样的噪声，消不掉"题目是从所有可能的题里抽出来的"那部分噪声，见[误差条](09-conditions-corrections-uncertainty.md#error-bars)。

<a id="passk"></a>
## pass@k

给 k 次机会，至少对一次的概率。标准做法是采 $n\ge k$ 次，用组合数算"从 $n$ 次里随机挑 $k$ 次、全挑到错的"概率，再用 1 减：

$$
\text{pass@}k=\mathbb{E}_i\left[1-\frac{\binom{n-c_i}{k}}{\binom{n}{k}}\right]
$$

例子：$k=2$ 时 $1-\binom{7}{2}/\binom{10}{2}=1-21/45=0.5333$；$k=5$ 时 $1-\binom{7}{5}/\binom{10}{5}=1-21/252=0.9167$。三道题 9/3/0 的题库，pass@5 = 0.6389。

为什么不直接用 $1-(1-\hat p)^k$？把 $\hat p=0.3$ 代进去，$k=2$ 得 0.51，$k=5$ 得 0.8319，都偏低。代入式相当于有放回抽样，组合数形式（Codex 论文）在每道题上都是无偏的。human-eval、lighteval、Inspect 的实现都用它的乘积形式 $1-\prod_{i=n-c+1}^{n}(1-k/i)$，数值更稳。（[Codex 论文](https://arxiv.org/abs/2107.03374)）

ARC-AGI-2 允许每题提交 2 次，就是 pass@2，因为它的人类校准就是"至少两个人在 2 次以内解出"。

坑：pass@k 随 k 单调上升，拿 pass@64 和别人的 pass@1 比是不公平的比较。选择题、答案空间小的题（0–999 的整数），k 一大自然接近 1。$n$ 太小或 $k$ 接近 $n$ 时估计不稳，OLMo 3 为此专门加大了 $n$。

### RL 有没有扩展能力边界

pass@k 在 k 很大（比如 256）时可以粗略当作"这道题到底能不能做出来"。Yue 等（2025-04）发现 k 小时 RL 后的模型更好，k 大了基座模型追上并反超，结论是 RLVR 提高了低 k 的命中率、收窄了覆盖面；ProRL（2025-05）训练更久后在各个 k 上都超过基座；CoT-pass@k 要求推理也对（见 [O5](02-object.md#o5)），在这个口径下 RL 模型在各个 k 上都更好。争论有一部分是口径之争：只看答案时，大 k 下"推理错但蒙对"会被算成能力。（[Yue 等](https://arxiv.org/abs/2504.13837)、[ProRL](https://arxiv.org/abs/2505.24864)）

## pass^k

同一题连跑 k 次，每次都对的概率。它衡量可靠性，客服、分析师这类"每次都得靠谱"的场景最关心它：

$$
\text{pass}^k=\mathbb{E}_i\left[\frac{\binom{c_i}{k}}{\binom{n}{k}}\right]
$$

例子：$\text{pass}^2=\binom{3}{2}/\binom{10}{2}=3/45=0.0667$，而 pass@2 = 0.5333，差 8 倍；$\text{pass}^3=\binom{3}{3}/\binom{10}{3}=1/120=0.0083$（代入式 $0.3^3=0.027$）；只对了 3 次，$\text{pass}^5=0$。三道题 9/3/0 时 pass^5 = 0.1667，三道题 10/3/0 时 pass^3 = 0.3361。

| 同一道题（3/10） | pass@1 | pass@2 | pass@5 | pass^2 | pass^3 |
|---|---|---|---|---|---|
| 组合数估计 | 0.3 | 0.5333 | 0.9167 | 0.0667 | 0.0083 |
| 代入式 | 0.3 | 0.51 | 0.8319 | 0.09 | 0.027 |

真实榜单：τ-bench 提出它，GPT-4o 在 τ-retail 上 pass^8 降到约 25%。AA-AnalystAgent 头条是 pass^5，理由是"分析 agent 只有在不用复核时才有用"，同时报 pass@1 和 pass@5 区分可靠性和上限。

同一个 bench，跑的人不同，采样合并口径就不同。τ³-Banking 在 AA 是 97 题各跑 5 次、报 pass@1（平均），τ-bench 原版报 pass^k。AA 页面的 τ³-Banking 和 Sierra 论文里的 pass^k 不能放在一起比。

坑：pass^k 随 k 塌得很快，必须标明 k；用户模拟器会让同一题的失败相关，这时 pass^k 不再等于 $p^k$（见[用户模拟器](09-conditions-corrections-uncertainty.md#user-simulator)）。

## worst@k 和 best@k

连续分没法数"对了几次"，就取 k 次里最差或最好那次。HealthBench 的 worst-at-k 是 k 个回答里最差那次的细则分，再在题间平均，相当于连续分版的 pass^k。FrontierSWE v2 的柱子是 mean@5，须线从 worst@5 画到 best@5；FrontierSWE v1 的实现类任务没有一个模型做完，就用 best@5 的测试通过率当部分分；GDM 报 OSWorld 时取 3 次里的最大值。

坑：同一组采样报 best 还是 mean，常常不写清楚。best@k 和 pass@k 一样随 k 上升。

<a id="maj"></a>
## maj@k

采 k 次，先对抽出的答案投票，票数最多的答案作为最终答案，再判对错：

$$
\text{maj@}k=\frac{1}{N}\sum_i\mathbb{1}\big[\operatorname{mode}(a_{i,1},\dots,a_{i,k})=y_i\big]
$$

例 1：某题 8 个答案是 42、42、17、42、17、17、17、9，正确答案 42。计票 17 四票、42 三票，众数 17 是错的，maj@8 = 0；同一份采样 avg@8 = 3/8 = 0.375，pass@8 = 1。三种口径给出 0、0.375、1。

例 2：回到 3/10 那道题，错答案有两种情况。

- 错答案扎堆：`1/2, 1/3, 1/3, 1/2, 1/3, 2, 1/2, 1/3, 1/3, 7`，`1/3` 有 5 票，maj@10 = 0。
- 错答案分散：`1/2, 1/3, 5, 1/2, 2/3, 2, 1/2, 3/4, 1, 7`，其余答案各 1 票，`1/2` 以 3 票胜出，maj@10 = 1。

pass@1 都是 0.3，maj@10 一个是 0、一个是 1，取决于模型是"一致地错"还是"随机地错"。如果对每次的判定（对/错）取众数，两种情况都是 3 对 7 错，众数是"错"，结果都是 0。Inspect 的 `mode` reducer 做的是后者，它属于 [G1 的重复众数](05-g1-within-item.md#judge-merge)，和 maj@k 不是一回事。

坑：投票要在等价判定之后做，`1/2`、`0.5`、`\frac{2}{4}` 应算同一票，字符串规范化不等于数学等价；开放式回答没法投票；平票规则要写清楚；maj@k 和 pass@1 混在一张表里时，常被误读成"模型更强"，它评的是"模型 + 投票"这个系统。

<a id="selector"></a>
## 选择器

采 N 个，让奖励模型、测试用例或规则挑一个，再用真值判挑出来的那个：

$$
\text{BoN@}N=\frac{1}{N_q}\sum_i\mathbb{1}\big[\arg\max_{j\le N}r(a_{i,j})\ \text{正确}\big]
$$

选择器 $r$ 如果就是真值判定器，它退化为 pass@N；$r$ 越弱越接近 pass@1。用例 1 的 8 个答案，奖励模型如果最喜欢某个 42，得 1 分，最喜欢某个 17，得 0 分。

真实例子：DS-V4 的 Codeforces 每题生成 32 个候选，无放回抽 10 个随机排成提交顺序；OpenAI 的 o1-ioi 加上测试筛选后 rating 从 1807 到 2092 再到 2214。选择器是被测系统的一部分，必须和分数一起报。换算 rating 的方法见 [G3c Codeforces](07-g3-item-set.md#codeforces)。

在 Arena 上私下测 N 个变体、只公开最好的那个，也是 best-of-N，只是选择器换成了榜单本身，见[修正](09-conditions-corrections-uncertainty.md#leaderboard-illusion)。
