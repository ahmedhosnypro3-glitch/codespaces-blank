#!/usr/bin/env python3
"""Locate the small black text glyph clusters (tick labels / axis labels) inside
each slide_021 graph panel, so the axes geometry can be pinned down."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

FRAMES = {"TL": (121, 109, 400, 272), "TR": (563, 109, 842, 275),
          "BL": (121, 346, 400, 508), "BR": (564, 346, 842, 508)}

for name, (x0, y0, x1, y1) in FRAMES.items():
    sub = a[y0:y1 + 1, x0:x1 + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    # dark neutral ink (black text / black axes)
    dark = (sr < 155) & (sg < 155) & (sb < 155) & \
           (np.maximum.reduce([sr, sg, sb]) - np.minimum.reduce([sr, sg, sb]) < 45)
    print(f"\n=== {name} (frame x{x0}..{x1} y{y0}..{y1}) ===")
    # connected components (4-neighbour) via simple BFS
    lab = np.zeros(dark.shape, int)
    cur = 0
    H, Wd = dark.shape
    for yy in range(H):
        for xx in range(Wd):
            if dark[yy, xx] and lab[yy, xx] == 0:
                cur += 1
                stack = [(yy, xx)]
                lab[yy, xx] = cur
                while stack:
                    cy, cx = stack.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < Wd and dark[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur
                            stack.append((ny, nx))
    comps = []
    for c in range(1, cur + 1):
        ys, xs = np.nonzero(lab == c)
        if len(xs) >= 2:
            comps.append((y0 + ys.min(), y0 + ys.max(), x0 + xs.min(), x0 + xs.max(), len(xs)))
    comps.sort()
    for t, b, l, r, n in comps:
        print(f"   dark blob x{l}..{r} y{t}..{b} n={n} (h={b-t+1},w={r-l+1})")
