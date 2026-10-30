#!/usr/bin/env python3
"""Colour-classified ink runs for slide_014 regions.

Classes: K=black/dark grey, R=red, G=green, B=blue, P=purple/lilac.
Prints per-row runs with class, so text vs shape vs box can be told apart."""
import sys
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)


def classify(x0, y0, x1, y1, minrun=3, label="", rows=None):
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    sat = mx - mn
    cls = np.full(sub.shape[:2], ".")
    dark = mx < 215
    redish = (R > G + 35) & (R > B + 35) & (R > 90)
    greenish = (G > R + 30) & (G > B + 30) & (G > 80)
    blueish = (B > R + 30) & (B > G + 30) & (B > 80)
    purpleish = (R > B - 30) & (B > G + 20) & (sat > 18) & (mx > 150) & (mx < 250)
    cls[dark] = "K"
    cls[redish & dark] = "R"
    cls[greenish & dark] = "G"
    cls[blueish & dark] = "B"
    cls[purpleish & ~dark] = "P"
    print(f"\n== {label}: x[{x0}..{x1}] y[{y0}..{y1}] ==")
    yr = range(y0, y1) if rows is None else rows
    for j in yr:
        row = cls[j - y0]
        out, inr = [], False
        for i, v in enumerate(row):
            if v != "." and not inr:
                inr, st = True, i
            elif v == "." and inr:
                inr = False
                out.append((st + x0, i - 1 + x0, row[st]))
        if inr:
            out.append((st + x0, x1 - 1, row[st]))
        out = [o for o in out if o[1] - o[0] + 1 >= minrun]
        if out:
            print(f"  y={j:4d}  " + "  ".join(f"[{p}..{q}]{c}" for p, q, c in out))


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "thr":
        classify(400, 150, 545, 235, minrun=3, label="threshold box + O/P coloured")
    elif what == "w11":
        classify(150, 120, 290, 215, minrun=2, label="w11/w12 zone coloured")
    elif what == "eq":
        classify(84, 318, 592, 350, minrun=3, label="SUM1/SUM2 line coloured")
    elif what == "diag":
        classify(85, 100, 555, 305, minrun=3, label="main diagram coloured")
