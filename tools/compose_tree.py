#!/usr/bin/env python3
"""
Composes the four generated fragments into ONE complete tree and splices it
into index.html at the <!--T:TREE--> marker.

The earlier layout cut the tree into pieces — waves in §1, roots in §2, trunk
in §3, crown in §4 — so it was only ever seen a slice at a time. The client
asked for the whole logo, uncut, sitting in the background and drifting behind
the copy as you scroll. That means a single assembled tree in one viewBox.

Layout, in a 900 × 1500 viewBox (same proportions as the vertical lockup):

      y    0 ┌──────────────┐
             │    crown     │   canopy fragment, 600×520
         640 ├──────────────┤
             │    trunk     │   trunk fragment, squeezed to 100 wide
        1080 ├── ground ────┤   waves fragment, full width
             │    roots     │   roots fragment
        1440 └──────────────┘

  python3 tools/gen_tree.py && python3 tools/compose_tree.py
"""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
TREE = os.path.join(ROOT, "assets", "tree")
HTML = os.path.join(ROOT, "index.html")

# --- read the generated fragments ------------------------------------------
frag = open(os.path.join(TREE, "_inline.txt"), encoding="utf-8").read()
blocks, cur = {}, None
for line in frag.splitlines():
    m = re.match(r"<!--\s*(\w+)\s*-->", line.strip())
    if m:
        cur = m.group(1)
        blocks[cur] = []
    elif cur and line.strip():
        blocks[cur].append(line.strip())

for need in ("CANOPY", "TRUNK", "WAVES", "ROOTS"):
    if not blocks.get(need):
        raise SystemExit("missing %s — run tools/gen_tree.py first" % need)

# --- place each fragment ----------------------------------------------------
# scale x, scale y, translate x, translate y  (applied as translate then scale)
PLACE = {
    #            tx     ty     sx     sy
    "CANOPY": (150, 100, 1.00, 1.00),   # 600×520  -> x 150..750,  y 100..620
    "TRUNK":  (400, 610, 0.50, 0.48),   # 200×1000 -> x 400..500,  y 610..1090
    "WAVES":  (0, 1055, 0.75, 1.00),   # 1200×60  -> x 0..900,    y 1055..1115
    "ROOTS":  (120, 1090, 1.10, 0.95),   # 600×320  -> x 120..780,  y 1090..1394
}
ORDER = ["ROOTS", "WAVES", "TRUNK", "CANOPY"]   # crown paints last, on top

out = []
for name in ORDER:
    tx, ty, sx, sy = PLACE[name]
    out.append('<g class="t-%s" transform="translate(%s %s) scale(%s %s)">'
               % (name.lower(), tx, ty, sx, sy))
    out.extend(blocks[name])
    out.append("</g>")

body = "\n" + "\n".join(out) + "\n"

html = open(HTML, encoding="utf-8").read()
if "<!--T:TREE-->" not in html:
    raise SystemExit("marker <!--T:TREE--> missing from index.html")
html = re.sub(r"<!--T:TREE-->.*?(?=</svg>)", "<!--T:TREE-->" + body, html, count=1, flags=re.S)
open(HTML, "w", encoding="utf-8").write(html)

print("composed one complete tree: " +
      ", ".join("%s=%d" % (n, len(blocks[n])) for n in ORDER))
print("index.html now %.1f KB" % (os.path.getsize(HTML) / 1024))
