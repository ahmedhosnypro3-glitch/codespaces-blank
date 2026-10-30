#!/usr/bin/env python3
"""att9 follow-ups: (a) per-band digit x-centres rows 2-6; (b) calc-gap fill."""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
SUM = O48.sum(axis=2)

# digit sub-bands measured by measure_rows456.py: (row, y0, y1, xsearch)
BANDS = [
    (2, 218, 227, "5"), (2, 234, 244, "-1a"), (2, 249, 259, "-1b"),
    (3, 281, 290, "5"), (3, 297, 307, "-1a"), (3, 312, 322, "-1b"),
    (4, 350, 360, "5"), (4, 366, 376, "-1a"), (4, 382, 391, "-1b"),
    (5, 413, 423, "5"), (5, 429, 438, "-1a"), (5, 444, 454, "-1b"),
    (6, 479, 489, "5"), (6, 496, 505, "-1a"), (6, 511, 520, "-1b"),
]
print("===== digit-band x-centres (x725..756, thr<200) =====")
for r, y0, y1, tag in BANDS:
    zone = SUM[y0:y1, 725:757] < 600
    colmask = zone.any(axis=0)
    runs, s = [], None
    for i, v in enumerate(colmask):
        if v and s is None: s = i
        elif not v and s is not None: runs.append((725 + s, 725 + i - 1)); s = None
    if s is not None: runs.append((725 + s, 756))
    centres = [f"x{a}..{b}(c{(a + b) / 2:.1f})" for a, b in runs]
    print(f"  r{r} {tag} y{y0}..{y1}: {' '.join(centres)}")

print("\n===== calc-gap fill census (mid-gap rows, x300..840) =====")
for y, tag in [(144, "in box1"), (168, "in box1"), (201, "gap 197/206"),
               (230, "in box2"), (267, "gap 263/272"), (295, "in box3"),
               (334, "gap 330/338"), (365, "in box4"), (400, "gap 395/404"),
               (430, "in box5"), (466, "gap 461/470"), (500, "in box6")]:
    row = O48[y, 300:841]
    print(f"  y{y} ({tag}): mean={row.mean(axis=0).astype(int)} min={row.min()}")

print("\n===== 049 gap-fill comparison (same rows) =====")
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
for y in [201, 267, 334, 400, 466]:
    row = O49[y, 300:841]
    print(f"  y{y}: mean={row.mean(axis=0).astype(int)} min={row.min()}")
