"""基础例子：采样合并、对局拟合、跨 bench 合并、误差条。只用 Python 标准库。
运行：python3 scripts/basics.py
"""
import math, random, statistics
from math import comb
from collections import Counter

def sec(t): print(f"\n=== §{t} ===")
def sig(x): return 1/(1+math.exp(-x))
SCALE = 400/math.log(10)

# ---------- 通用：带权逻辑回归（牛顿法），用于 BT、风格控制、METR ----------
def logit_fit(X, y, w=None, iters=100, ridge=1e-9):
    n, p = len(X), len(X[0]); w = w or [1.0]*n
    b = [0.0]*p
    for _ in range(iters):
        g = [0.0]*p; H = [[0.0]*p for _ in range(p)]
        for xi, yi, wi in zip(X, y, w):
            z = sum(a*c for a, c in zip(xi, b)); pr = sig(z)
            for j in range(p):
                g[j] += wi*(yi-pr)*xi[j]
                for k in range(p): H[j][k] += wi*pr*(1-pr)*xi[j]*xi[k]
        for j in range(p): H[j][j] += ridge
        step = solve(H, g)
        b = [bj+s for bj, s in zip(b, step)]
        if max(abs(s) for s in step) < 1e-10: break
    return b

def solve(A, v):
    n = len(v); M = [row[:] + [v[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c]/M[c][c]
                for k in range(c, n+1): M[r][k] -= f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

def bt(battles, models, anchor):
    free = [m for m in models if m != anchor]
    X = [[(1 if a == m else -1 if b == m else 0) for m in free] for a, b, _ in battles]
    y = [s for *_, s in battles]
    beta = dict(zip(free, logit_fit(X, y))); beta[anchor] = 0.0
    return beta

# ---------- 1. 采样合并 ----------
sec("1 pass@k / pass^k / maj@k（n=10, c=3）")
def pass_at(n, c, k): return 1.0 if n-c < k else 1-comb(n-c, k)/comb(n, k)
def pass_hat(n, c, k): return comb(c, k)/comb(n, k)
for k in (1, 2, 3, 5):
    print(f"k={k}: pass@k={pass_at(10,3,k):.4f}  pass^k={pass_hat(10,3,k):.4f}  代入式 1-(1-p)^k={1-0.7**k:.4f}  p^k={0.3**k:.4f}")
qs = [(10, 9), (10, 3), (10, 0)]
print("三题 9/3/0：pass@1=%.4f pass@5=%.4f pass^5=%.4f" % tuple(statistics.mean(f(n, c, k) for n, c in qs) for f, k in ((pass_at, 1), (pass_at, 5), (pass_hat, 5))))
qs2 = [(10, 10), (10, 3), (10, 0)]
print("三题 10/3/0：pass@1=%.4f pass@5=%.4f pass^3=%.4f" % tuple(statistics.mean(f(n, c, k) for n, c in qs2) for f, k in ((pass_at, 1), (pass_at, 5), (pass_hat, 3))))
ans = ['42', '42', '17', '42', '17', '17', '17', '9']
print("8 个答案计票", Counter(ans).most_common(), "→ 真值 42 时 maj@8 =", int(Counter(ans).most_common(1)[0][0] == '42'), " avg@8 =", ans.count('42')/8, " pass@8 = 1")
gold = "1/2"
A = ["1/2","1/3","1/3","1/2","1/3","2","1/2","1/3","1/3","7"]
B = ["1/2","1/3","5","1/2","2/3","2","1/2","3/4","1","7"]
for nm, a in (("错答案扎堆", A), ("错答案分散", B)):
    s = [int(x == gold) for x in a]
    print(f"{nm}: pass@1={sum(s)/10} maj@10={int(Counter(a).most_common(1)[0][0]==gold)} 对判定取众数={Counter(s).most_common(1)[0][0]}")

# ---------- 2. 在线 Elo vs BT ----------
sec("2 在线 Elo 的顺序依赖")
models = ['A', 'B', 'C']
battles = [('A','B',1)]*6+[('A','B',0)]*4+[('B','C',1)]*7+[('B','C',0)]*3+[('A','C',1)]*8+[('A','C',0)]*2
def elo(bs, K=32):
    R = {m: 1000.0 for m in models}
    for a, b, s in bs:
        e = 1/(1+10**((R[b]-R[a])/400)); R[a] += K*(s-e); R[b] -= K*(s-e)
    return R
fmt = lambda R: {k: round(v, 1) for k, v in R.items()}
print("按表顺序:", fmt(elo(battles)))
print("倒序:    ", fmt(elo(battles[::-1])))
rng = random.Random(0); runs = []
for _ in range(1000):
    bs = battles[:]; rng.shuffle(bs); runs.append(elo(bs))
print("1000 次随机顺序 均值:", {m: round(statistics.mean(r[m] for r in runs), 1) for m in models},
      "标准差:", {m: round(statistics.pstdev(r[m] for r in runs), 1) for m in models})
print("分差→胜率:", {d: round(1/(1+10**(-d/400)), 4) for d in (0, 50, 100, 200, 400)})

sec("3 BT 一次性拟合（C=1000 锚点）")
b = bt(battles, models, 'C')
print("β:", {k: round(v, 3) for k, v in b.items()}, " Elo 尺度:", {k: round(v*SCALE+1000) for k, v in b.items()})
print("预测 A胜B %.3f  B胜C %.3f  A胜C %.3f（观测 .6 .7 .8）" % (sig(b['A']-b['B']), sig(b['B']-b['C']), sig(b['A']-b['C'])))
for mult in (1, 10):
    bs = battles*mult; boots = []
    r2 = random.Random(7)
    for _ in range(300):
        s = [bs[r2.randrange(len(bs))] for _ in bs]
        try: e = bt(s, models, 'C'); boots.append(e['A']*SCALE+1000)
        except ZeroDivisionError: pass
    boots.sort(); lo, hi = boots[int(.025*len(boots))], boots[int(.975*len(boots))-1]
    print(f"{30*mult} 场：A 的 95% bootstrap 区间约 [{lo:.0f}, {hi:.0f}]")
b4 = bt(battles+[('D','A',1)]*9+[('D','A',0)]+[('D','B',1)]*5+[('D','B',0)]*5, models+['D'], 'C')
print("加入 D 后:", {k: round(v*SCALE+1000) for k, v in b4.items()})

sec("4 风格控制（模拟数据）")
rng = random.Random(7); rows = []
true = {'L': 0.3, 'S': 0.3, 'R': 0.0}; g = 0.6
for a, c in (('L','S'), ('L','R'), ('S','R')):
    for _ in range(3000):
        z = rng.choice([1,1,1,0,-1]) if a == 'L' else rng.choice([1,0,-1])
        rows.append((a, c, z, int(rng.random() < sig(true[a]-true[c]+g*z))))
X0 = [[(1 if a=='L' else -1 if c=='L' else 0), (1 if a=='S' else -1 if c=='S' else 0)] for a, c, z, _ in rows]
y = [r[3] for r in rows]
raw = logit_fit(X0, y); sc = logit_fit([x+[r[2]] for x, r in zip(X0, rows)], y)
print("不控制 L,S Elo:", round(raw[0]*SCALE+1000), round(raw[1]*SCALE+1000), " 控制后:", round(sc[0]*SCALE+1000), round(sc[1]*SCALE+1000), " γ̂=%.3f" % sc[2])

sec("5 Crowd-BT 与 Leaderboard Illusion")
print("η=0.8、真实胜率 0.7 → 观测", round(0.8*0.7+0.2*0.3, 2))
r3 = random.Random(1); m = statistics.mean(max(r3.gauss(0, 1) for _ in range(10)) for _ in range(200000))
print("10 个同等变体只公开最好的：E[max Z]≈%.2f，SE=10 时虚高约 %.0f 分" % (m, 10*m))

sec("6 IPS（Agent Arena 式）")
data = [('M1', .8, 1)]*6+[('M1', .8, 0)]*2+[('M2', .2, 1)]+[('M2', .2, 0)]
w = [0.5/p for _, p, _ in data]
tot = sum(wi*yi for wi, (_, _, yi) in zip(w, data))/sum(w)
for t in ('M1', 'M2'):
    idx = [i for i, d in enumerate(data) if d[0] == t]
    mu = sum(w[i]*data[i][2] for i in idx)/sum(w[i] for i in idx)
    print(t, "权重", round(w[idx[0]], 3), "加权均值", round(mu, 3), "τ", round(mu-tot, 3))
print("加权总体", round(tot, 3), " 未加权", statistics.mean(d[2] for d in data))

sec("7 对固定基线比")
expand = {'>>': [1,1,1], '>': [1], '=': [0.5], '<': [0], '<<': [0,0,0]}
games = [('>>','>'), ('=','<'), ('>','>')]
s = [v for g2 in games for x in g2 for v in expand[x]]
plain = {'>>':1,'>':1,'=':.5,'<':0,'<<':0}
print("Arena-Hard 展开", s, "胜率", round(sum(s)/len(s), 4), " 不加权", round(statistics.mean(plain[x] for g2 in games for x in g2), 4))
print("AlpacaEval LC：原始胜率 σ(0.6·tanh1) =", round(sig(0.6*math.tanh(1)), 2), "→ 去掉长度项 0.50")
print("WildBench：(100+0−50+0)/4 =", (100+0-50+0)/4)

sec("8 IRT / ECI / tinyBenchmarks")
C_ = [0., 1., 2.5]; D_ = [-1., 1., 3.]; a_ = [2., 1.5, 1.]
print("模型1在bench1 %.3f；模型0未测bench2 预测 %.3f；模型2未测bench0 预测 %.3f" % (sig(a_[1]*(C_[1]-D_[1])), sig(a_[2]*(C_[0]-D_[2])), sig(a_[0]*(C_[2]-D_[0]))))
print("tinyBenchmarks：(70+610)/1000 =", (70+610)/1000)

sec("9 METR 时间跨度")
mins = [1,2,4,8,15,30,60,120,240,480]; succ = [1,1,1,.9,.8,.6,.5,.3,.1,0]
# logit p = β·log2h − β·log2t = c0 + c1·log2t ；分数成功率拆成两条带权样本
X, Y, W = [], [], []
for t, p in zip(mins, succ):
    for yy, ww in ((1, p), (0, 1-p)):
        if ww > 0: X.append([1.0, math.log2(t)]); Y.append(yy); W.append(ww)
c0, c1 = logit_fit(X, Y, W); beta = -c1; l50 = c0/beta
print("h50 = %.1f 分钟, β = %.3f, h80 = %.1f 分钟" % (2**l50, beta, 2**(l50-math.log(4)/beta)))

sec("10 跨 bench：三种合并，三个冠军")
S = {'X': [90,50,52], 'Y': [60,60,60], 'Z': [59,61,61]}
def mwr(S):
    out = {}
    for m in S:
        v = [1 if S[m][b] > S[o][b] else .5 if S[m][b] == S[o][b] else 0 for o in S if o != m for b in range(3)]
        out[m] = round(statistics.mean(v), 3)
    return out
def mrank(S):
    return {m: round(statistics.mean(1+sum(S[o][b] > S[m][b] for o in S) for b in range(3)), 2) for m in S}
print("平均分", {m: round(statistics.mean(v), 2) for m, v in S.items()}, "平均名次", mrank(S), "平均胜率", mwr(S))
S['W'] = [58,62,62]; print("加入 W 后平均胜率", mwr(S))
xs = [.40,.55,.50,.40,.45,.50,.60,.30,.70,.30,.10]; ws = [.15,.10,.05,.10,.10,.10,.05,.10,.05,.10,.10]
print("AA 指数手算：", round(100*sum(x*w for x, w in zip(xs, ws)), 1), " clamp:", {e: min(1, max(0, (e-500)/2000)) for e in (1100, 1600, 2200, 2600)})

sec("11 题内合并")
print("micro / macro / 全过 =", 9/12, (0.9+0)/2, 0)
crit = [(5, 1), (3, 1), (2, 0), (-4, 1), (-2, 0)]
print("HealthBench 例：", sum(p for p, m in crit if m)/sum(p for p, _ in crit if p > 0), " 去掉 −4 后", (5+3)/10)
print("C 的例子 (5+2−4)/(5+3+2) =", (5+2-4)/10)
print("PaperBench 树：", round((3*0.5+1*1+2*(1/3))/6, 3))
print("PRM 乘积：", round(0.95*0.9*0.3*0.95, 3))
print("Alignment Index：", round(100*(0.5*(1-math.sqrt(.04))+0.25*(1-math.sqrt(.01))+0.25*(1-math.sqrt(.09))), 1))
for nm, (c, p, i, a) in {'M1': (60,5,30,5), 'M2': (45,5,5,45)}.items():
    print(f"Omniscience {nm}: 准确率 {c/100} OI {100*(c-i)/100:.0f} 幻觉率 {i/(p+i+a):.3f}")
cor, cga = .4, 40/60
print("SimpleQA F =", round(2*cor*cga/(cor+cga), 2), " 扣分 p=9:", round(.4-9*.2, 2))
print("HLE 校准 RMSCE =", round(math.sqrt(.5*.3**2+.5*0), 3))
print("ARC-AGI-3 三关例：", round((1*1+2*0.25+3*0)/6, 3), "上限", 3/6)

sec("12 预训练：概率类指标")
print("BPB =", round(46/(100*math.log(2)), 3), " token 困惑度", round(math.exp(46/25), 2), round(math.exp(46/40), 2))
print("acc_norm 例：", {k: round(v, 3) for k, v in {'A': -3.0/8, 'B': -6.1/35, 'C': -3.2/6}.items()})
print("涌现：", {p: round(p**10, 3) for p in (0.8, 0.9, 0.95, 0.99)})

sec("13 误差条")
print("n=200, p=0.7: ±%.2f 个点" % (100*1.96*math.sqrt(.21/200)))
print("Llama 3 式 CI，S=0.3：N=30 ±%.1f，N=500 ±%.1f" % (100*1.96*math.sqrt(.21/30), 100*1.96*math.sqrt(.21/500)))
rng = random.Random(1); n = 200
d = [rng.gauss(0, 1) for _ in range(n)]
xa = [int(rng.random() < sig(.85+1.5*q)) for q in d]; xb = [int(rng.random() < sig(.65+1.5*q)) for q in d]
diff = [a-b for a, b in zip(xa, xb)]
print("配对：A %.3f B %.3f，非配对 SE %.4f，配对 SE %.4f" % (statistics.mean(xa), statistics.mean(xb),
      math.sqrt(statistics.variance(xa)/n+statistics.variance(xb)/n), statistics.stdev(diff)/math.sqrt(n)))
pe = [rng.gauss(0, 1.2) for _ in range(50)]
x = [int(rng.random() < sig(.8+pe[i//4])) for i in range(200)]; m = statistics.mean(x)
naive = statistics.stdev(x)/math.sqrt(200)
cl = math.sqrt(sum(sum(x[i]-m for i in range(c*4, c*4+4))**2 for c in range(50)))/200
print("聚类：均值 %.3f 朴素 SE %.4f 聚类 SE %.4f 倍数 %.2f" % (m, naive, cl, cl/naive))

sec("14 其他")
print("Glicko 例（r=1500, RD=200）:")
q = math.log(10)/400
def gf(rd): return 1/math.sqrt(1+3*q*q*rd*rd/math.pi**2)
opp = [(1400, 30, 1), (1550, 100, 0), (1700, 300, 0)]
E = [1/(1+10**(-gf(rd)*(1500-r)/400)) for r, rd, _ in opp]
d2 = 1/(q*q*sum(gf(rd)**2*e*(1-e) for (r, rd, _), e in zip(opp, E)))
r_new = 1500 + q/(1/200**2+1/d2)*sum(gf(rd)*(s-e) for (r, rd, s), e in zip(opp, E))
print("  r' = %.0f, RD' = %.1f" % (r_new, math.sqrt(1/(1/200**2+1/d2))))
print("TrueSkill 新人保守分 μ−3σ =", round(25-3*25/3, 6))
print("BB/100 =", 930/2/1000*100)
