#!/usr/bin/env python3
"""Pixel-measure slide_023.jpg: find letterbox, frames, boxes, and text colors."""
from PIL import Image
import collections
import numpy as np

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg")
a = np.asarray(img.convert("RGB"))
H, W, _ = a.shape
print(f"image: {W}x{H}")

# Row darkness profile to find the letterbox bar
rowmean = a.mean(axis=(1, 2))
for y in range(H - 30, H):
    print(f"  y={y} rowmean={rowmean[y]:.1f}")

# Column profile for vertical frames
colmean = a.mean(axis=(0, 2))

def hexs(rgb):
    return "#%02X%02X%02X" % tuple(int(v) for v in rgb)

# Most common colors
flat = a.reshape(-1, 3)
cnt = collections.Counter(map(tuple, flat[::7]))
print("\ntop colors:")
for rgb, n in cnt.most_common(14):
    print(f"  {hexs(rgb)}  n={n}")

# Red-ish pixels (frame / text) -> row/col extents
r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
red = (r > 120) & (g < 90) & (b < 90)
ys, xs = np.where(red)
print(f"\nred pixels: x {xs.min()}-{xs.max()} ({xs.min()/W:.3f}-{xs.max()/W:.3f}), y {ys.min()}-{ys.max()} ({ys.min()/H:.3f}-{ys.max()/H:.3f})")

# Blue-violet frame
violet = (b > 130) & (r > 60) & (r < 170) & (g > 50) & (g < 140) & (b - r > 40)
ys2, xs2 = np.where(violet)
if len(xs2):
    print(f"violet pixels: x {xs2.min()}-{xs2.max()} ({xs2.min()/W:.3f}-{xs2.max()/W:.3f}), y {ys2.min()}-{ys2.max()} ({ys2.min()/H:.3f}-{ys2.max()/H:.3f})")

# Yellow badge
yellow = (r > 200) & (g > 200) & (b < 190)
ys3, xs3 = np.where(yellow)
if len(xs3):
    print(f"yellow pixels: x {xs3.min()}-{xs3.max()} ({xs3.min()/W:.3f}-{xs3.max()/W:.3f}), y {ys3.min()}-{ys3.max()} ({ys3.min()/H:.3f}-{ys3.max()/H:.3f})")

# Green text
green = (g > 90) & (r < 110) & (b < 110)
ys4, xs4 = np.where(green)
if len(xs4):
    print(f"green pixels: x {xs4.min()}-{xs4.max()} ({xs4.min()/W:.3f}-{xs4.max()/W:.3f}), y {ys4.min()}-{ys4.max()} ({ys4.min()/H:.3f}-{ys4.max()/H:.3f})")
    # cluster green rows
    rows = sorted(set(ys4.tolist()))
    groups, cur = [], [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 3:
            cur.append(y)
        else:
            groups.append((cur[0], cur[-1]))
            cur = [y]
    groups.append((cur[0], cur[-1]))
    print("  green row bands:", groups)

# Blue text
blue = (b > 120) & (r < 100) & (g < 120)
ys5, xs5 = np.where(blue)
if len(xs5):
    print(f"blue pixels: x {xs5.min()}-{xs5.max()}, y {ys5.min()}-{ys5.max()}")
    rows = sorted(set(ys5.tolist()))
    groups, cur = [], [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 3:
            cur.append(y)
        else:
            groups.append((cur[0], cur[-1]))
            cur = [y]
    groups.append((cur[0], cur[-1]))
    print("  blue row bands:", groups)

# Peach fill detection (FDE9E0-ish)
peach = (r > 240) & (g > 210) & (g < 245) & (b > 200) & (b < 235)
ys6, xs6 = np.where(peach)
if len(xs6):
    print(f"peach pixels: x {xs6.min()}-{xs6.max()}, y {ys6.min()}-{ys6.max()}")
    rows = sorted(set(ys6.tolist()))
    groups, cur = [], [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 4:
            cur.append(y)
        else:
            groups.append((cur[0], cur[-1]))
            cur = [y]
    groups.append((cur[0], cur[-1]))
    print("  peach row bands:", groups)
    for (y0, y1) in groups:
        sel = (ys6 >= y0) & (ys6 <= y1)
        print(f"    band y {y0}-{y1}: x {xs6[sel].min()}-{xs6[sel].max()} ({xs6[sel].min()/W:.3f}-{xs6[sel].max()/W:.3f})")

# cream fill (FFFDE0-ish): r>245 g>240 b in 200-235
cream = (r > 245) & (g > 240) & (b > 200) & (b < 240) & (r - b > 10)
ys7, xs7 = np.where(cream)
if len(xs7):
    rows = sorted(set(ys7.tolist()))
    groups, cur = [], [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 4:
            cur.append(y)
        else:
            groups.append((cur[0], cur[-1]))
            cur = [y]
    groups.append((cur[0], cur[-1]))
    print("cream row bands:", groups)
    for (y0, y1) in groups:
        sel = (ys7 >= y0) & (ys7 <= y1)
        print(f"    band y {y0}-{y1}: x {xs7[sel].min()}-{xs7[sel].max()} ({xs7[sel].min()/W:.3f}-{xs7[sel].max()/W:.3f})")
