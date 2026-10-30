#!/usr/bin/env python3
"""S20c prephase PIL forensics for slide 031 frame: curve color, plot markers,
dashed guide, arrow/label band, eq box. Banked evidence for delta_vs_related.md
rows 10/13/14 (vision-pending items that PIL can settle)."""
import numpy as np
from PIL import Image

F = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_031.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

def fam(px):
    r, g, b = px
    if max(r, g, b) - min(r, g, b) < 28 and max(r, g, b) > 190:
        return "gray/white"
    return None

def census(x0, y0, x1, y1, vthr=200, exclude_border=2):
    reg = im[y0:y1, x0:x1]
    counts = {}
    samples = {}
    for yy in range(reg.shape[0]):
        for xx in range(reg.shape[1]):
            r, g, b = reg[yy, xx]
            v = max(r, g, b)
            if v >= vthr:
                continue
            if fam((r, g, b)) == "gray/white":
                # gray axes #969897 family
                key = "gray"
            elif r > 120 and g < 90 and b < 90:
                key = "red"
            elif abs(r - g) < 40 and abs(g - b) < 40 and v < 120:
                key = "near-black"
            elif g >= r and g >= b and v < 200:
                key = f"greenish"
            elif b > r and b > g:
                key = "blueish"
            else:
                key = "other"
            counts[key] = counts.get(key, 0) + 1
            if key not in samples:
                samples[key] = (x0 + xx, y0 + yy, (int(r), int(g), int(b)))
    return counts, samples

print("== 1. 031 plot interior x578..806 y70..306 (excl red border, axes) ==")
c, s = census(578, 70, 806, 306)
for k in sorted(c, key=c.get, reverse=True):
    print(f"  {k:10s} n={c[k]:6d} first={s[k]}")

print("== 2. exact colors along dark strokes (V<150) in plot interior ==")
reg = im[70:306, 578:806]
pts = {}
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if max(r, g, b) < 150 and not (r > 120 and g < 90 and b < 90):
            pts.setdefault((r // 16 * 16, g // 16 * 16, b // 16 * 16), []).append((578 + xx, 70 + yy))
for k in sorted(pts, key=lambda k: len(pts[k]), reverse=True)[:8]:
    v = pts[k]
    print(f"  rgb~{k} n={len(v):5d} e.g. {v[0]} {v[len(v)//2]} {v[-1]}")

print("== 3. dashed-guide region x650..672 y60..300: column red counts ==")
for xx in range(650, 673):
    col = im[60:300, xx]
    n = sum(1 for r, g, b in col if r > 120 and g < 90 and b < 90)
    if n:
        print(f"  x{xx}: red n={n}")

print("== 4. arrow/label band x230..570 y292..330 color census ==")
reg = im[292:330, 230:570]
counts, samples = {}, {}
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if r > 200 and 120 < g < 210 and 130 < b < 220:
            key = "pink"
        elif r > 120 and g < 90 and b < 90:
            key = "red"
        elif 90 < r < 200 and g < 90 and b > 90:
            key = "purple/magenta"
        elif max(r, g, b) < 150:
            key = "dark-text"
        else:
            continue
        counts[key] = counts.get(key, 0) + 1
        samples.setdefault(key, (230 + xx, 292 + yy, (int(r), int(g), int(b))))
for k in sorted(counts, key=counts.get, reverse=True):
    print(f"  {k:14s} n={counts[k]:6d} first={samples[k]}")

print("== 5. pink band extent (pink fill) ==")
ys, xs = [], []
reg = im[280:340, 230:600]
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if r > 200 and 120 < g < 210 and 130 < b < 220:
            ys.append(280 + yy); xs.append(230 + xx)
if xs:
    print(f"  pink bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} n={len(xs)}")
else:
    print("  no pink fill found in band region")

print("== 6. eq-box hunt x360..580 y140..250: non-background clusters ==")
reg = im[140:250, 360:580]
rows = {}
for yy in range(reg.shape[0]):
    n = 0
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if max(r, g, b) < 215 and not (abs(r-g) < 12 and abs(g-b) < 12):
            n += 1
    if n > 2:
        rows[140 + yy] = n
for y, n in sorted(rows.items()):
    print(f"  y{y}: colored-dark n={n}")

print("== 7. eq-box border color: scan x360..580 y140..250 for red/blue border lines ==")
reg = im[140:250, 360:580]
hits = {}
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if r > 110 and g < 90 and b < 90:
            hits.setdefault("red", []).append((360 + xx, 140 + yy))
        elif b > 100 and b > r + 40 and g < 100:
            hits.setdefault("blue", []).append((360 + xx, 140 + yy))
        elif 60 < r < 140 and 20 < g < 90 and 30 < b < 110:
            hits.setdefault("maroon", []).append((360 + xx, 140 + yy))
for k, v in hits.items():
    xs2 = [p[0] for p in v]; ys2 = [p[1] for p in v]
    print(f"  {k}: n={len(v)} bbox x{min(xs2)}..{max(xs2)} y{min(ys2)}..{max(ys2)} e.g. {v[:3]}")
if not hits:
    print("  no red/blue/maroon border pixels found in eq-box hunt region")

print("== 8. title band y60..95 x60..560: color run extents ==")
reg = im[60:95, 60:560]
runs = {}
for yy in range(reg.shape[0]):
    for xx in range(reg.shape[1]):
        r, g, b = reg[yy, xx]
        if max(r, g, b) < 190:
            if r > 100 and g < 90 and b < 90:
                key = "red"
            elif b > 90 and b > r + 30:
                key = "blue"
            elif g > 90 and g > r + 20 and g > b + 20:
                key = "green"
            elif max(r, g, b) < 100:
                key = "near-black"
            else:
                key = "midgray"
            runs.setdefault(key, []).append((60 + xx, 60 + yy))
for k, v in sorted(runs.items()):
    xs2 = [p[0] for p in v]; ys2 = [p[1] for p in v]
    print(f"  {k:9s} n={len(v):5d} x{min(xs2)}..{max(xs2)} y{min(ys2)}..{max(ys2)}")
