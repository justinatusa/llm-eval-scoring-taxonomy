#!/usr/bin/env python3
"""进阶机制例子：Plackett–Luce、平局模型、合成对局、支配分、Codeforces 换算、判官合并、集合指标、用户模拟器、效率、BPB。
只用 Python 标准库。运行：python3 scripts/mechanisms.py"""
import math, random, statistics, itertools

LOG10E400 = 400 / math.log(10)   # 把自然对数尺度的 θ 换成 Elo 尺度
def hr(t): print("\n" + "=" * 8 + " " + t + " " + "=" * 8)

# ---------------- §1 Plackett–Luce / 平局模型 ----------------
hr("§1a PL：一个完整排序的概率")
w = {"A": 3.0, "B": 2.0, "C": 1.0, "D": 0.5}
def pl_prob(order, w):
    p, rest = 1.0, list(order)
    for x in order:
        p *= w[x] / sum(w[y] for y in rest); rest.remove(x)
    return p
print("P(A>B>C>D) =", round(pl_prob("ABCD", w), 4), "= 3/6.5 * 2/3.5 * 1/1.5")
print("核对:", round(3/6.5*2/3.5*1/1.5, 4))
print("全部 24 个排序概率之和 =", round(sum(pl_prob(o, w) for o in itertools.permutations("ABCD")), 6))
# Y-of-X: 只报前 Y 名（top-Y）也能写似然
print("只看第一名 P(A 第一) =", round(3/6.5, 4), "；PL 在两两时退化为 BT: P(A>B)=3/5 =", 3/5)

hr("§1b PL 最大似然（Hunter MM） vs 拆成两两再跑 BT")
rankings = ["ABCD", "ABDC", "BACD", "ACBD", "CABD", "BADC", "ABCD", "DBAC", "ABCD", "BCAD"]
items = "ABCD"
def pl_mle(rankings, items, iters=2000):
    g = {i: 1.0 for i in items}
    for _ in range(iters):
        wins = {i: 0.0 for i in items}; den = {i: 0.0 for i in items}
        for r in rankings:
            for k in range(len(r) - 1):          # 最后一名那一步概率=1，不计
                wins[r[k]] += 1
                s = sum(g[x] for x in r[k:])
                for x in r[k:]: den[x] += 1 / s
        g = {i: wins[i] / den[i] for i in items}
        z = math.exp(statistics.mean(math.log(v) for v in g.values()))
        g = {i: v / z for i, v in g.items()}
    return g
def bt_mle(pairs, items, iters=5000, half_ties=None):
    """pairs: list of (winner, loser, weight)。MM 算法。"""
    g = {i: 1.0 for i in items}
    for _ in range(iters):
        W = {i: 0.0 for i in items}; D = {i: 0.0 for i in items}
        for a, b, c in pairs:
            W[a] += c
            D[a] += c / (g[a] + g[b]); D[b] += c / (g[a] + g[b])
        g = {i: (W[i] / D[i] if D[i] else g[i]) for i in items}
        z = math.exp(statistics.mean(math.log(v) for v in g.values()))
        g = {i: v / z for i, v in g.items()}
    return g
def elo(g, anchor=None, base=1000):
    e = {i: LOG10E400 * math.log(v) for i, v in g.items()}
    off = base - (e[anchor] if anchor else statistics.mean(e.values()))
    return {i: round(v + off) for i, v in e.items()}
pl = pl_mle(rankings, items)
pairs_full = [(r[i], r[j], 1) for r in rankings for i in range(4) for j in range(i + 1, 4)]
pairs_top = []
# Design Arena 式：4 个模型两组先比，胜者对胜者、负者对负者，再一场定 2/3 名 → 5 场两两
for r in rankings:
    pos = {m: k for k, m in enumerate(r)}
    A, B, C, D = sorted(items)  # 固定初始分组 (A,B) (C,D)
    w1, l1 = (A, B) if pos[A] < pos[B] else (B, A)
    w2, l2 = (C, D) if pos[C] < pos[D] else (D, C)
    for x, y in [(w1, l1), (w2, l2)]: pairs_top.append((x, y, 1))
    for x, y in [(w1, w2), (l1, l2)]: pairs_top.append((x, y, 1) if pos[x] < pos[y] else (y, x, 1))
    s1 = max([w1, w2], key=lambda m: pos[m]); s2 = min([l1, l2], key=lambda m: pos[m])
    pairs_top.append((s1, s2, 1) if pos[s1] < pos[s2] else (s2, s1, 1))
