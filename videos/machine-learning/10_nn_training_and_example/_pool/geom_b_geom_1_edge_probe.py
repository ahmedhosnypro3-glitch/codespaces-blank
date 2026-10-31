#!/usr/bin/env python3
"""Lane G (b_geom_1) structure/edge measurement — experiment."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_1"
SLIDES = ["001", "004", "005", "006", "007"]


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(np.int16)
    r = np.asarray(Image.open(f"{TMP}/frame_{n}.png").convert("RGB")).astype(np.int16)
    return o, r


def red_rect(a):
    h, w = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 110) & (r - g > 35) & (r - b > 35)
    rows = np.nonzero(red.sum(axis=1) > 0.50 * w)[0]
    cols = np.nonzero(red.sum(axis=0) > 0.50 * h)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


def edges(a, k=7, thr=26):
    """Structure mask: local median-filter difference -> all drawn edges."""
    lum = a.astype(np.float32).mean(axis=2)
    med = ndimage.median_filter(lum, size=k)
    return np.abs(lum - med) > thr


def runs(idx, gap):
    if len(idx) == 0:
        return []
    out, s, p = [], int(idx[0]), int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i - p > gap:
            out.append((s, p + 1))
            s = i
        p = i
    out.append((s, p + 1))
    return out


for n in SLIDES:
    o, r = load(n)
    obr, rbr = red_rect(o), red_rect(r)
    oe, re_ = edges(o), edges(r)
    # mask borders (5px band) in each
    for m, rect in ((oe, obr), (re_, rbr)):
        x0, y0, x1, y1 = rect
        m[max(0, y0 - 4):y0 + 5, :] = False
        m[max(0, y1 - 4):y1 + 5, :] = False
        m[:, max(0, x0 - 4):x0 + 5] = False
        m[:, max(0, x1 - 4):x1 + 5] = False
    print("=== slide_%s  orig rect %s  rend rect %s" % (n, obr, rbr))
    print("  ORIG rows:", runs(np.nonzero(oe.sum(axis=1) >= 3)[0], 5))
    print("  REND rows:", runs(np.nonzero(re_.sum(axis=1) >= 3)[0], 5))
