#!/usr/bin/env python3
"""Structural RLE map of the ORIGINAL frame: per row (step 4px), the x-runs of
each non-white, non-panel colour class. Gives box borders, band extents, fills
and the stacked-column geometry in one artifact."""
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
OG = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)
H, W = OG.shape[:2]
r, g, b = OG[:, :, 0], OG[:, :, 1], OG[:, :, 2]


def cls(px):
    R, G, B = px
    if R > 245 and G > 245 and B > 245:
        return None                      # white
    if abs(R - 233) < 12 and abs(G - 233) < 12 and abs(B - 231) < 12:
        return "P"                       # panel gray E9E9E7
    if R > 150 and G < 110 and B < 110:
        return "R"                       # red stroke/text
    if B > 150 and R < 90 and G < 90:
        return "b"                       # strong blue
    if G > 120 and R < 150 and B < 150:
        return "g"                       # green
    if R > 200 and G > 200 and B > 150 and B < 225:
        return "y"                       # yellow band
    if R > 230 and G < 225 and B < 225:
        return "k"                       # pink/salmon
    if B > 220 and R < 240 and G > 230:
        return "c"                       # pale blue
    if R < 120 and G < 120 and B < 120:
        return "#"                       # black
    return "."


def runs_for(y):
    row = OG[y]
    prev = None
    out = []
    start = 0
    for x in range(W):
        c = cls(row[x])
        if c != prev:
            if prev is not None:
                out.append((prev, start, x - 1))
            prev = c
            start = x
    if prev is not None:
        out.append((prev, start, W - 1))
    # keep only meaningful runs (non-white, non-panel, or panel runs > 40px)
    keep = [(c, a, bq) for c, a, bq in out
            if c not in (None, "P") or (bq - a) > 40]
    return keep


prev_sig = None
for y in range(45, H, 2):
    rr = runs_for(y)
    sig = tuple((c, a // 8, bq // 8) for c, a, bq in rr)
    if sig != prev_sig:
        txt = " ".join(f"{c}:{a}-{bq}" for c, a, bq in rr)
        print(f"y={y:3d} | {txt[:200]}")
        prev_sig = sig
