"""生成 images/ 下的全部插图。需要 matplotlib 和一款中文字体（如 Noto Sans CJK SC）。

用法：python3 scripts/make_figures.py
"""
import csv
import math
import os
import random
from collections import Counter
from itertools import combinations
from math import comb

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")
os.makedirs(IMG, exist_ok=True)

for name in ("Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", "SimHei", "WenQuanYi Zen Hei"):
    if any(f.name == name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 160

BLUE, ORANGE, GREEN, GREY, RED, PURPLE = "#3b6ea8", "#e08a2c", "#4a9a5b", "#8a8a8a", "#c0504d", "#7a5aa6"
LIGHT = {BLUE: "#dce7f3", ORANGE: "#fbe6cf", GREEN: "#dcefe0", GREY: "#eeeeee", PURPLE: "#e8e0f2"}


def box(ax, x, y, w, h, text, color=BLUE, fs=11, weight="normal", fill=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.015",
                                fc=fill or LIGHT.get(color, "#f5f5f5"), ec=color, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, linespacing=1.4)


def arrow(ax, x0, y0, x1, y1, color=GREY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4))


def save(fig, name):
    fig.savefig(os.path.join(IMG, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("images/" + name)


# ---------- 1. 总图：四大类和小类 ----------
def load_rows():
    with open(os.path.join(ROOT, "data", "benchmarks.csv"), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def overview():
    rows = load_rows()
    total = len(rows)
    top = Counter(r["属于哪一类"].split("；")[0] for r in rows)
    sub = Counter(r["小类"] for r in rows)
    cols = [
        ("单独给一个模型打分", BLUE, ["1.1 程序对答案", "1.2 跑起来再判", "1.3 模型判答案对不对", "1.4 按细则逐条判",
                               "1.5 概率式评分", "1.6 换算成人类的量", "1.7 没有满分的开放量", "1.8 被评的是判官"]),
        ("对照参考产出与相对比较", ORANGE, ["对照固定参考产出", "人来投票", "模型当裁判", "对局规则判胜负", "各自打分后按名次比"]),
        ("真实使用数据", PURPLE, []),
        ("跨 bench 合成指数", GREEN, []),
    ]
    fig, ax = plt.subplots(figsize=(13, 10.2))
    ax.set_xlim(0, 1); ax.set_ylim(-0.06, 1); ax.axis("off")
    ax.text(0.5, 0.975, f"附录收录的 {total} 个 bench，按分数的来路分四类", ha="center", va="center", fontsize=16, weight="bold")
    x = 0.04
    for name, color, _ in cols:
        w = 0.92 * top[name] / total
        ax.add_patch(plt.Rectangle((x, 0.895), w, 0.04, fc=color, ec="white"))
        if w > 0.08:
            ax.text(x + w / 2, 0.915, f"{name} {top[name] / total:.0%}", ha="center", va="center", color="white", fontsize=11, weight="bold")
        x += w
    ax.text(0.96, 0.873, "条带宽度＝各大类所占比例", ha="right", va="center", fontsize=10, color=GREY)
    pos = [(0.04, 0.76), (0.37, 0.76), (0.70, 0.76), (0.70, 0.60)]
    for (name, color, subs), (x0, y0) in zip(cols, pos):
        w = 0.28
        box(ax, x0, y0, w, 0.08, f"{name}\n{top[name]} 个 · {top[name] / total:.1%}", color, fs=13, weight="bold", fill=LIGHT[color])
        if not subs:
            continue
        h, gap = 0.06, 0.026
        y = y0 - 0.045
        extra = 0.06 if len(subs) > 5 and subs[5].startswith("1.6") else 0
        ax.plot([x0 + 0.01, x0 + 0.01], [y0, y - (len(subs) - 1) * (h + gap) - h / 2 - extra], color=color, lw=1.4)
        for i, s in enumerate(subs):
            if extra and i == 5:
                ax.plot([x0 + 0.03, x0 + w], [y - 0.008, y - 0.008], color=GREY, lw=1, ls="--")
                ax.text(x0 + 0.03 + (w - 0.03) / 2, y - 0.032, "几种特殊情况，判法仍是上面五种之一", ha="center", va="center", fontsize=9.5, color=GREY)
                y -= extra
            n = sub[s]
            ax.plot([x0 + 0.01, x0 + 0.03], [y - h / 2, y - h / 2], color=color, lw=1.4)
            box(ax, x0 + 0.03, y - h, w - 0.03, h, f"{s}\n{n} 个 · {n / total:.1%}", color, fs=10.5, fill="white")
            y -= h + gap
    save(fig, "overview.png")


def years():
    rows = load_rows()
    c = Counter(int(r["发布时间"][:4]) for r in rows if r["发布时间"][:4].isdigit())
    ys = list(range(min(c), max(c) + 1))
    fig, ax = plt.subplots(figsize=(8, 3.6))
    bars = ax.bar(ys, [c[y] for y in ys], color=BLUE, width=0.6)
    for b, y in zip(bars, ys):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, str(c[y]), ha="center", fontsize=11)
    ax.set_xticks(ys)
    ax.set_xticklabels([f"{y}\n（截至 10 月）" if y == 2026 else str(y) for y in ys])
    ax.set_ylabel("bench 数")
    ax.set_title("附录 bench 的发布年份", fontsize=13)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_ylim(0, max(c.values()) * 1.15)
    save(fig, "years.png")


# ---------- 2. 一道题到一个分数 ----------
def pipeline():
    steps = [
        ("模型输出", "一段回答、一份补丁\n或一串操作", GREY, "跑法：6.1 节"),
        ("判一道题", "程序对答案、跑测试\n模型判官、两两比较", BLUE, "第 1、3 章"),
        ("合并多条判定", "多条细则、多个判官\n门控和阈值", BLUE, "2.1、2.2 节"),
        ("合并多次采样", "平均、至少对一次\n每次都对", PURPLE, "2.3 节"),
        ("整套题合成总分", "平均、拟合对局\n换算成人类的量", GREEN, "2.4 节、第 3 章"),
        ("跨 bench 合成", "加权指数\n联合拟合", GREEN, "第 5 章"),
    ]
    fig, ax = plt.subplots(figsize=(14, 4.6))
    ax.set_xlim(0, 1); ax.set_ylim(-0.05, 1); ax.axis("off")
    w, gap = 0.14, 0.024
    by = 0.38
    for i, (t, d, c, ch) in enumerate(steps):
        x = 0.01 + i * (w + gap)
        box(ax, x, by, w, 0.2, t, c, fs=13, weight="bold")
        ax.text(x + w / 2, by - 0.12, d, ha="center", va="center", fontsize=10.5, color="#444444", linespacing=1.5)
        ax.text(x + w / 2, by - 0.25, ch, ha="center", va="center", fontsize=10, color=c if c != GREY else "#666666")
        if i < len(steps) - 1:
            arrow(ax, x + w + 0.002, by + 0.1, x + w + gap - 0.002, by + 0.1)
    # 另一条路：先对答案投票或挑一个，再判
    x0 = 0.01; x1 = 0.01 + (w + gap)
    bx, bw = x0 + w * 0.3, x1 + w * 0.7 - (x0 + w * 0.3)
    box(ax, bx, 0.74, bw, 0.16, "多次采样先对答案投票或挑一个\n（maj@k、选择器）", PURPLE, fs=10.5)
    arrow(ax, x0 + w * 0.5, by + 0.2, bx + 0.01, 0.74)
    arrow(ax, bx + bw - 0.01, 0.74, x1 + w * 0.5, by + 0.2)
    ax.text(bx + bw + 0.025, 0.82, "另一条路：先合答案，再判", ha="left", va="center", fontsize=10.5, color=PURPLE)
    ax.text(0.5, -0.02, "每一步都有几种做法，选哪一种都会改变最后的数字", ha="center", fontsize=11, color=GREY)
    save(fig, "pipeline.png")


# ---------- 3. 单独打分类八个小类的判分示意 ----------
def class1():
    sub = Counter(r["小类"] for r in load_rows())
    spec = [
        ("1.1 程序对答案", ["模型回答", "抽出最终答案", "和标准答案比", "对 1 / 错 0"]),
        ("1.2 跑起来再判", ["补丁或操作", "沙箱里运行", "测试、终态检查", "全过才算对"]),
        ("1.3 模型判答案对不对", ["模型回答", "判官读回答\n和标准答案", "是否一回事", "对 1 / 错 0"]),
        ("1.4 按细则逐条判", ["模型交付物", "判官逐条打勾", "每条过或不过\n可带正负分值", "细则分"]),
        ("1.5 概率式评分", ["标准文本或选项", "不生成，读概率", "比较选项概率\n或算每字节比特", "准确率、BPB"]),
        ("1.6 换算成人类的量", ["任务成败", "对照人类耗时\n或人类成绩", "拟合或换算", "人类小时数\n或 rating"]),
        ("1.7 没有满分的开放量", ["经营或优化任务", "一直运行到结束", "记录最终结果", "余额、偏好分"]),
        ("1.8 被评的是判官", ["判官的判定", "和人工标注\n或已知对错比", "判得对不对", "准确率、F1"]),
    ]
    fig, ax = plt.subplots(figsize=(13, 10.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    hh, step = 0.095, 0.124
    for i, (name, steps) in enumerate(spec):
        y = 0.89 - i * step
        ax.text(0.0, y + hh / 2, f"{name} · {sub[name]} 个", ha="left", va="center", fontsize=12.5, weight="bold", color=BLUE)
        x0, w, gap = 0.30, 0.155, 0.022
        for j, s in enumerate(steps):
            x = x0 + j * (w + gap)
            box(ax, x, y, w, hh, s, BLUE if j < 3 else GREEN, fs=10.5, fill="white" if j < 3 else LIGHT[GREEN])
            if j < 3:
                arrow(ax, x + w + 0.002, y + hh / 2, x + w + gap - 0.002, y + hh / 2)
    ax.plot([0, 1], [0.89 - 5 * step + hh + 0.0145] * 2, color=GREY, lw=0.8, ls="--")
    save(fig, "class1-subclasses.png")


# ---------- 4. pass@k、pass^k、maj@k 随 k 变化 ----------
def maj_expect(answers, gold, k):
    tot = 0.0
    subs = list(combinations(range(len(answers)), k))
    for idx in subs:
        c = Counter(answers[i] for i in idx)
        top = max(c.values())
        winners = [a for a, v in c.items() if v == top]
        tot += (gold in winners) / len(winners)
    return tot / len(subs)


def sampling():
    n, c = 10, 3
    ks = list(range(1, 11))
    p1 = [c / n] * len(ks)
    pk = [1 - comb(n - c, k) / comb(n, k) if n - c >= k else 1.0 for k in ks]
    ph = [comb(c, k) / comb(n, k) for k in ks]
    gold = "1/2"
    clustered = ["1/2", "1/3", "1/3", "1/2", "1/3", "2", "1/2", "1/3", "1/3", "7"]
    spread = ["1/2", "1/3", "5", "1/2", "2/3", "2", "1/2", "3/4", "1", "7"]
    mc = [maj_expect(clustered, gold, k) for k in ks]
    ms = [maj_expect(spread, gold, k) for k in ks]
    fig, ax = plt.subplots(figsize=(9, 5.6))
    ax.plot(ks, pk, "-o", color=BLUE, label="至少对一次（pass@k）")
    ax.plot(ks, p1, "--", color=GREY, label="平均（pass@1）＝0.3")
    ax.plot(ks, ms, "-s", color=GREEN, label="投票，错答案分散（maj@k）")
    ax.plot(ks, mc, "-s", color=ORANGE, label="投票，错答案扎堆（maj@k）")
    ax.plot(ks, ph, "-o", color=RED, label="每次都对（pass^k）")
    ax.set_xlabel("k：给几次机会，或取几个答案"); ax.set_ylabel("这道题的得分")
    ax.set_xticks(ks); ax.set_ylim(-0.03, 1.05)
    ax.set_title("同一道题，采样 10 次对 3 次", fontsize=13)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=10, frameon=False)
    save(fig, "sampling-curves.png")


# ---------- 5. 在线 Elo 的顺序依赖和 BT ----------
def sig(x):
    return 1 / (1 + math.exp(-x))


def bt_fit(battles, models, iters=2000):
    """简单的梯度上升 BT，均值归零。"""
    b = {m: 0.0 for m in models}
    for _ in range(iters):
        g = {m: 0.0 for m in models}
        for a, o, s in battles:
            p = sig(b[a] - b[o]); g[a] += s - p; g[o] -= s - p
        for m in models:
            b[m] += 0.05 * g[m]
        mu = sum(b.values()) / len(b)
        b = {m: v - mu for m, v in b.items()}
    return b


SCALE = 400 / math.log(10)


def elo_order():
    models = ["A", "B", "C"]
    battles = [("A", "B", 1)] * 6 + [("A", "B", 0)] * 4 + [("B", "C", 1)] * 7 + [("B", "C", 0)] * 3 + [("A", "C", 1)] * 8 + [("A", "C", 0)] * 2

    def traj(bs, K=32):
        R = {m: 1000.0 for m in models}; out = [R["A"]]
        for a, o, s in bs:
            e = 1 / (1 + 10 ** ((R[o] - R[a]) / 400)); R[a] += K * (s - e); R[o] -= K * (s - e); out.append(R["A"])
        return out

    fig, ax = plt.subplots(figsize=(9, 5.4))
    rng = random.Random(0)
    for i in range(30):
        bs = battles[:]; rng.shuffle(bs)
        ax.plot(traj(bs), color=GREY, alpha=0.18, lw=1, label="随机打乱顺序" if i == 0 else None)
    t1, t2 = traj(battles), traj(battles[::-1])
    ax.plot(t1, color=BLUE, lw=2.2, label=f"按表里顺序：最后 {t1[-1]:.0f}")
    ax.plot(t2, color=ORANGE, lw=2.2, label=f"倒过来：最后 {t2[-1]:.0f}")
    b = bt_fit(battles, models)
    a_bt = 1000 + b["A"] * SCALE
    ax.axhline(a_bt, color=GREEN, ls="--", lw=2, label=f"一次性拟合（BT）：{a_bt:.0f}，与顺序无关")
    ax.set_xlabel("已经打完的场数"); ax.set_ylabel("A 的分数（三人平均为 1000）")
    ax.set_title("同样 30 场对局，换个顺序，在线 Elo 给 A 的分就不同", fontsize=13)
    ax.grid(alpha=0.25); ax.legend(fontsize=10, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    save(fig, "elo-order.png")


# ---------- 6. 新模型加入后老模型名次翻转 ----------
def new_model():
    before = {"A": 1231, "B": 1155, "C": 1000}
    after = {"A": 1181, "B": 1201, "C": 1000, "D": 1338}
    colors = {"A": BLUE, "B": ORANGE, "C": GREY, "D": GREEN}
    fig, ax = plt.subplots(figsize=(7.5, 5.6))
    for m in "ABC":
        ax.plot([0, 1], [before[m], after[m]], "-o", color=colors[m], lw=2.4, ms=8)
        ax.text(-0.06, before[m], f"{m}  {before[m]}", ha="right", va="center", fontsize=12, color=colors[m])
        ax.text(1.06, after[m], f"{after[m]}  {m}", ha="left", va="center", fontsize=12, color=colors[m])
    ax.plot([1], [after["D"]], "o", color=colors["D"], ms=9)
    ax.text(1.06, after["D"], f"{after['D']}  D（新加入）", ha="left", va="center", fontsize=12, color=colors["D"])
    ax.set_xlim(-0.45, 1.6); ax.set_ylim(960, 1380)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["加入 D 之前", "加入 D 之后"], fontsize=12)
    ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ("left", "right", "top")]
    ax.set_title("A 和 B 之间没有新比赛，名次却翻了过来", fontsize=13)
    save(fig, "new-model-flip.png")


# ---------- 7. 三种跨 bench 合并，三个冠军 ----------
def three_champions():
    def stats(data):
        ms = list(data)
        nb = len(next(iter(data.values())))
        avg = {m: sum(v) / nb for m, v in data.items()}
        rank = {m: sum(1 + sum(data[o][b] > data[m][b] for o in ms if o != m) for b in range(nb)) / nb for m in ms}
        win = {m: sum((data[m][b] > data[o][b]) + 0.5 * (data[m][b] == data[o][b]) for b in range(nb) for o in ms if o != m)
               / (nb * (len(ms) - 1)) for m in ms}
        return avg, rank, win

    data = {"X": (90, 50, 52), "Y": (60, 60, 60), "Z": (59, 61, 61)}
    avg, rank, win = stats(data)
    _, _, win_w = stats({**data, "W": (58, 62, 62)})
    colors = {"X": BLUE, "Y": GREY, "Z": ORANGE, "W": PURPLE}
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.6))
    panels = [("平均分", "越高越好", avg, max, "{:.1f}"), ("平均名次", "越小越好", rank, min, "{:.2f}"),
              ("平均胜率", "越高越好", win, max, "{:.3f}"), ("加入 W (58, 62, 62) 后\n的平均胜率", "越高越好", win_w, max, "{:.3f}")]
    for ax, (title, note, vals, best, f) in zip(axes, panels):
        ms = list(vals)
        champ = best(vals, key=vals.get)
        bars = ax.bar(ms, [vals[m] for m in ms], color=[colors[m] for m in ms],
                      alpha=1, edgecolor=["black" if m == champ else "none" for m in ms], linewidth=1.6)
        for bar, m in zip(bars, ms):
            if m != champ:
                bar.set_alpha(0.35)
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), ("★ " if m == champ else "") + f.format(vals[m]),
                    ha="center", va="bottom", fontsize=11, weight="bold" if m == champ else "normal")
        ax.set_title(f"{title}（{note}）\n冠军：{champ}", fontsize=12)
        ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ("left", "right", "top")]
        ax.set_ylim(0, max(vals.values()) * 1.2)
    axes[3].axvspan(-0.5, 3.5, color=PURPLE, alpha=0.04, zorder=-1)
    fig.suptitle("同一份三个 bench 的成绩：X (90, 50, 52)  Y (60, 60, 60)  Z (59, 61, 61)", fontsize=12, y=1.13)
    fig.text(0.5, -0.03, "平均名次的柱子越短越好；★ 标的是各自口径下的冠军", ha="center", fontsize=10, color=GREY)
    save(fig, "three-champions.png")


