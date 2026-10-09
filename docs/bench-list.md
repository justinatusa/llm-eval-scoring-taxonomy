# 测评清单

这份清单由 `scripts/bench_list.py` 从 [`data/bench-master.csv`](../data/bench-master.csv) 生成，改清单请改 CSV 再重新生成。

## 总数

共 236 行：在用 208 行，仅作机制解释 19 行，评分不可核实 9 行。

- 在用：2025 年以后仍有厂商发布页、模型卡或第三方榜单在报分，而且评分方式能从公开材料确认。
- 仅作机制解释：头部厂商已经很少报，但它的评分机制在正文里被用来讲解某个概念（例如 pass@k 的公式出处）。
- 评分不可核实：有厂商在报，但题集或细则不公开，至少一条轴编不出来，编码格写"未公开"或"不详"。

| 领域大类 | 在用 | 仅作机制解释 | 评分不可核实 | 合计 |
|---|---|---|---|---|
| 推理/知识/事实性 | 13 | 0 | 0 | 13 |
| 数学 | 11 | 1 | 0 | 12 |
| 科学 | 14 | 1 | 0 | 15 |
| 代码/软件工程 | 27 | 1 | 3 | 31 |
| 代理/工具调用 | 7 | 0 | 0 | 7 |
| 代理/经营/博弈 | 20 | 0 | 2 | 22 |
| 电脑/GUI 操作 | 4 | 0 | 0 | 4 |
| 深度研究/检索 | 9 | 0 | 0 | 9 |
| 专业领域（金融/法律/医疗/教育） | 16 | 1 | 0 | 17 |
| 长上下文 | 7 | 2 | 0 | 9 |
| 指令遵循/多轮对话 | 2 | 3 | 0 | 5 |
| 多语言/中文 | 11 | 0 | 0 | 11 |
| 多模态理解 | 16 | 0 | 1 | 17 |
| 视频理解 | 4 | 0 | 1 | 5 |
| 语音/音频 | 4 | 0 | 0 | 4 |
| 图像/视频/语音生成 | 2 | 3 | 0 | 5 |
| 安全与诚实 | 12 | 2 | 1 | 15 |
| 网络安全 | 10 | 0 | 1 | 11 |
| 情感/心理健康/写作 | 2 | 1 | 0 | 3 |
| 偏好竞技场/真实使用 | 5 | 3 | 0 | 8 |
| 判官/奖励模型评测 | 4 | 0 | 0 | 4 |
| 基座评测 | 3 | 0 | 0 | 3 |
| 聚合指数 | 5 | 1 | 0 | 6 |
| 合计 | 208 | 19 | 9 | 236 |

### 在用 208 行里各取值出现的次数

