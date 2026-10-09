"""从 data/bench-master.csv 生成 docs/bench-list.md，并打印各轴取值的计数。

只用标准库。用法（在仓库根目录）：
    python3 scripts/bench_list.py            # 重写 docs/bench-list.md
    python3 scripts/bench_list.py --check    # 只核对文件是否和 CSV 一致
"""
import collections
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "bench-master.csv")
OUT_PATH = os.path.join(ROOT, "docs", "bench-list.md")

STATUSES = ["在用", "仅作机制解释", "评分不可核实"]
AXES = [("J 判官", "J"), ("O 对象", "O"), ("S 信号", "S"), ("R 参照", "R"),
        ("G1 题内", "G1"), ("G2 采样", "G2"), ("G3 题集", "G3"), ("G4 跨 bench", "G4")]

LEGEND = [
    ("OAI-Astra", "OpenAI GPT-6 Astra 发布页", "https://openai.com/index/gpt-6-astra/"),
    ("OAI-6.1", "GPT-6.1 Sol 系统卡补充", "https://deploymentsafety.openai.com/gpt-6-1-sol"),
    ("OAI-6-Oct", "GPT-6 Sol/Luna 十月更新系统卡", "https://deploymentsafety.openai.com/gpt-6-october/evaluations-with-challenging-prompts"),
    ("ANT-O55", "Anthropic Claude Opus 5.5 发布页", "https://www.anthropic.com/claude-opus-5-5"),
    ("ANT-O5", "Anthropic Claude Opus 5 发布页", "https://www.anthropic.com/news/claude-opus-5"),
    ("ANT-O5SC", "Claude Opus 5 系统卡 PDF", "https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf"),
    ("GDM-Argon", "Gemini 4 Argon 评测方法", "https://deepmind.google/models/evals-methodology/gemini-4-argon"),
    ("GDM-3.8F", "Gemini 3.8 Flash 模型卡", "https://deepmind.google/models/model-cards/gemini-3-8-flash/"),
    ("GDM-3.5F", "Gemini 3.5 Flash 模型卡", "https://deepmind.google/models/model-cards/gemini-3-5-flash/"),
    ("xAI-4.7", "Grok 4.7 发布页", "https://x.ai/news/grok-4-7"),
    ("DS-V4", "DeepSeek-V4-Pro 模型说明和技术报告", "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro"),
    ("Kimi-K3", "Kimi K3 模型说明（含脚注）", "https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md"),
    ("GLM-5.3", "Z.ai GLM-5.3 发布博客", "https://z.ai/blog/glm-5.3"),
    ("Qwen3.8", "Qwen3.8 模型说明（含脚注）", "https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8"),
    ("Seed2.1", "字节 Seed2.1 页面", "https://seed.bytedance.com/en/seed2_1"),
    ("MiniMax-M3", "MiniMax-M3 模型说明和评测结果", "https://huggingface.co/MiniMaxAI/MiniMax-M3"),
    ("Step3.7", "Step 3.7 Flash 模型说明", "https://huggingface.co/stepfun-ai/Step-3.7-Flash"),
    ("Hy3", "腾讯混元 Hy3 发布页（只列了 bench 名字）", "https://www.tencentcloud.com/techpedia/144773"),
    ("Meta-MS1.3", "Meta Muse Spark 1.3 页面", "https://dev.meta.ai/models/muse-spark"),
    ("SEAL", "Scale 排行榜，单榜地址为 scale.com/leaderboard/<slug>", "https://scale.com/leaderboard"),
    ("Vals", "Vals AI 榜单，单榜地址为 vals.ai/benchmarks/<slug>", "https://www.vals.ai/benchmarks"),
    ("AA", "Artificial Analysis 方法页（指数 v4.3.2）", "https://artificialanalysis.ai/methodology/intelligence-benchmarking"),
]


def split_codes(v):
    """一格里可能有多个取值：'+' 表示叠用，'|' 表示不同版本或口径，'→' 表示换算前后。"""
    if not v or v in ("—", "继承", "未公开", "不详"):
        return [v] if v else []
    return [p.strip() for p in re.split(r"[+|→]", v) if p.strip()]


def cell(v):
    v = (v or "").replace("\n", " ").replace("|", "\\|").replace("$", "\\$")
    return v if v else " "


def load():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def chain(r):
    return " → ".join(cell(r[k]) for k in ("G1 题内", "G2 采样", "G3 题集", "G4 跨 bench"))


