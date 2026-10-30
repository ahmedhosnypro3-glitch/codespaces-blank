#!/usr/bin/env python3
"""Slide 31 geometry: node circles + text-line extents (original border excluded)."""
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
a = np.asarray(Image.open(f"{BASE}/slide_031.jpg").convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]
IN = 13.33 / 960.0


def groups(idx, gap=3):
    idx = sorted(idx); out = []; st = prev = None
    for v in idx:
        if st is None: st = prev = v
        elif v - prev <= gap: prev = v
        else: out.append((st, prev)); st = prev = v
    if st is not None: out.append((st, prev))
    return out


def lines(mask, name, minpx=2, x0=34, x1=928):
    m = mask.copy(); m[:, :x0] = False; m[:, x1:] = False
    prof = m.sum(axis=1)
    print(f"-- {name}")
    for y0, y1 in groups([y for y in range(H) if prof[y] >= minpx], gap=2):
        sub = m[y0:y1 + 1]
        cc = np.where(sub.any(axis=0))[0]
        print(f"   y {y0}..{y1} in {y0*IN:.2f}..{y1*IN:.2f}  x {cc.min()}..{cc.max()} "
              f"in {cc.min()*IN:.2f}..{cc.max()*IN:.2f}")


red = (r > 140) & (r - g > 60) & (r - b > 60)
blue = (b > 130) & (b - r > 55) & (b - g > 30)
blk = (r < 90) & (g < 90) & (b < 90)
lines(red, "RED", 2)
print()
lines(blue, "BLUE", 2)
print()
lines(blk, "BLACK", 3)

# node/arrow blobs in the diagram area (x>=420, y<=240) that are not text-black
print()
print("-- colored blobs (nodes) x>=420 y<=245")
colored = ~(((r > 150) & (g > 150) & (b > 150)) | blk | red | blue)
colored[:, :420] = False; colored[245:, :] = False
lab, n = ndimage.label(colored)
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 40: continue
    cy, cx = ys.mean(), xs.mean()
    col = a[ys, xs].mean(axis=0).astype(int)
    print(f"   blob {i} n={len(ys)} center ({cx:.0f},{cy:.0f}) in ({cx*IN:.2f},{cy*IN:.2f}) "
          f"rgb={tuple(col)} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")

# saturated blue arrows bottom (big blue blobs)
print()
print("-- big saturated-blue blobs (arrows) in y>250")
sb = (b > 150) & (b - r > 80) & (b - g > 60)
sb[:250, :] = False
lab2, n2 = ndimage.label(sb)
for i in range(1, n2 + 1):
    ys, xs = np.where(lab2 == i)
    if len(ys) < 100: continue
    print(f"   arrow blob n={len(ys)} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} "
          f"in x{xs.min()*IN:.2f}..{xs.max()*IN:.2f} y{ys.min()*IN:.2f}..{ys.max()*IN:.2f}")
