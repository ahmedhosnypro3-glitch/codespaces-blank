#!/usr/bin/env python3
"""Longest-run analysis to separate real gridlines from label text, per panel."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

FRAMES = {"TL": (121, 109, 400, 272), "TR": (563, 109, 842, 275),
          "BL": (121, 346, 400, 508), "BR": (564, 346, 842, 508)}

# any ink that is not white: gridlines (light gray), axes (black), curves (colored), text (black)
def nonwhite(sub):
    return (sub.max(axis=2) < 248) | (sub.min(axis=2) < 248)


def longest_run(row):
    best = cur = 0
    start = bs = None
    for i, v in enumerate(row):
        if v:
            if cur == 0:
                start = i
            cur += 1
            if cur > best:
                best, bs = cur, start
        else:
            cur = 0
    return best, bs


for name, (x0, y0, x1, y1) in FRAMES.items():
    sub = a[y0:y1 + 1, x0:x1 + 1]
    ink = nonwhite(sub)
    H, Wd = ink.shape
    print(f"\n=== {name} frame x{x0}..{x1} y{y0}..{y1} (w={Wd},h={H}) ===")
    print("  ROWS with long ink run (>0.55*W):")
    for yy in range(H):
        b, s = longest_run(ink[yy])
        if b > Wd * 0.55:
            print(f"    y={y0+yy}: run {b} from x{x0+s}")
    print("  COLS with long ink run (>0.45*H):")
    for xx in range(Wd):
        b, s = longest_run(ink[:, xx])
        if b > H * 0.45:
            print(f"    x={x0+xx}: run {b} from y{y0+s}")