def render(rows):
    by_status = collections.Counter(r["状态"] for r in rows)
    groups = []
    for r in rows:
        if r["领域大类"] not in groups:
            groups.append(r["领域大类"])
    used = [r for r in rows if r["状态"] == "在用"]
    out = []
    w = out.append
    w("# 测评清单")
    w("")
    w("这份清单由 `scripts/bench_list.py` 从 [`data/bench-master.csv`](../data/bench-master.csv) 生成，改清单请改 CSV 再重新生成。")
    w("")
    w("## 总数")
    w("")
    w(f"共 {len(rows)} 行：在用 {by_status['在用']} 行，仅作机制解释 {by_status['仅作机制解释']} 行，评分不可核实 {by_status['评分不可核实']} 行。")
    w("")
    w("- 在用：2025 年以后仍有厂商发布页、模型卡或第三方榜单在报分，而且评分方式能从公开材料确认。")
    w("- 仅作机制解释：头部厂商已经很少报，但它的评分机制在正文里被用来讲解某个概念（例如 pass@k 的公式出处）。")
    w("- 评分不可核实：有厂商在报，但题集或细则不公开，至少一条轴编不出来，编码格写\"未公开\"或\"不详\"。")
    w("")
    w("| 领域大类 | 在用 | 仅作机制解释 | 评分不可核实 | 合计 |")
    w("|---|---|---|---|---|")
    for g in groups:
        c = collections.Counter(r["状态"] for r in rows if r["领域大类"] == g)
        w(f"| {g} | {c['在用']} | {c['仅作机制解释']} | {c['评分不可核实']} | {sum(c.values())} |")
    w(f"| 合计 | {by_status['在用']} | {by_status['仅作机制解释']} | {by_status['评分不可核实']} | {len(rows)} |")
    w("")
    w(f"### 在用 {len(used)} 行里各取值出现的次数")
    w("")
    w("一行有多个取值（叠用、分版本）时各计一次。各取值的含义见 [README 的轴图](../README.md#axes)。")
    w("")
    w("| 轴 | 计数 |")
    w("|---|---|")
    for col, short in AXES:
        c = collections.Counter()
        for r in used:
            for p in dict.fromkeys(split_codes(r[col])):
                c[p] += 1
        w(f"| {short} | " + "，".join(f"{cell(k)} {v}" for k, v in c.most_common()) + " |")
    c = collections.Counter(r["入口类"] for r in used)
    w("| 入口类 | " + "，".join(f"{cell(k)} {v}" for k, v in c.most_common()) + " |")
    w("")
    w("## 读法")
    w("")
    w("- 编码列依次是判官 J、对象 O、信号 S、参照 R，以及合并链 G1 → G2 → G3 → G4。\"—\"表示这一层不做事；\"继承\"表示指数沿用组件自己的判法。")
    w("- 一格多值：`+` 是同时叠用（例如判官:平均占比+全过+门控），`|` 是不同版本或口径各一种（例如 FrontierSWE v1 \\| v2），`→` 是换算前后（细则分换成合成对局）。")
    w("- 入口类是 README 里的三类：1 单模型对标准，2 多模型比较，3 其他（指数、元评测、真实使用等）。")
    w("- 使用方列用简称，见下面的简称表。")
    w("")
    w("## 简称")
    w("")
    w("| 简称 | 来源 |")
    w("|---|---|")
    for k, desc, url in LEGEND:
        w(f"| {k} | [{cell(desc)}]({url}) |")
    w("")
    w("其他使用方直接写机构名（Arena、Epoch、MathArena、METR、Kaggle 等）；只写厂商名（如 Kimi、GDM、Meta）的，指该厂商 2026 年其他模型的发布材料。")
    w("")
    for status in STATUSES:
        sub = [r for r in rows if r["状态"] == status]
        w(f"## {status}（{len(sub)} 行）")
        w("")
        for g in groups:
            gr = [r for r in sub if r["领域大类"] == g]
            if not gr:
                continue
            w(f"### {g}（{len(gr)}）" if status == "在用" else f"#### {g}（{len(gr)}）")
            w("")
            w("| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |")
            w("|---|---|---|---|---|---|---|---|---|---|---|")
            for r in gr:
                note = r["编码说明"] or r["备注"]
                link = f"[链接]({r['链接']})" if r["链接"].startswith("http") else cell(r["链接"])
                w("| " + " | ".join([
                    r["编号"], cell(r["名称"]), cell(r["入口类"]), cell(r["J 判官"]), cell(r["O 对象"]),
                    cell(r["S 信号"]), cell(r["R 参照"]), chain(r), cell(note), cell(r["使用方（2026）"]), link]) + " |")
            w("")
    return "\n".join(out).rstrip() + "\n"


def main():
    rows = load()
    text = render(rows)
    if "--check" in sys.argv:
        same = os.path.exists(OUT_PATH) and open(OUT_PATH, encoding="utf-8").read() == text
        print("bench-list.md 与 CSV 一致" if same else "bench-list.md 需要重新生成")
        sys.exit(0 if same else 1)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    c = collections.Counter(r["状态"] for r in rows)
    print(f"共 {len(rows)} 行：" + "，".join(f"{s} {c[s]}" for s in STATUSES))


if __name__ == "__main__":
    main()
