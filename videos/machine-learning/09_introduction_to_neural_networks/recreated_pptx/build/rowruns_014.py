#!/usr/bin/env python3
"""Per-row dark-run boundaries for slide_014 regions (numeric, exact)."""
import sys
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("L")

def rowruns(x0, y0, x1, y1, thr=190, minrun=2, label=""):
    crop = np.asarray(im.crop((x0, y0, x1, y1))).astype(int)
    print(f"\n== {label}: rows x[{x0}..{x1}] y[{y0}..{y1}] thr={thr} ==")
    for j in range(crop.shape[0]):
        r = crop[j]
        ink = r < thr
        out, inr = [], False
        for i, v in enumerate(ink):
            if v and not inr:
                inr, st = True, i
            elif not v and inr:
                inr = False
                out.append((st + x0, i - 1 + x0))
        if inr:
            out.append((st + x0, x1 - 1))
        out = [o for o in out if o[1] - o[0] + 1 >= minrun]
        if out:
            print(f"  y={y0+j:4d}  " + "  ".join(f"[{a}..{b}]w{b-a+1}" for a, b in out))

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "thr":
        rowruns(405, 190, 545, 230, thr=190, minrun=2, label="threshold box rows")
    elif what == "thrcols":
        # vertical extents of specific x columns
        x0, x1, y0, y1 = 405, 545, 150, 260
        crop = np.asarray(im.crop((x0, y0, x1, y1))).astype(int)
        ink = crop < 190
        print("== vertical ink runs per x column group ==")
        colink = ink.any(axis=0)
        out, inr = [], False
        for i, v in enumerate(colink):
            if v and not inr:
                inr, st = True, i
            elif not v and inr:
                inr = False
                out.append((st + x0, i - 1 + x0))
        if inr:
            out.append((st + x0, x1 - 1))
        for a, b in out:
            sub = ink[:, a - x0:b - x0 + 1]
            ys = np.where(sub.any(axis=1))[0]
            print(f"  x[{a}..{b}] w={b-a+1}  ink y[{ys.min()+y0}..{ys.max()+y0}]")
    elif what == "eq":
        rowruns(84, 322, 592, 350, thr=190, minrun=2, label="SUM1/SUM2 line rows")
