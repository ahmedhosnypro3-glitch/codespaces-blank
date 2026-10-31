#!/usr/bin/env python3
"""Word-level segmentation of formula-box ink runs for slide_021.jpg:
gaps >= GAP px separate words/groups; each group reports its color profile."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 110) & (R - G > 45) & (R - B > 45)
blue = (B > 90) & (B - R > 45) & (B - G > 30)
green = (G > 70) & (G - R > 30) & (G - B > 30)
black = (R < 140) & (G < 140) & (B < 140)
ink = red | blue | green | black

BOXES = {
    "TL": (113, 54, 412, 105),
    "TR": (550, 54, 849, 105),
    "BL": (94, 284, 428, 339),
    "BR": (584, 286, 813, 337),
}
GAP = 3


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
    print(f"\n=== {name} ===")
    sub = ink[y0:y1 + 1, x0:x1 + 1]
    cols = sub.sum(axis=0)
    groups = []
    for cs, ce in runs(cols > 0):
        if groups and cs - groups[-1][1] - 1 < GAP:
            groups[-1] = (groups[-1][0], ce)
        else:
            groups.append((cs, ce))
    for gs, ge in groups:
        sl = (slice(y0, y1 + 1), slice(x0 + gs, x0 + ge + 1))
        c = {"R": int(red[sl].sum()), "B": int(blue[sl].sum()),
             "G": int(green[sl].sum()), "K": int(black[sl].sum())}
        dom = max(c, key=c.get)
        prof = []
        for col in "RBGK":
            if c[col] > 0:
                prof.append(f"{col}:{c[col]}")
        print(f"  x {x0+gs}..{x0+ge} w={ge-gs+1} dom={dom}  [{' '.join(prof)}]")
