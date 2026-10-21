# 数学分析 · 上册预习讲义

**在线版**：https://lugabeeee.github.io/math-analysis-preview/

写给数学系大一新生的《数学分析》上册预习讲义，按**华东师范大学数学科学学院编《数学分析》第六版（上册）**的章节顺序编排。

## 特点

- **单文件、完全离线**：整本讲义是一个 `index.html`，公式用 MathJax 矢量渲染、内联在文件里，断网也能正常阅读。
- **预习 + 正式内容并存**：每章开头「课前 3 问」→ 本章地图 → 定义与白话解释 → 交互实验 → 证明与例题 → 章末自测。左下角可切「只看预习线」。
- **11 个可拖动交互实验**：上确界、ε-N、ε-δ、一致连续、间断点四型、夹逼、割线→切线、Taylor 逼近、二分法、Riemann 和、p 积分。纯 Canvas 手写，无外部依赖。
- **每个实验都能「自动演示」**：点标题栏 `▶`，参数往返动画，滑块实时跟着动；支持全屏放大。
- **跟随主题**：切换深色/浅色时所有画布自动重绘。
- **5 段讲解动画**（ManimGX 渲染，base64 内联）：ε-N、ε-δ、割线→切线、拉格朗日中值定理、Riemann 和。同样是单文件、断网可播。
- **一页速览**：全学期十二件事的骨架表，5 分钟建立全局。
- **Ctrl+K 全文搜索**：按定义名、定理名、小节标题、题目快速跳转，本地索引、离线可用。
- **点选判分**：每章 1 道选择题 + 附录 B 8 道判断，点选立刻判对错并给解析，结果存在本地。
- **附录**：A 公式速查、B 二十题综合自测（答案折叠）、C 十六周学习路线。

## 目录

| 节 | 内容 |
|---|---|
| ★ | 一页速览 · 全书骨架（最前面，5 分钟建立全局） |
| 00 | 导言 · 数学的语言 |
| 01 | 实数与函数 |
| 02 | 数列极限 |
| 03 | 函数极限 |
| 04 | 函数的连续性 |
| 05 | 导数与微分 |
| 06 | 微分中值定理 |
| 07 | 实数的完备性 |
| 08 | 不定积分 |
| 09 | 定积分 |
| 10 | 定积分的应用 |
| 11 | 反常积分 |
| A / B / C | 公式速查 / 综合自测 / 学习路线 |

## 目录结构

```
videos/*.mp4         讲解动画（base64 内联进 index.html）
engine/mathlab.js    交互实验引擎（框架层，与内容无关，可搬到别的页面）
engine/mathlab.css   实验外观
src/labs.js          本书 11 个实验定义（MathLab.absorb）
src/shell.html       页面模板：{{CONTENT}} {{ENGINE_CSS}} {{ENGINE_JS}} {{LABS_JS}}
src/*.html           各章节与附录
buildlib.py          组装 + 构建期编号
build.py             生成 index.html
make_sample.py       抽出单章样张
```

## 两个产物

| 文件 | 大小 | 视频 | 用途 |
|---|---|---|---|
| `index.html` | 2.2 MB | `videos/` 外链，即点即播 | 在线版 / GitHub Pages |
| `index-offline.html` | 2.6 MB | base64 内联 | 断网、U 盘、单文件传阅 |

视频默认折叠成一行「▶ 看动画」，不占版面。

## 重新构建

```bash
# 依赖：Python 3；MathJax 在 assets/tex-svg.js（如需更新，从 cdn.jsdelivr.net 下载）
python3 build.py             # 同时生成 index.html 与 index-offline.html
python3 make_sample.py ch2   # 可选：单章样张

# 动画（在工作区根目录，需 .runtime/venv）
.runtime/venv/bin/python manimx/render.py            # 下册先导三片
# 上册五片见 manimx/scenes_analysis.py，用 manimgx render 逐段出片后放进 videos/
```

编号在构建期写入，不依赖 CSS counter；引擎与实验定义分别内联，最终仍是单文件。

## 抓取与隐私

页面带 `<meta name="robots" content="noindex, nofollow, noarchive">`，仓库根目录有 `robots.txt`（`Disallow: /`）：
链接可以正常分享和访问，但主流搜索引擎不会收录。若要彻底下线，删掉 GitHub Pages 的发布源即可。

## 说明

内容为个人预习整理，不替代教材、课堂与老师讲义。若有笔误欢迎提 issue。
