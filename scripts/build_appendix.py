"""从 data/benchmarks.csv 生成 book/appendix.md。只用标准库。

用法：python3 scripts/build_appendix.py
"""
import csv
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "benchmarks.csv")
OUT_PATH = os.path.join(ROOT, "book", "appendix.md")

ORDER = [
    "推理/知识/事实性", "数学", "科学", "代码/软件工程", "代理/工具调用", "电脑/GUI 操作",
    "代理/经营/博弈", "深度研究/检索", "长上下文", "指令遵循/多轮对话", "多语言/中文",
    "多模态理解", "视频理解", "语音/音频", "图像/视频/语音生成",
    "专业领域（金融/法律/医疗/教育）", "情感/心理健康/写作", "安全与诚实", "网络安全",
    "基座评测", "偏好竞技场/真实使用", "聚合指数", "判官/奖励模型评测",
]
SKIP = {"", "—", "无", "单信号", "单信号 1/0", "单次"}


def cell(s):
    return s.replace("|", "\\|").replace("$", "\\$").replace("\n", " ").strip()


def how_judged(r):
    who, ref = r["谁来判"].strip(), r["跟什么比"].strip()
    if ref in SKIP or ref == "继承":
        return who
    return f"{who}；对照{ref}"


def how_merged(r):
    parts = [r[k].strip() for k in ("一道题内怎么合", "多次采样怎么合", "整套题怎么合成总分")]
    parts = [p for p in parts if p not in SKIP]
    return "；".join(parts) if parts else "—"


CLASSES = [
    ("单独给一个模型打分", "chapter1.md", ["1.1 程序对答案", "1.2 跑起来再判", "1.3 模型判答案对不对", "1.4 按细则逐条判",
                                     "1.5 概率式评分", "1.6 换算成人类的量", "1.7 没有满分的开放量", "1.8 被评的是判官"]),
    ("对照参考产出与相对比较", "chapter3.md", ["对照固定参考产出", "人来投票", "模型当裁判", "对局规则判胜负", "各自打分后按名次比"]),
    ("真实使用数据", "chapter4.md", ["真实使用数据"]),
    ("跨 bench 合成指数", "chapter5.md", ["跨 bench 合成指数"]),
]
SOURCES = (
    "这些 bench 有两个来路。一是 2026 年各家的模型卡和发布页：OpenAI 的 GPT-6 Astra 和 GPT-6.1 Sol，"
    "Anthropic 的 Claude Opus 5 和 Opus 5.5，Google DeepMind 的 Gemini 4 Argon 和 Gemini 3.8 Flash，xAI 的 Grok 4.7，"
    "Meta 的 Muse Spark 1.3，以及 DeepSeek-V4、Qwen3.8、Kimi K3、GLM-5.3、Seed 2.1、MiniMax-M3、Step 3.7 Flash 和混元 Hy3。"
    "二是第三方榜单：Artificial Analysis、Vals、Scale SEAL、LMArena、Epoch、MathArena、LiveBench 等。"
    "两边合并、去重，再按领域补齐缺口。每个 bench 的计分方法都对照过它的原始论文、方法页或代码。"
)


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    total = len(rows)
    by_sub = {}
    for r in rows:
        by_sub.setdefault(r["小类"], []).append(r)
    known = {s for _, _, subs in CLASSES for s in subs}
    unknown = set(by_sub) - known
    if unknown:
        raise SystemExit(f"未知小类：{unknown}")
    dom_rank = {d: i for i, d in enumerate(ORDER)}
    years = Counter(r["发布时间"][:4] for r in rows if r["发布时间"][:4].isdigit())
    top3 = "，".join(f"{y} 年的 {years[y]} 个" for y in sorted(years, reverse=True)[:3])

    def anchor(i, j):
        return f"c{i + 1}-{j + 1}"

    lines = [
        "# 附录 书中涉及的 bench",
        "",
        SOURCES + f"按发布年份，{top3}：",
        "",
        "![附录 bench 的发布年份分布](../images/years.png)",
        "",
        f"下面按正文的四类和小类分组列出这 {total} 个 bench，同一小类里按领域排列。"
        "“怎么判”写谁来判、拿什么作对照，程序和模型一起判的按最终对错由谁定归类，并在这一栏末尾注明；"
        "“怎么合成总分”依次写一道题内、多次采样和整套题三步，没有特别处理的步骤略去。"
        "少数 bench 同时属于两类，按主要的一类归入，名称后面注明另一类。"
        "更完整的字段在 [data/benchmarks.csv](../data/benchmarks.csv)。",
        "",
        "| 大类 | 小类 | 数量 | 占比 |",
        "|---|---|---|---|",
    ]
    for i, (cls, _, subs) in enumerate(CLASSES):
        n_cls = sum(len(by_sub.get(s, [])) for s in subs)
        for j, s in enumerate(subs):
            n = len(by_sub.get(s, []))
            label = f"{cls}（{n_cls} 个）" if j == 0 else ""
            sub = "—" if len(subs) == 1 else f"[{s}](#{anchor(i, j)})"
            lines.append(f"| {label} | {sub} | {n} | {n / total:.1%} |")
    lines.append("")
    for i, (cls, chap, subs) in enumerate(CLASSES):
        n_cls = sum(len(by_sub.get(s, [])) for s in subs)
        lines += [f'<a id="c{i + 1}"></a>', "", f"## {cls}（{n_cls} 个）", "",
                  f"正文见[第 {chap[7:-3]} 章]({chap})。", ""]
        for j, s in enumerate(subs):
            rs = sorted(by_sub.get(s, []), key=lambda r: (dom_rank.get(r["领域大类"], 99), r["名称"]))
            if len(subs) > 1:
                lines += [f'<a id="{anchor(i, j)}"></a>', "", f"### {s}（{len(rs)} 个）", ""]
            lines += ["| 名称 | 领域 | 怎么判 | 怎么合成总分 |", "|---|---|---|---|"]
            for r in rs:
                name_cell = cell(r["名称"])
                if r["来源"].strip():
                    name_cell = f"[{name_cell}]({r['来源'].strip()})"
                parts = r["属于哪一类"].split("；")
                if len(parts) > 1:
                    name_cell += f"（也属于{parts[1]}）"
                lines.append(f"| {name_cell} | {cell(r['领域'])} | {cell(how_judged(r))} | {cell(how_merged(r))} |")
            lines.append("")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{total} 个 bench → {OUT_PATH}")


if __name__ == "__main__":
    main()
