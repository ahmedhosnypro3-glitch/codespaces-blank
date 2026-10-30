#!/usr/bin/env python3
"""Focused measurements for tables and bottom arrow."""
from PIL import Image
import numpy as np

F = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

ink = (r < 215) | (g < 215) | (b < 215)
dark = (r < 110) & (g < 110) & (b < 110)
blue = (b > 120) & (b - r > 60) & (b - g > 60)
gray = (abs(r - g) < 10) & (abs(r - b) < 10) & (r > 100) & (r < 200)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i-1)); s = None
    if s is not None: out.append((s, len(vec)-1))
    return out

# Table regions with cell boundaries from predecessor
tables = {
    "TOP":  {"x0": 98, "x1": 302, "y0": 174, "y1": 226, "cols": [98, 166, 234, 302], "rows": [174, 191, 209, 226]},
    "MID":  {"x0": 90, "x1": 294, "y0": 342, "y1": 395, "cols": [90, 158, 226, 294], "rows": [342, 360, 377, 395]},
    "BOT":  {"x0": 422, "x1": 625, "y0": 458, "y1": 511, "cols": [422, 490, 558, 625], "rows": [458, 475, 493, 511]},
}

print("=== TABLE GRIDLINES (ink mask) ===")
for name, t in tables.items():
    print(f"\n {name} TABLE x{t['x0']}..{t['x1']} y{t['y0']}..{t['y1']}")
    # Vertical gridlines at col boundaries
    for x in t['cols']:
        col = ink[t['y0']:t['y1']+1, x]
        rr = runs(col)
        long = [(s+t['y0'], e+t['y0']) for s,e in rr if e-s >= 10]
        if long:
            # Use the longest run
            best = max(long, key=lambda se: se[1]-se[0])
            s, e = best
            core_col = tuple(np.median(a[s:e+1, x], axis=0).astype(int))
            print(f"   v-grid x={x}: {long} core {core_col}")
    # Horizontal gridlines at row boundaries
    for y in t['rows']:
        row = ink[y, t['x0']:t['x1']+1]
        rr = runs(row)
        long = [(s+t['x0'], e+t['x0']) for s,e in rr if e-s >= 50]
        if long:
            best = max(long, key=lambda se: se[1]-se[0])
            s, e = best
            core_row = tuple(np.median(a[y, s:e+1], axis=0).astype(int))
            print(f"   h-grid y={y}: {long} core {core_row}")

# Bottom arrow: scan dark pixels in the bottom panel center region
print("\n=== BOTTOM ARROW DETAILED ===")
# Arrow spans from expression end (~x270) to table start (~x422)
# Look at y ~470..490 (vertical center of bottom panel)
for y in range(465, 495):
    row = dark[y, 300:420]
    rr = runs(row)
    if rr:
        print(f" y={y}: dark runs {[(s+300,e+300) for s,e in rr]}")
    row2 = blue[y, 300:420]
    rr2 = runs(row2)
    if rr2:
        print(f" y={y}: BLUE runs {[(s+300,e+300) for s,e in rr2]}")

# Also check the full arrow span using ink
print("\n Full arrow span (ink, y=475..485):")
for y in range(475, 486):
    row = ink[y, 270:420]
    rr = runs(row)
    if rr:
        print(f" y={y}: {[(s+270,e+270) for s,e in rr]}")

# Panel border blue: scan for blue at panel boundaries
print("\n=== PANEL BLUE BORDERS (precise) ===")
for label, y in [("P1 top", 130), ("P1 bot", 230), ("P2 top", 290), ("P2 bot", 395), ("P3 top", 415), ("P3 bot", 520)]:
    row = blue[y, 70:900]
    rr = runs(row)
    long = [(s+70, e+70) for s,e in rr if e-s >= 100]
    if long:
        print(f" {label} y={y}: {long}")

# Left/right vertical borders
for x in [76, 880]:
    print(f"\n x={x} vertical:")
    for y in range(125, 525, 5):
        col = blue[y, max(0,x-2):x+3]
        if col.any():
            print(f"  y={y}: blue")

# Font size estimation: cap height 19px for title (419px wide, 33 chars)
# "Inverse Problem of Singular Matrix" = 33 chars including spaces
# Arial Bold: advance ~0.55em per char. 33 * 0.55 * size = 419 → size ≈ 23pt
# Cap height = 0.716 * size = 19 → size = 26.5pt
# Let's estimate ~24-26pt for title.
# Chain text "Singular Matrix" (15 chars): width 600-462=138px → 138/15/0.55 ≈ 16.7pt
# "Non-Singular Matrix" (19 chars): 680-517=163px → 163/19/0.55 ≈ 15.6pt
# Table digits: '40' height ~15px (rows 193-208 in map) → cap 10px? size ~14pt
# Let's measure digit height more precisely
print("\n=== DIGIT HEIGHT ===")
# Top table r2c2 '40' spans y194..204 in ascii map = 11px cap
# Mid table r2c1 '10' - check
for y in range(360, 378):
    if dark[y, 100:120].any():
        print(f" mid r2c1 ink at y={y}")

# Badge numeral '21' - check font
print("\n=== BADGE NUMERAL ===")
for y in range(56, 92):
    row = dark[y, 857:896]
    rr = runs(row)
    if rr:
        print(f" y={y}: {rr}")