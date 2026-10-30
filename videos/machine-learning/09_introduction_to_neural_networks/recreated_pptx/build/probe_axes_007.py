#!/usr/bin/env python3
"""Probe red axes, arrowheads and text positions in slide 007 original."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def reddish(x, y):
    px = a[y, x]
    return px, bool(px[0] > 140 and px[0] - px[1] > 60 and px[0] - px[2] > 60)


def runs_along_col(x, y0, y1):
    out = []
    for y in range(y0, y1):
        px, ok = reddish(x, y)
        if ok:
            out.append((y, tuple(int(v) for v in px)))
    return out


def runs_along_row(y, x0, x1):
    out = []
    for x in range(x0, x1):
        px, ok = reddish(x, y)
        if ok:
            out.append((x, tuple(int(v) for v in px)))
    return out


print("== vertical probes (looking for a red vertical axis) ==")
for x in (288, 290, 291, 292, 293, 294, 372, 374, 375, 376, 377, 378, 380):
    rr = runs_along_col(x, 115, 478)
    if rr:
        ys = [t[0] for t in rr]
        print(f"x={x}: n={len(rr)} y={min(ys)}..{max(ys)} sample={rr[:3]} {rr[-2:]}")

print("== horizontal probes (looking for a red horizontal axis) ==")
for y in (410, 412, 414, 415, 416, 417, 418, 420, 430, 432, 434, 435, 436, 437, 438):
    rr = runs_along_row(y, 160, 755)
    if rr:
        xs = [t[0] for t in rr]
        print(f"y={y}: n={len(rr)} x={min(xs)}..{max(xs)} sample={rr[:3]} {rr[-2:]}")

print("== red thick clusters (arrowheads) ==")
red = (r > 140) & (r - g > 60) & (r - b > 60)
from scipy import ndimage

lab, n = ndimage.label(red)
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 150:
        continue
    if not (115 <= ys.min() and ys.max() <= 477 and 156 <= xs.min() and xs.max() <= 756):
        continue
    w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    if w <= 26 and h <= 26:
        continue
    print(f"  blob n={len(xs)} bbox=[{xs.min()},{ys.min()},{xs.max()},{ys.max()}] w={w} h={h}")

print("== black text blobs inside panel (the '+ve' labels) ==")
black = (r < 110) & (g < 110) & (b < 110)
lab, n = ndimage.label(black)
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 12:
        continue
    if not (115 <= ys.min() and ys.max() <= 477 and 156 <= xs.min() and xs.max() <= 756):
        continue
    print(f"  black n={len(xs)} bbox=[{xs.min()},{ys.min()},{xs.max()},{ys.max()}]")
