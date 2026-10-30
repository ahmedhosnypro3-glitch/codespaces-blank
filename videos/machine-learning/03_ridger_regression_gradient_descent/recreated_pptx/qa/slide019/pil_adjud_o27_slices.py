#!/usr/bin/env python3
"""O27 probe 4 — slide_019 original: horizontal color-slice census across the
whole table at key rows (norm-label row, W-entry rows, test-grid rows)."""
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

def slice_runs(y, tag, x0=60, x1=900, minlen=3):
    """print color runs along row y"""
    runs = []
    cur, start = None, x0
    for x in range(x0, x1):
        c = cls(orig[y, x])
        if c != cur:
            if cur is not None and x - start >= minlen:
                runs.append((start, x, cur))
            cur, start = c, x
    if cur is not None and x1 - start >= minlen:
        runs.append((start, x1, cur))
    print(f"--- y={y} {tag}: " + "  ".join(f"x{a}..{b}:{c}" for a, b, c in runs if c != "."))

def cell_runs(y0, y1, x0, x1, tag):
    """dominant ink color inside a cell"""
    h = {}
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = cls(orig[y, x])
            h[c] = h.get(c, 0) + 1
    print(f"{tag:52s} {h}")

print("############ ROW SLICES (runs of length>=3, '.' suppressed) ############")
# g1 norm-label row (build: y273..289) — sample y281 (mid-text)
slice_runs(281, "g1 norm-label row")
# g2 norm-label row (y376..394)
slice_runs(384, "g2 norm-label row")
# g3 norm-label row (y486..504)
slice_runs(494, "g3 norm-label row")

print("\n############ CELL COLORS: norm label '||W||^2' per column/group ############")
# build: norm label textBox(x0+6, gy+68, 76, 16) -> y gy+68..gy+84
for cname, x0 in [("NOREG", 124), ("RIDGE3", 384), ("RIDGE10", 644)]:
    for gi, gy in enumerate([205, 310, 420]):
        cell_runs(gy+69, gy+83, x0+8, x0+80, f"{cname} g{gi+1} norm label cell")

print("\n############ CELL COLORS: W entries per column/group ############")
for cname, x0 in [("NOREG", 124), ("RIDGE3", 384), ("RIDGE10", 644)]:
    for gi, gy in enumerate([205, 310, 420]):
        cell_runs(gy+8, gy+60, x0+47, x0+68, f"{cname} g{gi+1} W entries cell")

print("\n############ W= LABEL: raw px samples (W glyph vs '=') ############")
# NOREG g1: label at x0+16..x0+37, y gy+22..gy+38 (build). orig?
for cname, x0 in [("NOREG", 124), ("RIDGE3", 384)]:
    for gi, gy in enumerate([205, 310, 420]):
        cell_runs(gy+23, gy+37, x0+17, x0+36, f"{cname} g{gi+1} W-label cell")
        # sample the exact W glyph pixels
        sub = orig[gy+23:gy+37, x0+17:x0+36]
        px = sub.reshape(-1, 3)
        ink = px[(px.min(axis=1) < 220)]
        if len(ink):
            print(f"  {cname} g{gi+1} W-label ink mean RGB = {tuple(ink.mean(axis=0).astype(int))}")
