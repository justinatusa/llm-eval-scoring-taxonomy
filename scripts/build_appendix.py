"""从 data/benchmarks.csv 生成 book/appendix.md。只用标准库。

用法：python3 scripts/build_appendix.py
"""
import csv
import os
from collections import OrderedDict

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
    ("1 单题直接出分", ["1.1 程序对答案", "1.2 跑起来再判", "1.3 模型判答案对不对", "1.4 按细则逐条判", "1.5 基座模型：读概率和少样本"]),
    ("2 多模型相互比较", ["人来投票", "模型当裁判", "对局规则判胜负", "各自打分后按名次比"]),
    ("3 其他出分方式", ["3.1 对照固定参考产出", "3.2 换算成人类的量", "3.3 没有满分的开放量", "3.4 真实使用数据", "3.5 跨 bench 合成指数", "3.6 评测判官本身"]),
]
CHAPTER = {"1": "chapter1.md", "2": "chapter2.md", "3": "chapter3.md"}


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    total = len(rows)
    by_sub = {}
    for r in rows:
        by_sub.setdefault(r["小类"], []).append(r)
    known = {s for _, subs in CLASSES for s in subs}
    unknown = set(by_sub) - known
    if unknown:
        raise SystemExit(f"未知小类：{unknown}")
    dom_rank = {d: i for i, d in enumerate(ORDER)}

    def anchor(i, j):
        return f"c{i + 1}-{j + 1}"

    lines = [
        "# 附录 书中涉及的 bench",
        "",
        f"这里列出 {total} 个 bench，按正文的三大类和小类分组，同一小类里按领域排列。"
        "“怎么判”写谁来判、拿什么作对照；“怎么合成总分”依次写一道题内、多次采样和整套题三步，"
        "没有特别处理的步骤略去。少数 bench 同时用了两种出分方式，按主要的一种归类，名称后面注明另一种。"
        "更完整的字段在 [data/benchmarks.csv](../data/benchmarks.csv)。",
        "",
        "| 大类 | 小类 | 数量 | 占比 |",
        "|---|---|---|---|",
    ]
    for i, (cls, subs) in enumerate(CLASSES):
        n_cls = sum(len(by_sub.get(s, [])) for s in subs)
        for j, s in enumerate(subs):
            n = len(by_sub.get(s, []))
            lines.append(f"| {cls if j == 0 else ''}{f'（{n_cls} 个）' if j == 0 else ''} | [{s}](#{anchor(i, j)}) | {n} | {n / total:.1%} |")
    lines.append("")
    for i, (cls, subs) in enumerate(CLASSES):
        n_cls = sum(len(by_sub.get(s, [])) for s in subs)
        num, name = cls.split(" ", 1)
        lines += [f"## 第 {num} 类 {name}（{n_cls} 个）", "",
                  f"正文见[第 {num} 章]({CHAPTER[num]})。", ""]
        for j, s in enumerate(subs):
            rs = sorted(by_sub.get(s, []), key=lambda r: (dom_rank.get(r["领域大类"], 99), r["名称"]))
            lines += [f'<a id="{anchor(i, j)}"></a>', "", f"### {s}（{len(rs)} 个）", "",
                      "| 名称 | 领域 | 怎么判 | 怎么合成总分 |", "|---|---|---|---|"]
            for r in rs:
                name_cell = cell(r["名称"])
                if r["来源"].strip():
                    name_cell = f"[{name_cell}]({r['来源'].strip()})"
                parts = r["属于哪一类"].split("；")
                if len(parts) > 1:
                    name_cell += f"（也用到{parts[1].split(' ', 1)[1]}）"
                lines.append(f"| {name_cell} | {cell(r['领域'])} | {cell(how_judged(r))} | {cell(how_merged(r))} |")
            lines.append("")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{total} 个 bench → {OUT_PATH}")


if __name__ == "__main__":
    main()
