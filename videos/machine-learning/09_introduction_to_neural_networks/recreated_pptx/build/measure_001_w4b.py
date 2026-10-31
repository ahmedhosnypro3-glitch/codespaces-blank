#!/usr/bin/env python3
"""slide_001 w4: per-band ink geometry for ORIGINAL vs fresh RENDER, in inches."""
import os
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = os.path.join(V, "unique_slides/slide_001.jpg")
RENDER = os.path.join(V, "recreated_pptx/build/slide_001_rendered-1.png")


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float64)


def analyze(path, ppi, label, box):
    a = load(path)
    H, W = a.shape[:2]
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    ink = L < 175
    x0, y0, x1, y1 = box
    ink[:y0, :] = False
    ink[y1 + 1:, :] = False
    ink[:, :x0] = False
    ink[:, x1 + 1:] = False
    r = ink.sum(axis=1)
    bands, inb = [], False
    for y in range(H):
        if r[y] > 1 and not inb:
            st, inb = y, True
        elif r[y] <= 1 and inb:
            bands.append([st, y - 1])
            inb = False
    if inb:
        bands.append([st, H - 1])
    print("=" * 96)
    print("### %s  (%.2f px/in)  box=%s" % (label, ppi, box))
    for (by0, by1) in bands:
        sub = ink[by0:by1 + 1]
        if sub.sum() < 15:
            continue
        xs = np.nonzero(sub.sum(axis=0) > 0)[0]
        if len(xs) < 2:
            continue
        px = a[by0:by1 + 1][sub]
        q = (px // 24).astype(int)
        key = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
        vals, cnts = np.unique(key, return_counts=True)
        k = vals[np.argmax(cnts)]
        dom = np.array([(k // 10000) * 24 + 12, ((k // 100) % 100) * 24 + 12, (k % 100) * 24 + 12])
        print("  y %5.2f-%5.2f in  x %5.2f-%5.2f in  w=%5.2f h=%5.2f  px=%6d  #%02X%02X%02X"
              % (by0 / ppi, (by1 + 1) / ppi, xs.min() / ppi, (xs.max() + 1) / ppi,
                 (xs.max() - xs.min() + 1) / ppi, (by1 - by0 + 1) / ppi,
                 int(sub.sum()), int(dom[0]), int(dom[1]), int(dom[2])))


analyze(ORIG, 72.0, "ORIGINAL slide_001.jpg", (62, 46, 899, 514))
analyze(RENDER, 150.0, "RENDER slide_001_rendered-1.png", (15, 15, 1986, 1110))
