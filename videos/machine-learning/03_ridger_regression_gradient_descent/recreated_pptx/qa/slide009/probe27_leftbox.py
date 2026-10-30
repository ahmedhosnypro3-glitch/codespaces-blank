#!/usr/bin/env python3
"""Probe 27: LEFT annotation box, measured the same way the RIGHT one was
(fixed white predicate: panel interior measures (250,252,249)).
Reports its border columns/rows, fill color, and the equation ink inside.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
WHT = (r > 244) & (g > 244) & (b > 243)
NOTW = ~WHT


def lr(mask):
    best = (0, 0, 0)
    cur = 0
    st = 0
    for i, v in enumerate(mask):
        if v:
            if cur == 0:
                st = i
            cur += 1
            if cur > best[0]:
                best = (cur, st, i)
        else:
            cur = 0
    return best


print("########## LEFT annotation box: scan columns x 190..340 ##########")
for xx in range(196, 340):
    n, s, e = lr(NOTW[130:200, xx])
    if n >= 20:
        print(f"  x={xx}: vertical non-white run y {130+s}..{130+e} (n={n})")

print("\n########## LEFT rows y 140..182, longest runs ##########")
for y in range(140, 183):
    n, s, e = lr(NOTW[y, 190:340])
    if n >= 10:
        print(f"  y={y}: run x {190+s}..{190+e} (n={n})")

print("\n########## fill samples along the LEFT box ##########")
for y in (148, 152, 155, 170, 174):
    print(f"  y={y}:", [tuple(a[y, x]) for x in (216, 220, 240, 300, 312, 316)])

print("\n########## ink (achromatic black, sum<460, SAT<=50) in LEFT box ##########")
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
BLK = ((r + g + b) < 460) & ((mx - mn) <= 50)
sub = BLK[144:180, 210:320]
ys, xs = np.where(sub)
print(f"  ink x {210+xs.min()}..{210+xs.max()} (w={xs.max()-xs.min()+1}) "
      f"y {144+ys.min()}..{144+ys.max()} (h={ys.max()-ys.min()+1})")
print("  per-row ink spans:")
for i in range(sub.shape[0]):
    if sub[i].sum():
        w = np.where(sub[i])[0]
        print(f"    y={144+i}: x {210+w.min()}..{210+w.max()} n={sub[i].sum()}")
