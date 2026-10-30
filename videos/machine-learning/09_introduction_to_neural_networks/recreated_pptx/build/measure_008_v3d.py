#!/usr/bin/env python3
"""Final targeted probes: panel edges, callout boxes, ? boxes, axes, lines, hatch fills."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(label, "EMPTY")
        return
    print(f"{label}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} n={len(xs)}")


reddish = (r > 140) & (g < 130) & (b < 130) & ((r - g) > 60)
print("--- vertical reddish lines in panel zone ---")
for xx in range(100, 900):
    n = reddish[110:505, xx].sum()
    if n > 150:
        ys = np.where(reddish[110:505, xx])[0] + 110
        print("  col", xx, "n", n, "y", ys.min(), ys.max())
print("--- horizontal reddish lines ---")
for yy in range(100, 520):
    n = reddish[yy, 100:900].sum()
    if n > 150:
        xs = np.where(reddish[yy, 100:900])[0] + 100
        print("  row", yy, "n", n, "x", xs.min(), xs.max())

print("--- Undefined box: blue ink in x 55-170, y 115-175 ---")
blueish = (b > 140) & (r < 150) & (g < 170) & ((b - r) > 40)
m = np.zeros_like(blueish)
m[110:180, 50:175] = True
bbox(blueish & m, "blue undefined")
for yy in range(125, 165):
    xs = np.where(blueish[yy, 50:175])[0] + 50
    if len(xs):
        print("   row", yy, "x", xs.min(), xs.max(), "n", len(xs))
for xx in range(55, 165):
    ys = np.where(blueish[110:180, xx])[0] + 110
    if len(ys):
        print("   col", xx, "y", ys.min(), ys.max(), "n", len(ys))
print("   fill sample (110,145):", tuple(a[145, 110]), " (120,150):", tuple(a[150, 120]))

print("--- New Class box: magenta ink in x 640-820, y 330-410 ---")
mag = (r > 170) & (b > 150) & (g < 180) & ((r - g) > 50) & ((b - g) > 40)
m = np.zeros_like(mag)
m[330:410, 640:820] = True
bbox(mag & m, "magenta newclass")
for yy in range(335, 405):
    xs = np.where(mag[yy, 640:820])[0] + 640
    if len(xs) > 3:
        print("   row", yy, "x", xs.min(), xs.max(), "n", len(xs))
for xx in range(645, 815):
    ys = np.where(mag[330:410, xx])[0] + 330
    if len(ys) > 3:
        print("   col", xx, "y", ys.min(), ys.max(), "n", len(ys))
print("   fill sample (750,383):", tuple(a[383, 750]))

print("--- ? boxes: sample colors at v2 centers ---")
for (cx, cy) in [(612, 193), (263, 280), (432, 317), (442, 434), (660, 150), (590, 180), (240, 270), (420, 320)]:
    print("   ", (cx, cy), tuple(a[cy, cx]), tuple(a[cy + 8, cx + 8]))
# salmon-ish scan with looser threshold restricted to panel
salmon = (r >= 235) & (g >= 195) & (g <= 235) & (b >= 175) & (b <= 215) & ((r - b) >= 20) & ((r - g) >= 8)
salmon[:110] = False
salmon[500:] = False
salmon[:, :150] = False
salmon[:, 800:] = False
from collections import deque
seen = np.zeros(salmon.shape, bool)
ys0, xs0 = np.where(salmon)
res = []
for y0, x0 in zip(ys0, xs0):
    if seen[y0, x0]:
        continue
    q = deque([(y0, x0)])
    seen[y0, x0] = True
    pix = []
    while q:
        y, x = q.popleft()
        pix.append((y, x))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and salmon[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    q.append((yy, xx))
    if len(pix) >= 200:
        ys = [p[0] for p in pix]
        xs = [p[1] for p in pix]
        res.append((min(xs), max(xs), min(ys), max(ys), len(pix)))
res.sort(key=lambda t: -t[4])
for c in res[:8]:
    print("   salmon comp x %d-%d y %d-%d n=%d center (%.0f,%.0f)" %
          (c[0], c[1], c[2], c[3], c[4], (c[0] + c[1]) / 2, (c[2] + c[3]) / 2))

print("--- axes: vertical line x? red ink columns y 130-500 (relaxed) ---")
for xx in range(280, 320):
    n = reddish[130:500, xx].sum()
    if n > 60:
        print("  col", xx, n)
print("--- horizontal axis rows x 200-700 ---")
for yy in range(400, 460):
    n = reddish[yy, 200:700].sum()
    if n > 60:
        print("  row", yy, n)

print("--- hatch fills at grid points ---")
for (sx, sy) in [(200, 130), (300, 130), (500, 130), (700, 130), (200, 200), (300, 200), (500, 200), (650, 200),
                 (200, 300), (300, 300), (500, 300), (650, 300), (750, 250),
                 (200, 400), (300, 420), (450, 450), (600, 450), (700, 420), (750, 350),
                 (230, 260), (240, 300), (190, 250)]:
    print("   ", (sx, sy), tuple(a[sy, sx]))

print("--- title colors ---")
print("   red sample (400,62):", tuple(a[62, 400]), " blue sample (380,90):", tuple(a[90, 380]))
print("--- line colors ---")
# blue line: scan diagonal region x 350-642, find bluest px per column
for xx in (400, 450, 500, 550, 600):
    col = a[130:470, xx]
    idx = np.argmax(col[:, 2] - col[:, 0])
    print("   blue line at x", xx, "y", idx + 130, tuple(col[idx]))
for xx in (300, 400, 500, 600, 680):
    col = a[130:470, xx]
    idx = np.argmax(col[:, 1] - col[:, 0])
    print("   green line at x", xx, "y", idx + 130, tuple(col[idx]))
for xx in (300, 350, 400, 450, 500, 550):
    col = a[130:500, xx]
    idx = np.argmax(col[:, 0] - col[:, 1])
    print("   red line at x", xx, "y", idx + 130, tuple(col[idx]))
