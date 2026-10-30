#!/usr/bin/env python3
"""Probe 8k: sub-pixel tracking of the four let-box delimiter strokes (orig + render, left + right box).

Per box: ink runs per row inside a stroke x-window, every 4 rows, with mean RGB per run,
plus column ink-profile so stroke columns are exact.
"""
from PIL import Image
import numpy as np

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB")).astype(int)

CASES = [
    ("ORIG left box", ORIG, 140, 215),
    ("REND left box", REND, 140, 215),
    ("ORIG right box", ORIG, 465, 555),
    ("REND right box", REND, 465, 555),
]

def runs_in_row(row_mask, x0):
    out = []
    in_run = False
    for i, v in enumerate(row_mask):
        if v and not in_run:
            start = i; in_run = True
        elif not v and in_run:
            out.append((x0 + start, x0 + i - 1)); in_run = False
    if in_run:
        out.append((x0 + start, x0 + len(row_mask) - 1))
    return out

for label, img, wx0, wx1 in CASES:
    print(f"===== {label} stroke window x{wx0}..{wx1}, y95..220 =====")
    reg = img[95:220, wx0:wx1]
    ink = reg.min(axis=2) < 215
    # column profile
    colsum = ink.sum(axis=0)
    prof = "".join(str(min(9, colsum[i] // 4)) for i in range(0, wx1 - wx0))
    print(f"col ink profile (x{wx0}+i, digit=ink-rows/4): {prof}")
    peaks = [wx0 + i for i in range(len(colsum)) if colsum[i] >= 30]
    print(f"columns with >=30 ink rows: {peaks}")
    for yy in range(0, 220 - 95, 4):
        rr = runs_in_row(ink[yy], wx0)
        if not rr:
            continue
        parts = []
        for (a, b) in rr:
            seg = img[95 + yy, a:b + 1]
            m = seg.mean(axis=0).astype(int)
            parts.append(f"x{a}..{b} rgb({m[0]},{m[1]},{m[2]})")
        print(f"  y{95+yy:3d}: " + "  |  ".join(parts))
    print()
