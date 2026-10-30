#!/usr/bin/env python3
"""Clean plot-region measurement on slide_034.jpg (frame px, 1px = 1pt).

Scans the right-hand plot region column-by-column and row-by-row so the
geometry is unambiguous. No crops, no offsets.
"""
import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
im = np.asarray(Image.open(f"{BASE}/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

gray = (abs(r - 233) < 18) & (abs(g - 233) < 18) & (abs(b - 231) < 20)
white = (r > 244) & (g > 244) & (b > 244)
dark = (r < 105) & (g < 105) & (b < 105)
red = (r > 95) & (r - g > 45) & (r - b > 20)
pink = (r > 215) & (g < 175) & (b < 200) & (r - g > 45) & (r - b > 25)
blue = (b > 105) & (b - r > 40) & (b - g > 15)

print(f"image {W}x{H}")
print("--- whole-slide colour counts ---")
for nm, m in (("gray", gray), ("white", white), ("dark", dark), ("red", red), ("pink", pink), ("blue", blue)):
    print(f"  {nm:6s} n={int(m.sum())}")

print()
print("=== WHITE region bbox (contiguous, whole slide) ===")
ys, xs = np.where(white)
print(f"  rows {ys.min()}..{ys.max()}  cols {xs.min()}..{xs.max()}  n={white.sum()}")
# per-row white counts for rows 40..330
print()
print("=== per-row white count, rows 40..330 ===")
for y in range(40, 331):
    n = int(white[y].sum())
    if n > 20:
        print(f"  row {y:4d}: white n={n}")

print()
print("=== per-col white count, cols 560..912, rows 40..330 ===")
sub = white[40:330, 560:913]
cs = sub.sum(axis=0)
for i, n in enumerate(cs):
    if n > 40:
        print(f"  col {560+i:4d}: white n={int(n)}")

print()
print("=== DARK column profile in rows 60..320 (n>8 => spine) ===")
sub = dark[60:320, :]
cs = sub.sum(axis=0)
run = []
for i, n in enumerate(cs):
    if n > 8:
        run.append((i, int(n)))
print("  " + " | ".join(f"c{i}:{n}" for i, n in run))

print()
print("=== DARK row profile in cols 600..860 (n>8 => spine) ===")
sub = dark[:, 600:860]
rs = sub.sum(axis=1)
run = []
for i, n in enumerate(rs):
    if n > 8:
        run.append((i, int(n)))
print("  " + " | ".join(f"r{i}:{n}" for i, n in run))

print()
print("=== RED pixel map inside candidate plot box ===")
# candidate: cols 560..912, rows 40..320
R = red[40:320, 560:913]
print(f"  red in rows40..320 cols560..912: n={int(R.sum())}")
ys, xs = np.where(R)
if len(ys):
    print(f"  bbox rows {40+ys.min()}..{40+ys.max()} cols {560+xs.min()}..{560+xs.max()}")
    # histogram of red per column
    percol = R.sum(axis=0)
    nz = [(560+i, int(n)) for i, n in enumerate(percol) if n > 0]
    print("  red by col: " + " ".join(f"{c}:{n}" for c, n in nz[:80]))
print()
print("=== PINK pixel map inside candidate plot box ===")
P = pink[40:320, 560:913]
print(f"  pink n={int(P.sum())}")
ys, xs = np.where(P)
if len(ys):
    print(f"  bbox rows {40+ys.min()}..{40+ys.max()} cols {560+xs.min()}..{560+xs.max()}")

print()
print("=== NON-white NON-gray ('curve/ink') inside rows 40..320, cols 560..912 ===")
ink = ~(white | gray)
I = ink[40:320, 560:913]
percol = I.sum(axis=0)
nz = [(560+i, int(n)) for i, n in enumerate(percol) if n > 0]
print(f"  ink n={int(I.sum())}, cols with ink: {len(nz)}")
print("  per-col counts (first 100): " + " ".join(f"{c}:{n}" for c, n in nz[:100]))
