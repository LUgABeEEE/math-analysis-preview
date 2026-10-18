#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建整本讲义：src/ 内容 + engine/ 引擎 + assets/ MathJax → index.html（单文件、离线）。

编号（定义/定理/命题/引理/推论/例）在构建期写死，不依赖 CSS counter。
"""
import os
import re

import buildlib

parts = buildlib.content_parts()
raw = "\n".join(buildlib.read(p) for p in parts)
body = buildlib.prepare_body(raw)
html = buildlib.assemble(body)

dst = os.path.join(buildlib.ROOT, "index.html")
with open(dst, "w", encoding="utf-8") as f:
    f.write(html)

nums = re.findall(r'<span class="num">([^<]+)</span>', html)
print(f"built {dst}  ({len(html)/1048576:.2f} MB)  from {len(parts)} parts")
print("编号:", " | ".join(nums) if nums else "none")
