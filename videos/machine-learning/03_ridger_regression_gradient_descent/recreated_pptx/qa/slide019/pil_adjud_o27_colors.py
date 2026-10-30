#!/usr/bin/env python3
"""O27 probe 3 — slide_019 original: exact ink colors of Test header row, x1/x2
value rows, and ||W||^2 labels (yellow-aware), plus ASCII of two test grids."""
from PIL import Image
import numpy as np

ROOT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(ROOT + "/unique_slides/slide_019.jpg").convert("RGB")).astype(int)

def cls(px):
    r, g, b = px
    if r > 200 and g > 200 and b > 200:
        return "."
    if r > 205 and g > 200 and b <= 200:
        return "y"
    if b > r + 25 and b > g + 15:
        return "B"
    if r > g + 40 and r > b + 40:
        return "R"
    if g > r + 25 and g > b + 25:
        return "G"
    if abs(r - g) < 35 and abs(g - b) < 35:
        return "#"
    return "+"

def amap(x0, x1, y0, y1, tag, ds=1):
    print(f"===== {tag} frame x{x0}..{x1} y{y0}..{y1} (ds={ds}) =====")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, ds))
    print(hdr)
    for yf in range(y0, y1, ds):
        row = []
        for xf in range(x0, x1, ds):
            block = orig[yf:int(yf+ds), int(xf):int(xf+ds)].reshape(-1, 3)
            classes = [cls(px) for px in block]
            order = {"#": 0, "B": 1, "R": 2, "G": 3, "+": 4, "y": 5, ".": 6}
            best = min(classes, key=lambda c: order[c])
            row.append(best if best != "." else ("y" if all(c in ".y" for c in classes) else "."))
        print(f"{yf:4d} " + "".join(row))

def ink_hist(x0, y0, x1, y1, tag):
    h = {}
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = cls(orig[y, x])
            if c not in (".", "y"):
                h[c] = h.get(c, 0) + 1
    print(f"{tag:46s} {h}")

# ── ASCII of the two full test grids, NOREG g1 and RIDGE3 g1
amap(206, 382, 205, 303, "ORIG NOREG g1 test grid")
amap(466, 642, 205, 303, "ORIG RIDGE3 g1 test grid")

# ── norm label per-cell ink (yellow-aware)
for cname, x0 in [("NOREG", 124), ("RIDGE3", 384), ("RIDGE10", 644)]:
    for gi, gy in enumerate([205, 310, 420]):
        ink_hist(x0+6, gy+66, x0+82, gy+86, f"{cname} g{gi+1} '||W||^2' label (y-aware)")

# ── per-COLUMN breakdown of Test headers and x rows (NOREG g1)
v0, gx1 = 124 + 142, 380
colW = (gx1 - v0) / 3
for ti in range(3):
    ink_hist(int(v0+ti*colW), 209, int(v0+(ti+1)*colW), 226, f"NOREG g1 Test header col{ti+1} (x{int(v0+ti*colW)}..{int(v0+(ti+1)*colW)})")
    ink_hist(int(v0+ti*colW), 228, int(v0+(ti+1)*colW), 246, f"NOREG g1 x1 row col{ti+1}")
    ink_hist(int(v0+ti*colW), 247, int(v0+(ti+1)*colW), 266, f"NOREG g1 x2 row col{ti+1}")
    ink_hist(int(v0+ti*colW), 274, int(v0+(ti+1)*colW), 294, f"NOREG g1 y  row col{ti+1}")

# ── RIDGE3 g1 per-column
v0b = 384 + 142
colWb = (640 - v0b) / 3
for ti in range(3):
    ink_hist(int(v0b+ti*colWb), 209, int(v0b+(ti+1)*colWb), 226, f"RIDGE3 g1 Test header col{ti+1}")
    ink_hist(int(v0b+ti*colWb), 228, int(v0b+(ti+1)*colWb), 246, f"RIDGE3 g1 x1 row col{ti+1}")
    ink_hist(int(v0b+ti*colWb), 247, int(v0b+(ti+1)*colWb), 266, f"RIDGE3 g1 x2 row col{ti+1}")

# ── RIDGE10 g1 per-column
v0c = 644 + 142
colWc = (888 - v0c) / 3
for ti in range(3):
    ink_hist(int(v0c+ti*colWc), 209, int(v0c+(ti+1)*colWc), 226, f"RIDGE10 g1 Test header col{ti+1}")
    ink_hist(int(v0c+ti*colWc), 228, int(v0c+(ti+1)*colWc), 246, f"RIDGE10 g1 x1 row col{ti+1}")
    ink_hist(int(v0c+ti*colWc), 247, int(v0c+(ti+1)*colWc), 266, f"RIDGE10 g1 x2 row col{ti+1}")
