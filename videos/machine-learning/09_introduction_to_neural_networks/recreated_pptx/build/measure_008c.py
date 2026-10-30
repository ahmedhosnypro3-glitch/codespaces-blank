#!/usr/bin/env python3
"""Hue-based structural measurement of the ORIGINAL slide_008 frame."""
import numpy as np
from PIL import Image
from collections import Counter

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(ORIG).convert("RGB").resize((960, 540), Image.LANCZOS)
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

def hsv_mask(lo, hi, smin, vmin):
    # compute hue in degrees
    diff = mx - mn
    with np.errstate(divide="ignore", invalid="ignore"):
        idx = (diff == 0)
        h = np.zeros_like(mx, dtype=float)
        m = (mx == r) & ~idx
        h[m] = ((g - b)[m] / diff[m]) % 6
        m = (mx == g) & ~idx
        h[m] = (b - r)[m] / diff[m] + 2
        m = (mx == b) & ~idx
        h[m] = (r - g)[m] / diff[m] + 4
        h = h * 60
    return (h >= lo) & (h < hi) & (sat >= smin) & (mx >= vmin)

def blobs(name, mask, grid=12, topn=8):
    ys, xs = np.nonzero(mask)
    n = len(xs)
    if n == 0:
        print(f"{name:16s} n=0")
        return
    c = Counter((int(x // grid), int(y // grid)) for x, y in zip(xs, ys))
    # merge into weighted centers of top cells
    tot = sum(c.values())
    print(f"{name:16s} n={n:6d} grid={grid} cells={len(c)}")
    for (cx, cy), v in c.most_common(topn):
        print(f"    cell({cx},{cy}) n={v}  -> px ~[{cx*grid}-{(cx+1)*grid}, {cy*grid}-{(cy+1)*grid}]")

# 1. plot frame: red saturated pixels, look for long horizontal/vertical runs
red = hsv_mask(0, 12, 0.5, 60) | ((r - 90 > g + 40) & (r - 90 > b + 40))
rows = red.sum(axis=1)
cols = red.sum(axis=0)
print("=== plot frame search (red long lines) ===")
print("row sums > 200:", [(i, int(rows[i])) for i in np.nonzero(rows > 200)[0]])
print("col sums > 150:", [(i, int(cols[i])) for i in np.nonzero(cols > 150)[0]][:20])

print("\n=== hue masks (original) ===")
blobs("red(h0-12)", hsv_mask(0, 12, 0.45, 50))
blobs("red(345-360)", hsv_mask(340, 361, 0.45, 50))
blobs("green", hsv_mask(90, 170, 0.45, 50))
blobs("blue", hsv_mask(180, 260, 0.45, 50))
blobs("yellow", hsv_mask(35, 65, 0.55, 120))
blobs("orange", hsv_mask(12, 35, 0.55, 120))

# bounding rows for green dots only (small saturated green dots)
print("\n=== green detail ===")
gm = hsv_mask(90, 170, 0.5, 80)
ys, xs = np.nonzero(gm)
print("green count", len(xs))
# exclude the big green arrow line: use small-blob morphology via 3x3 erosion
from scipy import ndimage as ndi
try:
    lbl, n = ndi.label(gm)
    sizes = ndi.sum(gm, lbl, range(1, n + 1))
    print(f"green components={n} top sizes={sorted([int(s) for s in sizes], reverse=True)[:14]}")
    big = np.argwhere(sizes > 40).flatten() + 1
    dots = dict(zip(range(1, n + 1), sizes))
    dotmask = np.isin(lbl, [k for k, v in dots.items() if v <= 40])
    ys, xs = np.nonzero(dotmask)
    if len(xs):
        print(f"green DOT pixels={len(xs)} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
        print("  dot blob centers:", sorted(set((int(x // 8) * 8, int(y // 8) * 8) for x, y in zip(xs, ys)))[:20])
except Exception as e:
    print("scipy unavailable:", e)
