#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从全书中抽出一章，生成单章样张（同样完全离线）。用法: python3 make_sample.py ch2"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, ASSETS = os.path.join(ROOT, "src"), os.path.join(ROOT, "assets")
want = sys.argv[1] if len(sys.argv) > 1 else "ch2"

shell = open(os.path.join(SRC, "shell.html"), encoding="utf-8").read()
mathjax = open(os.path.join(ASSETS, "tex-svg.js"), encoding="utf-8").read().replace("</script", "<\\/script")
parts = sorted(glob.glob(os.path.join(SRC, "[0-9]*.html")))
body = "\n".join(open(p, encoding="utf-8").read() for p in parts)

# 取出 hero 和目标章节
hero = re.search(r'<header class="hero">.*?</header>', body, re.S)
sec = re.search(r'<section class="chap" id="%s".*?</section>\s*(?=<section|$)' % want, body, re.S)
if not sec:
    sys.exit("chapter not found: " + want)

body = re.sub(r'class="box (thm|prop|lem|cor)" data-k="([^"]+)"><div class="tag">',
              r'class="box \1"><div class="tag" data-k="\2">', body)

# 编号
NR = re.compile(r'<section class="chap" id="[^"]+"[^>]*data-no="([^"]+)"'
                r'|<div class="box (def|thm|prop|lem|cor|ex)"[^>]*>\s*<div class="tag"(?: data-k="([^"]+)")?>')
def autonumber(html):
    out, pos, ch, cdef, cres, cex = [], 0, "?", 0, 0, 0
    for m in NR.finditer(html):
        out.append(html[pos:m.start()]); pos = m.end()
        if m.group(1) is not None:
            raw = m.group(1); ch = str(int(raw)) if raw.isdigit() else raw
            cdef = cres = cex = 0; out.append(m.group(0)); continue
        kind, label = m.group(2), m.group(3)
        if kind == "def": cdef += 1; txt = f"定义 {ch}.{cdef}"
        elif kind == "ex": cex += 1; txt = f"例 {ch}.{cex}"
        else: cres += 1; txt = f"{label or '定理'} {ch}.{cres}"
        out.append(m.group(0) + f'<span class="num">{txt}</span>\u3000')
    out.append(html[pos:]); return "".join(out)

sample = (hero.group(0) if hero else "") + autonumber(sec.group(0))
out = shell.replace("{{CONTENT}}", sample).replace("{{MATHJAX}}", mathjax)
dst = os.path.join(ROOT, f"样张-{want}.html")
open(dst, "w", encoding="utf-8").write(out)
print("sample ->", dst, f"({len(out)/1048576:.2f} MB)")
