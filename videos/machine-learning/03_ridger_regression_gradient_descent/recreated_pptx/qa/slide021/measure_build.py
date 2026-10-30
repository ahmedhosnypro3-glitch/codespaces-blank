#!/usr/bin/env python3
"""measure_build.py — consolidated BUILD probe for slide 021.

Everything the build script needs, in frame px (960x540, 1px=1pt=1/72in):
  A. panel blue outline spans (left/right/top/bottom per panel)
  B. all five arrows: bbox + 1px ASCII class map
  C. per-cell digit ink ASCII maps for all 27 table cells (3x3 x 3 tables)
  D. chain element tight bboxes (x-clusters per color class)
  E. yellow highlight band rects (bright-yellow mask, per middle-table cell)
Banked output: measure_build_out.txt
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

red = (r > 100) & (r - g > 60) & (r - b > 60)
blue = (b > 120) & (b - r > 60) & (b - g > 60)
green = (g > 100) & (g - r > 50) & (g - b > 50)
dark = (r < 110) & (g < 110) & (b < 110)
bright_yellow = (r > 230) & (g > 230) & (b < 190) & (b > 100)
ink_lt = (r < 215) | (g < 215) | (b < 215)


def runs(vec):
    out = []
    s = None
    for i, v in enumerate(vec):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(vec) - 1))
    return out


def cls(x, y):
    if dark[y, x]:
        return "#"
    if blue[y, x]:
        return "B"
    if red[y, x]:
        return "R"
    if green[y, x]:
        return "G"
    if ink_lt[y, x]:
        return "+"
    return "."


print("=== A. PANEL BLUE OUTLINE ===")
# vertical blue runs over the whole frame
for x in range(60, 910):
    rr = runs(blue[:, x])
    longr = [(s, e) for (s, e) in rr if e - s >= 25]
    if longr:
        pts = [tuple(a[y, x]) for (s, e) in longr for y in range(s, e + 1, 8)]
        print(f" vline x={x}: {longr} core~{pts[len(pts)//2]}")
print(" -- horizontal blue runs --")
for y in range(40, 540):
    rr = runs(blue[y, :])
    longr = [(s, e) for (s, e) in rr if e - s >= 25]
    if longr:
        pts = [tuple(a[y, x]) for (s, e) in longr for x in range(s, e + 1, 40)]
        print(f" hline y={y}: {longr} core~{pts[len(pts)//2]}")

print("\n=== B. ARROWS (bbox + map) ===")
ARROWS = {
    "top arrow1": (455, 485, 190, 212),
    "top arrow2": (655, 685, 190, 212),
    "mid arrow1": (482, 512, 355, 380),
    "mid arrow2": (720, 750, 355, 380),
    "bottom arrow": (355, 395, 468, 492),
}
for name, (x0, x1, y0, y1) in ARROWS.items():
    m = blue[y0:y1, x0:x1] | dark[y0:y1, x0:x1]
    if not m.any():
        print(f" {name}: EMPTY")
        continue
    ys, xs = np.where(m)
    print(f" {name}: bbox x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
    for y in range(ys.min() + y0, ys.max() + y0 + 1):
        print(f"   {y}: {x0:3d} " + "".join(cls(x, y) for x in range(x0, x1)))

print("\n=== C. TABLE CELL DIGIT MAPS ===")
TABLES = {
    "top": (98, 166, 234, 302, 174, 191, 209, 226),
    "mid": (90, 158, 226, 294, 342, 360, 377, 395),
    "bot": (422, 490, 558, 625, 458, 475, 493, 511),
}
CELLCONTENT = {}
for tname, (c0, c1, c2, c3, r0, r1, r2, r3) in TABLES.items():
    cols = [c0, c1, c2, c3]
    rows = [r0, r1, r2, r3]
    for ri in range(3):
        for ci in range(3):
            x0, x1 = cols[ci], cols[ci + 1]
            y0, y1 = rows[ri], rows[ri + 1]
            sub = dark[y0:y1, x0:x1] | ink_lt[y0:y1, x0:x1]
            # tight crop around cell ink
            colany = sub.any(axis=0)
            rowany = sub.any(axis=1)
            xs2 = np.where(colany)[0]
            ys2 = np.where(rowany)[0]
            if not len(xs2):
                print(f" {tname} r{ri+1}c{ci+1}: EMPTY")
                continue
            xa, xb = xs2.min(), xs2.max()
            ya, yb = ys2.min(), ys2.max()
            print(f" {tname} r{ri+1}c{ci+1}: cell x{x0}..{x1} y{y0}..{y1} "
                  f"ink x{x0+xa}..{x0+xb} y{y0+ya}..{y0+yb} (adv {xb-xa+1})")
            for y in range(y0 + ya, y0 + yb + 1):
                print(f"    {y}: " + "".join(cls(x, y) for x in range(x0 + xa, x0 + xb + 1)))

print("\n=== D. CHAIN ELEMENTS (per-class x-clusters, per band) ===")
CHAINS = {
    "top chain": (330, 810, 183, 215),
    "mid chain": (330, 890, 354, 386),
}
for name, (x0, x1, y0, y1) in CHAINS.items():
    for cname, mask in (("red", red), ("dark", dark), ("blue", blue), ("green", green)):
        m = mask[y0:y1, x0:x1]
        if not m.any():
            continue
        cols = np.where(m.any(axis=0))[0]
        cl = []
        s = cols[0]
        p = cols[0]
        for x in cols[1:]:
            if x - p > 4:
                cl.append((s + x0, p + x0))
                s = x
            p = x
        cl.append((s + x0, p + x0))
        ys = np.where(m.any(axis=1))[0]
        print(f" {name} {cname}: y {ys.min()+y0}..{ys.max()+y0} x clusters {cl}")

print("\n=== E. YELLOW HIGHLIGHT BANDS ===")
my = bright_yellow[335:400, 85:300]
ys, xs = np.where(my)
if len(ys):
    print(f" bright-yellow bbox x {xs.min()+85}..{xs.max()+85} y {ys.min()+335}..{ys.max()+335}")
    for y in range(ys.min() + 335, ys.max() + 336):
        rr = runs(bright_yellow[y, 85:300])
        if rr:
            print(f"  y={y}: {[(s+85, e+85) for s, e in rr]}")

print("\n=== F. PANEL-INTERIOR WHITE CHECK (sample points) ===")
for (x, y) in [(300, 150), (300, 400), (700, 480), (150, 145), (150, 300), (500, 500)]:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")
