#!/usr/bin/env python3
"""b09 s018: panel rectangle edges (fill + border) in the original."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
o = np.asarray(Image.open(NS + "unique_slides/slide_018.jpg").convert("RGB")).astype(np.int16)

def is_fill(p):
    return abs(p[0] - 218) < 10 and abs(p[1] - 206) < 10 and abs(p[2] - 194) < 10

def is_border(p):
    return abs(p[0] - 210) < 22 and abs(p[1] - 165) < 25 and abs(p[2] - 172) < 25

print("== scan for the pink border on a horizontal line y=120 (x 350..920) ==")
row = [x for x in range(350, 920) if is_border(o[120, x])]
print("  border px:", row[:8], "...", row[-8:] if len(row) > 8 else "")

print("== scan for the pink border on a vertical line x=600 (y 40..230) ==")
col = [y for y in range(40, 230) if is_border(o[y, 600])]
print("  border px:", col[:8], "...", col[-8:] if len(col) > 8 else "")

print("== cream fill extent per row (x 360..910) ==")
for y in (62, 64, 66, 100, 150, 190, 194, 196, 198, 200, 202, 204):
    xs = [x for x in range(350, 930) if is_fill(o[y, x])]
    print(f"  y={y}: {min(xs) if xs else '-'}..{max(xs) if xs else '-'} (n={len(xs)})")

print("== cream fill extent per column (y 55..215) ==")
for x in (368, 372, 400, 600, 800, 880, 884, 888, 892, 896, 900):
    ys = [y for y in range(50, 220) if is_fill(o[y, x])]
    print(f"  x={x}: {min(ys) if ys else '-'}..{max(ys) if ys else '-'} (n={len(ys)})")

print("\n== magenta '1' circle positions (strict magenta, lower band) ==")
mg = (o[:, :, 0] > 100) & (o[:, :, 2] > 90) & (o[:, :, 1] < 85) & (abs(o[:, :, 0] - o[:, :, 2]) < 70)
for x0, x1 in ((360, 420), (450, 530), (540, 615)):
    m = mg[175:212, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"  x{x0}-{x1}: ink x {x0+xs.min()}..{x0+xs.max()} y {175+ys.min()}..{175+ys.max()} n={len(xs)}")
