#!/usr/bin/env python3
"""w2 box tracing — exact box edges, corner radii, fills, stroke colors.
READ-ONLY measurement of unique_slides/slide_023.jpg (960x540)."""
import numpy as np
from PIL import Image
from collections import Counter

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]


def runs(mask_row):
    xi = np.where(mask_row)[0]
    if not len(xi):
        return []
    out = []
    s = p = int(xi[0])
    for x in xi[1:]:
        if x > p + 1:
            out.append((s, p)); s = int(x)
        p = int(x)
    out.append((s, p))
    return out


greenfill = (G > R + 6) & (G > B + 6) & (G > 200) & (R > 180) & (G < 252)
print("== GREEN box: per-row leftmost/rightmost green-fill x ==")
for y in list(range(104, 130)) + list(range(210, 228)):
    rr = runs(greenfill[y, 60:900])
    rr = [(s + 60, e + 60) for s, e in rr if e - s >= 2]
    if rr:
        print(f"  y{y}: runs={rr}")

print("\n== GREEN box: per-column top/bottom (x=100..760 sample) ==")
for x in [100, 200, 400, 600, 700, 745, 752, 758, 762, 768]:
    col = np.where(greenfill[95:245, x])[0]
    if len(col):
        print(f"  x{x}: green fill rows {col.min()+95}..{col.max()+95} n={len(col)}")
    else:
        print(f"  x{x}: none")

print("\n== GREEN corner radius (top-left): first green row per y, x from 90 ==")
for y in range(105, 122):
    xs = np.where(greenfill[y, 85:130])[0]
    print(f"  y{y}: leftmost x={xs.min()+85 if len(xs) else None}")
print("  bottom-left:")
for y in range(206, 224):
    xs = np.where(greenfill[y, 85:130])[0]
    print(f"  y{y}: leftmost x={xs.min()+85 if len(xs) else None}")
print("  top-right:")
for y in range(105, 122):
    xs = np.where(greenfill[y, 720:800])[0]
    print(f"  y{y}: rightmost x={xs.max()+720 if len(xs) else None}")
print("  bottom-right:")
for y in range(206, 224):
    xs = np.where(greenfill[y, 720:800])[0]
    print(f"  y{y}: rightmost x={xs.max()+720 if len(xs) else None}")

print("\n== anomaly x756..775 y100..120 (raw colours) ==")
for y in range(102, 122):
    seg = a[y, 750:790]
    print(f"  y{y}: " + " ".join(f"{x}:{tuple(seg[x-750])}" for x in range(750, 790, 4)))

# ---- BLUE box ----
print("\n== BLUE box ==")
bluefill = (B > R + 3) & (B > 240) & (R > 240) & (G > 243)
for y in list(range(226, 240)) + list(range(418, 432)):
    rr = runs(bluefill[y, 60:900])
    rr = [(s + 60, e + 60) for s, e in rr if e - s >= 2]
    print(f"  y{y}: runs={rr[:4]}{'...' if len(rr) > 4 else ''}")
print("  per-column top/bottom:")
for x in [90, 100, 200, 400, 600, 850, 860, 865, 868, 872]:
    col = np.where(bluefill[220:440, x])[0]
    if len(col):
        print(f"   x{x}: rows {col.min()+220}..{col.max()+220} n={len(col)}")
    else:
        print(f"   x{x}: none")
print("  corner profile top-left:")
for y in range(226, 244):
    xs = np.where(bluefill[y, 80:130])[0]
    print(f"   y{y}: leftmost x={xs.min()+80 if len(xs) else None}")
print("  top-right:")
for y in range(226, 244):
    xs = np.where(bluefill[y, 830:890])[0]
    print(f"   y{y}: rightmost x={xs.max()+830 if len(xs) else None}")
print("  bottom-left:")
for y in range(412, 432):
    xs = np.where(bluefill[y, 80:130])[0]
    print(f"   y{y}: leftmost x={xs.min()+80 if len(xs) else None}")
print("  bottom-right:")
for y in range(412, 432):
    xs = np.where(bluefill[y, 830:890])[0]
    print(f"   y{y}: rightmost x={xs.max()+830 if len(xs) else None}")

# ---- YELLOW box ----
print("\n== YELLOW box ==")
yfill = (R > 243) & (G > 243) & (B > 200) & (B < 243) & (R - B > 10)
for y in list(range(430, 448)) + list(range(520, 537)):
    rr = runs(yfill[y, 60:900])
    rr = [(s + 60, e + 60) for s, e in rr if e - s >= 2]
    print(f"  y{y}: runs={rr[:4]}{'...' if len(rr) > 4 else ''}")
print("  per-column top/bottom:")
for x in [90, 100, 200, 400, 600, 860, 868, 870, 875]:
    col = np.where(yfill[425:, x])[0]
    if len(col):
        print(f"   x{x}: rows {col.min()+425}..{col.max()+425} n={len(col)}")
    else:
        print(f"   x{x}: none")
print("  top-left corner:")
for y in range(430, 450):
    xs = np.where(yfill[y, 78:130])[0]
    print(f"   y{y}: leftmost x={xs.min()+78 if len(xs) else None}")
print("  top-right corner:")
for y in range(430, 450):
    xs = np.where(yfill[y, 830:890])[0]
    print(f"   y{y}: rightmost x={xs.max()+830 if len(xs) else None}")
print("  bottom-left corner:")
for y in range(515, 534):
    xs = np.where(yfill[y, 78:130])[0]
    print(f"   y{y}: leftmost x={xs.min()+78 if len(xs) else None}")
print("  bottom-right corner:")
for y in range(515, 534):
    xs = np.where(yfill[y, 830:890])[0]
    print(f"   y{y}: rightmost x={xs.max()+830 if len(xs) else None}")

print("\n== stroke colours (core, modal) ==")
print("  green top y=110 x200..700:", Counter(map(tuple, a[110, 200:700][::7].tolist())).most_common(3))
print("  green left x=98 y150..210:", Counter(map(tuple, a[150:210, 98].tolist())).most_common(3))
print("  green right x=754 y150..210:", Counter(map(tuple, a[150:210, 754].tolist())).most_common(3))
print("  green bottom y=218 x200..700:", Counter(map(tuple, a[218, 200:700][::7].tolist())).most_common(3))
print("  blue top y=228 x200..700:", Counter(map(tuple, a[228, 200:700][::7].tolist())).most_common(3))
print("  blue left x=88 y300..400:", Counter(map(tuple, a[300:400, 88].tolist())).most_common(3))
print("  blue right x=868 y300..400:", Counter(map(tuple, a[300:400, 868].tolist())).most_common(3))
print("  blue bottom y=425 x200..700:", Counter(map(tuple, a[425, 200:700][::7].tolist())).most_common(3))
print("  yell top y=435 x200..700:", Counter(map(tuple, a[435, 200:700][::7].tolist())).most_common(3))
print("  yell left x=86 y460..520:", Counter(map(tuple, a[460:520, 86].tolist())).most_common(3))
print("  yell right x=874 y460..520:", Counter(map(tuple, a[460:520, 874].tolist())).most_common(3))
print("  yell bottom y=530 x200..700:", Counter(map(tuple, a[530, 200:700][::7].tolist())).most_common(3))

print("\n== vertical gaps between boxes ==")
for y in range(216, 232):
    print(f"  y{y} x300..500:", Counter(map(tuple, a[y, 300:500][::13].tolist())).most_common(2))
for y in range(424, 442):
    print(f"  y{y} x300..500:", Counter(map(tuple, a[y, 300:500][::13].tolist())).most_common(2))
