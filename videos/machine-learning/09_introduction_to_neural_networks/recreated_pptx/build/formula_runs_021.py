#!/usr/bin/env python3
"""Per-run color/position extraction of the four formula boxes in slide_021.jpg."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

BOXES = {
    "TL": (113, 54, 412, 105),
    "TR": (550, 54, 849, 105),
    "BL": (94, 284, 428, 339),
    "BR": (584, 286, 813, 337),
}

red = (R > 110) & (R - G > 45) & (R - B > 45)
blue = (B > 90) & (B - R > 45) & (B - G > 30)
green = (G > 70) & (G - R > 30) & (G - B > 30)
black = (R < 140) & (G < 140) & (B < 140)
ink = red | blue | green | black


def runs(mask1d):
    out, start = [], None
    for i, v in enumerate(mask1d):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(mask1d) - 1))
    return out


for name, (x0, y0, x1, y1) in BOXES.items():
    print(f"\n=== {name} box x{x0}..{x1} y{y0}..{y1} ===")
    sub_ink = ink[y0:y1 + 1, x0:x1 + 1]
    rowc = sub_ink.sum(axis=1)
    print("  ink rows:", [(y0 + i, int(c)) for i, c in enumerate(rowc) if c > 0])
    # split into text bands
    bands = runs(rowc > 0)
    for bs, be in bands:
        if be - bs < 1:
            continue
        band = sub_ink[bs:be + 1]
        cols = band.sum(axis=0)
        print(f"  band y {y0+bs}..{y0+be}")
        for cs, ce in runs(cols > 0):
            if ce - cs < 0:
                continue
            sl = (slice(y0 + bs, y0 + be + 1), slice(x0 + cs, x0 + ce + 1))
            counts = {"red": int(red[sl].sum()),
                      "blue": int(blue[sl].sum()),
                      "green": int(green[sl].sum()),
                      "black": int(black[sl].sum())}
            dom = max(counts, key=counts.get)
            print(f"    x {x0+cs}..{x0+ce} (w {ce-cs+1}) dom={dom} {counts}")