bt_full = bt_mle(pairs_full, items); bt_top = bt_mle(pairs_top, items)
print("PL MLE Elo:          ", elo(pl))
print("全拆两两(6对/排序) BT:", elo(bt_full))
print("Design Arena 式 5 场 BT:", elo(bt_top), " 两两场次:", len(pairs_top))
print("三者名次:", [sorted(items, key=lambda i: -x[i]) for x in (pl, bt_full, bt_top)])

hr("§1c 平局：Davidson 与 Rao–Kupper")
pi, pj = 2.0, 1.0
nu = 0.5
den = pi + pj + nu * math.sqrt(pi * pj)
dav = (pi / den, pj / den, nu * math.sqrt(pi * pj) / den)
print("Davidson ν=0.5: P(i胜)=%.4f P(j胜)=%.4f P(平)=%.4f 和=%.4f" % (*dav, sum(dav)))
th = 1.5
rk_i = pi / (pi + th * pj); rk_j = pj / (pj + th * pi)
print("Rao–Kupper θ=1.5: P(i胜)=%.4f P(j胜)=%.4f P(平)=%.4f 和=%.4f" % (rk_i, rk_j, 1 - rk_i - rk_j, 1))
print("  平局闭式 (θ²−1)πiπj/((πi+θπj)(πj+θπi)) =", round((th**2 - 1) * pi * pj / ((pi + th * pj) * (pj + th * pi)), 4))
# 平局记半胜 vs Davidson 拟合：同一组数据
games = [("A", "B", "w")] * 6 + [("A", "B", "t")] * 8 + [("A", "B", "l")] * 2 + \
        [("B", "C", "w")] * 5 + [("B", "C", "t")] * 1 + [("B", "C", "l")] * 4 + \
        [("A", "C", "w")] * 7 + [("A", "C", "t")] * 0 + [("A", "C", "l")] * 3
half = []
for a, b, o in games:
    if o == "w": half.append((a, b, 1))
    elif o == "l": half.append((b, a, 1))
    else: half += [(a, b, .5), (b, a, .5)]
g_half = bt_mle(half, "ABC")
def davidson_fit(games, items, iters=4000, lr=0.05):
    th = {i: 0.0 for i in items}; lnu = 0.0
    for _ in range(iters):
        grad = {i: 0.0 for i in items}; gnu = 0.0
        for a, b, o in games:
            pa, pb, nu_ = math.exp(th[a]), math.exp(th[b]), math.exp(lnu)
            s = math.sqrt(pa * pb); d = pa + pb + nu_ * s
            # d log d / d th_a
            dda = (pa + nu_ * s / 2) / d; ddb = (pb + nu_ * s / 2) / d; ddn = nu_ * s / d
            if o == "w": grad[a] += 1 - dda; grad[b] += -ddb; gnu += -ddn
            elif o == "l": grad[b] += 1 - ddb; grad[a] += -dda; gnu += -ddn
            else: grad[a] += .5 - dda; grad[b] += .5 - ddb; gnu += 1 - ddn
        for i in items: th[i] += lr * grad[i] / len(games) * 10
        lnu += lr * gnu / len(games) * 10
        m = statistics.mean(th.values()); th = {i: v - m for i, v in th.items()}
    return {i: math.exp(v) for i, v in th.items()}, math.exp(lnu)
g_dav, nu_hat = davidson_fit(games, "ABC")
print("平局记半胜 BT Elo:", elo(g_half), "  Davidson Elo:", elo(g_dav), " ν̂=%.3f" % nu_hat)
print("  A–B 有 8 场平局；两种口径名次相同，分差不同")

# ---------------- §2 合成对局 ----------------
hr("§2 AA-Briefcase 合成对局的几种读法（AA 未公开比较单位和平局规则）")
# 3 个模型，4 个任务，每任务的细则通过数 / 细则总数
checks = [10, 10, 20, 5]
passed = {"M1": [9, 6, 10, 5], "M2": [8, 7, 15, 3], "M3": [8, 6, 12, 4]}
models = list(passed)
def crowd_bt_p(theta_i, theta_j, eps=0.0):
    s = 1 / (1 + math.exp(-(theta_i - theta_j))); return eps + (1 - 2 * eps) * s
