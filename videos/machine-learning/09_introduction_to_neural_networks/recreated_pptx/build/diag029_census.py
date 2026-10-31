#!/usr/bin/env python3
"""Census the MODE (most common) RGB inside each slide-029 feature region."""
import numpy as np
from PIL import Image
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_029.jpg"
REND = f"{V}/recreated_pptx/build/slide_029_rejudge_rendered-1.png"

O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
R = np.asarray(Image.open(REND).convert("RGB")).astype(int)
OPPI = O.shape[1] / 13.3333
RPPI = R.shape[1] / 13.3333

# (label, x0,y0,x1,y1) in INCHES - interior of the fill, away from text
REGIONS = [
    ("bg outside panel L",        0.30, 0.90, 0.85, 1.20),
    ("bg outside panel R",        9.50, 5.10, 12.00, 5.70),
    ("panel beige interior",      1.10, 4.90, 7.40, 5.20),
    ("paleyellow LEFT",           1.20, 6.50, 3.20, 6.85),
    ("paleyellow CENTER",         4.30, 6.45, 6.90, 6.85),
    ("paleyellow RIGHT",          9.40, 6.35, 11.80, 6.90),
    ("classbox 1 fill",           8.05, 2.38, 8.20, 2.55),
    ("classbox 2 fill",           8.05, 3.35, 8.20, 3.52),
    ("classbox 3 fill",           8.05, 4.54, 8.20, 4.71),
    ("legend fill",              10.50, 2.05, 11.50, 2.15),
    ("note box fill",             9.60, 3.83, 11.00, 3.95),
    ("blue callout fill",         3.15, 5.62, 3.95, 5.90),
    ("green callout fill",        5.40, 5.62, 6.30, 5.90),
    ("magenta InputSample fill",  0.95, 1.42, 1.25, 1.55),
    ("magenta TargetLabel fill",  8.58, 1.40, 8.90, 1.52),
    ("error bar mid",             7.75, 2.30, 7.90, 2.60),
    ("error bar lower",           7.75, 4.60, 7.90, 4.90),
    ("node col1 outline area",    2.00, 2.35, 2.20, 2.50),
    ("node col3 fill",            5.80, 3.30, 6.10, 3.55),
]


def mode_colors(a, ppi, x0, y0, x1, y1, k=4):
    xs = slice(int(round(x0 * ppi)), int(round(x1 * ppi)))
    ys = slice(int(round(y0 * ppi)), int(round(y1 * ppi)))
    sub = a[ys, xs].reshape(-1, 3)
    c = Counter(map(tuple, sub.tolist()))
    out = []
    for col, n in c.most_common(k):
        out.append(f"#{col[0]:02X}{col[1]:02X}{col[2]:02X} ({100*n/len(sub):.0f}%)")
    return len(sub), out


print(f"{'region':28s} {'n':>7s}  ORIGINAL mode colors")
for name, x0, y0, x1, y1 in REGIONS:
    n, o = mode_colors(O, OPPI, x0, y0, x1, y1)
    print(f"{name:28s} {n:7d}  {' | '.join(o)}")

print()
print(f"{'region':28s} {'n':>7s}  RENDER mode colors")
for name, x0, y0, x1, y1 in REGIONS:
    n, r = mode_colors(R, RPPI, x0, y0, x1, y1)
    print(f"{name:28s} {n:7d}  {' | '.join(r)}")
