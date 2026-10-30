#!/usr/bin/env python3
"""Measure slide 007 original frame: panel, axes, lines, hatch regions, dots."""
import json
from collections import defaultdict

import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("frame size", W, H)

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def mask_close(rgb, tol=28):
    m = np.ones((H, W), bool)
    for i in range(3):
        m &= np.abs(a[:, :, i] - rgb[i]) <= tol
    return m


def bbox(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


def summarize(name, m):
    bb = bbox(m)
    print(f"{name}: n={int(m.sum())} bbox={bb}")
    return bb


strong_red = (r > 170) & (g < 90) & (b < 90)
strong_blue = (b > 150) & (r < 110) & (g < 130)
strong_green = (g > 110) & (r < 120) & (b < 120)
yellow = (r > 200) & (g > 190) & (b < 140)
black = (r < 90) & (g < 90) & (b < 90)

# --- panel border: find the inner maroon rectangle (thin, ~#C00000)
maroon = (r > 140) & (r < 220) & (g < 70) & (b < 70)
ys, xs = np.nonzero(maroon)
print("maroon bbox", xs.min(), ys.min(), xs.max(), ys.max())

# vertical maroon runs: look for long vertical lines in the plot area
panel = maroon.copy()
panel[:100, :] = False
panel[500:, :] = False
col_counts = panel.sum(axis=0)
row_counts = panel.sum(axis=1)
print("top maroon columns", sorted([(int(c), i) for i, c in enumerate(col_counts)], reverse=True)[:8])
print("top maroon rows", sorted([(int(c), i) for i, c in enumerate(row_counts)], reverse=True)[:8])

# --- axes (red) inside plot: separate from decision line d1
# vertical axis: column with many strong_red pixels between y 120..430
inner = strong_red.copy()
inner[:115, :] = False
inner[485:, :] = False
cc = inner.sum(axis=0)
print("red column counts top:", sorted([(int(c), i) for i, c in enumerate(cc)], reverse=True)[:10])
rr = inner.sum(axis=1)
print("red row counts top:", sorted([(int(c), i) for i, c in enumerate(rr)], reverse=True)[:10])

# --- hatch colors
hatch_green = mask_close((169, 224, 169), 22)
hatch_blue = mask_close((154, 154, 240), 26)
hatch_pink = mask_close((229, 169, 169), 22)
summarize("hatch_green", hatch_green)
summarize("hatch_blue", hatch_blue)
summarize("hatch_pink", hatch_pink)

# row spans of each hatch family
for name, m in [("green", hatch_green), ("blue", hatch_blue), ("pink", hatch_pink)]:
    rows = defaultdict(list)
    for y in range(H):
        xs2 = np.nonzero(m[y])[0]
        if len(xs2):
            rows[y] = [int(xs2.min()), int(xs2.max()), int(len(xs2))]
    ys2 = sorted(rows)
    if not ys2:
        continue
    print(f"--- {name} hatch rows {ys2[0]}..{ys2[-1]}")
    for y in ys2:
        lo, hi, n = rows[y]
        print(f"  y={y} x={lo}..{hi} n={n}")

# --- dots: saturated fills
print("--- strong color dot clusters")
for name, m in [("red", strong_red), ("green", strong_green), ("blue", strong_blue)]:
    mm = m.copy()
    mm[:115, :] = False
    mm[485:, :] = False
    mm[:, :150] = False
    mm[:, 765:] = False
    # remove line pixels: keep only blobs (use simple labeling)
    from scipy import ndimage

    lab, n = ndimage.label(mm)
    out = []
    for i in range(1, n + 1):
        ys3, xs3 = np.nonzero(lab == i)
        if len(xs3) < 40:
            continue
        out.append((int(xs3.mean()), int(ys3.mean()), len(xs3), int(xs3.min()), int(xs3.max()), int(ys3.min()), int(ys3.max())))
    print(name, "blobs:", sorted(out))