print("Crowd-BT ε=0 退化为 BT: p=", crowd_bt_p(0.4, 0.0, 0), " vs σ(0.4)=", round(1/(1+math.exp(-0.4)), 6))
print("ε=0.1 时 p=", round(crowd_bt_p(0.4, 0.0, 0.1), 6), " 上下限被压到 [0.1,0.9]")
def matches(variant):
    out = []
    for a, b in itertools.combinations(models, 2):
        for t in range(len(checks)):
            ra, rb = passed[a][t] / checks[t], passed[b][t] / checks[t]
            if variant == "per_task_tie_half":
                if ra > rb: out.append((a, b, 1))
                elif rb > ra: out.append((b, a, 1))
                else: out += [(a, b, .5), (b, a, .5)]
            elif variant == "per_task_ties_dropped":
                if ra > rb: out.append((a, b, 1))
                elif rb > ra: out.append((b, a, 1))
            elif variant == "fractional":   # 按通过率当软胜：a 得 ra/(ra+rb)
                if ra + rb > 0: out += [(a, b, ra / (ra + rb)), (b, a, rb / (ra + rb))]
    if variant == "overall":
        tot = {m: sum(passed[m]) / sum(checks) for m in models}
        for a, b in itertools.combinations(models, 2):
            if tot[a] > tot[b]: out.append((a, b, 1))
            elif tot[b] > tot[a]: out.append((b, a, 1))
            else: out += [(a, b, .5), (b, a, .5)]
    return out
print("各模型逐任务通过率:", {m: [round(p / c, 2) for p, c in zip(passed[m], checks)] for m in models})
print("各模型总通过率(微平均):", {m: round(sum(passed[m]) / sum(checks), 3) for m in models})
for v in ["per_task_tie_half", "per_task_ties_dropped", "fractional"]:
    ms = matches(v)
    print(f"{v:24s} Elo(锚 M2=1000):", elo(bt_mle(ms, models), anchor="M2"))
ov = matches("overall")
print("overall(整体比一次)      对局:", ov, "→ 全胜全负，BT MLE 发散（需先验/正则），所以不可能是这种朴素读法")

# ---------------- §3 支配分 ----------------
hr("§3 支配分 = 对随机对手、随机任务的胜率 = (N − 平均名次)/(N − 1)")
ranks = {"P": [1, 2, 1], "Q": [2, 1, 3], "R": [3, 4, 2], "S": [4, 3, 4]}   # 3 个任务、4 个模型
N = 4; T = 3
for m in ranks:
    wins = sum(1 for t in range(T) for o in ranks if o != m and ranks[m][t] < ranks[o][t])
    dom = wins / ((N - 1) * T); avg = statistics.mean(ranks[m])
    print(m, "胜场", wins, "/", (N - 1) * T, "支配分=%.4f" % dom, " (N−avg)/(N−1)=%.4f" % ((N - avg) / (N - 1)))
# 有并列：并列取平均名次、对局记半胜，恒等式仍成立
ranks_t = {"P": [1.5, 1], "Q": [1.5, 2], "R": [3, 3]}
for m in ranks_t:
    w_ = sum((1 if ranks_t[m][t] < ranks_t[o][t] else .5 if ranks_t[m][t] == ranks_t[o][t] else 0)
             for t in range(2) for o in ranks_t if o != m)
    print("并列例", m, "支配=%.4f" % (w_ / 4), " 公式=%.4f" % ((3 - statistics.mean(ranks_t[m])) / 2))
fs_v1 = [("Claude Fable 5", 2.88, 88), ("GLM-5.3", 4.50, 78), ("Grok 4.6", 4.53, 78), ("Grok 4.5", 5.47, 72),
         ("GLM-5.2", 6.21, 67), ("Claude Opus 4.8", 6.35, 67), ("GPT-5.5", 6.68, 65), ("Claude Opus 4.7", 8.00, 56),
         ("Claude Opus 4.6", 9.18, 49), ("GPT-5.4", 9.65, 46), ("Gemini 3.1 Pro", 11.50, 34), ("Composer 2.5", 11.59, 34),
         ("GLM-5.1", 12.88, 26), ("DeepSeek V4 Pro", 13.06, 25), ("Kimi K2.5", 13.26, 23), ("Kimi K2.6", 13.44, 22),
         ("Qwen3.6-Plus", 13.82, 20)]