# ---------- 8. 判官合并：同一份投票，不同规则 ----------
def judge_merge():
    votes = [[1, 1, 1, 0, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1]]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1, 1.25]})
    for i, row in enumerate(votes):
        for j, v in enumerate(row):
            ax.add_patch(plt.Rectangle((j, 2 - i), 0.92, 0.92, fc=GREEN if v else RED, alpha=0.8))
            ax.text(j + 0.46, 2 - i + 0.46, "过" if v else "不过", ha="center", va="center", color="white", fontsize=12, weight="bold")
    ax.set_xlim(-0.1, 5); ax.set_ylim(-0.1, 3)
    ax.set_xticks([j + 0.46 for j in range(5)]); ax.set_xticklabels([f"细则 {j + 1}" for j in range(5)], fontsize=11)
    ax.set_yticks([2 - i + 0.46 for i in range(3)]); ax.set_yticklabels([f"判官 {i + 1}" for i in range(3)], fontsize=11)
    [ax.spines[s].set_visible(False) for s in ax.spines]; ax.tick_params(length=0)
    ax.set_title("三个判官对同一份答卷的判定", fontsize=12)
    rules = [
        ("逐条多数票，再看是否全过", "1"),
        ("逐条要求一致，再看是否全过", "0"),
        ("每个判官先看全过，再取占比", "1/3"),
        ("每题抽一个判官", "0 或 1，平均 1/3"),
        ("逐条取平均，再摊平算通过率", "0.867"),
    ]
    ax2.axis("off"); ax2.set_xlim(-0.03, 1); ax2.set_ylim(-0.02, 1.02)
    ax2.set_title("这道题的分", fontsize=12)
    for k, (r, v) in enumerate(rules):
        y = 0.86 - k * 0.19
        box(ax2, 0.0, y - 0.07, 0.58, 0.14, r, PURPLE, fs=11, fill="white")
        ax2.text(0.62, y, v, ha="left", va="center", fontsize=15, weight="bold", color=PURPLE)
    save(fig, "judge-merge.png")


