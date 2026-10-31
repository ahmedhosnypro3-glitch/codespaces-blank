#!/usr/bin/env python3
"""Slide 024: exact panel rectangles via row-run analysis of non-background ink."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

BG = np.array([232, 232, 230])
# panel-ish: white fill, peach fill, border colors, or dark ink; NOT background gray,
# NOT the pure frame-red lines, NOT the badge yellow.
WHITE = (r > 243) & (g > 243) & (b > 243)
PEACH = (r > 236) & (g > 208) & (g < 248) & (b > 186) & (b < 240) & (r - g > 8)
BORDER_ISH = (np.abs(o - BG).sum(axis=2) > 40) & ~WHITE & ~PEACH
panel = WHITE | PEACH | BORDER_ISH
# drop the outer frame columns and badge/title rows
panel[:, :66] = False; panel[:, 856:] = False
panel[:95, :] = False
panel[486:, :] = False

print("=== row runs (panel interiors), y 96..485 ===")
prev_runs = None
for y in range(96, 486):
    row = panel[y, 66:856]
    xs = np.nonzero(row)[0]
    if not len(xs):
        print(y, "-"); continue
    # group with gap tolerance 3
    grp, st = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i-1] > 5:
            grp.append((st + 66, xs[i-1] + 66)); st = xs[i]
    grp.append((st + 66, xs[-1] + 66))
    # merge tiny groups
    grp = [g2 for g2 in grp if g2[1] - g2[0] > 15]
    key = tuple(grp)
    if key != prev_runs:
        print(y, grp)
        prev_runs = key
