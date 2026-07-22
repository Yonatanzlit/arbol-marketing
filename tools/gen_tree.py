#!/usr/bin/env python3
"""
Generates the Arbol line-art tree as stroke-based SVG paths.

PLACEHOLDER NOTICE
------------------
The client supplied the logo only as JPG. A raster has no strokes, so it cannot
draw itself in. This script produces a scribble tree in the same construction
language as the logo (continuous tangled loops, calm waves at the ground) so the
site can be built and reviewed now.

It is NOT the client's logo and must be replaced by a proper trace of the
original vector (.ai/.eps/.svg) before launch. The real logo lockups ship
untouched as JPG in the header and footer.

Output: assets/tree/*.svg fragments + a python dict printed for embedding.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "tree")
os.makedirs(OUT, exist_ok=True)

rnd = random.Random(20260721)  # deterministic: same tree on every regeneration


def catmull_rom(pts, closed=True):
    """Smooth a point list into a cubic bezier path string."""
    n = len(pts)
    if closed:
        get = lambda i: pts[i % n]
        rng = range(n)
    else:
        get = lambda i: pts[max(0, min(n - 1, i))]
        rng = range(n - 1)
    d = "M%.1f,%.1f" % (pts[0][0], pts[0][1])
    for i in rng:
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += "C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed:
        d += "Z"
    return d


def loop(cx, cy, rx, ry, wob=0.16, rot=0.0, samples=44):
    """A wobbly, hand-drawn-feeling closed loop."""
    k1, k2 = rnd.choice([2, 3]), rnd.choice([4, 5, 6])
    p1, p2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
    a2 = wob * rnd.uniform(0.35, 0.7)
    pts = []
    for i in range(samples):
        t = 2 * math.pi * i / samples
        m = 1 + wob * math.sin(k1 * t + p1) + a2 * math.sin(k2 * t + p2)
        x, y = rx * m * math.cos(t), ry * m * math.sin(t)
        ca, sa = math.cos(rot), math.sin(rot)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return catmull_rom(pts, closed=True)


def wave(width, cy, amp, periods, samples=None, phase=0.0):
    """A calm ground wave, echoing the logo's baseline."""
    samples = samples or int(periods * 8)
    pts = []
    for i in range(samples + 1):
        t = i / samples
        y = cy + amp * math.sin(2 * math.pi * periods * t + phase) \
              + amp * 0.4 * math.sin(2 * math.pi * periods * 2.3 * t + phase * 1.7)
        pts.append((t * width, y))
    return catmull_rom(pts, closed=False)


# ---------------------------------------------------------------- canopy
# Overlapping loops in three greens. The logo's crown is DENSE — an outer ring
# of big loops alone leaves a hollow centre, so we interleave a second set of
# smaller loops clustered near the middle to fill it.
CANOPY_W, CANOPY_H = 600, 520
canopy = []
CX, CY = CANOPY_W / 2, CANOPY_H / 2

# Outer ring: 11 large loops around the perimeter
for i in range(11):
    ang = 2 * math.pi * i / 11 + rnd.uniform(-0.22, 0.22)
    d = rnd.uniform(0.55, 1.0)
    cx = CX + math.cos(ang) * 74 * d
    cy = CY + math.sin(ang) * 58 * d
    r = rnd.uniform(120, 172)
    canopy.append({
        "d": loop(cx, cy, r, r * rnd.uniform(0.72, 0.92), wob=rnd.uniform(0.12, 0.21),
                  rot=rnd.uniform(0, math.pi)),
        "tone": ["leaf", "mid", "canopy"][i % 3],
        "w": round(rnd.uniform(2.2, 3.4), 1),
    })

# Inner cluster: 9 smaller loops filling the centre
for i in range(9):
    ang = rnd.uniform(0, 2 * math.pi)
    d = rnd.uniform(0.0, 1.0) ** 0.5
    cx = CX + math.cos(ang) * 66 * d
    cy = CY + math.sin(ang) * 52 * d
    r = rnd.uniform(48, 104)
    canopy.append({
        "d": loop(cx, cy, r, r * rnd.uniform(0.7, 0.98), wob=rnd.uniform(0.16, 0.28),
                  rot=rnd.uniform(0, math.pi)),
        "tone": ["canopy", "leaf", "mid"][i % 3],
        "w": round(rnd.uniform(1.8, 2.8), 1),
    })

# ---------------------------------------------------------------- trunk
# The logo's trunk is two near-parallel lines that splay slightly at the base.
TRUNK_W, TRUNK_H = 200, 1000
trunk = []
for side, off in ((-1, 0), (1, 1)):
    pts = []
    for i in range(19):
        t = i / 18
        flare = (t ** 2.6) * 26          # splays outward toward the ground
        sway = math.sin(t * 3.1 + off) * 4.5
        pts.append((TRUNK_W / 2 + side * (7 + flare) + sway, t * TRUNK_H))
    trunk.append(catmull_rom(pts, closed=False))

