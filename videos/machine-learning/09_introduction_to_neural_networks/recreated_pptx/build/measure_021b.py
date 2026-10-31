#!/usr/bin/env python3
"""Precise panel/frame measurement for slide_021.jpg."""
import numpy as np
from PIL import Image

try:
    from scipy import ndimage
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

pink = (R > 240) & (G > 200) & (G < 244) & (B > 200) & (B < 244) & (R - B > 12)
blue = (B > 110) & (B - R > 45) & (B - G > 45)
red_loose = (R > 115) & (R - G > 28) & (R - B > 28)
black = (R < 90) & (G < 90) & (B < 90)
yellow = (R > 235) & (G > 225) & (B < 200) & (R - B > 40)


def runs(vals, cond):
    out, start = [], None
    for i, v in enumerate(vals):
        if cond(v) and start is None:
            start = i
        elif not cond(v) and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(vals) - 1))
    return out


print("=== PINK components ===")
if HAVE_SCIPY:
    lab, n = ndimage.label(pink)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) > 400:
            print(f"  comp{i}: n={len(xs)} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
else:
    print("  no scipy")

print("\n=== BLUE vertical lines (col counts > 40) ===")
bc = blue.sum(axis=0)
for x in np.nonzero(bc > 40)[0]:
    rr = runs(blue[:, x], lambda v: v)
    print(f"  col {x}: count={bc[x]} rows {rr}")

print("\n=== BLUE horizontal lines (row counts > 40) ===")
br = blue.sum(axis=1)
for y in np.nonzero(br > 40)[0]:
    rr = runs(blue[y, :], lambda v: v)
    print(f"  row {y}: count={br[y]} cols {rr}")

print("\n=== RED loose: row profile (count>30) ===")
rl = red_loose.sum(axis=1)
for y in np.nonzero(rl > 30)[0]:
    print(f"  row {y}: {rl[y]} cols {runs(red_loose[y,:], lambda v: v)}")

print("\n=== RED loose: col profile (count>30) ===")
cl = red_loose.sum(axis=0)
for x in np.nonzero(cl > 30)[0]:
    print(f"  col {x}: {cl[x]} rows {runs(red_loose[:,x], lambda v: v)}")

print("\n=== BLACK rows (count>200) ===")
bk = black.sum(axis=1)
for y in np.nonzero(bk > 200)[0]:
    print(f"  row {y}: {bk[y]} cols {runs(black[y,:], lambda v: v)}")

print("\n=== YELLOW badge ===")
if HAVE_SCIPY:
    lab, n = ndimage.label(yellow)
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) > 100:
            print(f"  comp{i}: n={len(xs)} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
print("  yellow pixels in x 750..830, y 20..90:",
      [(int(x), int(y), tuple(a[y, x])) for y in range(30, 80, 6) for x in range(760, 830, 10) if yellow[y, x]])
