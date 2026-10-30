#!/usr/bin/env python3
"""Slide 041 measurement pass A2: line-band segmentation of the top panel plus
ASCII-art dumps of each text line so glyphs can be read directly.

Banks measurements_a2.json. Panel measured in pass A1: x69..718, y55..129.
"""
import json
import os

import numpy as np
from PIL import Image

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
HERE = os.path.dirname(os.path.abspath(__file__))

a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]

# ink = anything notably darker / more saturated than the pale FFFFCC fill
fill = np.array([255, 247, 224])
d = np.abs(a - fill[None, None, :]).sum(axis=2)
ink = d > 90

# restrict to panel
PANEL = (69, 55, 718, 129)
sub_ink = ink[PANEL[1]:PANEL[3] + 1, PANEL[0]:PANEL[2] + 1]
rows = sub_ink.sum(axis=1)

# group contiguous ink rows into bands (gap >= 3 rows splits)
bands = []
y = 0
n = len(rows)
while y < n:
    if rows[y] > 0:
        y0 = y
        while y < n and rows[y] > 0:
            y += 1
        # extend through small gaps
        yend = y - 1
        gap = 0
        yy = y
        while yy < n and rows[yy] == 0 and gap < 4:
            gap += 1
            yy += 1
        if gap < 4 and yy < n and rows[yy] > 0:
            continue
        bands.append((y0 + PANEL[1], yend + PANEL[1]))
    else:
        y += 1

# merge bands separated by <= 2 rows
merged = []
for b in bands:
    if merged and b[0] - merged[-1][1] <= 2:
        merged[-1] = (merged[-1][0], b[1])
    else:
        merged.append(list(b))
bands = [tuple(b) for b in merged]

print("PANEL ink row bands (frame px):")
for b in bands:
    seg = sub_ink[b[0] - PANEL[1]:b[1] - PANEL[1] + 1]
    cols = np.where(seg.sum(axis=0) > 0)[0]
    print("  y %d..%d (h=%d)  x %d..%d" % (b[0], b[1], b[1] - b[0] + 1,
                                           PANEL[0] + cols.min(), PANEL[0] + cols.max()))

# column groups within each band
print("\nPANEL column groups per band:")
detail = {}
for b in bands:
    seg = sub_ink[b[0] - PANEL[1]:b[1] - PANEL[1] + 1]
    cs = seg.sum(axis=0)
    groups = []
    x = 0
    m = len(cs)
    while x < m:
        if cs[x] > 0:
            x0 = x
            while x < m and cs[x] > 0:
                x += 1
            groups.append((x0 + PANEL[0], x - 1 + PANEL[0]))
        else:
            x += 1
    # merge groups separated by <= 2 px
    mg = []
    for g in groups:
        if mg and g[0] - mg[-1][1] <= 2:
            mg[-1] = (mg[-1][0], g[1])
        else:
            mg.append(list(g))
    groups = [tuple(g) for g in mg]
    detail[str(b)] = groups
    print("  y %d..%d: %s" % (b[0], b[1], groups))

with open(os.path.join(HERE, "measurements_a2.json"), "w") as f:
    json.dump({"panel": list(PANEL), "bands": [list(b) for b in bands],
               "groups": {k: [list(g) for g in v] for k, v in detail.items()}}, f, indent=1)

# ASCII dump helper
def dump(x0, y0, x1, y1, title, sx=1, sy=1):
    print("\n=== %s  (x%d..%d y%d..%d) ===" % (title, x0, x1, y0, y1))
    seg = ink[y0:y1 + 1, x0:x1 + 1]
    hs, ws = seg.shape
    ho, wo = hs // sy, ws // sx
    for r in range(ho):
        line = ""
        for c in range(wo):
            blk = seg[r * sy:(r + 1) * sy, c * sx:(c + 1) * sx]
            line += "#" if blk.any() else "."
        print(line)


def hexclass(y0, y1, x0, x1):
    seg = a[y0:y1 + 1, x0:x1 + 1]
    m = ink[y0:y1 + 1, x0:x1 + 1]
    px = seg[m]
    if not len(px):
        return {}
    # classify
    red = ((px[:, 0] - px[:, 1] > 60) & (px[:, 0] - px[:, 2] > 60)).sum()
    blue = ((px[:, 2] - px[:, 0] > 60) & (px[:, 2] - px[:, 1] > 30)).sum()
    green = ((px[:, 1] - px[:, 0] > 40) & (px[:, 1] - px[:, 2] > 40)).sum()
    dark = ((px.max(axis=1) - px.min(axis=1) < 60) & (px.mean(axis=1) < 120)).sum()
    navy = ((px[:, 2] - px[:, 0] > 40) & (px[:, 2] - px[:, 1] > 40) & (px.max(axis=1) < 190)).sum()
    return {"red": int(red), "blue": int(blue), "green": int(green),
            "dark": int(dark), "navy": int(navy), "n": int(len(px))}
