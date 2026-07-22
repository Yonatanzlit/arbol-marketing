#!/usr/bin/env python3
"""
Generates 3d/index.html from the flat index.html.

Derived rather than hand-written on purpose: the client's Spanish copy is
copied across byte-for-byte, so the 3D version can never drift from the
approved wording. Re-run after any copy change to the flat site.

  python3 tools/build_3d.py && python3 tools/verify_copy.py --file 3d/index.html

It never writes to index.html — the live flat version is untouched.
"""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(ROOT, "index.html")
DST = os.path.join(ROOT, "3d", "index.html")

h = open(SRC, encoding="utf-8").read()

# --- assets live one level up ----------------------------------------------
h = h.replace('href="assets/', 'href="../assets/')
h = h.replace('src="assets/', 'src="../assets/')

# --- stylesheets: shared base + 3D overrides -------------------------------
h = h.replace(
    '<link rel="stylesheet" href="styles.css?v=1">',
    '<link rel="stylesheet" href="../styles.css?v=1">\n'
    '<link rel="stylesheet" href="overrides.css?v=1">'
)

# --- title / social ---------------------------------------------------------
h = h.replace(
    "<title>Árbol Trade &amp; Marketing | Servicios Corporativos y Trade Marketing</title>",
    "<title>Árbol Trade &amp; Marketing — versión 3D</title>"
)

# --- swap the inline flat SVGs for lightweight <img> fallbacks --------------
# They only ever render when WebGL is unavailable, so there is no reason to
# carry ~50 KB of duplicated path data in this file.
FALLBACK = {
    "seed-art": '<img src="../assets/tree/waves.svg" alt="" class="fb-waves">',
    "roots-art": '<img src="../assets/tree/roots.svg" alt="" class="fb-roots">',
    "trunk-art": '<img src="../assets/tree/trunk.svg" alt="" class="fb-trunk">',
    "canopy-art": '<img src="../assets/tree/canopy.svg" alt="" class="fb-canopy">',
}
for cls, repl in FALLBACK.items():
    h = re.sub(
        r'(<div class="art [^"]*%s[^"]*"[^>]*>).*?(</div>)' % cls,
        lambda m, r=repl: m.group(1) + r + m.group(2),
        h, flags=re.S,
    )

# --- mark sections so the 3D CSS can target them ---------------------------
h = h.replace('class="sect s-', 'class="sect s-3d s-')

# --- the WebGL canvas, behind everything -----------------------------------
h = h.replace(
    '<a class="skip" href="#contenido">',
    '<canvas id="scene" aria-hidden="true"></canvas>\n\n'
    '<a class="skip" href="#contenido">'
)

# --- version switcher -------------------------------------------------------
SWITCH = '''
<nav class="switch" aria-label="Versión del sitio">
  <a href="../">Clásica</a>
  <a href="./" aria-current="page">3D</a>
</nav>
'''
h = h.replace('<script src="script.js?v=1"></script>',
              SWITCH + '<script src="../script.js?v=1"></script>\n'
              '<script type="module" src="scene.js?v=1"></script>')

os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, "w", encoding="utf-8").write(h)
print("wrote 3d/index.html  (%.1f KB, flat version is %.1f KB)"
      % (os.path.getsize(DST) / 1024, os.path.getsize(SRC) / 1024))
