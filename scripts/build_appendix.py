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


def main():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    groups = OrderedDict((g, []) for g in ORDER)
    for r in rows:
        groups.setdefault(r["领域大类"], []).append(r)
    lines = [
        "# 附录 书中涉及的 bench",
        "",
        f"这里按领域列出 {len(rows)} 个 bench。"
        "“怎么判”写谁来判、拿什么作对照；“怎么合成总分”依次写一道题内、多次采样和整套题三步，"
        "没有特别处理的步骤略去；“属于哪一类”对应正文的章节编号。"
        "更完整的字段（报告的数字、谁在报这个分、发布时间）在 [data/benchmarks.csv](../data/benchmarks.csv)。",
        "",
    ]
    for g, rs in groups.items():
        if not rs:
            continue
        lines += [f"## {g}", "", "| 名称 | 怎么判 | 怎么合成总分 | 属于哪一类 |", "|---|---|---|---|"]
        for r in rs:
            name = cell(r["名称"])
            if r["来源"].strip():
                name = f"[{name}]({r['来源'].strip()})"
            lines.append(f"| {name} | {cell(how_judged(r))} | {cell(how_merged(r))} | {cell(r['属于哪一类'])} |")
        lines.append("")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{len(rows)} 个 bench → {OUT_PATH}")


if __name__ == "__main__":
    main()
