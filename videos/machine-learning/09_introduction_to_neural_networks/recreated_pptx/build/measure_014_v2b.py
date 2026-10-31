#!/usr/bin/env python3
"""Slide 014 v2 build measurements, part 2: fills, circles, step boxes, connectors."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
SX, SY = 13.333 / W, 7.5 / H
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def px2in(x, y):
    return (round(x * SX, 3), round(y * SY, 3))


def bbox(mask, minpx=30, n=10):
    lab, nlab = ndimage.label(mask)
    if nlab == 0:
        return []
    sizes = ndimage.sum(mask, lab, range(1, nlab + 1))
    out = []
    for i in np.argsort(sizes)[::-1]:
        if sizes[i] < minpx:
            break
        ys, xs = np.where(lab == i + 1)
        out.append((xs.min(), ys.min(), xs.max(), ys.max(), int(sizes[i])))
    return out[:n]


print("=== inset fill samples (right-bottom cream box) ===")
for (x, y) in [(570, 330), (600, 450), (700, 330), (860, 450), (868, 320), (840, 380)]:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

print("\n=== step-box fills (main x415..470 y194..226) ===")
for (x, y) in [(420, 200), (450, 220), (430, 210), (466, 196)]:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

print("\n=== numbered circle fills (probe around expected 1,2,3) ===")
for (x, y) in [(266, 105), (266, 258), (333, 252), (262, 100), (338, 245)]:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

print("\n=== title color sample ===")
for (x, y) in [(280, 62), (330, 70), (600, 62)]:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

print("\n=== connector colors: sample line pixels between nodes ===")
for (x, y) in [(180, 140), (200, 165), (300, 130), (300, 160), (240, 240),
               (330, 170), (340, 215), (400, 205), (480, 210), (620, 390), (640, 400)]:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

# numbered circles: saturated red/maroon disks near the three nodes
print("\n=== red/maroon disks (numbered circles) ===")
red = (r > 120) & (r > g + 60) & (r > b + 40)
for bl in bbox(red, 120, 14):
    w, h = bl[2] - bl[0] + 1, bl[3] - bl[1] + 1
    if 8 <= w <= 40 and 8 <= h <= 40:
        m = a[bl[1]:bl[3], bl[0]:bl[2]].reshape(-1, 3).mean(axis=0).astype(int)
        print(f"  x[{bl[0]}..{bl[2]}] y[{bl[1]}..{bl[3]}] ctr_in={px2in((bl[0]+bl[2])//2, (bl[1]+bl[3])//2)} "
              f"{w}x{h}px mean=#{m[0]:02X}{m[1]:02X}{m[2]:02X}")

print("\n=== white numeral pixels inside those disks ===")
for (cx, cy) in [(266, 105), (266, 258), (333, 252)]:
    reg = a[cy - 10:cy + 10, cx - 10:cx + 10]
    white = (reg[:, :, 0] > 200) & (reg[:, :, 1] > 200) & (reg[:, :, 2] > 200)
    ys, xs = np.where(white)
    if len(xs):
        print(f"  near ({cx},{cy}): white ink x[{xs.min()+cx-10}..{xs.max()+cx-10}] "
              f"y[{ys.min()+cy-10}..{ys.max()+cy-10}] n={len(xs)} in={px2in(xs.min()+cx-10, ys.min()+cy-10)}")
    else:
        print(f"  near ({cx},{cy}): no white ink")

print("\n=== O/P text boxes ===")
for (x0, x1, y0, y1, nm) in [(425, 475, 225, 255, "main O/P"), (805, 855, 360, 395, "inset O/P")]:
    reg = a[y0:y1, x0:x1]
    dark = reg.sum(axis=2) < 330
    ys, xs = np.where(dark)
    if len(xs):
        print(f"  {nm}: x[{xs.min()+x0}..{xs.max()+x0}] y[{ys.min()+y0}..{ys.max()+y0}] "
              f"in=({px2in(xs.min()+x0, ys.min()+y0)}..{px2in(xs.max()+x0, ys.max()+y0)})")

print("\n=== threshold legend (>0 => 1 / <=0 => 0) ===")
reg = a[110:150, 330:415]
dark = reg.sum(axis=2) < 400
ys, xs = np.where(dark)
print(f"  x[{xs.min()+330}..{xs.max()+330}] y[{ys.min()+110}..{ys.max()+110}] "
      f"in=({px2in(xs.min()+330, ys.min()+110)}..{px2in(xs.max()+330, ys.max()+110)})")
rows = dark.sum(axis=1)
print("  row profile:", "".join("#" if v > 2 else "." for v in rows))

print("\n=== input labels x1 x2 ===")
for (y0, y1, nm) in [(140, 170, "x1"), (240, 270, "x2")]:
    reg = a[y0:y1, 85:135]
    dark = reg.sum(axis=2) < 330
    ys, xs = np.where(dark)
    if len(xs):
        print(f"  {nm}: x[{xs.min()+85}..{xs.max()+85}] y[{ys.min()+y0}..{ys.max()+y0}] "
              f"in=({px2in(xs.min()+85, ys.min()+y0)}..{px2in(xs.max()+85, ys.max()+y0)})")
