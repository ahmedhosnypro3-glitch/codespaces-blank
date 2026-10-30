#!/usr/bin/env python3
"""measure_yellow.py — decode the middle-table yellow diagonal highlight strokes.

Composite analysis: FDFD96 (253,253,150) is translucent over black digits -> olive.
Reconstruct band geometry + alpha from raw RGB.
"""
from PIL import Image
import numpy as np

F = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)

def probe(x, y, label):
    print(f"  {label} ({x},{y}) = {tuple(a[y, x])}")

print("### raw samples")
# cell r1c1 = x91..157 y342..359 ; digit '17' dark strokes around x120..130 y346..356
probe(100, 350, "cell r1c1 left bg (expected highlight or white)")
probe(140, 345, "cell r1c1 right bg")
probe(123, 350, "cell r1c1 digit stroke area")
probe(147, 350, "cell r1c1 right of band")
probe(300, 300, "panel white bg")
probe(200, 350, "cell r1c2 digit '10' stroke")
probe(160, 350, "cell r1c2 left bg (white expect)")
probe(230, 350, "cell r1c3 bg")
probe(876, 73, "badge fill")
probe(112, 360, "cell r2c1 bg")

print("\n### composite decode: classify each px in cell r1c1")
YL = np.array([253, 253, 150]); BL = np.array([0, 0, 0]); WH = np.array([255, 255, 255])

def decode(x0, x1, y0, y1, label):
    print(f" -- {label} x{x0}..{x1} y{y0}..{y1}")
    print("    legend: Y=solid FDFD96  o=olive(highlighter over black)  #=pure black  g=gridline gray  .=white")
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            px = a[y, x]
            d_yl = np.abs(px - YL).sum(); d_bl = np.abs(px - BL).sum()
            if d_yl < 60: row.append('Y')
            elif d_bl < 60: row.append('#')
            elif px[0] > 235 and px[1] > 235 and px[2] > 235: row.append('.')
            elif abs(px[0] - px[1]) < 12 and abs(px[1] - px[2]) < 25 and px[0] > 140: row.append('g')
            else: row.append('o')
        print(f"    {y:3d} " + ''.join(row))

decode(92, 156, 341, 360, "cell r1c1 (17)")
decode(160, 224, 359, 377, "cell r2c2 (43)")
decode(228, 292, 377, 395, "cell r3c3 (95)")
decode(160, 224, 341, 360, "cell r1c2 (10) — non-highlighted reference")

print("\n### yellow band geometry (yellow-mask bbox per row, full cells)")
yellow = (a[..., 0] > 170) & (a[..., 1] > 170) & (a[..., 2] < 150)
for nm, (x0, x1, y0, y1) in {"r1c1": (91, 157, 342, 359), "r2c2": (159, 225, 360, 377), "r3c3": (227, 293, 377, 395)}.items():
    xs_all = []
    for y in range(y0, y1 + 1):
        rr = [(s + x0, e + x0) for s, e in
              [(lambda v: (int(np.argmax(v)), int(len(v) - np.argmax(v[::-1]))))(yellow[y, x0:x1 + 1])]]
        cols = np.where(yellow[y, x0:x1 + 1])[0]
        if len(cols):
            print(f"  {nm} y={y}: yellow x {cols.min()+x0}..{cols.max()+x0} (n={len(cols)})")
            xs_all.append((y, cols.min() + x0, cols.max() + x0))
    if xs_all:
        print(f"  {nm} BAND: x {min(t[1] for t in xs_all)}..{max(t[2] for t in xs_all)} y {xs_all[0][0]}..{xs_all[-1][0]}")

print("\n### alpha estimate: px on a digit stroke inside highlight vs the same digit outside")
# '1' of '17' in cell r1c1: find darkest-ish px inside highlight
sub = a[344:358, 110:140]
flat = sub.reshape(-1, 3)
srt = flat[np.argsort(flat.sum(axis=1))]
print("  cell r1c1 darkest-6 px:", [tuple(v) for v in srt[:6]])
# reference '1' of '10' in cell r1c2 (x187..198, y346..355)
sub2 = a[344:358, 183:202]
srt2 = sub2.reshape(-1, 3)[np.argsort(sub2.reshape(-1, 3).sum(axis=1))]
print("  cell r1c2 ('10') darkest-6 px:", [tuple(v) for v in srt2[:6]])
# background inside highlight away from digits
print("  highlight purest px (max sum) in r1c1:", tuple(flat[np.argsort(flat.sum(axis=1))][-3:]))
