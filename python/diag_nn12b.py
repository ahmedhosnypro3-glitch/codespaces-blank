#!/usr/bin/env python3
"""Palette + structure measurement of slide_012.jpg."""
import numpy as np
from PIL import Image
from collections import Counter

P = "videos/machine-learning/10_nn_training_and_example/unique_slides/slide_012.jpg"
im = Image.open(P).convert("RGB")
o = np.asarray(im).astype(int)
H, W = 540, 960
IN = 13.33 / W

cnt = Counter(map(tuple, o.reshape(-1, 3)))
print("=== top 24 colors ===")
for c, n in cnt.most_common(24):
    print(f"  {c}  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  n={n:>7}  ({100*n/(H*W):.2f}%)")

bg = cnt.most_common(1)[0][0]
print("\nbg =", bg)
mask_bg = (np.abs(o[:, :, 0] - bg[0]) < 10) & (np.abs(o[:, :, 1] - bg[1]) < 10) & (np.abs(o[:, :, 2] - bg[2]) < 10)
print("bg frac:", round(mask_bg.mean(), 3))

print("\n=== rows by non-bg count (band 10) ===")
nb = (~mask_bg).sum(axis=1)
for y0 in range(0, H, 10):
    bar = "#" * min(50, nb[y0:y0 + 10].sum() // 200)
    print(f"  rows {y0:>3}-{y0+9:>3}: {nb[y0:y0+10].sum():>6} {bar}")

print("\n=== distinct color regions on a vertical scan x=490 (through diagram) ===")
prev = None; start = 0
segs = []
for y in range(H):
    c = tuple(o[y, 490])
    if c != prev:
        if prev is not None and y - start >= 3:
            segs.append((start, y - 1, prev))
        prev = c; start = y
if H - start >= 3:
    segs.append((start, H - 1, prev))
for s, e, c in segs:
    print(f"  rows {s:>3}-{e:>3} ({(e-s+1)*IN:.2f}in): #{c[0]:02X}{c[1]:02X}{c[2]:02X}")

print("\n=== distinct color regions on horizontal scan y=150 ===")
prev = None; start = 0
segs = []
for x in range(W):
    c = tuple(o[150, x])
    if c != prev:
        if prev is not None and x - start >= 3:
            segs.append((start, x - 1, prev))
        prev = c; start = x
if W - start >= 3:
    segs.append((start, W - 1, prev))
for s, e, c in segs:
    print(f"  cols {s:>3}-{e:>3} ({(e-s+1)*IN:.2f}in): #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
