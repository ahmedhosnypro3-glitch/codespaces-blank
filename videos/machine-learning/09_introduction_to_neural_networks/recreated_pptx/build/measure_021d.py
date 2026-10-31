#!/usr/bin/env python3
"""Surgical per-graph dump for slide_021.jpg."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

GRAPHS = {
    "TL_relu": (122, 110, 399, 271),
    "TR_prelu": (564, 110, 841, 274),
    "BL_elu": (122, 347, 399, 508),
    "BR_softplus": (564, 347, 841, 508),
}

red = (R > 110) & (R - G > 28) & (R - B > 28)
gray = (np.maximum.reduce([R, G, B]) < 246) & (np.maximum.reduce([R, G, B]) > 165) \
    & (np.maximum.reduce([R, G, B]) - np.minimum.reduce([R, G, B]) < 18)
dark = (R < 150) & (G < 150) & (B < 150) & (np.maximum.reduce([R, G, B]) - np.minimum.reduce([R, G, B]) < 40)


def runs(vals, cond, minlen=1):
    out, start = [], None
    for i, v in enumerate(vals):
        if cond(v) and start is None:
            start = i
        elif not cond(v) and start is not None:
            if i - start >= minlen:
                out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(vals) - 1))
    return out


for name, (x0, y0, x1, y1) in GRAPHS.items():
    print(f"\n=== {name} box x{x0}..{x1} y{y0}..{y1} ===")
    H = y1 - y0 + 1
    Wd = x1 - x0 + 1
    sub_gray = gray[y0:y1 + 1, x0:x1 + 1]
    sub_dark = dark[y0:y1 + 1, x0:x1 + 1]
    sub_red = red[y0:y1 + 1, x0:x1 + 1]
    gc = sub_gray.sum(axis=0)
    gr = sub_gray.sum(axis=1)
    print("  gray-col candidates:", [(x0 + i, int(gc[i])) for i in np.nonzero(gc > H * 0.55)[0]])
    print("  gray-row candidates:", [(y0 + i, int(gr[i])) for i in np.nonzero(gr > Wd * 0.55)[0]])
    dc = sub_dark.sum(axis=0)
    dr = sub_dark.sum(axis=1)
    print("  dark-col candidates:", [(x0 + i, int(dc[i])) for i in np.nonzero(dc > H * 0.55)[0]])
    print("  dark-row candidates:", [(y0 + i, int(dr[i])) for i in np.nonzero(dr > Wd * 0.55)[0]])
    ys, xs = np.nonzero(sub_red)
    if len(xs):
        print(f"  RED n={len(xs)} x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()}")
        for yy in range(y0, y1 + 1, 4):
            sel = np.nonzero(sub_red[yy - y0])[0]
            if len(sel):
                print(f"    y={yy}: x {x0+sel.min()}..{x0+sel.max()} n={len(sel)}")
    else:
        print("  RED: none")