bad = [(n, a, d, round(100 * (17 - a) / 16, 1)) for n, a, d in fs_v1 if abs(100 * (17 - a) / 16 - d) > 0.5 + 100 * 0.005 / 16]
print("FrontierSWE v1 17 行核对 (N=17)，不符的行:", bad if bad else "无")
print("  例: 2.88 →", round(100 * (17 - 2.88) / 16, 1), "%；13.82 →", round(100 * (17 - 13.82) / 16, 1), "%")

# ---------------- §4 Codeforces ----------------
hr("§4 Codeforces：罚分口径 → 名次 → rating")
# 4a 罚分口径：模型某题的分 = 解出该题、且失败次数相同的人类得分的中位数
human_solves = {  # 题目 -> [(失败次数, 得分)]
    "A": [(0, 480), (0, 470), (1, 430), (0, 490), (1, 420)],
    "B": [(0, 900), (2, 760), (0, 940), (1, 850), (0, 910)],
    "C": [(1, 1500), (0, 1700), (1, 1450), (3, 1300)]}
model_attempts = {"A": 0, "B": 1, "C": None}  # 模型：A 首交过，B 失败 1 次后过，C 没过
score = 0
for p, f in model_attempts.items():
    if f is None: continue
    pool = [s for ff, s in human_solves[p] if ff == f]
    s = statistics.median(pool); score += s
    print(f"题 {p}: 失败 {f} 次 → 同失败次数人类得分 {pool} 中位数 {s}")
print("模型总分 =", score)
random.seed(0)
humans = sorted([random.gauss(1900, 350) for _ in range(40)], reverse=True)   # 40 名人类的赛前 rating
# 简化：人类名次与 rating 同序（真实比赛用实际得分排序）
model_rank = 11   # 假设总分排第 11（1-based，含模型自身共 41 人）
def P(ra, rb): return 1 / (1 + 10 ** ((rb - ra) / 400))
def seed(r, others, plus_one=True): return (1 if plus_one else 0) + sum(P(o, r) for o in others)
def solve(target, plus_one):
    lo, hi = 0, 5000
    for _ in range(60):
        mid = (lo + hi) / 2
        if seed(mid, humans, plus_one) > target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
r_cf = solve(model_rank, True)          # 官方：seed = 1 + Σ P(j 胜 i)
r_ce = solve(model_rank, False)         # CodeElo 论文式：m = Σ 1/(1+10^{(r−r_i)/400})，无 +1
# OpenAI 2502.06807：对“观测到的名次关系”做最大似然
def loglik(r):
    ll = 0
    for k, h in enumerate(humans):     # 人类 k 的名次：k<10 排在模型前，其余在后
        p = P(r, h)
        ll += math.log(1 - p) if k < model_rank - 1 else math.log(p)
    return ll
r_ml = max(range(0, 5001), key=loglik)
print("官方 seed(+1) 反解 rating = %.0f" % r_cf)
print("CodeElo 式(无 +1)     rating = %.0f   (与官方差 %.0f)" % (r_ce, r_ce - r_cf))
print("OpenAI 式名次似然 MLE  rating = %d" % r_ml)
print("  官方 seed(+1)=名次 正是该似然的一阶条件：Σ_h P(h 胜模型) = 排在模型前的人数 = 名次−1，所以两者一致；去掉 +1 等于把名次错算一位")
print("（官方真实更新还会取 seed 与实际名次的几何平均、再 (R−r)/2，这只对已有 rating 的选手生效）")
# 4b 多场平均与“百分位”
print("CodeElo 表 6 摘录：1073≈50 百分位，1603≈90，2157≈99（同一 rating 在不同年份人口里百分位不同）")

# ---------------- §5 判官合并 ----------------
hr("§5 判官合并：同一份判定矩阵，六种合法")
# 一个任务、5 条细则、3 个判官的 0/1 判定
J = [[1, 1, 1, 0, 1],   # 判官 1
     [1, 1, 0, 1, 1],   # 判官 2
     [1, 1, 1, 1, 1]]   # 判官 3
