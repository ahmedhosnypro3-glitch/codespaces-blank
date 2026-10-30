#!/usr/bin/env python3
"""Pass 3: color census per panel, curve tracing, dot finding, red-arrow tracing."""
import numpy as np
from PIL import Image
from scipy import ndimage
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]


def census(x0, x1, y0, y1, label, topn=10):
    sub = IM[y0:y1, x0:x1].reshape(-1, 3)
    ink = sub[(sub.max(axis=1) - sub.min(axis=1) > 30) | (sub.sum(axis=1) < 500)]
    cnt = Counter(map(tuple, np.round(ink / 20) * 20))
    print(f"-- {label} ink census ({len(ink)} px):")
    for col, npx in cnt.most_common(topn):
        print(f"   ~{col} n={npx}")


print("== PANEL COLOR CENSUS ==")
census(100, 470, 130, 460, "LEFT panel interior")
census(490, 850, 130, 460, "RIGHT panel interior")

# ---------- loose blue mask: ANY distinctly blue ink ----------
print("\n== LOOSE BLUE (b-r>40, b>110) COMPONENTS ==")
blue = (b - r > 40) & (b > 110)
# remove house strokes/badge/border? border IS dark blue — keep, mark separately
lbl, n = ndimage.label(blue)
info = []
for i in range(1, n + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) < 15:
        continue
    info.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max(), i, ys, xs))
info.sort(key=lambda t: -t[0])
for size, x0, x1, y0, y1, i, ys, xs in info[:14]:
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    print(f"  n={size} x {x0}-{x1} y {y0}-{y1} w={w_} h={h_} cx={(x0+x1)/2:.0f} cy={(y0+y1)/2:.0f} fill={size/(w_*h_):.2f}")

# ---------- left curve trace: for each column, mean y of blue ink in LEFT panel ----------
print("\n== LEFT CURVE TRACE (col -> mean blue y), step 20 ==")
lmask = blue.copy()
lmask[:, :100] = False; lmask[:, 470:] = False; lmask[:130, :] = False; lmask[465:, :] = False
lmask &= (b - r > 60)  # curve blue, not border-dark
for x in range(100, 470, 20):
    col = np.where(lmask[:, x])[0]
    if len(col):
        print(f"  x={x}: y {col.min()}-{col.max()} mean={col.mean():.0f} n={len(col)}")
    else:
        print(f"  x={x}: -")

print("\n== RIGHT CURVE TRACE (col -> blue y), step 20 ==")
rmask = blue.copy()
rmask[:, :500] = False; rmask[:, 855:] = False; rmask[:130, :] = False; rmask[465:, :] = False
rmask &= (b - r > 40)
for x in range(500, 855, 20):
    col = np.where(rmask[:, x])[0]
    if len(col):
        print(f"  x={x}: y {col.min()}-{col.max()} mean={col.mean():.0f} n={len(col)}")
    else:
        print(f"  x={x}: -")

# ---------- trace the two big red diagonal components ----------
print("\n== RED DIAGONAL TRACE (left: x154-265 y211-444; right: x507-617 y208-440) ==")
red_ink = (r > 120) & ((r - g) > 40) & ((r - b) > 40)
red_content = red_ink.copy()
red_content[:, :65] = False; red_content[:, 895:] = False; red_content[530:, :] = False
# title band too
red_content[:110, :] = False
lblr, nr = ndimage.label(red_content)
for i in range(1, nr + 1):
    ys, xs = np.where(lblr == i)
    if len(ys) < 100:
        continue
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(f"  comp n={len(ys)} x {x0}-{x1} y {y0}-{y1}")
    # trace: for sample rows, the x extent (shows tilt)
    for yy in range(y0, y1 + 1, max(1, (y1 - y0) // 8)):
        row = np.where(lblr[yy] == i)[0]
        if len(row):
            print(f"    y={yy}: x {row.min()}-{row.max()} n={len(row)}")
    for xx in range(x0, x1 + 1, max(1, (x1 - x0) // 8)):
        colm = np.where(lblr[:, xx] == i)[0]
        if len(colm):
            print(f"    x={xx}: y {colm.min()}-{colm.max()} n={len(colm)}")

# ---------- x-axis arrows ----------
print("\n== X-AXIS ARROW TRACE ==")
for label_, (ax0, ax1, ay0, ay1) in [("LEFT xaxis", (280, 430, 434, 452)), ("RIGHT xaxis", (635, 785, 430, 448))]:
    m = red_ink[ay0:ay1, ax0:ax1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {label_}: x {ax0+xs.min()}-{ax0+xs.max()} y {ay0+ys.min()}-{ay0+ys.max()} n={len(ys)}")
        for yy in range(ay0, ay1):
            row = np.where(red_ink[yy, ax0:ax1])[0]
            if len(row):
                print(f"    y={yy}: x {ax0+row.min()}-{ax0+row.max()}")

# ---------- black tiny arrow near left valley? ----------
print("\n== BLACK INK in left panel lower region (x 100-470, y 380-465) ==")
darkm = (r < 120) & (g < 120) & (b < 120)
darkm[:, :65] = False
sub = darkm[380:465, 100:470]
lbld, nd = ndimage.label(sub)
for i in range(1, nd + 1):
    ys, xs = np.where(lbld == i)
    if len(ys) >= 2:
        print(f"  comp n={len(ys)} x {100+xs.min()}-{100+xs.max()} y {380+ys.min()}-{380+ys.max()}")

# ---------- title row profile ----------
print("\n== TITLE ROW PROFILE (x 185..690) ==")
tm = (r > 120) & ((r - g) > 40) & ((r - b) > 40)
tm[:, :185] = False; tm[:, 690:] = False
for yy in range(68, 106):
    row = np.where(tm[yy, :])[0]
    if len(row):
        print(f"  y={yy}: n={len(row)} x {row.min()}-{row.max()}")
