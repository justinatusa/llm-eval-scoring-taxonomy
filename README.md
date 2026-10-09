# 大模型评测的最后一步：分数是怎么算出来的

模型的输出有了以后，还要经过判对错、合并多次采样、合并多个判官、把一整套题合成一个数这几步，才变成榜单上的那个分数。这几步的选择能让同一个评测的数字差出好几倍。这本小书讲清楚这些步骤：按分数的来路把评测分成三类，单题直接出分、多模型相互比较、其他方式，再讲三类共用的合并方法、一个分数能信多少，最后用这些知识读懂十几个主流榜单。正文里的数值例子都可以用仓库里的脚本复现，附录列出书中涉及的 227 个 bench。

## 目录

| 章 | 主题 | 一句话 |
|---|---|---|
| [引言](book/introduction.md) | 一个分数是怎么来的 | 同一个评测换一种算法，数字可以差好几倍；三种出分方式和全书的读法 |
| [第 1 章](book/chapter1.md) | 单题直接出分 | 程序对答案、把东西跑起来再判、请模型当判官，一道题多条检查和一整套题怎么合成分数 |
| [第 2 章](book/chapter2.md) | 多模型相互比较出分 | 从在线 Elo 到 Bradley–Terry，平局、裁判噪声、长度偏好和配对，以及新模型一来老分就变 |
| [第 3 章](book/chapter3.md) | 其他出分方式 | 对照固定参考产出、换算成人类的量、没有满分的开放量、真实使用数据、跨 bench 合成指数、评测判官本身 |
| [第 4 章](book/chapter4.md) | 三类评测共用的两种合并 | 同一道题跑很多次怎么合（pass@k、pass^k、maj@k、选择器），很多个判官怎么合 |
| [第 5 章](book/chapter5.md) | 一个分数能信多少 | 跑法和用户模拟器、谁决定送什么进来、误差条、分数怎么过期 |
| [第 6 章](book/chapter6.md) | 读懂几个主流榜单 | Artificial Analysis、LMArena、Vals、SEAL、METR、Epoch 等榜单的头条数字各自怎么来 |
| [附录](book/appendix.md) | 书中涉及的 bench | 227 个 bench 按领域列出：怎么判、怎么合成总分、属于哪一类 |

## 数据和脚本

[data/benchmarks.csv](data/benchmarks.csv) 是附录背后的完整数据，共 227 行，每行一个 bench，列出领域、属于哪一类、谁来判、跟什么比、一道题内怎么合、多次采样怎么合、整套题怎么合成总分、是否跨模型拟合、报告的数字、谁在报这个分、发布时间和来源链接。

脚本只用 Python 标准库，固定了随机种子：

```bash
python3 scripts/basics.py        # 采样合并、Elo 与 BT、风格控制、IPS、METR、跨 bench 合并、误差条
python3 scripts/mechanisms.py    # Plackett–Luce、平局模型、合成对局、支配分、Codeforces 换算、判官合并
python3 scripts/build_appendix.py  # 由 data/benchmarks.csv 生成 book/appendix.md
```

正文里写作 "`python3 scripts/basics.py` §3" 的地方，指脚本输出中对应编号的一节。两份输出也保存在 [scripts/basics.out.txt](scripts/basics.out.txt) 和 [scripts/mechanisms.out.txt](scripts/mechanisms.out.txt)。