nc = 5
avg_share = [statistics.mean(J[k][c] for k in range(3)) for c in range(nc)]
maj = [int(sum(J[k][c] for k in range(3)) >= 2) for c in range(nc)]
una = [int(all(J[k][c] for k in range(3))) for c in range(nc)]
print("逐条 判官占比:", [round(x, 3) for x in avg_share], " 逐条通过率(微平均)=", round(statistics.mean(avg_share), 3))
print("逐条 多数票:", maj, " 全过?", int(all(maj)))
print("逐条 一致通过:", una, " 全过?", int(all(una)))
harvey = statistics.mean(int(all(J[k])) for k in range(3))
print("Harvey 式 all-pass = 判官里“全部细则都过”的占比 =", round(harvey, 3), "（只有判官 3 全过）")
print("单判官随机抽: 期望 all-pass =", round(harvey, 3), "但单次实现只能是 0 或 1")
# 单侧覆盖：确定性数值预检只能把 fail 改成 pass
llm = [0, 1, 0, 1]; precheck = [1, 0, 0, 1]
print("AnalystAgent 式单侧覆盖: LLM", llm, "预检", precheck, "→", [max(a, b) for a, b in zip(llm, precheck)])
# 方差：判官独立出错，比较几种合法的分数标准差
random.seed(1)
TRUTH = [1] * 60 + [0] * 40          # 固定 100 题，真实通过率 0.60
def sim(rule, err=0.15, reps=4000):
    truth = TRUTH
    scores = []
    for _ in range(reps):
        tot = 0
        for t in truth:
            v = [t if random.random() > err else 1 - t for _ in range(3)]
            tot += {"single": v[0], "avg": sum(v) / 3, "majority": int(sum(v) >= 2), "unanimous": int(all(v))}[rule]
        scores.append(tot / len(truth))
    return statistics.mean(scores), statistics.pstdev(scores), statistics.mean(truth)
for rule in ["single", "avg", "majority", "unanimous"]:
    m, s, tr = sim(rule)
    print(f"  {rule:9s} 均值={m:.3f} 标准差={s:.4f} （真实={tr:.2f}，每个判官独立错 15%）")
print("  理论期望: 单判官/平均 = .6×.85+.4×.15 = %.3f；多数 = .6×P(≥2 对)+.4×P(≥2 错) = %.3f；一致 = .6×.85³+.4×.15³ = %.3f" % (
    .6*.85+.4*.15, .6*(.85**3+3*.85**2*.15)+.4*(.15**3+3*.15**2*.85), .6*.85**3+.4*.15**3))

# ---------------- §6 集合指标 ----------------
hr("§6 集合 F1 vs 全召回下的精确率（ITBench-AA）")
gold_groups = [{"svc-a", "pod-a-1"}, {"db"}]          # 两个根因组（第一个有别名）
non_root = [{"svc-b"}]                                 # 非根因实体
def score_itb(pred):
    hit, fp, used = set(), 0, set()
    for p in pred:
        g = next((i for i, G in enumerate(gold_groups) if p in G), None)
        if g is None: fp += 1          # 未匹配或映射到非根因组都算 FP
        elif g in used: continue       # 同一别名组只算一次
        else: used.add(g); hit.add(g)
    if len(hit) < len(gold_groups): return 0.0
    return len(hit) / (len(hit) + fp)
def f1(pred, gold_flat):
    S, G = set(pred), gold_flat
    tp = len(S & G); 
    if tp == 0: return 0.0
    P_, R_ = tp / len(S), tp / len(G); return 2 * P_ * R_ / (P_ + R_)
gold_flat = {"svc-a", "db"}   # F1 版本：不做别名合并，每组一个代表
cases = {"只报一个根因": ["svc-a"], "两个根因": ["svc-a", "db"], "两个根因+别名": ["svc-a", "pod-a-1", "db"],
         "两个根因+1个错": ["svc-a", "db", "svc-b"], "撒网 6 个": ["svc-a", "db", "svc-b", "x", "y", "z"]}
for k, p in cases.items():
    print(f"  {k:14s} F1={f1(p, gold_flat):.3f}  P@full-recall={score_itb(p):.3f}")