# ---------- 9. METR：成功率对人类耗时的逻辑回归 ----------
def metr_fit():
    mins = [1, 2, 4, 8, 15, 30, 60, 120, 240, 480]
    succ = [1, 1, 1, .9, .8, .6, .5, .3, .1, 0]
    # 带权逻辑回归 logit p = c0 + c1·log2 t，和 scripts/basics.py §9 一致
    c0 = c1 = 0.0
    for _ in range(100):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for t, p in zip(mins, succ):
            x = math.log2(t); q = sig(c0 + c1 * x)
            g0 += p - q; g1 += (p - q) * x
            v = q * (1 - q); h00 += v; h01 += v * x; h11 += v * x * x
        det = h00 * h11 - h01 * h01
        c0 += (h11 * g0 - h01 * g1) / det; c1 += (h00 * g1 - h01 * g0) / det
    beta = -c1; l50 = c0 / beta; l80 = l50 - math.log(4) / beta
    fig, ax = plt.subplots(figsize=(9, 5))
    xs = [i / 20 for i in range(-10, 200)]
    ax.plot([2 ** x for x in xs], [sig(c0 + c1 * x) for x in xs], color=BLUE, lw=2.2, label="拟合的逻辑曲线")
    ax.plot(mins, succ, "o", color=ORANGE, ms=8, label="各任务组的实际成功率")
    for lv, pr, col, name in ((l50, 0.5, GREEN, "h50"), (l80, 0.8, RED, "h80")):
        h = 2 ** lv
        ax.plot([h, h], [0, pr], ls="--", color=col, lw=1.4); ax.plot([0.5, h], [pr, pr], ls="--", color=col, lw=1.4)
        left = name == "h80"
        ax.text(h / 1.08 if left else h * 1.08, 0.03, f"{name} ≈ {h:.1f} 分钟", color=col, fontsize=11, weight="bold",
                ha="right" if left else "left")
    ax.set_xscale("log", base=2)
    ax.set_xticks(mins); ax.set_xticklabels(["1 分", "2 分", "4 分", "8 分", "15 分", "30 分", "1 时", "2 时", "4 时", "8 时"])
    ax.set_xlim(0.7, 700); ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel("人类专家完成任务的耗时（对数刻度）"); ax.set_ylabel("模型成功率")
    ax.set_title("50% 跨度约 50 分钟，80% 跨度只有约 18 分钟", fontsize=13)
    ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=10, loc="upper right")
    save(fig, "metr-fit.png")


