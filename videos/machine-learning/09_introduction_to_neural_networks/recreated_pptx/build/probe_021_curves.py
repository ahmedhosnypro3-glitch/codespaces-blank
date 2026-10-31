#!/usr/bin/env python3
"""Trace the coloured curves and locate the small black text labels in each
slide_021 graph panel."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

FRAMES = {"TL": (121, 109, 400, 272), "TR": (563, 109, 842, 275),
          "BL": (121, 346, 400, 508), "BR": (564, 346, 842, 508)}


def trace(name, x0, y0, x1, y1, maskfn, label):
    sub = a[y0:y1 + 1, x0:x1 + 1]
    m = maskfn(sub[:, :, 0], sub[:, :, 1], sub[:, :, 2])
    print(f"\n--- {name} {label}: n={int(m.sum())}")
    ys, xs = np.nonzero(m)
    if not len(xs):
        print("   none")
        return
    print(f"   bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()}")
    # print x-centroid per row, every 6 rows
    for yy in range(y0, y1 + 1, 6):
        sel = np.nonzero(m[yy - y0])[0]
        if len(sel):
            # split into runs
            runs = []
            st = sel[0]; prev = sel[0]
            for v in sel[1:]:
                if v != prev + 1:
                    runs.append((st, prev)); st = v
                prev = v
            runs.append((st, prev))
            print(f"   y={yy}: " + " ".join(f"[{x0+s}..{x0+e}]" for s, e in runs))


def red_mask(r, g, b):
    return (r - g > 25) & (r - b > 25) & (r > 100)


def blue_mask(r, g, b):
    return (b - r > 45) & (b - g > 35) & (b > 100)


def orange_mask(r, g, b):
    return (r - b > 55) & (g - b > 20) & (r > 150) & (g > 80)


def green_mask(r, g, b):
    return (g - r > 40) & (g - b > 30) & (g > 90)


for name, (x0, y0, x1, y1) in FRAMES.items():
    trace(name, x0, y0, x1, y1, red_mask, "RED")
    trace(name, x0, y0, x1, y1, blue_mask, "BLUE")
    trace(name, x0, y0, x1, y1, orange_mask, "ORANGE")
    trace(name, x0, y0, x1, y1, green_mask, "GREEN")
