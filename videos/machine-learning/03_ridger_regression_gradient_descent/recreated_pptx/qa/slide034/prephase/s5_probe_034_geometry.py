#!/usr/bin/env python3
"""S5 carrier probe — settle 034 build geometry straight from the frame."""
from PIL import Image
import numpy as np

F = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = im.shape
print("frame", W, "x", H)

def px(x, y): return tuple(im[y, x])

def runs(cols, key):
    out = []
    for x0 in range(cols[0], cols[1]):
        v = im[y_scan[x0]] if False else None

def colscan(x, y0, y1, label):
    print(f"--- col x={x} y{y0}..{y1} ({label})")
    prev = None
    for y in range(y0, y1):
        c = px(x, y)
        key = tuple(v // 12 * 12 for v in c)
        if key != prev:
            print(f"  y={y} rgb={c}")
            prev = key

def rowscan(y, x0, x1, label):
    print(f"--- row y={y} x{x0}..{x1} ({label})")
    prev = None
    for x in range(x0, x1):
        c = px(x, y)
        key = tuple(v // 12 * 12 for v in c)
        if key != prev:
            print(f"  x={x} rgb={c}")
            prev = key

# 1. table vertical structure at two text-free columns
colscan(210, 315, 525, "data col interior (avoid text rows: sample between)")
# 2. horizontal scan across each band mid-line
rowscan(345, 60, 895, "band1 mid")
rowscan(395, 60, 895, "band2 mid")
rowscan(440, 60, 895, "band3 mid")
rowscan(470, 60, 895, "slope mid")
rowscan(495, 60, 895, "next-x mid")

# 3. eq box ink bbox
sub = im[171:218, 467:599]
dark = (sub.max(axis=2) < 160)
ys, xs = np.where(dark)
if len(xs):
    print("eq ink bbox x", xs.min() + 467, "..", xs.max() + 467, " y", ys.min() + 171, "..", ys.max() + 171,
          " n=", len(xs))

# 4. arrow region census
print("--- arrow region x140..205 y295..348")
sub = im[295:348, 140:205]
red = (sub[:, :, 0] > 130) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
white = (sub.min(axis=2) > 200)
ys, xs = np.where(red)
print("red bbox x", xs.min() + 140, "..", xs.max() + 140, " y", ys.min() + 295, "..", ys.max() + 295, " n=", len(xs))
ys, xs = np.where(white)
print("white bbox x", xs.min() + 140, "..", xs.max() + 140, " y", ys.min() + 295, "..", ys.max() + 295, " n=", len(xs))
for y in range(295, 348, 4):
    row = red[y - 295]
    segs = np.where(row)[0]
    if len(segs):
        print(f"  red y={y}: x {segs.min()+140}..{segs.max()+140} n={len(segs)}")

# 5. plot teal ink median + bbox
sub = im[59:313, 608:845].reshape(-1, 3)
r, g, b = sub[:, 0], sub[:, 1], sub[:, 2]
teal = (g > r + 30) & (b > r + 20) & (g > 120)
print("plot teal px n=", teal.sum(), "median rgb", np.median(sub[teal], axis=0) if teal.sum() else None)
im2 = im[:, :, :]
tealm = (im2[:, :, 1] > im2[:, :, 0] + 30) & (im2[:, :, 2] > im2[:, :, 0] + 20) & (im2[:, :, 1] > 120)
sub2 = tealm[59:313, 608:845]
ys, xs = np.where(sub2)
print("teal bbox x", xs.min() + 608, "..", xs.max() + 608, " y", ys.min() + 59, "..", ys.max() + 59)

# 6. cyan insert bbox + border
sub = im[325:375, 655:800]
cy = (sub[:, :, 1] > 200) & (sub[:, :, 2] > 130) & (sub[:, :, 0] < 190) & (sub[:, :, 2] < 210)
ys, xs = np.where(cy)
print("cyan fill bbox x", xs.min() + 655, "..", xs.max() + 655, " y", ys.min() + 325, "..", ys.max() + 325,
      " n=", len(xs), " median", np.median(sub[cy], axis=0))
# border color: scan the vertical edges
for x in [668, 669, 670, 788, 789, 790]:
    cols = im[335:365, x]
    dk = cols[(cols.max(axis=1) < 150)]
    if len(dk):
        print(f"  insert edge x={x} dark n={len(dk)} median {np.median(dk, axis=0)}")

# 7. slope inset boxes: red-bordered boxes inside y459..478
sub = im[459:479, 140:880]
redm = (sub[:, :, 0] > 140) & (sub[:, :, 1] < 80) & (sub[:, :, 2] < 80)
colred = redm.sum(axis=0)
peaks = [x + 140 for x in range(len(colred)) if colred[x] >= 8]
print("slope red vertical cols:", peaks)
sub2 = im[459:479, 143:147]
print("slope c1 inset fill sample", np.median(im[464:474, 150:170].reshape(-1, 3), axis=0))
print("slope c15 fill sample", np.median(im[464:474, 715:735].reshape(-1, 3), axis=0))
print("slope c17 fill sample", np.median(im[464:474, 795:815].reshape(-1, 3), axis=0))

# 8. next-x red grid verticals
sub = im[484:503, 140:880]
redm = (sub[:, :, 0] > 140) & (sub[:, :, 1] < 80) & (sub[:, :, 2] < 80)
colred = redm.sum(axis=0)
peaks = [x + 140 for x in range(len(colred)) if colred[x] >= 8]
print("next-x red vertical cols:", peaks)

# 9. param box fills
for y in [250, 256, 262, 266, 272, 278, 284, 290, 296, 302]:
    print("param y=", y, "x80:", px(80, y), "x100:", px(100, y), "x150:", px(150, y), "x168:", px(168, y))
# param border color
print("param border left x75:", [px(74, y) for y in [250, 275, 300]], "x175:", [px(175, y) for y in [250, 275, 300]])

# 10. explanatory box border/fill
print("expl border scan row y=253..303 at x=269..271:", [px(270, y) for y in range(250, 305, 6)])
print("expl fill sample:", np.median(im[262:272, 300:340].reshape(-1, 3), axis=0))
print("expl border top:", [px(x, 251) for x in range(280, 600, 60)], [px(x, 252) for x in range(280, 600, 60)])
print("expl border bot:", [px(x, 300) for x in range(280, 600, 60)], [px(x, 301) for x in range(280, 600, 60)])
print("expl border right:", [px(597, y) for y in range(255, 300, 8)], [px(598, y) for y in range(255, 300, 8)])