# ---------------------------------------------------------------- roots
ROOT_W, ROOT_H = 600, 320
roots = []
for i in range(9):
    side = -1 if i % 2 == 0 else 1
    depth = rnd.uniform(0.42, 1.0)
    spread = rnd.uniform(0.3, 1.0)
    pts = [(ROOT_W / 2, 0)]
    steps = 7
    for s in range(1, steps + 1):
        t = s / steps
        x = ROOT_W / 2 + side * (t ** 1.35) * 250 * spread + math.sin(t * 5 + i) * 12
        y = (t ** 0.78) * ROOT_H * depth
        pts.append((x, y))
    roots.append({"d": catmull_rom(pts, closed=False),
                  "tone": ["canopy", "brand", "mid"][i % 3],
                  "w": round(2.6 - 1.1 * (i / 9), 1)})

# ---------------------------------------------------------------- ground waves
waves = []
for i, (amp, per, ph) in enumerate([(16, 2.6, 0.0), (12, 3.7, 1.1), (9, 2.0, 2.3)]):
    waves.append({"d": wave(1200, 30, amp, per, phase=ph),
                  "tone": ["leaf", "mid", "canopy"][i],
                  "w": [2.5, 2.0, 1.5][i]})

# ---------------------------------------------------------------- seed
seed = loop(300, 40, 17, 22, wob=0.07, rot=0.15)
sprout = catmull_rom([(300, 24), (299, 6), (303, -14), (300, -34)], closed=False)


def svg(name, viewbox, body, extra=""):
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" fill="none" '
         'stroke-linecap="round" stroke-linejoin="round" %s>\n%s\n</svg>\n'
         % (viewbox, extra, body))
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(s)
    return s


TONES = {"leaf": "#7CC01F", "mid": "#689F1E", "canopy": "#375B29", "brand": "#00690C"}

svg("canopy", "0 0 %d %d" % (CANOPY_W, CANOPY_H),
    "\n".join('<path d="%s" stroke="%s" stroke-width="%s" pathLength="1"/>'
              % (p["d"], TONES[p["tone"]], p["w"]) for p in canopy))
svg("trunk", "0 0 %d %d" % (TRUNK_W, TRUNK_H),
    "\n".join('<path d="%s" stroke="#375B29" stroke-width="3" pathLength="1"/>' % d for d in trunk))
svg("roots", "0 0 %d %d" % (ROOT_W, ROOT_H),
    "\n".join('<path d="%s" stroke="%s" stroke-width="%s" pathLength="1"/>'
              % (p["d"], TONES[p["tone"]], p["w"]) for p in roots))
svg("waves", "0 0 1200 60",
    "\n".join('<path d="%s" stroke="%s" stroke-width="%s" pathLength="1"/>'
              % (p["d"], TONES[p["tone"]], p["w"]) for p in waves))

# Emit an HTML-ready fragment file for pasting inline into index.html
with open(os.path.join(OUT, "_inline.txt"), "w") as f:
    f.write("<!-- CANOPY -->\n")
    for p in canopy:
        f.write('<path class="cp" d="%s" stroke="var(--%s)" stroke-width="%s" pathLength="1"/>\n'
                % (p["d"], p["tone"], p["w"]))
    f.write("\n<!-- TRUNK -->\n")
    for d in trunk:
        f.write('<path class="tk" d="%s" stroke="var(--canopy)" stroke-width="3" pathLength="1"/>\n' % d)
    f.write("\n<!-- ROOTS -->\n")
    for p in roots:
        f.write('<path class="rt" d="%s" stroke="var(--%s)" stroke-width="%s" pathLength="1"/>\n'
                % (p["d"], p["tone"], p["w"]))
    f.write("\n<!-- WAVES -->\n")
    for p in waves:
        f.write('<path class="wv" d="%s" stroke="var(--%s)" stroke-width="%s" pathLength="1"/>\n'
                % (p["d"], p["tone"], p["w"]))
    f.write("\n<!-- SEED -->\n")
    f.write('<path class="sd" d="%s" stroke="var(--brand)" stroke-width="2.4" pathLength="1"/>\n' % seed)
    f.write('<path class="sp" d="%s" stroke="var(--brand)" stroke-width="2.2" pathLength="1"/>\n' % sprout)

print("wrote", OUT)
print("canopy paths:", len(canopy), "| trunk:", len(trunk), "| roots:", len(roots), "| waves:", len(waves))