# ---------------- §7 用户模拟器 ----------------
hr("§7 用户模拟器带来的方差")
ls = {"GPT-4o": (67.8, 1.2), "Sonnet 3.7": (67.0, 3.3), "Sonnet 4.5": (75.9, 3.5), "Kimi-K2-Thinking": (71.3, 1.9)}
means = [v[0] for v in ls.values()]
print("Lost in Simulation 表：同一 agent 换 4 个用户模型，成功率极差 = %.1f 点，模型间标准差 = %.2f" % (max(means) - min(means), statistics.stdev(means)))
print("  而同一用户模型 3 次重跑的标准差只有 1.2–3.5 点 → 换模拟器的影响大于重跑噪声")
for dom_, crit, tot in [("airline", 13, 47), ("retail", 12, 40), ("telecom", 6, 16)]:
    print(f"  τ² {dom_:8s}: 模拟器致命错误 {crit}% → 若这些对话被判失败，分数最多被低估约 {crit} 点（上界，非估计值）")
# pass^k：独立 vs 模拟器引入共同失败
p = 0.7
print("pass^k 独立假设 p=0.7: ", [round(p ** k, 3) for k in (1, 2, 4, 8)])
# 若每个任务以 10% 概率被模拟器"带偏"，此时成功率降为 0.2，否则为 p'
q, p_bad = 0.10, 0.2
p_good = (p - q * p_bad) / (1 - q)  # 保持 pass^1 不变
mix = [round(q * p_bad ** k + (1 - q) * p_good ** k, 3) for k in (1, 2, 4, 8)]
print("pass^k 若模拟器对 10% 任务系统性带偏(pass^1 仍=0.7):", mix, " → pass^k 衰减变慢，k 越大差越多")

# ---------------- §8 效率 ----------------
hr("§8 效率并入分数")
def rhae_game(human, ai, total_levels):
    ws = list(range(1, total_levels + 1)); s = 0
    for lvl, (h, a) in enumerate(zip(human, ai), start=1):
        s += lvl * min((h / a) ** 2, 1.15)
    return s / sum(ws)
human = [10, 12, 20, 25, 30]; ai = [10, 24, 18, 50]   # 只通了 4 关
print("ARC-AGI-3 关分:", [round(min((h / a) ** 2, 1.15), 4) for h, a in zip(human, ai)])
print("游戏分 = Σ 关号×关分 / 15 = %.4f ；上限 10/15 = %.4f" % (rhae_game(human, ai, 5), 10 / 15))
ai_fast = [5, 5, 5, 5]
print("全部关卡比人快很多时 = %.4f > 0.6667 → 1.15 上限和“最多 66.7%%”两句话在数值上冲突，官方需另有截断" % rhae_game(human, ai_fast, 5))
pin, pcache, pout = 3.0, 0.3, 15.0   # $/M token
print("AA 混合价 7:2:1 (缓存命中:输入:输出) = (7×%.1f+2×%.1f+1×%.1f)/10 = $%.2f/M" % (pcache, pin, pout, (7 * pcache + 2 * pin + pout) / 10))
pts = {"A": (0.5, 40), "B": (1.2, 55), "C": (2.0, 52), "D": (4.0, 70), "E": (9.0, 71), "F": (12.0, 69)}
front = [k for k, (c, s) in pts.items() if not any((c2 <= c and s2 >= s) and (c2, s2) != (c, s) for c2, s2 in pts.values())]
print("成本-分数 帕累托前沿:", front, "（C、F 被支配）")
# 把成本“并进”一个数的几种方式会给出不同名次
for k, (c, s) in pts.items():
    print(f"  {k}: 分={s} 成本=${c}  分/美元={s / c:6.1f}  分−10·log10(成本)={s - 10 * math.log10(c):5.1f}")

# ---------------- §9 BPB ----------------
hr("§9 O1：NLL → bits-per-byte")
text = "The quick brown fox jumps over the lazy dog."
nbytes = len(text.encode("utf-8")); ntok = 10; nll_nats_per_tok = 2.3
bpb = ntok * nll_nats_per_tok / (math.log(2) * nbytes)
print(f"{ntok} 个 token、每 token 平均 NLL {nll_nats_per_tok} nats、{nbytes} 字节 → BPB = {ntok}×{nll_nats_per_tok}/(ln2×{nbytes}) = {bpb:.4f}")
print("换一个分词器（20 个 token、每 token 1.15 nats）BPB 不变:", round(20 * 1.15 / (math.log(2) * nbytes), 4), "→ 这就是跨分词器比较用 BPB 的原因")
