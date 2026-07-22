#!/usr/bin/env python3
"""
Splices the generated tree paths into index.html at the <!--T:NAME--> markers.

This is a one-time generator, not a build step: it writes the paths straight
into index.html, and the committed index.html is what ships. Re-run it only if
you regenerate the artwork with gen_tree.py.

  python3 tools/gen_tree.py && python3 tools/inline_tree.py
"""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
TREE = os.path.join(ROOT, "assets", "tree")
HTML = os.path.join(ROOT, "index.html")

frag = open(os.path.join(TREE, "_inline.txt")).read()

# _inline.txt is emitted in labelled blocks by gen_tree.py
blocks = {}
cur = None
for line in frag.splitlines():
    m = re.match(r"<!--\s*(\w+)\s*-->", line.strip())
    if m:
        cur = m.group(1)
        blocks[cur] = []
    elif cur and line.strip():
        blocks[cur].append(line.strip())

# SEED holds both the seed loop and its sprout
parts = {
    "WAVES": blocks.get("WAVES", []),
    "ROOTS": blocks.get("ROOTS", []),
    "TRUNK": blocks.get("TRUNK", []),
    "CANOPY": blocks.get("CANOPY", []),
    "SEED": blocks.get("SEED", []),
}

html = open(HTML, encoding="utf-8").read()
for name, paths in parts.items():
    if not paths:
        raise SystemExit("no paths found for %s — run gen_tree.py first" % name)
    body = "\n" + "\n".join(paths) + "\n"
    marker = "<!--T:%s-->" % name
    pattern = re.compile(
        r"<!--T:%s-->.*?(?=</svg>)" % name, re.S
    )
    if marker not in html:
        raise SystemExit("marker %s missing from index.html" % marker)
    html = pattern.sub(marker + body, html, count=1)

open(HTML, "w", encoding="utf-8").write(html)
print("inlined:", ", ".join("%s=%d" % (k, len(v)) for k, v in parts.items()))
print("index.html now %.1f KB" % (os.path.getsize(HTML) / 1024))