# ---------- 10. 误差条宽度随题量变化 ----------
def ci_width():
    ns = list(range(10, 1001, 5))
    fig, ax = plt.subplots(figsize=(9, 5))
    for p, col in ((0.5, BLUE), (0.7, ORANGE), (0.9, GREEN)):
        ax.plot(ns, [100 * 1.96 * math.sqrt(p * (1 - p) / n) for n in ns], color=col, lw=2.2, label=f"准确率 {p:.1f}")
    for n, lab in ((30, "AIME 一年 30 题"), (200, "200 题"), (500, "500 题")):
        hw = 100 * 1.96 * math.sqrt(0.21 / n)
        ax.plot([n], [hw], "o", color=ORANGE, ms=7)
        ax.annotate(f"{lab}：±{hw:.1f}", (n, hw), xytext=(12, 10), textcoords="offset points", fontsize=10.5, color="#444444")
    ax.set_xscale("log")
    ax.set_xticks([10, 30, 100, 200, 500, 1000]); ax.set_xticklabels(["10", "30", "100", "200", "500", "1000"])
    ax.set_xlabel("题量 n（对数刻度）"); ax.set_ylabel("95% 区间的半宽（百分点）")
    ax.set_title("题量翻 4 倍，误差条才缩一半", fontsize=13)
    ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=10)
    save(fig, "ci-width.png")


