#!/usr/bin/env python3
"""Probe 18: definitive caption-color classification.

For each of the four caption lines, classify every ink pixel (darker than the
off-white band) as RED (r-g > 25 and r-b > 25, red > 60), BLUE, or DARK
(achromatic or weakly warm: max-min channel <= 25), and report counts plus the
x-extent of each class. This settles whether the captions are red (as the spec
claims) or near-black (as the darkest pixels suggest).
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

band = (r + g + b) <= 690          # ink vs off-white caption background
SAT = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
redish = band & (r - g > 20) & (r - b > 20) & (r > 60)
dark = band & (SAT <= 22)

REGIONS = [
    ("LCAP line1", 100, 470, 487, 505),
    ("LCAP line2", 100, 470, 506, 525),
    ("RCAP line1", 495, 838, 487, 505),
    ("RCAP line2", 495, 838, 506, 525),
]
for nm, x0, x1, y0, y1 in REGIONS:
    rr = redish[y0:y1 + 1, x0:x1 + 1]
    dd = dark[y0:y1 + 1, x0:x1 + 1]
    print(f"\n===== {nm} x{x0}..{x1} y{y0}..{y1} =====")
    for label, m in (("RED", rr), ("DARK", dd)):
        ys, xs = np.where(m)
        if not len(ys):
            print(f"  {label}: 0 px")
            continue
        print(f"  {label}: {m.sum():5d} px  x {x0+xs.min()}..{x0+xs.max()} "
              f"y {y0+ys.min()}..{y0+ys.max()}")
    # sample the most saturated dark-ish pixels overall
    allm = rr | dd
    if allm.sum():
        px = a[y0:y1 + 1, x0:x1 + 1][allm]
        s = px.sum(axis=1)
        dk = px[s < np.percentile(s, 5)]
        print(f"  darkest 5% mean RGB ({dk[:,0].mean():.0f},{dk[:,1].mean():.0f},{dk[:,2].mean():.0f})"
              f"  n={len(dk)}")
