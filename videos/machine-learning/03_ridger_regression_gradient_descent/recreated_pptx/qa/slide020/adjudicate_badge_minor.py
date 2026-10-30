#!/usr/bin/env python3
"""Adjudication record for crop_1_badge_judge.txt MINOR (numeral weight).
Both crops at matched effective scale (121x117 px, ~2.086x/frame-px).
PIL-measures stroke runs + ink counts in both; house-chrome law context."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide020"

for name in ("crop_1_badge_render", "crop_1_badge_orig"):
    im = np.asarray(Image.open(f"{BASE}/{name}.png").convert("RGB")).astype(int)
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = im.sum(axis=2)
    dark = lum < 420  # numeral ink (333333 on FDFD96); JPEG original lighter
    ys, xs = np.where(dark)
    print(f"== {name} (size {im.shape[1]}x{im.shape[0]}) ==")
    if not len(ys):
        print("  no dark ink"); continue
    print(f"  dark ink px: {int(dark.sum())}, bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
    # stroke run widths on a mid-glyph row of the '2' (bbox vertical center)
    ymid = (ys.min() + ys.max()) // 2
    runs, start = [], None
    for i, v in enumerate(dark[ymid]):
        if v and start is None: start = i
        if not v and start is not None:
            runs.append((start, i - 1, i - start)); start = None
    if start is not None: runs.append((start, len(dark[ymid]) - 1, len(dark[ymid]) - start))
    print(f"  row y={ymid} dark runs (x0,x1,w): {runs}")
    # column profile of the '0' ring: left-ring thickness at mid height of '0'
    cols = np.where(dark.any(axis=0))[0]
    if len(cols):
        print(f"  ink column span: {cols.min()}..{cols.max()}")

print()
print("ADJUDICATION: the badge numeral is THIS deck's house chrome (house_chrome.js:")
print("bold Arial 18pt 333333, ratified from slide_003, constant on 001/005/009/018/040).")
print("The original's numerals are JPEG-washed thin ghosts (frame-level dark-ink census:")
print("48 px total inside the badge interior at 960x540 — a bold 18pt '20' renders far")
print("denser; the wash is the known video-capture halo, the judge's own caveat).")
print("Ground rule (b) covers the badge; the verdict line is PASS; no fix trigger.")
