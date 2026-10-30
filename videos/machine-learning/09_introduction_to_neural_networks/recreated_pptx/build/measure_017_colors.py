#!/usr/bin/env python3
"""Classify ink inside slide 017's bottom equation boxes by colour.

Prints, for the left and right box interiors (excluding the border), the
per-row x-runs of RED / GREEN / BLACK / DARK-RED ink so the exact case
layout (brace position, value vs condition columns) can be rebuilt.
"""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "unique_slides/slide_017.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def classify():
    red = (R > 120) & (G < 95) & (B < 95) & (R - G > 65) & (R - B > 65)
    green = (G > 80) & (G - R > 20) & (G - B > 20)
    black = (R < 90) & (G < 90) & (B < 90)
    darkred = (R > 90) & (R < 200) & (G < 70) & (B < 70)
    return {"RED": red, "GREEN": green, "BLACK": black, "DARKRED": darkred}


def runs_in_row(mask, y, x0, x1, minlen=1):
    xs = np.where(mask[y, x0:x1 + 1])[0] + x0
    if len(xs) == 0:
        return []
    out, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i - 1] + 1:
            if xs[i - 1] - s + 1 >= minlen:
                out.append((int(s), int(xs[i - 1])))
            s = xs[i]
    if xs[-1] - s + 1 >= minlen:
        out.append((int(s), int(xs[-1])))
    return out


cls = classify()
for name, (x0, x1, y0, y1) in [("LEFT", (116, 413, 460, 505)),
                               ("RIGHT", (497, 796, 460, 505))]:
    print(f"\n########## {name} box interior x{x0}-{x1} y{y0}-{y1} ##########")
    for cname, m in cls.items():
        total = m[y0:y1 + 1, x0:x1 + 1].sum()
        if total == 0:
            continue
        print(f"\n  --- {cname} ({total} px) ---")
        for y in range(y0, y1 + 1):
            rr = runs_in_row(m, y, x0, x1, minlen=1)
            if rr:
                rr = [r for r in rr if r[1] - r[0] >= 0]
                print(f"    y={y}: {rr}")
