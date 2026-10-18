#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 src/ 下的 shell.html + 各章片段 + MathJax 拼成单文件 index.html（完全离线）。

编号（定义/定理/命题/引理/推论/例）在构建期写死，不依赖 CSS counter。
"""
import glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(ROOT, "assets")

shell = open(os.path.join(SRC, "shell.html"), encoding="utf-8").read()
mathjax = open(os.path.join(ASSETS, "tex-svg.js"), encoding="utf-8").read()

# 内联进 <script> 时唯一需要防的是 </script，替换成 <\/script 在 JS 中语义等价
mathjax = mathjax.replace("</script", "<\\/script")
assert "</script" not in mathjax

parts = sorted(glob.glob(os.path.join(SRC, "[0-9]*.html")) + glob.glob(os.path.join(SRC, "zz-*.html")))
if not parts:
    raise SystemExit("no content parts found")
body = "\n".join(open(p, encoding="utf-8").read() for p in parts)

# 1) 把 data-k 从 .box 挪到 .tag 上（标签词的来源）
body = re.sub(r'class="box (thm|prop|lem|cor)" data-k="([^"]+)"><div class="tag">',
              r'class="box \1"><div class="tag" data-k="\2">', body)

# 2) 构建期编号
NUMBER_RE = re.compile(
    r'<section class="chap" id="[^"]+"[^>]*data-no="([^"]+)"'
    r'|<div class="box (def|thm|prop|lem|cor|ex)"[^>]*>\s*<div class="tag"(?: data-k="([^"]+)")?>'
)


def autonumber(html: str) -> str:
    out, pos = [], 0
    ch, cdef, cres, cex = "?", 0, 0, 0
    for m in NUMBER_RE.finditer(html):
        out.append(html[pos:m.start()])
        pos = m.end()
        if m.group(1) is not None:                      # 新的一章：重置计数
            raw = m.group(1)
            ch = str(int(raw)) if raw.isdigit() else raw
            cdef = cres = cex = 0
            out.append(m.group(0))
            continue
        kind, label = m.group(2), m.group(3)
        if kind == "def":
            cdef += 1
            txt = f"定义 {ch}.{cdef}"
        elif kind == "ex":
            cex += 1
            txt = f"例 {ch}.{cex}"
        else:
            cres += 1
            txt = f"{label or '定理'} {ch}.{cres}"
        out.append(m.group(0) + f'<span class="num">{txt}</span>\u3000')
    out.append(html[pos:])
    return "".join(out)


body = autonumber(body)

out = shell.replace("{{CONTENT}}", body).replace("{{MATHJAX}}", mathjax)
dst = os.path.join(ROOT, "index.html")
open(dst, "w", encoding="utf-8").write(out)

nums = re.findall(r'<span class="num">([^<]+)</span>', out)
print(f"built {dst}  ({len(out)/1048576:.2f} MB)  from {len(parts)} parts")
print("编号:", " | ".join(nums) if nums else "none")
