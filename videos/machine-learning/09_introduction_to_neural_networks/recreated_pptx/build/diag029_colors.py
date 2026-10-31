#!/usr/bin/env python3
"""Probe actual pixel colors at known slide-029 feature locations."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_029.jpg"
REND = f"{V}/recreated_pptx/build/slide_029_rejudge_rendered-1.png"

O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
R = np.asarray(Image.open(REND).convert("RGB")).astype(int)
OPPI = O.shape[1] / 13.3333
RPPI = R.shape[1] / 13.3333


def px(a, ppi, xin, yin):
    x = int(round(xin * ppi))
    y = int(round(yin * ppi))
    return tuple(a[y, x])


def median_box(a, ppi, x0, y0, x1, y1):
    xs = slice(int(x0 * ppi) + 2, int(x1 * ppi) - 1)
    ys = slice(int(y0 * ppi) + 2, int(y1 * ppi) - 1)
    sub = a[ys, xs].reshape(-1, 3)
    return tuple(int(v) for v in np.median(sub, axis=0)), len(sub)


PROBES = [
    ("bg field",            4.00, 4.00),
    ("paleyellow LEFT",     2.00, 6.55),
    ("paleyellow CENTER",   5.50, 6.45),
    ("paleyellow RIGHT",   10.00, 6.40),
    ("classbox 1 fill",     8.15, 2.46),
    ("classbox 2 fill",     8.15, 3.43),
    ("classbox 3 fill",     8.15, 4.62),
    ("legend fill",         10.00, 2.10),
    ("note box fill",      10.00, 3.95),
    ("blue callout fill",   3.20, 5.65),
    ("green callout fill",  5.45, 5.65),
    ("magenta InputSample", 1.00, 1.45),
    ("magenta TargetLabel", 8.60, 1.45),
    ("error bar mid",       7.80, 3.50),
    ("error bar mid2",      7.82, 2.30),
    ("error bar mid3",      7.78, 4.80),
    ("panel beige",         1.20, 2.00),
    ("panel beige 2",       7.40, 5.20),
    ("node col3 green fill",6.90 - 1.00, 3.10),
]

print(f"{'probe':26s} {'ORIGINAL px':>18s}   {'RENDER px':>18s}")
for name, x, y in PROBES:
    o = px(O, OPPI, x, y)
    r = px(R, RPPI, x, y)
    print(f"{name:26s} {str(o):>18s}   {str(r):>18s}")

print("\n-- median over small boxes (robust) --")
BOXES = [
    ("error bar O",      7.72, 2.30, 7.92, 2.60),
    ("error bar R",      7.72, 2.30, 7.92, 2.60),
    ("class fill O",     8.05, 2.40, 8.20, 2.52),
    ("class fill R",     8.05, 2.40, 8.20, 2.52),
]
for name, x0, y0, x1, y1 in BOXES:
    o, no = median_box(O, OPPI, x0, y0, x1, y1)
    r, nr = median_box(R, RPPI, x0, y0, x1, y1)
    print(f"{name:26s} O={o} (n={no})   R={r} (n={nr})")
