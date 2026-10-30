#!/usr/bin/env python3
"""PIL-first adjudication of crop_18 header_strip MAJORs + D3 replacement finding.

Checks, orig (slide_019.jpg 960x540) vs render_18.png (2001x1125, 2.0843x):
  1. header text ink color per column (blue-prefix+red-tail vs all-red)
  2. header box fill tints per column
  3. background fill inside the W-matrix/label zone (orig white vs render gray?)
"""
from PIL import Image
import os

os.chdir("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")

o = Image.open("unique_slides/slide_019.jpg").convert("RGB")
r = Image.open("recreated_pptx/qa/slide019/render_18.png").convert("RGB")
S = r.size[0] / o.size[0]
op, rp = o.load(), r.load()

def ink_stats_orig(x0, x1, y0, y1):
    """classify non-bg ink in orig crop: red-ish vs blue-ish px + x-spans."""
    reds, blues, other = [], [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            R, G, B = op[x, y]
            if R > 150 and G < 110 and B < 110:
                reds.append(x)
            elif B > 120 and R < 120 and G < 120:
                blues.append(x)
    return reds, blues

def ink_stats_render(x0, x1, y0, y1):
    reds, blues = [], []
    for y in range(int(y0 * S), int(y1 * S)):
        for x in range(int(x0 * S), int(x1 * S)):
            R, G, B = rp[x, y]
            if R > 150 and G < 110 and B < 110:
                reds.append(x / S)
            elif B > 120 and R < 120 and G < 120:
                blues.append(x / S)
    return reds, blues

def span(v):
    return f"x{min(v):.0f}..{max(v):.0f}" if v else "-"

COLS = [("NO REG", 124, 380), ("RIDGE 3", 384, 640), ("RIDGE 10", 644, 900)]
print("== 1. HEADER TEXT INK (frame y181..200) ==")
for name, x0, x1 in COLS:
    orr, orb = ink_stats_orig(x0, x1, 181, 200)
    rrr, rrb = ink_stats_render(x0, x1, 181, 200)
    print(f"{name:9s} ORIG red {len(orr):4d} px {span(orr)} | blue {len(orb):4d} px {span(orb)}")
    print(f"{name:9s} REND red {len(rrr):4d} px {span(rrr)} | blue {len(rrb):4d} px {span(rrb)}")

print("\n== 2. HEADER BOX FILL (bg census y173..179, away from ink rows) ==")
from collections import Counter
for name, x0, x1 in COLS:
    co = Counter()
    cr = Counter()
    for y in range(173, 180):
        for x in range(x0 + 3, x1 - 3):
            co[op[x, y]] += 1
            cr[rp[int(x * S), int(y * S)]] += 1
    print(f"{name:9s} ORIG top3 {co.most_common(3)}")
    print(f"{name:9s} REND top3 {cr.most_common(3)}")

print("\n== 3. W-ZONE BACKGROUND (label+matrix zone, away from ink) ==")
ZONES = [
    ("NO REG g1 W-zone", 130, 205, 285, 300),
    ("NO REG g2 W-zone", 130, 205, 390, 405),
    ("RIDGE3 g1 W-zone", 390, 465, 285, 300),
    ("RIDGE3 g3 W-zone", 390, 465, 500, 515),
    ("RIDGE10 g1 W-zone", 650, 725, 285, 300),
]
for name, x0, x1, y0, y1 in ZONES:
    co = Counter()
    cr = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            co[op[x, y]] += 1
            cr[rp[int(x * S), int(y * S)]] += 1
    print(f"{name:18s} ORIG {co.most_common(2)} | REND {cr.most_common(2)}")

print("\n== 4. TEST-GRID ZONE BG (render grid area vs orig, e.g. NO REG g1 grid) ==")
for name, x0, x1, y0, y1 in [("NO REG g1 grid", 212, 375, 285, 295),
                             ("RIDGE3 g1 grid", 472, 635, 285, 295)]:
    co = Counter()
    cr = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            co[op[x, y]] += 1
            cr[rp[int(x * S), int(y * S)]] += 1
    print(f"{name:18s} ORIG {co.most_common(2)} | REND {cr.most_common(2)}")
