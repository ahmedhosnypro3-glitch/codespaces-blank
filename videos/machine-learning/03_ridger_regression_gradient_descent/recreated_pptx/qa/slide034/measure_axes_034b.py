#!/usr/bin/env python3
"""Measure the exact axis-line extents and key overlay elements of 034's plot."""
import numpy as np
from PIL import Image

ROOT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
im = np.asarray(Image.open(ROOT + "/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 608, 847, 60, 312
box = im[Y0:Y1, X0:X1]
lum = box.sum(axis=2)

# ---- x-axis line: row 172, find its dark span (excluding the red frame border)
row = lum[172 - Y0, :]
dark = row < 560
xs = np.where(dark)[0]
runs, cur = [], None
for i in xs:
    if cur is None:
        cur = [i, i]
    elif i == cur[1] + 1:
        cur[1] = i
    else:
        runs.append(tuple(cur)); cur = [i, i]
if cur: runs.append(tuple(cur))
print("x-axis dark runs (frame x):", [(X0+a, X0+b) for a, b in runs])

# ---- y-axis line: col 721-722
col = lum[:, 721 - X0]
darkc = col < 560
ys = np.where(darkc)[0]
runs, cur = [], None
for i in ys:
    if cur is None:
        cur = [i, i]
    elif i == cur[1] + 1:
        cur[1] = i
    else:
        runs.append(tuple(cur)); cur = [i, i]
if cur: runs.append(tuple(cur))
print("y-axis dark runs (frame y):", [(Y0+a, Y0+b) for a, b in runs])

# ---- curve stroke core color: most saturated cyan pixels
r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]
cyan = (b - r > 55) & (g - r > 30) & (b > 140)
if cyan.sum():
    sel = box[cyan]
    idx = np.argsort(sel[:, 2])
    print("cyan darkest 20 rgb:", sel[idx[:20]].tolist())
    print("cyan median rgb:", np.median(sel, axis=0).astype(int).tolist())
    print("cyan brightest rgb:", np.percentile(sel, 90, axis=0).astype(int).tolist())

# ---- tick marks ON the axis: small dark protrusions at row 173/171
for rr in [169, 170, 171, 173, 174]:
    row = lum[rr - Y0, :] < 560
    xs = np.where(row)[0]
    runs, cur = [], None
    for i in xs:
        if cur is None: cur = [i, i]
        elif i <= cur[1] + 2: cur[1] = i
        else: runs.append(tuple(cur)); cur = [i, i]
    if cur: runs.append(tuple(cur))
    print(f"row {rr} runs:", [(X0+a, X0+b) for a, b in runs])

# y ticks on the y-axis cols
for cc in [719, 720, 723, 724]:
    col = lum[:, cc - X0] < 560
    ys = np.where(col)[0]
    runs, cur = [], None
    for i in ys:
        if cur is None: cur = [i, i]
        elif i <= cur[1] + 2: cur[1] = i
        else: runs.append(tuple(cur)); cur = [i, i]
    if cur: runs.append(tuple(cur))
    print(f"col {cc} runs:", [(Y0+a, Y0+b) for a, b in runs])

# ---- green ellipse + orange arrow bboxes
green = (g > 200) & (r < 160) & (b < 130)
ys, xs = np.where(green)
if len(xs): print("green bbox frame x %d..%d y %d..%d" % (X0+xs.min(), X0+xs.max(), Y0+ys.min(), Y0+ys.max()))
orange = (r > 200) & (g > 100) & (g < 190) & (b < 90)
ys, xs = np.where(orange)
if len(xs): print("orange bbox frame x %d..%d y %d..%d" % (X0+xs.min(), X0+xs.max(), Y0+ys.min(), Y0+ys.max()))

# ---- red dashed vertical near x779-787 y144-172?
rd = (r > 140) & (r - g > 45) & (r - b > 45)
strip = rd[:, 770 - X0: 795 - X0]
ys, xs = np.where(strip)
if len(xs): print("red-ish in x770..795: y %d..%d (rel x cols %s)"
                  % (Y0+ys.min(), Y0+ys.max(), [770+int(i) for i in np.unique(xs)]))

# pink callout box border/fill
pink = (r > 210) & (g > 150) & (g < 215) & (b > 180) & (b - g > 30)
ys, xs = np.where(pink)
print("pink fill bbox frame x %d..%d y %d..%d" % (X0+xs.min(), X0+xs.max(), Y0+ys.min(), Y0+ys.max()))
darkpink = (r > 120) & (b > 100) & (r - g > 40) & (lum < 620)
ys, xs = np.where(darkpink)
if len(xs): print("dark/magenta ink bbox frame x %d..%d y %d..%d" % (X0+xs.min(), X0+xs.max(), Y0+ys.min(), Y0+ys.max()))