# ---------- 11. 逐 token 平稳变好，整题像是突然学会 ----------
def emergence():
    ps = [0.5 + i / 400 for i in range(201)]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(ps, ps, color=GREY, ls="--", lw=1.6, label="每个 token 写对的概率 p")
    ax.plot(ps, [p ** 10 for p in ps], color=BLUE, lw=2.4, label="10 个 token 全对的概率 p¹⁰")
    for p in (0.8, 0.9, 0.95, 0.99):
        ax.plot([p], [p ** 10], "o", color=ORANGE, ms=7)
        ax.annotate(f"{p ** 10:.3f}", (p, p ** 10), xytext=(-38, 6), textcoords="offset points", fontsize=10.5)
    ax.set_xlabel("每个 token 写对的概率 p"); ax.set_ylabel("正确率")
    ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 1.02)
    ax.set_title("p 平稳上升，精确匹配却像突然学会", fontsize=13)
    ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=10, loc="upper left")
    save(fig, "emergence.png")


# ---------- 12. AA 智能指数的组件权重 ----------
def aa_weights():
    groups = [
        ("Agents 30%", GREEN, [("AA-Briefcase", 15), ("GDPval-AA", 10), ("AutomationBench-AA", 5)]),
        ("编程 20%", BLUE, [("Terminal-Bench 4.0", 10), ("SciCode", 10)]),
        ("通用 30%", ORANGE, [("AA-Omniscience 准确率", 10), ("AA-Omniscience 1 − 幻觉率", 5), ("GDP.pdf", 10), ("AA-LCR", 5)]),
        ("科学推理 20%", PURPLE, [("HLE", 10), ("CritPt", 10)]),
    ]
    rows = [(g, col, n, w) for g, col, comps in groups for n, w in comps]
    fig, ax = plt.subplots(figsize=(10, 6))
    ys = list(range(len(rows)))[::-1]
    ax.barh(ys, [w for *_, w in rows], color=[col for _, col, _, _ in rows], height=0.65)
    for y, (g, col, n, w) in zip(ys, rows):
        ax.text(w + 0.3, y, f"{w}%", va="center", fontsize=11)
    ax.set_yticks(ys); ax.set_yticklabels([n for _, _, n, _ in rows], fontsize=11)
    i = 0
    for g, col, comps in groups:
        top, bot = ys[i], ys[i + len(comps) - 1]
        ax.text(18.5, (top + bot) / 2, g, va="center", ha="left", fontsize=12, weight="bold", color=col)
        ax.plot([18, 18], [bot - 0.35, top + 0.35], color=col, lw=3)
        i += len(comps)
    ax.set_xlim(0, 24); ax.set_xticks([])
    [ax.spines[k].set_visible(False) for k in ("top", "right", "bottom")]
    ax.set_title("AA 智能指数：11 项加权，权重偏向 agent 任务", fontsize=13)
    fig.text(0.5, 0.0, "Briefcase 和 GDPval-AA 是 Elo，先用 clamp((Elo − 500)/2000) 压到 0 到 1", ha="center", fontsize=10, color=GREY)
    save(fig, "aa-weights.png")


if __name__ == "__main__":
    overview(); years(); pipeline(); class1(); sampling(); elo_order(); new_model(); three_champions(); judge_merge()
    metr_fit(); ci_width(); emergence(); aa_weights()
