#!/usr/bin/env python3
"""S20c prephase PIL forensics for slide 034 frame: plot marker inventory,
curve/label band colors, eq-box border cross-check. Banked evidence for
delta_vs_related.md row 9 (vision-pending items PIL can settle)."""
import numpy as np
from PIL import Image

F = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

print("== 1. 034 plot interior x610..843 y61..311: color census ==")
reg = im[61:311, 610:843]
counts, samples = {}, {}
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        v = max(r, g, b)
        if v >= 200:
            continue
        if r > 120 and g < 90 and b < 90:
            key = "red"
        elif g > 120 and g > r + 30 and g > b + 30:
            key = "green"
        elif b > 120 and b > r + 30 and b > g + 20:
            key = "blue"
        elif 120 < r < 220 and 140 < g < 230 and b > 180 and b > r:
            key = "teal/cyan"
        elif abs(r-g) < 25 and abs(g-b) < 25:
            key = "gray/dark"
        elif r > 150 and 90 < g < 160 and b < 110:
            key = "orange"
        elif r > 150 and g < 110 and b > 110:
            key = "pink/magenta"
        else:
            key = "other"
        counts[key] = counts.get(key, 0) + 1
        samples.setdefault(key, (610 + xx, 61 + yy, (int(r), int(g), int(b))))
for k in sorted(counts, key=counts.get, reverse=True):
    print(f"  {k:12s} n={counts[k]:6d} first={samples[k]}")

print("== 2. red blobs (candidate dots) in plot interior: connected-ish clusters ==")
redmask = (im[:, :, 0] > 130) & (im[:, :, 1] < 95) & (im[:, :, 2] < 95)
reg_red = redmask[61:311, 610:843]
ys, xs = np.nonzero(reg_red)
print(f"  red px n={len(xs)}")
if len(xs):
    pts = sorted(zip((xs + 610).tolist(), (ys + 61).tolist()))
    # crude cluster by x gap
    clusters, cur = [], [pts[0]]
    for p in pts[1:]:
        if p[0] - cur[-1][0] <= 6:
            cur.append(p)
        else:
            clusters.append(cur); cur = [p]
    clusters.append(cur)
    for c in clusters:
        cxs = [p[0] for p in c]; cys = [p[1] for p in c]
        print(f"  cluster n={len(c):4d} x{min(cxs)}..{max(cxs)} y{min(cys)}..{max(cys)}")

print("== 3. teal curve column profile (teal px per column, x610..843) ==")
tealmask = (im[:, :, 2] > 150) & (im[:, :, 1] > 140) & (im[:, :, 0] < 190) & (im[:, :, 2] > im[:, :, 0] + 20)
prof = []
for xx in range(610, 843):
    n = int(tealmask[61:311, xx].sum())
    if n:
        prof.append((xx, n))
if prof:
    print(f"  teal columns x{prof[0][0]}..{prof[-1][0]} count={len(prof)} peak={max(prof, key=lambda t: t[1])}")
    print("  sample:", prof[:6], "...", prof[-4:])
else:
    print("  no teal found in 610..843")

print("== 4. label band below plot x600..900 y315..360: text color census ==")
reg = im[315:360, 600:900]
counts, samples = {}, {}
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if max(r, g, b) >= 200:
            continue
        if r > 150 and g < 120 and b > 120:
            key = "pink/magenta"
        elif r > 120 and g < 95 and b < 95:
            key = "red"
        elif abs(r-g) < 25 and abs(g-b) < 25:
            key = "gray/dark"
        else:
            key = "other"
        counts[key] = counts.get(key, 0) + 1
        samples.setdefault(key, (600 + xx, 315 + yy, (int(r), int(g), int(b))))
for k in sorted(counts, key=counts.get, reverse=True):
    print(f"  {k:12s} n={counts[k]:6d} first={samples[k]}")

print("== 5. orange arrow hunt x600..900 y60..320 ==")
reg = im[60:320, 600:900]
hits = [(600+xx, 60+yy, (int(r), int(g), int(b)))
        for yy in range(reg.shape[0]) for xx in range(reg.shape[1])
        if reg[yy, xx][0] > 190 and 90 < reg[yy, xx][1] < 170 and reg[yy, xx][2] < 110]
print(f"  orange px n={len(hits)}" + (f" bbox x{min(p[0] for p in hits)}..{max(p[0] for p in hits)} y{min(p[1] for p in hits)}..{max(p[1] for p in hits)} e.g. {hits[:3]}" if hits else ""))

print("== 6. eq box re-pin (034): red border rows/cols in x460..612 y160..225 ==")
reg = im[160:225, 460:612]
rows = {}
for yy in range(reg.shape[0]):
    n = sum(1 for xx in range(reg.shape[1]) if reg[yy, xx][0] > 110 and reg[yy, xx][1] < 90 and reg[yy, xx][2] < 90)
    if n > 30:
        rows[160+yy] = n
cols = {}
for xx in range(reg.shape[1]):
    n = sum(1 for yy in range(reg.shape[0]) if reg[yy, xx][0] > 110 and reg[yy, xx][1] < 90 and reg[yy, xx][2] < 90)
    if n > 20:
        cols[460+xx] = n
print("  border rows:", rows)
print("  border cols:", cols)
