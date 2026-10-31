#!/usr/bin/env python3
"""Detect plot axis/gridline rows and cols per graph, with their colors."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

GRAPHS = {
    "TL_relu": (122, 110, 399, 271),
    "TR_prelu": (564, 110, 841, 274),
    "BL_elu": (122, 347, 399, 508),
    "BR_softplus": (564, 347, 841, 508),
}


def lines(profile, thresh, coords):
    out, start = [], None
    for i, v in enumerate(profile):
        if v >= thresh and start is None:
            start = i
        elif v < thresh and start is not None:
            out.append((coords(start, i)))
            start = None
    if start is not None:
        out.append((coords(start, len(profile))))
    return out


for name, (x0, y0, x1, y1) in GRAPHS.items():
    print(f"\n=== {name} x{x0}..{x1} y{y0}..{y1} ===")
    h = y1 - y0 + 1
    w = x1 - x0 + 1
    sub = a[y0:y1 + 1, x0:x1 + 1, :]
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    sat = mx - mn
    neutral = (sat < 22) & (mx < 245)   # gray-ish incl. grid + axes + text
    colcount = neutral.sum(axis=0)
    rowcount = neutral.sum(axis=1)
    print("  vertical neutral lines (col count > 0.45h):")
    for s, e in lines(colcount, h * 0.45, lambda s, e: (s, e)):
        cols = range(s, e)
        vals = [tuple(sub[:, c].mean(axis=0).astype(int)) for c in cols if colcount[c] >= h * 0.45]
        print(f"    x {x0+s}..{x0+e-1} mean color {np.array(vals).mean(axis=0).astype(int) if vals else None}")
    print("  horizontal neutral lines (row count > 0.45w):")
    for s, e in lines(rowcount, w * 0.45, lambda s, e: (s, e)):
        rows = [r for r in range(s, e) if rowcount[r] >= w * 0.45]
        vals = [tuple(sub[r, :].mean(axis=0).astype(int)) for r in rows]
        print(f"    y {y0+s}..{y0+e-1} mean color {np.array(vals).mean(axis=0).astype(int) if vals else None}")
    # gray level histogram of neutral pixels
    vals = sub[neutral]
    hist, edges = np.histogram(vals.max(axis=1), bins=10, range=(120, 245))
    print("  neutral brightness hist:", list(zip(edges.astype(int), hist)))
