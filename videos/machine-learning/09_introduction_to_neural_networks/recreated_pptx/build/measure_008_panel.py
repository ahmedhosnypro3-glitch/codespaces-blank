#!/usr/bin/env python3
"""Locate the white plot panel and the true axis extents on slide_008.jpg."""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

nearwhite = (R > 240) & (G > 240) & (B > 238)
red = (R > 110) & (R - G > 40) & (R - B > 40)

print("=== white coverage per column (rows 120-500) ===")
wc = nearwhite[120:500].sum(axis=0)
runs = [(x, int(wc[x])) for x in range(W)]
big = [(x, n) for x, n in runs if n > 300]
print("cols >300 white:", big[:10], "...", big[-10:] if big else "")
print("min/max col with >300 white:", (big[0][0], big[-1][0]) if big else None)

print()
print("=== white coverage per row (cols 100-850) ===")
wr = nearwhite[:, 100:850].sum(axis=1)
big_r = [(y, int(wr[y])) for y in range(H) if wr[y] > 550]
print("rows >550 white:", big_r)

print()
print("=== red vertical lines: col red counts over y 45..514 ===")
for x in range(W):
    n = red[45:514, x].sum()
    if n > 100:
        ys = np.where(red[45:514, x])[0] + 45
        # contiguous run containing the middle
        print(f"  col {x}: n={n} y {ys.min()}-{ys.max()}")

print()
print("=== red horizontal lines: row red counts over x 62..899 ===")
for y in range(H):
    n = red[y, 62:899].sum()
    if n > 300:
        xs = np.where(red[y, 62:899])[0] + 62
        print(f"  row {y}: n={n} x {xs.min()}-{xs.max()}")

print()
print("=== column x=310 red runs (y 42..517) ===")
col = red[:, 310]
runs = []
cur = None
for y in range(42, 518):
    if col[y]:
        if cur is None: cur = [y, y]
        else: cur[1] = y
    elif cur:
        runs.append(tuple(cur)); cur = None
if cur: runs.append(tuple(cur))
print("  runs:", runs)

print()
print("=== row y=436 red runs (x 59..903) ===")
row = red[436, :]
runs = []
cur = None
for x in range(59, 904):
    if row[x]:
        if cur is None: cur = [x, x]
        else: cur[1] = x
    elif cur:
        runs.append(tuple(cur)); cur = None
if cur: runs.append(tuple(cur))
print("  runs:", runs[:40])

print()
print("=== row y=435 red runs ===")
row = red[435, :]
runs = []
cur = None
for x in range(59, 904):
    if row[x]:
        if cur is None: cur = [x, x]
        else: cur[1] = x
    elif cur:
        runs.append(tuple(cur)); cur = None
if cur: runs.append(tuple(cur))
print("  runs:", runs[:40])

print()
print("=== New Class box region colors x 705..800, y 365..400 ===")
for y in range(368, 400, 3):
    print(' y', y, [tuple(a[y, x]) for x in (712, 716, 720, 740, 760, 780, 784, 788)])