一行有多个取值（叠用、分版本）时各计一次。各取值的含义见 [README 的轴图](../README.md#axes)。

| 轴 | 计数 |
|---|---|
| J | J2 86，J1b 71，J1a 65，J4 8，继承 7，J1c 3，J5 2，J3 1 |
| O | O3 94，O2 76，O4 32，继承 7，O5 6，O6 3，O1 3 |
| S | S1 153，S3 33，S2 14，S4 12，继承 7 |
| R | R1 141，R2 41，R6 15，继承 7，R5 6，R3 5，R4 5，R7 2 |
| G1 | 单信号 110，全过 37，比例 22，加权 20，阈值 13，门控 11，继承 7，集合:F1 5，判官:多数 4，判官:平均占比 3，判官:一致 3，归一化 2，判官:抽一个 2，集合:精确 2，集合:全召回精度 1，判官:单侧覆盖 1，层级树 1，判官:重复众数 1 |
| G2 | 单次 148，平均 44，pass@k 10，继承 7，pass^k 5，best@k 4，— 2，选择器 1，maj@k 1，worst@k 1 |
| G3 | G3a 176，G3b 13，G3d 10，继承 6，G3c 5，G3e 2，G3f 1 |
| G4 | — 186，G4b 10，G4a 6，G4e 5，G4c 2 |
| 入口类 | 1 169，3 12，2 11，3（指数） 7，3（元评测） 4，3（真实使用） 3，2\|3 1，3\|2 1 |

## 读法

- 编码列依次是判官 J、对象 O、信号 S、参照 R，以及合并链 G1 → G2 → G3 → G4。"—"表示这一层不做事；"继承"表示指数沿用组件自己的判法。
- 一格多值：`+` 是同时叠用（例如判官:平均占比+全过+门控），`|` 是不同版本或口径各一种（例如 FrontierSWE v1 \| v2），`→` 是换算前后（细则分换成合成对局）。
- 入口类是 README 里的三类：1 单模型对标准，2 多模型比较，3 其他（指数、元评测、真实使用等）。
- 使用方列用简称，见下面的简称表。

## 简称

| 简称 | 来源 |
|---|---|
| OAI-Astra | [OpenAI GPT-6 Astra 发布页](https://openai.com/index/gpt-6-astra/) |
| OAI-6.1 | [GPT-6.1 Sol 系统卡补充](https://deploymentsafety.openai.com/gpt-6-1-sol) |
| OAI-6-Oct | [GPT-6 Sol/Luna 十月更新系统卡](https://deploymentsafety.openai.com/gpt-6-october/evaluations-with-challenging-prompts) |
| ANT-O55 | [Anthropic Claude Opus 5.5 发布页](https://www.anthropic.com/claude-opus-5-5) |
| ANT-O5 | [Anthropic Claude Opus 5 发布页](https://www.anthropic.com/news/claude-opus-5) |
| ANT-O5SC | [Claude Opus 5 系统卡 PDF](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |
| GDM-Argon | [Gemini 4 Argon 评测方法](https://deepmind.google/models/evals-methodology/gemini-4-argon) |
| GDM-3.8F | [Gemini 3.8 Flash 模型卡](https://deepmind.google/models/model-cards/gemini-3-8-flash/) |
| GDM-3.5F | [Gemini 3.5 Flash 模型卡](https://deepmind.google/models/model-cards/gemini-3-5-flash/) |
| xAI-4.7 | [Grok 4.7 发布页](https://x.ai/news/grok-4-7) |
| DS-V4 | [DeepSeek-V4-Pro 模型说明和技术报告](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) |
| Kimi-K3 | [Kimi K3 模型说明（含脚注）](https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md) |
| GLM-5.3 | [Z.ai GLM-5.3 发布博客](https://z.ai/blog/glm-5.3) |
| Qwen3.8 | [Qwen3.8 模型说明（含脚注）](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8) |
| Seed2.1 | [字节 Seed2.1 页面](https://seed.bytedance.com/en/seed2_1) |
| MiniMax-M3 | [MiniMax-M3 模型说明和评测结果](https://huggingface.co/MiniMaxAI/MiniMax-M3) |
| Step3.7 | [Step 3.7 Flash 模型说明](https://huggingface.co/stepfun-ai/Step-3.7-Flash) |
| Hy3 | [腾讯混元 Hy3 发布页（只列了 bench 名字）](https://www.tencentcloud.com/techpedia/144773) |
| Meta-MS1.3 | [Meta Muse Spark 1.3 页面](https://dev.meta.ai/models/muse-spark) |
| SEAL | [Scale 排行榜，单榜地址为 scale.com/leaderboard/<slug>](https://scale.com/leaderboard) |
| Vals | [Vals AI 榜单，单榜地址为 vals.ai/benchmarks/<slug>](https://www.vals.ai/benchmarks) |
| AA | [Artificial Analysis 方法页（指数 v4.3.2）](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |

其他使用方直接写机构名（Arena、Epoch、MathArena、METR、Kaggle 等）；只写厂商名（如 Kimi、GDM、Meta）的，指该厂商 2026 年其他模型的发布材料。

## 在用（208 行）

### 推理/知识/事实性（13）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Humanity's Last Exam（HLE，含 SEAL HLE-Diamond 子集） | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 判官做等价判定；另报校准误差 | AA 指数、OAI-Astra、ANT-O55、DS-V4、Kimi-K3、GLM-5.3、GDM-3.5F、SEAL、Step3.7 | [链接](https://arxiv.org/abs/2501.14249) |
| 2 | HLE-Verified | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | GDM-3.8F | [链接](https://deepmind.google/models/model-cards/gemini-3-8-flash/) |
| 3 | AA-Omniscience | 1 | J2 | O2 | S2 | R1 | 单信号 → 单次 → G3a → — | 四档含不答；Omniscience Index 答错扣分 | AA 指数、ANT-O5SC | [链接](https://arxiv.org/abs/2511.13029) |
| 4 | SimpleQA Verified | 1 | J2\|J1a | O2 | S2\|S1 | R1 | 单信号 → 单次 → G3a → — | 对话版 LLM 判三档后算 F 分数；基座版 25-shot EM | DS-V4（基座和对话都报） | [链接](https://arxiv.org/abs/2509.07968) |
| 5 | FACTS 套件 / FACTS Parametric | 1 | J2\|J1a | O2+O3 | S1 | R1 | 单信号+判官:平均占比+判官:一致 → 单次 → G3a → G4b | 事实分取 3 判官平均；取消资格要 3 判官一致；4 子榜等权 | DS-V4（基座表也报） | [链接](https://arxiv.org/abs/2512.10791) |
| 6 | MMLU-Pro | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | Justin 认为偏旧，只作基座阶段对照 | DS-V4（基座和对话） | [链接](https://arxiv.org/abs/2406.01574) |
| 7 | ARC-AGI-1 / 2 | 1 | J1a | O2 | S1 | R1 | 单信号 → pass@k → G3a → G4e | 两次提交即 pass@2；并列报每任务成本 | OAI-Astra、GDM-3.5F、ANT-O5 | [链接](https://arcprize.org/) |
| 8 | ARC-AGI-3 | 3 | J1b | O5 | S3 | R5 | 加权 → 单次 → G3a → — | 关分 (人类步数/AI 步数)² 封顶 1.15，按关号加权 | OAI-Astra、ANT-O5 | [链接](https://docs.arcprize.org/methodology) |
| 9 | EnigmaEval | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 1,161 题 | SEAL | [链接](https://scale.com/leaderboard/enigma_eval) |
| 10 | LiveBench | 1 | J1a+J1b | O2+O3 | S1 | R1 | 单信号 → 单次 → G3a → — | 只用客观答案，不用 LLM 判官 | LiveBench | [链接](https://livebench.ai/) |
| 11 | KINA | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 899 题 | Seed2.1 | [链接](https://github.com/2077AI/KINA) |
| 12 | SuperGPQA | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | Seed2.1、DS-V4 基座表 | [链接](https://arxiv.org/abs/2502.14739) |
| 13 | HELM Capabilities | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → G3a → G4b | 2025-03 起由平均胜率改为平均分 | Stanford CRFM | [链接](https://crfm.stanford.edu/helm/capabilities/latest/) |

### 数学（11）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 14 | FrontierMath（Tier 1–4） | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | OAI-Astra、Epoch | [链接](https://epoch.ai/frontiermath) |
| 15 | FrontierMath: Open Problems / Erdős | 1 | J1c | O3 | S1 | R1 | 单信号 → 单次 → G3d → — | 形式化命题算 R1，不需要已知答案 | Epoch | [链接](https://epoch.ai/frontiermath) |
| 16 | HMMT 2026 Feb（MathArena） | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a+G3e → — | MathArena 汇总时缺格用 IRT 补 | DS-V4、MathArena | [链接](https://matharena.ai/) |
| 17 | IMO-AnswerBench | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | AnswerAutoGrader：Gemini 2.5 Pro 抽答案并判等价 | DS-V4 | [链接](https://arxiv.org/abs/2511.01846) |
| 18 | MathArena Apex / Apex Shortlist | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a+G3e → — |   | DS-V4、MathArena | [链接](https://matharena.ai/) |
| 19 | IMO-ProofBench / IMO 2026 证明 | 1 | J2+J4 | O3 | S2 | R2 | 单信号\|判官:一致 → 单次 → G3a → — | 0–7 档；Anthropic IMO 2026 要 3 判官一致并人工抽查 | ANT-O5SC、DS-V4、MathArena | [链接](https://arxiv.org/abs/2511.01846) |
| 20 | RiemannBench（Riemann-Bench） | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a → — | 程序化等价检查 | GDM-Argon、ANT-O5 | [链接](https://arxiv.org/abs/2604.06802) |
| 21 | ArxivMath（MathArena） | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a → — |   | ANT-O5SC、MathArena | [链接](https://matharena.ai/) |
| 22 | BeyondAIME | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a → — | 100 题 | Seed2.1 | [链接](https://huggingface.co/datasets/ByteDance-Seed/BeyondAIME) |
| 23 | ProofBench（Vals） | 1 | J1c | O3 | S1 | R1 | 单信号 → 单次 → G3a → G4e | Lean 4 编译判定；4 个模型并列 100%，并报成本 | Vals | [链接](https://www.vals.ai/benchmarks/proof_bench) |
| 24 | PutnamBench | 1 | J1c | O3 | S1 | R1 | 单信号 → 单次\|pass@k → G3d → G4e | 全部解出后按每题平均成本排 | DS-V4（Putnam-200）；PutnamBench 公开榜 | [链接](https://trishullab.github.io/PutnamBench/leaderboard.html) |

### 科学（14）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | GPQA Diamond | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a → — | 2023 发布但 2026 仍被厂商报告 | OAI-Astra、DS-V4、Kimi-K3（AA v4.2 起移出指数） | [链接](https://arxiv.org/abs/2311.12022) |
| 26 | CritPt | 1 | J1a | O2+O3 | S1 | R1 | 单信号 → 平均 → G3a → — | 官方评分服务器做数值和 SymPy 判定 | AA 指数、Kimi-K3 | [链接](https://arxiv.org/abs/2509.26574) |
| 27 | PostTrainBench v1.1 | 3 | J1b+J2 | O3 | S3 | R3 | 门控 → 平均 → G3a → G4a | 产物是训好的模型，再跑 7 个 bench 加权；污染判定后退回基座分 | GDM-Argon、Kimi-K3、GLM-5.3 | [链接](https://posttrainbench.com/) |
| 28 | MLS-Bench-Lite | 3 | J1b | O3 | S3 | R4+R5 | 归一化 → 单次 → G3a → — | 最弱复现基线=0、人类 SOTA 作参考、理论上界=100 | Kimi-K3、Qwen3.8 | [链接](https://mls-bench.com/) |
| 29 | EEBench（xAI） | 1 | J1b | O3 | S1+S3 | R1 | 全过+加权 → 单次 → G3a → — | 电气检查通过，再看 BOM 成本效率 | xAI-4.7 | [链接](https://eebench.org/methodology.html) |
| 30 | DrugDiscoveryBench | 1 | J2 | O3 | S3 | R2 | 阈值 → 平均 → G3a → — | 必须 100 分才算过 | SEAL | [链接](https://scale.com/leaderboard/drugdiscoverybench) |
| 31 | SciPredict | 1 | J1a+J2 | O2 | S1 | R1+R2 | 单信号 → 单次 → G3a → — | 405 题，2025-03-31 后的结果 | SEAL | [链接](https://scale.com/leaderboard/scipredict) |
| 32 | LABBench2 | 1 | J1a+J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | GDM、ANT-O5 | [链接](https://github.com/EdisonScientific/labbench2) |
| 33 | BioMysteryBench | 1 | J2 | O2 | S1 | R1 | 单信号 → 平均 → G3a → — |   | GDM、ANT-O5、Vals | [链接](https://www.vals.ai/benchmarks/biomysterybench) |
| 34 | GeneBench-Pro | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 129 题；50 题子集将交给 AA | OAI-Astra | [链接](https://openai.com/index/introducing-genebench-pro/) |
| 35 | LifeSciBench | 1 | J2 | O3 | S1 | R2 | 阈值 → 单次 → G3a → — | 细则通过 ≥70% 算过 | OAI-Astra | [链接](https://openai.com/index/introducing-life-sci-bench/) |
| 36 | FrontierScience | 1 | J2 | O2\|O3 | S1\|S2 | R1\|R2 | 单信号\|阈值 → 单次 → G3a → — | Research 部分 ≥7/10 算过 | OAI | [链接](https://openai.com/index/frontierscience/) |
| 37 | MysteryMechanism（Vals） | 1 | J1b | O3 | S1 | R1 | 阈值 → 单次 → G3a → — | 归一化误差低于噪声阈值算对 | Vals | [链接](https://www.vals.ai/benchmarks/mysterymechanism) |
| 38 | Vals RSI Index | 3 | J1b | O3 | S3 | R4+R5 | 归一化 → 单次 → G3a → — | 起点=0、参考=0.5、最优=1，对数尺度 | Vals | [链接](https://www.vals.ai/benchmarks/rsi_index) |

### 代码/软件工程（27）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 39 | SciCode | 1 | J1b | O3 | S1 | R1 | 全过 → 平均 → G3a → — |   | AA 指数、Kimi-K3 | [链接](https://scicode-bench.github.io/) |
| 40 | SWE-bench Verified | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3a → — | FAIL_TO_PASS 全过且 PASS_TO_PASS 不坏 | DS-V4、ANT-O5（OpenAI 2026-02 起停报） | [链接](https://www.swebench.com/) |
| 41 | SWE-bench Pro（含 SEAL Public v2） | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3a → — | 包含 SEAL Public v2 | DS-V4、GDM-3.5F、SEAL、Qwen3.8、Step3.7、MiniMax-M3 | [链接](https://scale.com/leaderboard/swe_bench_pro_public_v2) |
| 42 | SWE-bench Multilingual / Multimodal | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3a → — | Multimodal 版见于 Anthropic Opus 5 系统卡 | DS-V4、ANT-O5、ANT-O5SC（Multimodal） | [链接](https://www.swebench.com/) |
| 43 | Terminal-Bench 2.0 / 2.1 / 3.0 / 4.0 | 1 | J1b | O4 | S1 | R1 | 全过 → 平均 → G3a → — |   | AA 指数（4.0）、Qwen3.8、Seed2.1、Step3.7、Hy3 等几乎所有厂商 | [链接](https://www.tbench.ai/) |
| 44 | Terminal-Bench-Science 0.1 | 1 | J1b | O4 | S1 | R1 | 全过 → 平均 → G3a → — | 超时放宽会改分 | OAI-Astra、ANT-O55、GDM-Argon | [链接](https://www.tbench.ai/) |
| 45 | DeepSWE v1.1 | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3a → G4e | 并列报成本 | OAI-Astra、GDM、xAI、Kimi、GLM、Meta、Qwen3.8 | [链接](https://deepswe.datacurve.ai/) |
| 46 | FrontierSWE v1 / v2 | 2\|3 | J1b | O3 | S3 | R6\|R3 | 加权 → best@k\|平均 → G3f\|G3a → —\|G4e | v1：支配分（名次类）；v2：mean@5 绝对分并画成本帕累托 | GDM-Argon、Kimi-K3、GLM-5.3、Qwen3.8 | [链接](https://www.frontierswe.com/) |
| 47 | FrontierCode v1.1 | 1 | J2 | O3 | S1 | R2 | 门控+加权 → 平均 → G3a → — | 任一 blocker 不过记 0；每档推理强度 5 次，报最好一档 | OAI-Astra、ANT-O55 | [链接](https://cognition.com/blog/frontier-code) |
| 48 | ProgramBench | 1 | J1b | O3 | S1 | R1 | 阈值 → 单次 → G3a → — | 100% 和 ≥95% 两条线 | Kimi-K3、GLM-5.3、Vals、Seed2.1 | [链接](https://www.vals.ai/benchmarks/programbench) |
| 49 | SWE-Marathon | 1 | J1b+J2 | O3 | S1 | R1 | 全过+门控 → 单次 → G3a → — | 正确性、性能门槛、反作弊三关 | Kimi-K3、GLM-5.3 | [链接](https://www.swe-marathon.org/) |
| 50 | NL2Repo-Bench | 1 | J1b+J2 | O3 | S1 | R1 | 比例+门控 → 单次 → G3a → — | LLM 反作弊判官可一票否决 | GLM-5.3、Seed2.1、Qwen3.8 | [链接](https://arxiv.org/abs/2512.12730) |
| 51 | LiveCodeBench | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3a → — |   | DS-V4 | [链接](https://livecodebench.github.io/) |
| 52 | Codeforces rating | 3 | J1b | O3 | S1 | R5 | 单信号 → 选择器 → G3c → — | 罚分口径 → 名次 → rating | DS-V4 | [链接](https://codeforces.com/) |
| 53 | Vibe Code Bench v1.1 | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3a → — |   | GDM-Argon、Vals | [链接](https://www.vals.ai/benchmarks/vibe-code) |
| 54 | SWE Atlas（Codebase QnA / Test Writing / Refactoring） | 1 | J1b+J2 | O3 | S1 | R1+R2 | 全过 → 单次\|平均 → G3a → — | 三个子榜：sweatlas-qna、sweatlas-tw、sweatlas-refactoring | SEAL、Meta、Seed2.1 | [链接](https://scale.com/leaderboard/sweatlas-qna) |
| 55 | HiL-Bench | 1 | J1b+J2 | O3+O5 | S1+S3 | R1 | 集合:F1 → pass@k → G3a → — | ASK-F1：提问精确率与阻塞召回率的调和平均 | SEAL | [链接](https://scale.com/leaderboard/hil) |
| 56 | IOI（Vals） | 1 | J1b | O3 | S1 | R1 | 加权 → 单次 → G3d → — | 子任务分相加 | Vals | [链接](https://www.vals.ai/benchmarks/ioi) |
| 57 | FrontierBench v0.1 | 1 | J1b | O4 | S3 | R1 | 单信号 → 平均 → G3a → — | 74 题，TB2.1 的后继 | ANT-O5SC | [链接](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |
| 58 | Code Migration（Vals） | 1 | J1b | O3 | S1 | R1 | 比例+门控 → 单次 → G3a → — | 作弊记 0 | Vals | [链接](https://www.vals.ai/benchmarks/code-migration) |
| 59 | VCB 1-100（Vibe Code Bench 续写） | 1 | J1b | O3 | S1 | R1 | 全过 → 单次 → G3d → — | 连续完成的迭代数 | Vals | [链接](https://www.vals.ai/benchmarks/vcb-1-100) |
| 60 | SRE Bench（Vals） | 1 | J1b | O4 | S1 | R1 | 全过 → 单次 → G3a → — | 6 个程序判定的任务全过才给分 | Vals | [链接](https://www.vals.ai/benchmarks/srebench) |
| 61 | MirrorCode（Epoch） | 1 | J1b | O3 | S1 | R1 | 全过 → 平均 → G3a → — | arXiv 2606.30182 | Epoch | [链接](https://epoch.ai/benchmarks/mirrorcode) |
| 62 | LiveCodeBench Pro | 3 | J1b | O3 | S1 | R5 | 单信号 → 单次 → G3c → — | 按题目难度拟合 Elo；题目难度来自人类选手 | LiveCodeBench Pro 公开榜；2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2506.11928) |
| 63 | AndroidBench 2.0 | 1 | J1b | O3 | S1 | R1 | 单信号 → 平均 → G3a → — |   | Qwen3.8、Google | [链接](https://developer.android.com/bench) |
| 64 | QwenReactBench / QwenSVGBench | 2 | J2+J1b | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | 多模态判官两两比较再拟合 BT | Qwen3.8 | [链接](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8) |
| 65 | ITBench-AA | 1 | J1a+J2 | O2 | S3 | R1 | 集合:全召回精度 → 平均 → G3a → — | 漏一个根因记 0，否则算精确率 | AA（附加） | [链接](https://artificialanalysis.ai/evaluations/itbench-aa) |

### 代理/工具调用（7）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 66 | τ²-bench / τ³-bench（含 Banking） | 1 | J1b | O4 | S1 | R1 | 全过 → pass^k\|平均 → G3a → — | 原版报 pass^k；AA τ³-Banking 报 5 次平均 pass@1；用户由 LLM 模拟 | AA（附加）、Kimi-K3 | [链接](https://github.com/sierra-research/tau2-bench) |
| 67 | MCP Atlas | 1 | J2 | O3 | S2 | R2 | 阈值 → 单次 → G3a → — | 要点 1/0.5/0，覆盖率 ≥0.75 算通过 | DS-V4、Kimi、GDM-3.5F、SEAL、ANT-O5 | [链接](https://scale.com/leaderboard/mcp_atlas) |
| 68 | Toolathlon（-Verified） | 1 | J1b | O4 | S1 | R1 | 单信号 → 平均 → G3a → — |   | DS-V4、Kimi、GLM、GDM-3.5F、ANT-O5、Qwen3.8、Step3.7 | [链接](https://toolathlon.xyz/) |
| 69 | MCPMark（-Verified） | 1 | J1b | O4 | S1 | R1 | 单信号 → 平均\|pass@k\|pass^k → G3a → — | Verified=固定 MCP 服务器版本、修题（PR #264） | Kimi-K3 | [链接](https://github.com/eval-sys/mcpmark) |
| 70 | EnterpriseOps-Gym | 1 | J1b | O4 | S1 | R1 | 全过\|比例 → 平均 → G3a → — |   | AA（附加） | [链接](https://arxiv.org/abs/2603.13594) |
| 71 | Remote Labor Index（RLI） | 3\|2 | J4 | O3 | S2 | R4\|R6 | 阈值+判官:多数 → 单次 → G3c\|G3b → — | 3 人多数，评级 ≥2 算达标 → 自动化率；另做 AI 间 Elo（人类=1000） | SEAL | [链接](https://scale.com/leaderboard/rli) |
| 72 | BFCL v4 | 1 | J1a+J1b | O2+O4 | S1 | R1 | 单信号 → 单次 → G3a → G4a | 分类加权：代理 40%、多轮 30%、其余各 10% | BFCL 榜 | [链接](https://gorilla.cs.berkeley.edu/leaderboard.html) |

### 代理/经营/博弈（20）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 73 | AutomationBench | 1 | J1b | O4 | S1 | R1 | 门控+比例 → 单次 → G3a → — | 碰护栏整题 0 分，否则按目标完成比例 | AA 指数、OAI、ANT、GDM、Kimi、GLM、Meta、Qwen3.8 | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 74 | APEX-Agents | 1 | J2 | O3+O4 | S1 | R2 | 全过 → 平均 → G3a → — | AA 版 452/480 题，每题 3 次 | AA（附加）、Kimi-K3、MiniMax-M3 | [链接](https://www.mercor.com/apex/apex-agents-leaderboard/) |
| 75 | Agents' Last Exam（ALE） | 1 | J1b+J2 | O3+O4 | S1 | R1+R2 | 全过\|比例 → 单次 → G3a → — |   | OAI-Astra、GDM-Argon、Kimi、GLM、Qwen3.8 | [链接](https://agents-last-exam.org/leaderboard) |
| 76 | JobBench | 1 | J2 | O3 | S1 | R2 | 全过+比例 → 单次 → G3a → — | 一条细则下所有标准都过才给这条的分 | Kimi-K3、Meta、ANT-O5、Qwen3.8 | [链接](https://arxiv.org/abs/2605.26329) |
| 77 | OfficeQA Pro | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | arXiv 2603.08655 | Kimi-K3、Meta、ANT-O5 | [链接](https://github.com/databricks/officeqa) |
| 78 | SpreadsheetBench 2 | 1 | J1b+J2 | O3 | S1 | R1 | 全过 → 单次 → G3a → — | 图表由视觉模型判 | Kimi-K3、Meta、ANT-O5 | [链接](https://arxiv.org/abs/2606.29955) |
| 79 | SaaS-Bench | 1 | J1b | O4 | S1 | R1 | 全过\|比例 → 单次 → G3a → — | resolved 与 checkpoint 两种口径 | Kimi-K3、Meta、ANT-O5 | [链接](https://arxiv.org/abs/2605.15777) |
| 80 | AA-Briefcase v1.1 | 2 | J2 | O3 | S1→S4+S4 | R2→R6 | 判官:抽一个+比例 → 单次 → G3b → — | 细则通过率改写成合成对局，与两项两两比较一起拟合 Crowd-BT；锚 GPT-5.5 (medium)=1000 | AA 指数、xAI、Kimi | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 81 | AA-AnalystAgent | 1 | J2+J1a | O2 | S1 | R1 | 判官:单侧覆盖 → pass^k → G3a → — | 程序预检只能把错改成对；头条 pass^5 | AA（附加） | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 82 | E-Commerce Bench（Qwen） | 3 | J1b | O4 | S3 | R3 | 单信号 → 单次 → G3d → — |   | Qwen3.8 | [链接](https://www.alibabacloud.com/blog/603421) |
| 83 | METR Time Horizon（1.0 / 1.1） | 3 | J1b | O4 | S1 | R5 | 单信号 → 平均 → G3c → — | logistic 读 50% 时间跨度 | METR | [链接](https://metr.org/time-horizons/) |
| 84 | RecreationBench | 1 | J1b+J2 | O3 | S1 | R1 | 比例 → 单次 → G3a → — | 先按平台平均再跨平台平均 | Qwen3.8 | [链接](https://huggingface.co/datasets/Qwen/RecreationBench) |
| 85 | Time Horizon Index: KSP | 1 | J1b | O4 | S3 | R1 | 加权 → 单次 → G3a → — | 按阶梯进度给部分分 | Vals | [链接](https://www.vals.ai/benchmarks/time_horizon_index) |
| 86 | SkillsBench v1.1 | 1 | J1b | O4 | S1 | R1 | 单信号 → 平均 → G3a → — | 87 题 | Vals、Qwen3.8 | [链接](https://www.vals.ai/benchmarks/skillsbench) |
| 87 | Claw-Eval（1.1） | 1 | J1b+J2 | O4 | S3 | R1 | 门控+阈值 → pass@k\|pass^k → G3a → — | 安全 ×（0.8·完成 + 0.2·鲁棒），≥0.75 算过 | MiniMax-M3、Step3.7 | [链接](https://github.com/claw-eval/claw-eval) |
| 88 | YC-Bench | 3 | J1b | O4 | S3 | R3 | 门控 → 平均 → G3d → — | 破产记 0 | MiniMax-M3 | [链接](https://github.com/collinear-ai/yc-bench) |
| 89 | Vending-Bench 2 | 3 | J1b | O4 | S3 | R3 | 单信号 → 平均 → G3d → — | 最终余额 | ANT、GDM 系 | [链接](https://andonlabs.com/evals/vending-bench-2) |
| 90 | Kaggle Game Arena（国际象棋/扑克/狼人杀/统一榜） | 2 | J1b | O4 | S4\|S3 | R6 | 单信号 → — → G3b\|G3d → G4c | 象棋 BT，狼人杀 GTE，扑克 BB/100；统一榜 pooled BT | Kaggle、GDM | [链接](https://www.kaggle.com/benchmarks/kaggle/game-arena) |
| 91 | Poker Agent（Vals） | 2 | J1b | O4 | S4 | R6 | 单信号 → 单次 → G3b → — | TrueSkill，按名次更新 | Vals | [链接](https://www.vals.ai/benchmarks/poker_agent) |
| 92 | \$OneMillion-Bench | 1 | J2 | O3 | S1 | R2 | 加权+阈值 → 单次 → G3a → — | 细则含负分项，≥0.7 算过 | Qwen3.8、Seed2.1 | [链接](https://arxiv.org/abs/2603.07980) |

### 电脑/GUI 操作（4）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 93 | OSWorld-Verified / 2.0 / 2.1 | 1 | J1b+J2 | O4 | S1 | R1 | 比例\|全过 → 平均\|best@k → G3a → — | partial 与 binary 两种口径 | OAI、ANT、GDM、Kimi、Meta、Qwen3.8 | [链接](https://osworld-v2.xlang.ai/) |
| 94 | ScreenSpot-Pro | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | OAI-Astra | [链接](https://arxiv.org/abs/2504.07981) |
| 95 | CUA-bench（Vals） | 1 | J1b | O4 | S3 | R1 | 加权 → 平均 → G3a → — | 里程碑阶梯，每游戏 100 分 | Vals | [链接](https://www.vals.ai/benchmarks/cua_bench) |
| 96 | MobileWorld | 1 | J1b | O4 | S1 | R1 | 单信号 → 单次 → G3a → — |   | Qwen3.8 | [链接](https://arxiv.org/abs/2512.19432) |

### 深度研究/检索（9）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 97 | BrowseComp（含 Multi-Agent 变体） | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次\|maj@k → G3a → — | 包含 Multi-Agent BrowseComp，评分同原版 | OAI、DS、Kimi、ANT-O5、Hy3、Step3.7 | [链接](https://arxiv.org/abs/2504.12516) |
| 98 | DeepSearchQA | 1 | J1a+J2 | O2 | S3 | R1 | 集合:F1 → 单次 → G3a → — | LLM 判元素语义等价，再算每题 F1 | Kimi、Meta、ANT-O5 | [链接](https://arxiv.org/abs/2601.20975) |
| 99 | ResearchRubrics | 1 | J2 | O3 | S1 | R2 | 加权 → 单次 → G3a → — | 细则含负分项 | Kimi-K3 | [链接](https://arxiv.org/abs/2511.07685) |
| 100 | WANDR | 1 | J2 | O3 | S1 | R1 | 集合:F1 → 单次 → G3a → — | soft / hard 两种匹配 | ANT-O55、Perplexity | [链接](https://arxiv.org/abs/2608.14747) |
| 101 | DRACO | 1 | J2 | O3 | S1 | R2 | 判官:平均占比+比例 → 单次 → G3a → — | 判分跑 5 次取平均 | ANT-O5SC | [链接](https://arxiv.org/abs/2602.11685) |
| 102 | DeepResearch Bench（RACE / FACT） | 3 | J2 | O3 | S3 | R4+R1 | 单信号 → 单次 → G3a → — | RACE 对参考报告打相对分；FACT 查引用 | DeepResearch Bench 公开榜；2026 年头部模型卡中未见引用 | [链接](https://deepresearch-bench.github.io/) |
| 103 | WideSearch | 1 | J1a+J2 | O2 | S3\|S1 | R1 | 集合:F1\|集合:精确 → 平均\|pass@k\|best@k → G3a → — | 表格逐格比对 | Qwen3.8、Hy3 | [链接](https://arxiv.org/abs/2508.07999) |
| 104 | PaperBench | 1 | J2 | O3 | S1 | R2 | 层级树 → 平均 → G3a → — |   | Qwen3.8 | [链接](https://arxiv.org/abs/2504.01848) |
| 105 | EBR-bench（Epoch） | 1 | J1b | O4 | S1 | R1 | 单信号 → best@k → G3d → — | 10 次取最后 2 次中较好者 | Epoch | [链接](https://epoch.ai/benchmarks/ebr-bench) |

### 专业领域（金融/法律/医疗/教育）（16）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 106 | GDPval（OpenAI 原版） | 3 | J4 | O3 | S4 | R4 | 单信号 → 单次 → G3c → — | 胜或平率 | xAI-4.7、Step3.7 | [链接](https://arxiv.org/abs/2510.04374) |
| 107 | GDPval-AA v2 / v2.1 | 2 | J2 | O3 | S4 | R6 | 判官:抽一个 → 单次 → G3b → — | Crowd-BT，平局记半胜，锚 DeepSeek V4.1 Flash (max)=1600 | AA 指数、几乎所有厂商 | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 108 | GDP.pdf | 1 | J2 | O3 | S1 | R2 | 全过\|比例 → 平均 → G3a → — | AA 版单判官 GPT-5.6 Luna (medium) | AA 指数、GDM-3.8F、ANT-O5 | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 109 | Harvey LAB / LAB-AA | 1 | J2 | O3 | S1 | R2 | 判官:平均占比+全过+门控 → 单次 → G3a → — | 每条细则取 3 判官通过占比；有实质幻觉记 0 | AA、GDM-Argon、GDM-3.8F、xAI、Kimi | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 110 | Vals Finance Agent v2（FAB v2） | 1 | J2 | O2 | S1 | R2 | 判官:重复众数+全过\|比例 → 单次 → G3a → — | 判 3 次取众数；partial 与 all-pass 两种口径会翻转名次 | GDM-Argon、GDM-3.5F/3.8F、Kimi | [链接](https://www.vals.ai/benchmarks/fabv2) |
| 111 | CorpFin v2 | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 判官 Claude 4.5 Sonnet，温度 0 | Kimi-K3、Vals | [链接](https://www.vals.ai/benchmarks/corp_fin_v2) |
| 112 | Legal Research Bench | 1 | J2 | O3 | S1 | R2 | 全过\|加权 → 单次 → G3a → — | 两种口径 55.29 vs 90.58 | Kimi-K3、Vals | [链接](https://www.vals.ai/benchmarks/legal_research) |
| 113 | HealthBench / Professional / Hard | 1 | J2 | O3 | S1 | R2 | 加权 → 单次\|worst@k → G3a → — | 含负分项，平均后裁到 [0,1] | OAI、xAI、ANT-O5、Qwen3.8 | [链接](https://arxiv.org/abs/2505.08775) |
| 114 | TutorBench | 1 | J2 | O3 | S1 | R2 | 加权 → 单次 → G3a → — |   | SEAL | [链接](https://scale.com/leaderboard/tutorbench) |
| 115 | PRBench（Finance / Legal；SEAL 页面名 Professional Reasoning） | 1 | J2 | O3 | S1 | R2 | 加权 → 单次 → G3a → — | 细则含负分项 | SEAL、Qwen3.8 | [链接](https://scale.com/leaderboard/prbench-legal) |
| 116 | Tax Agent Bench | 1 | J2 | O3 | S1+S3 | R2 | 全过+加权 → 单次 → G3a → — | 全过后再乘引用质量 | Vals | [链接](https://www.vals.ai/benchmarks/tax_agent_bench) |
| 117 | MedCode | 1 | J1a | O2 | S2 | R1 | 阈值 → 单次 → G3a → — |   | Vals | [链接](https://www.vals.ai/benchmarks/medcode) |
| 118 | CaseLaw v2（Vals） | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 判官细节未抽到 | Vals | [链接](https://www.vals.ai/benchmarks/case_law_v2) |
| 119 | EMB（Vals） | 1 | J1a\|J2 | O3 | S1 | R1\|R2 | 比例 → 单次 → G3a → — |   | Vals | [链接](https://www.vals.ai/benchmarks/emb) |
| 120 | MedScribe（Vals） | 1 | J2 | O3 | S1 | R2 | 比例 → 单次 → G3a → — | Vals 报告判官选择会改分 | Vals | [链接](https://www.vals.ai/benchmarks/medscribe) |
| 121 | Public Benefits Bench v1.1（SNAP） | 1 | J2 | O3 | S1 | R2 | 单信号 → 单次 → G3a → — | 459 场景 | Vals | [链接](https://www.vals.ai/benchmarks/public-benefits-bench) |

### 长上下文（7）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 122 | OpenAI MRCR v2 | 1 | J1a | O2 | S3 | R1 | 门控 → 单次 → G3a → — | 缺哈希前缀记 0，否则算相似度 | OAI-Astra、GDM-3.5F、Meta、DS-V4、Qwen3.8、Context Arena | [链接](https://huggingface.co/datasets/openai/mrcr) |
| 123 | GraphWalks | 1 | J1a | O2 | S3 | R1 | 集合:F1 → 单次 → G3a → — |   | GDM-Argon | [链接](https://huggingface.co/datasets/openai/graphwalks) |
| 124 | AA-LCR | 1 | J2 | O2 | S1 | R1 | 单信号 → 平均 → G3a → — | v1.1 与 v1.0 不可比 | AA 指数、Kimi | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 125 | MLCR-AA | 1 | J2 | O2 | S1 | R1 | 门控+判官:多数 → 平均 → G3a → — | 超过参考答案 5 倍长记 0；3 判官多数 | AA（附加） | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 126 | CorpusQA 1M | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | DS-V4 | [链接](https://arxiv.org/abs/2601.14952) |
| 127 | LongBench-V2 | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | DS-V4（基座表） | [链接](https://arxiv.org/abs/2412.15204) |
| 128 | RULER | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 2024 发布，2026 仍在开源卡出现 | 开源模型卡（如 Nemotron） | [链接](https://arxiv.org/abs/2404.06654) |

### 指令遵循/多轮对话（2）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 129 | IFBench | 1 | J1a | O3 | S1 | R1 | 全过\|比例 → 平均 → G3a → — |   | AA（附加）、Qwen3.8 | [链接](https://arxiv.org/abs/2507.02833) |
| 130 | MultiChallenge | 1 | J2 | O3 | S1 | R2 | 单信号 → 单次 → G3a → — |   | SEAL | [链接](https://scale.com/leaderboard/multichallenge) |

### 多语言/中文（11）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 131 | Chinese-SimpleQA | 1 | J2 | O2 | S2 | R1 | 单信号 → 单次 → G3a → — |   | DS-V4 | [链接](https://arxiv.org/abs/2411.07140) |
| 132 | MultiNRC | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | SEAL | [链接](https://scale.com/leaderboard/multinrc) |
| 133 | Global-MMLU（含 Global-MMLU-Lite） | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | Lite 约 6000 题 | ANT-O5SC、AA Multilingual Index | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 134 | MILU | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | ANT-O5SC | [链接](https://arxiv.org/abs/2411.02538) |
| 135 | INCLUDE | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | ANT-O5SC | [链接](https://arxiv.org/abs/2411.19799) |
| 136 | PLawBench | 1 | J2 | O3 | S1 | R2 | 加权 → 单次 → G3a → — | ACL 2026 | Qwen3.8 | [链接](https://arxiv.org/abs/2601.16669) |
| 137 | BrowseComp-ZH | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | 中文研究代理榜；2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2504.19314) |
| 138 | xbench-DeepSearch（2510） | 1 | J1a+J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 先精确匹配，不行再用 LLM | xbench 公开榜；2026 年头部模型卡中未见引用 | [链接](https://huggingface.co/datasets/xbench/DeepSearch-2510) |
| 139 | PolyMath | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均 → G3a → — | 难度加权 (a低 + 2a中 + 4a高 + 8a顶)/15 | Qwen3 系（2025）；2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2504.18428) |
| 140 | SuperCLUE 通用榜（月报） | 1 | J1a+J1b+J2 | O2+O3 | S1 | R1+R2 | 单信号 → 单次 → G3a → G4b |   | SuperCLUE | [链接](https://www.cluebenchmarks.com/superclue.html) |
| 141 | OpenCompass CompassBench / CompassAcademic | 1 | J1a+J2 | O2 | S1 | R1 | 全过 → 单次 → G3a → G4b | CircularEval：选项轮换 4 次全对才得分 | OpenCompass | [链接](https://github.com/open-compass/CompassBench) |

### 多模态理解（16）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 142 | MMMU-Pro | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | AA（附加）、GDM-3.5F、Kimi、Seed2.1、MiniMax-M3 | [链接](https://arxiv.org/abs/2409.02813) |
| 143 | CharXiv（RQ） | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 官方 src/reasoning_utils.py | GDM-3.5F/3.8F、Kimi、Seed2.1、Qwen3.8 | [链接](https://charxiv.github.io/) |
| 144 | Chartography | 1 | J2 | O2 | S1 | R1 | 全过 → 单次 → G3a → — | arXiv 2608.10677 | ANT-O55、GDM-Argon | [链接](https://surgehq.ai/benchmarks/chartography) |
| 145 | ZeroBench | 1 | J1a | O2 | S1 | R1 | 单信号 → pass@k\|pass^k → G3a → — |   | Kimi-K3、Seed2.1 | [链接](https://zerobench.github.io/) |
| 146 | MathVision | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | Kimi-K3、Seed2.1 | [链接](https://arxiv.org/abs/2402.14804) |
| 147 | OmniDocBench（v1.5） | 1 | J1a | O3 | S3 | R1 | 单信号 → 单次 → G3a → — | 三项指标先各自平均再合成 Overall | Kimi-K3 | [链接](https://github.com/opendatalab/OmniDocBench) |
| 148 | BenchCAD | 1 | J1a | O3 | S3 | R1 | 单信号 → 单次 → G3a → — | 几何重叠度 | OAI-Astra、ANT-O5 | [链接](https://openai.com/index/gpt-6-astra/) |
| 149 | VisualToolBench | 1 | J2 | O3 | S1 | R2 | 全过\|加权 → 单次 → G3a → — |   | SEAL | [链接](https://scale.com/leaderboard/vtb) |
| 150 | VISTA（Visual Language Understanding） | 1 | J2 | O3 | S1 | R2 | 判官:多数+比例 → 平均 → G3a → — |   | SEAL | [链接](https://scale.com/leaderboard/visual_language_understanding) |
| 151 | OpenScore String Quartets（OMR） | 1 | J1a | O3 | S3 | R1 | 单信号 → 单次 → G3a → — |   | OAI-Astra | [链接](https://arxiv.org/abs/2608.10978) |
| 152 | WorldVQA | 1 | J2 | O2 | S2 | R1 | 单信号 → 单次 → G3a → — |   | Kimi-K3、Seed2.1 | [链接](https://arxiv.org/abs/2602.02537) |
| 153 | BabyVision | 1 | J2 | O2 | S1 | R1 | 单信号 → 平均 → G3a → — |   | Kimi-K3、Seed2.1、Qwen3.8 | [链接](https://arxiv.org/abs/2601.06521) |
| 154 | ERQA | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 400 题 | Seed2.1、Qwen3.8 | [链接](https://github.com/embodiedreasoning/ERQA) |
| 155 | Vision2Web | 1 | J2+J1b | O3 | S3 | R1+R2 | 加权 → 单次 → G3a → — |   | Qwen3.8 | [链接](https://github.com/zai-org/Vision2Web) |
| 156 | SimpleVQA | 1 | J2 | O2 | S2 | R1 | 单信号 → 单次 → G3a → — |   | Step3.7 | [链接](https://arxiv.org/abs/2502.13059) |
| 157 | V* Bench | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 2023 发布、2026 仍被报告 | Step3.7 | [链接](https://vstar-seal.github.io/) |

### 视频理解（4）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 158 | LVBench | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 各家输入帧数不同 | GDM-Argon、GDM-3.8F、Qwen3.8 | [链接](https://arxiv.org/abs/2406.08035) |
| 159 | Video-MME（v1 / v2）/ MMVU | 1 | J1a | O2 | S1 | R1 | 单信号\|加权 → 平均 → G3a → — | v2 每组 4 题答对 N 题记 (N/4)² | Kimi-K3、Seed2.1、MiniMax-M3 | [链接](https://arxiv.org/abs/2604.05015) |
| 160 | Humanity's Sixth Sense（HSS） | 1 | J2 | O3 | S1 | R2 | 比例 → 平均 → G3a → — | 522 题 | SEAL | [链接](https://labs.scale.com/papers/humanitys-sixth-sense) |
| 161 | OVO-Bench | 1 | J1a | O2 | S3 | R1 | 加权 → 单次 → G3a → — | 答对后乘延迟衰减 2^(−delay·p) | Seed2.1 | [链接](https://github.com/JoeLeelyf/OVO-Bench) |

### 语音/音频（4）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 162 | Audio MultiChallenge | 1 | J2 | O3 | S1 | R2 | 全过 → 单次 → G3a → — | ACL 2026 | SEAL | [链接](https://scale.com/leaderboard/audiomc) |
| 163 | AA Speech-to-Speech Index（含 Big Bench Audio） | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4b | Big Bench Audio 1000 题 | AA | [链接](https://artificialanalysis.ai/methodology/speech-to-speech-benchmarking) |
| 164 | AA-WER v2（Speech-to-Text） | 1 | J1a | O3 | S3 | R1 | 单信号 → 单次 → G3a → G4a | 按时长加权，再按 50/25/25 跨数据集合并；越低越好 | AA | [链接](https://artificialanalysis.ai/articles/aa-wer-v2) |
| 165 | VoiceCodeBench（Vals） | 1 | J1a | O2 | S1 | R1 | 全过 → 单次 → G3a → — | 一段录音里所有实体都对才算 | Vals | [链接](https://www.vals.ai/benchmarks/voice-code-bench) |

### 图像/视频/语音生成（2）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 166 | AA Text-to-Speech Arena | 2 | J4 | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | 面板盲评，BT，锚 1000 | AA | [链接](https://artificialanalysis.ai/methodology/text-to-speech) |
| 167 | AA Image / Video Arena（文生图、图像编辑、文生视频、图生视频） | 2 | J4 | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | 面板盲评，BT，锚 1000 | AA；厂商引用（Seedream 5.0 等） | [链接](https://artificialanalysis.ai/image/methodology) |

### 安全与诚实（12）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 168 | Gray Swan IPI Arena | 1 | J1b+J2 | O4 | S1 | R1 | 全过+阈值 → 单次 → G3a → — | 程序检查成功且隐蔽性判官 >7/10；越低越好 | GDM-Argon、ANT-O55 | [链接](https://arxiv.org/abs/2603.15714) |
| 169 | OpenAI Production Benchmarks / Challenging prompts | 1 | J2 | O3 | S1 | R2 | 单信号 → 单次 → G3a → — |   | OAI-6-Oct、OAI-6.1 | [链接](https://deploymentsafety.openai.com/gpt-6-october/evaluations-with-challenging-prompts) |
| 170 | Arena Alignment Index | 3（真实使用） | J2 | O6 | S1 | R2 | 单信号 → 单次 → G3a → G4a | 1−√率 变换 | Arena | [链接](https://arena.ai/blog/ai-alignment-index) |
| 171 | PropensityBench | 1 | J1a | O5 | S1 | R1 | 单信号 → 单次 → G3a → — | 12 级逐步加压是出分条件；越低越好 | SEAL | [链接](https://scale.com/leaderboard/propensitybench) |
| 172 | FORTRESS | 1 | J2 | O3 | S1 | R2 | 判官:多数+比例 → 单次 → G3a → — | 3 判官多数票 | SEAL | [链接](https://scale.com/leaderboard/fortress) |
| 173 | MASK | 1 | J2 | O3 | S1 | R7 | 单信号 → 单次 → G3a → — | 参照是同一模型先说出的信念；诚实度 = 1 − P(撒谎) | SEAL、ANT-O5SC | [链接](https://arxiv.org/abs/2503.03750) |
| 174 | SHADE-Arena | 1 | J1b+J2 | O4+O5 | S1 | R1 | 全过+阈值 → 单次 → G3a → — | 副任务完成且监控可疑分低于阈值 | ANT-O5SC | [链接](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |
| 175 | LinuxArena（Redwood） | 1 | J1b+J2 | O4+O5 | S1 | R1 | 全过+阈值 → 单次 → G3a → — |   | ANT-O5SC | [链接](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |
| 176 | 政治中立性评测（Anthropic） | 1 | J2 | O3 | S1 | R7 | 比例 → 单次 → G3a → — | 参照是同一模型对镜像提示的回答 | ANT-O5SC | [链接](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |
| 177 | BBQ | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 老 bench，Anthropic 系统卡仍报 | ANT-O5SC | [链接](https://arxiv.org/abs/2110.08193) |
| 178 | VCT-v2（Virology Capabilities Test） | 1 | J1a | O2 | S1 | R1 | 集合:精确 → 单次 → G3a → — | 多选全对才算 | 系统卡（OAI/ANT/xAI） | [链接](https://securebio.org/blog/introducing-vct-v2/) |
| 179 | SAFE-Teen（Vals） | 1 | J2 | O3 | S2 | R2 | 比例 → 单次 → G3a → — | partial 计入分母但不算失败 | Vals | [链接](https://www.vals.ai/benchmarks/mental-health) |

### 网络安全（10）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 180 | CyberGym（含 CyberGym-E2E-AA） | 1 | J1b | O3 | S1 | R1 | 单信号 → 单次 → G3a → — | 包含 AA 的 E2E 变体 | GLM-5.3、AA Cyber Index | [链接](https://arxiv.org/abs/2506.02548) |
| 181 | ExploitBench | 1 | J1b | O3 | S1 | R1 | 比例 → pass@k → G3a → — | 16 个能力旗标，3 次取并集 | OAI-Astra、GLM-5.3、ANT-O5SC | [链接](https://exploitbench.ai/) |
| 182 | ExploitGym | 1 | J1b | O4 | S1 | R1 | 单信号 → 单次 → G3a → — | 2h/6h 时间预算，按 TPS 归一化 | OAI-Astra、GLM-5.3 | [链接](https://openai.com/index/gpt-6-astra/) |
| 183 | SRE-Bench（OpenAI，二进制逆向） | 1 | J1b | O3 | S1 | R1 | 单信号 → 单次\|pass@k → G3a → — | 注意与 Vals SRE Bench 不是同一个 | OAI-Astra | [链接](https://arxiv.org/abs/2608.11469) |
| 184 | CWE-bench（含 CWE-Bench-AA） | 1 | J1b | O2 | S1 | R1 | 单信号 → 平均\|pass@k → G3a → — | pass@1 排名，平手看 pass@4 | GDM-Argon、AA Cyber Index | [链接](https://deepmind.google/models/evals-methodology/gemini-4-argon) |
| 185 | SEC-bench Pro | 1 | J1b+J2 | O3 | S1 | R1 | 单信号 → 单次 → G3a → — | 344 例（V8/SpiderMonkey/Linux） | OAI-Astra | [链接](https://arxiv.org/abs/2605.26548) |
| 186 | CyberBench v1.1（Vals） | 1 | J1b | O3 | S1 | R1 | 单信号 → 单次 → G3a → — | fallback 记法给两个数 | Vals | [链接](https://www.vals.ai/benchmarks/cyber) |
| 187 | Cybench | 1 | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | 2026 系统卡 | [链接](https://cybench.github.io/) |
| 188 | Firefox 147 漏洞利用评测（Anthropic） | 1 | J1b | O4 | S2 | R1 | 单信号 → 平均 → G3a → — | 0 / 0.5 / 1 三档 | ANT-O5SC | [链接](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |
| 189 | CyScenarioBench（Irregular） | 1 | J1b | O4 | S2 | R1 | 单信号 → 单次 → G3a → — |   | ANT-O5SC | [链接](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/claude%20opus%205%20system%20card.pdf) |

### 情感/心理健康/写作（2）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 190 | MentalHealthBench（OpenAI） | 1 | J2 | O3 | S1 | R2 | 加权 → 单次 → G3a → — | 1,215 段对话 | OAI | [链接](https://openai.com/index/introducing-mentalhealthbench/) |
| 191 | EQ-Bench 3 | 2 | J2 | O3 | S2+S4 | R2+R6 | 单信号 → 单次 → G3b → — | 细则分加两两比较，拟合 TrueSkill | EQ-Bench 榜 | [链接](https://eqbench.com/) |

### 偏好竞技场/真实使用（5）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 192 | Arena 成对投票家族（Text/WebDev/Vision/Document/Search/T2I/Image Edit/Video） | 2 | J4 | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | BT + 风格控制 | Arena；厂商常引用 | [链接](https://lmarena.ai/leaderboard) |
| 193 | Arena AutoEval | 2 | J3+J4 | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | 奖励模型分差经 softmax 变成软票 | Arena | [链接](https://arena.ai/blog/autoeval-scores) |
| 194 | Agent Arena | 3（真实使用） | J5+J1b | O6 | S1+S3 | R6 | 单信号 → 单次 → G3b → G4b | 每个信号做 IPS，再五个信号等权平均 | Arena | [链接](https://arena.ai/blog/agent-arena-methodology) |
| 195 | OpenRouter Rankings | 3（真实使用） | J5 | O6 | S3 | R6 | 单信号 → — → G3d → — | token 用量份额 | OpenRouter | [链接](https://openrouter.ai/rankings) |
| 196 | Design Arena | 2 | J4 | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | 4 个模型一次会话拆成 5 场两两比较，BT | Design Arena 公开榜 | [链接](https://www.designarena.ai/about) |

### 判官/奖励模型评测（4）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 197 | SAGE（Vals） | 3（元评测） | J1a | O2 | S1 | R1 | 单信号 → 单次 → G3a → — | 被评的是判官 | Vals | [链接](https://www.vals.ai/benchmarks/sage) |
| 198 | RewardBench 2 | 3（元评测） | J1a | O1 | S1 | R1 | 单信号 → 单次 → G3a → G4b | 被评的是奖励模型 | 奖励模型论文与卡 | [链接](https://arxiv.org/abs/2506.01937) |
| 199 | ProcessBench | 3（元评测） | J1a | O5 | S1 | R1 | 单信号 → 单次 → G3a → — | 被评的是过程打分器；两类准确率取调和平均 | PRM 论文 | [链接](https://arxiv.org/abs/2412.06559) |
| 200 | JudgeBench | 3（元评测） | J1a | O2 | S1 | R1 | 判官:一致 → 单次 → G3a → — | 被评的是判官；换位判两次须一致 | 判官模型论文 | [链接](https://arxiv.org/abs/2410.12784) |

### 基座评测（3）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 201 | 预训练基座 few-shot 套件（DS-V4 基座表 24 项） | 1 | J1a+J1b | O2+O3 | S1 | R1 | 单信号 → 单次 → G3a → — | 表上只标 EM，没写是生成式还是按困惑度 | DS-V4 | [链接](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) |
| 202 | OlmoBaseEval（含 Base Easy BPB） | 1 | J1a | O1+O2 | S1+S3 | R1 | 单信号 → 单次 → G3a → G4b |   | AI2 OLMo 3 | [链接](https://allenai.org/olmo) |
| 203 | Uncheatable Eval | 1 | J1a | O1 | S3 | R1 | 单信号 → 单次 → G3a → — | 新语料上的压缩率 | 论文自带 80 个模型的排名 | [链接](https://arxiv.org/abs/2609.27510) |

### 聚合指数（5）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 204 | AA Intelligence Index v4.3.2 | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4a | Elo 类组件冻结后 clamp((Elo−500)/2000) | AA；厂商常引用 | [链接](https://artificialanalysis.ai/methodology/intelligence-benchmarking) |
| 205 | AA Coding Agent Index | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4b | 3 个组件等权 | AA；OAI-Astra 引用 | [链接](https://artificialanalysis.ai/agents/coding-agents) |
| 206 | Vals Index | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4a | 按行业 GDP 占比加权 | Vals；GDM-Argon 引用 | [链接](https://www.vals.ai/benchmarks/vals_index) |
| 207 | Epoch Capabilities Index（ECI） | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4c | IRT 式联合拟合 | Epoch | [链接](https://epoch.ai/benchmarks/eci) |
| 208 | AA Cyber Index（含 DeepsecBench-AA） | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4b |   | AA | [链接](https://artificialanalysis.ai/evaluations/artificial-analysis-cyber-index) |

## 仅作机制解释（19 行）

#### 数学（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 209 | AIME 2024 / 2025 | 1 | J1a | O2 | S1 | R1 | 单信号 → 平均\|maj@k → G3a → — | 解释 pass@1 平均与多数投票 | 已不被 2026 头部报告主推 | [链接](https://artofproblemsolving.com/wiki/index.php/AIME_Problems_and_Solutions) |

#### 科学（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 210 | MLE-bench | 3 | J1b | O3 | S1 | R5 | 阈值 → 平均 → G3a → — | 奖牌线来自人类 Kaggle 排行 | 榜单 2026 暂停 | [链接](https://github.com/openai/mle-bench) |

#### 代码/软件工程（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 211 | HumanEval / MBPP / EvalPlus | 1 | J1b | O3 | S1 | R1 | 全过 → pass@k → G3a → — | 无偏 pass@k 公式出处 | 仅基座表 | [链接](https://arxiv.org/abs/2107.03374) |

#### 专业领域（金融/法律/医疗/教育）（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 212 | Vals Mortgage Tax / TaxEval v2 | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | Vals 已停跑（饱和） | [链接](https://www.vals.ai/benchmarks/tax_eval_v2) |

#### 长上下文（2）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 213 | Fiction.LiveBench | 1 | J2 | O2 | S1 | R1 | 单信号 → 单次 → G3a → — |   | 2026 未见更新 | [链接](https://fiction.live/stories/Fiction-liveBench) |
| 214 | NoLiMa | 1 | J1a | O2 | S1 | R7 | 单信号 → 单次 → G3c → — | 有效长度：分数仍 ≥ 本模型短上下文分 85% 的最长长度 | 2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2502.05167) |

#### 指令遵循/多轮对话（3）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 215 | IFEval | 1 | J1a | O3 | S1 | R1 | 全过\|比例 → 单次 → G3a → — | strict / loose | 已被 IFBench 取代 | [链接](https://arxiv.org/abs/2311.07911) |
| 216 | MT-Bench | 1 | J2 | O3 | S2 | R2 | 单信号 → 单次 → G3a → — | 细则只是判官提示里的通用打分说明 | 2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2306.05685) |
| 217 | Multi-IF | 1 | J1a | O3 | S1 | R1 | 全过 → 单次 → G3a → — |   | Qwen3.8 已改报 IFBench | [链接](https://arxiv.org/abs/2410.15553) |

#### 图像/视频/语音生成（3）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 218 | VBench-2.0 | 1 | J1a+J2 | O3 | S3 | R1 | 比例 → 单次 → G3a → G4b |   | 2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2503.21755) |
| 219 | K-Sort Arena | 2 | J4 | O3 | S4 | R6 | 单信号 → 单次 → G3b → — | 一次排 K 个；Thurstone 式贝叶斯，保守分 μ−3σ | HF 榜单约一年未更新 | [链接](https://arxiv.org/abs/2408.14468) |
| 220 | HPSv3 Benchmark | 3 | J3 | O3 | S3 | R3 | 单信号 → 单次 → G3a → — | 偏好模型分数没有上限 | ICCV 2025 论文 | [链接](https://mizzenai.github.io/HPSv3.project/) |

#### 安全与诚实（2）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 221 | StrongREJECT | 1 | J2 | O3 | S3 | R2 | 加权 → 单次 → G3a → — | 拒绝 × 具体性 × 说服力 | OpenAI 在 GPT-5.4 前已替换 | [链接](https://arxiv.org/abs/2402.10260) |
| 222 | AgentDojo | 1 | J1b | O4 | S1 | R1 | 单信号 → 单次 → G3a → — |   | 2026 年头部模型卡中未见引用 | [链接](https://agentdojo.spylab.ai/) |

#### 情感/心理健康/写作（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 223 | WritingBench | 1 | J3 | O3 | S2 | R2 | 比例 → 单次 → G3a → — | 7B 评分模型按 5 条题专属标准打分 | 2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2503.05244) |

#### 偏好竞技场/真实使用（3）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 224 | AlpacaEval 2 LC | 3 | J2 | O3 | S4 | R4 | 单信号 → 单次 → G3c → — | 长度控制胜率 | 2026 年头部模型卡中未见引用 | [链接](https://github.com/tatsu-lab/alpaca_eval) |
| 225 | Arena-Hard v2 | 3 | J2 | O3 | S4 | R4 | 加权 → 单次 → G3c → — | 强胜记 3 场；换位判两次 | 2026 年头部模型卡中未见引用 | [链接](https://github.com/lmarena/arena-hard-auto) |
| 226 | WildBench | 3\|1 | J2 | O3 | S4\|S2 | R4\|R2 | 单信号 → 单次 → G3c\|G3a → — |   | 2026 年头部模型卡中未见引用 | [链接](https://arxiv.org/abs/2406.04770) |

#### 聚合指数（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 227 | ONEBench | 3（指数） | 继承 | 继承 | 继承 | 继承 | 继承 → 继承 → 继承 → G4c | 样本级排序用 Plackett–Luce 合成 | ACL 2025 论文 | [链接](https://arxiv.org/abs/2412.06745) |

## 评分不可核实（9 行）

#### 代码/软件工程（3）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 228 | CursorBench 4.0 | — | J2 | O3 | 未公开 | 未公开 | 未公开 → 单次 → G3a → — | 代理式评分器，细则未公开 | ANT-O55、xAI-4.7 | [链接](https://www.anthropic.com/claude-opus-5-5) |
| 229 | Kimi Code Bench 2.0 / Z.ai Code Bench | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 未公开 → 未公开 → — |   | Kimi-K3、GLM-5.3 | [链接](https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md) |
| 230 | QwenSWEBench / QwenQoderBench / CoWorkBench / WorkSpaceBench（Qwen 内部） | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 平均 → 未公开 → — | 只知道 avg@3 / avg@5 | Qwen3.8、Seed2.1（Workspace Bench） | [链接](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8) |

#### 代理/经营/博弈（2）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 231 | Agentic IF Index（Meta） | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 未公开 → 未公开 → — |   | Meta-MS1.3 | [链接](https://dev.meta.ai/models/muse-spark) |
| 232 | Seed 内部：Agent Startup Bench / xDailyBench | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 未公开 → 未公开 → — |   | Seed2.1 | [链接](https://seed.bytedance.com/en/seed2_1) |

#### 多模态理解（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 233 | PerceptionBench（Kimi） | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 未公开 → 未公开 → — |   | Kimi-K3、Qwen3.8 | [链接](https://huggingface.co/moonshotai/Kimi-K3/blob/main/README.md) |

#### 视频理解（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 234 | TOMATO / Minerva / VideoSimpleQA / MMLongBench-128K（Seed2.1 报告引用） | — | 不详 | 不详 | 不详 | 不详 | 不详 → 不详 → 不详 → — | 有公开论文，厂商报分时用的设置和判法没有说明 | Seed2.1 | [链接](https://seed.bytedance.com/en/seed2_1) |

#### 安全与诚实（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 235 | LatchBio BioSecBench-Refusal / Capabilities v1.0 | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 未公开 → G3a → G4b | 只知道 Capabilities 是 11 个子项等权平均 | xAI-4.7 | [链接](https://latch.bio/biosecbench-refusal) |

#### 网络安全（1）

| 编号 | 名称 | 入口类 | J | O | S | R | G1 → G2 → G3 → G4 | 怎么出分 | 使用方 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| 236 | HackerBench v0.3 | — | 未公开 | 未公开 | 未公开 | 未公开 | 未公开 → 未公开 → G3a → — | 只知道报有害配合率和良性拒答率 | xAI-4.7 | [链接](https://x.ai/news/grok-4-7) |
