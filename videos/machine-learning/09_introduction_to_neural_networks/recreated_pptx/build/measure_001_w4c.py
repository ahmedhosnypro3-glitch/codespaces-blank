#!/usr/bin/env python3
"""slide_001 w4: region ink geometry, ORIGINAL vs fresh RENDER, crop to frame interior."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_001.jpg"
RENDER = f"{V}/recreated_pptx/build/slide_001_rendered-1.png"

REGIONS = [
    ("title",       1.30, 0.80, 12.00, 3.90),
    ("subtitle",    1.30, 3.90, 12.00, 4.55),
    ("prepared",    1.30, 4.55, 12.00, 5.75),
    ("instructors", 1.30, 5.75, 7.50, 7.45),
    ("logo",        7.50, 5.75, 12.00, 7.45),
]


def bands(a, sx, sy, box):
    H, W = a.shape[:2]
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    ink = L < 175
    px0, py0 = int(box[0] * sx), int(box[1] * sy)
    px1, py1 = min(W, int(box[2] * sx)), min(H, int(box[3] * sy))
    m = np.zeros_like(ink)
    m[py0:py1, px0:px1] = ink[py0:py1, px0:px1]
    rows = m.sum(axis=1)
    span = px1 - px0
    ruled = rows > 0.6 * span
    res, inb = [], False
    for y in range(H):
        hot = rows[y] > 1 and not ruled[y]
        if hot and not inb:
            st, inb = y, True
        elif not hot and inb:
            res.append((st, y - 1))
            inb = False
    if inb:
        res.append((st, H - 1))
    out = []
    for (a0, a1) in res:
        sub = m[a0:a1 + 1]
        if sub.sum() < 12:
            continue
        xs = np.nonzero(sub.sum(axis=0) > 0)[0]
        if len(xs) < 2:
            continue
        out.append((a0 / sy, (a1 + 1) / sy, xs.min() / sx, (xs.max() + 1) / sx, int(sub.sum())))
    return out


o = np.asarray(Image.open(ORIG).convert("RGB")).astype(float)
r = np.asarray(Image.open(RENDER).convert("RGB")).astype(float)
for name, a, sx, sy in (("ORIGINAL", o, 72.0, 518.0 / 7.5), ("RENDER", r, 150.0, 150.0)):
    print("=" * 92)
    print("### %s" % name)
    for reg, x0, y0, x1, y1 in REGIONS:
        print("-- %-12s [x %.2f-%.2f y %.2f-%.2f]" % (reg, x0, y0, x1, y1))
        for (ya0, ya1, xa0, xa1, n) in bands(a, sx, sy, (x0, y0, x1, y1)):
            print("     y %5.2f-%5.2f  x %5.2f-%5.2f  w=%5.2f h=%5.2f  ink=%6d"
                  % (ya0, ya1, xa0, xa1, xa1 - xa0, ya1 - ya0, n))
