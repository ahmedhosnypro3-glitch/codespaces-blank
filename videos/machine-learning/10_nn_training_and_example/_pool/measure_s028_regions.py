#!/usr/bin/env python3
"""Region-scoped text-band measurement for slide_028."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_028.jpg").convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

RED = (r > 120) & (r - g > 55) & (r - b > 55)
BLUE = (b > 100) & (b - r > 55) & (b - g > 30)
DARK = a.mean(axis=2) < 120
ORANGE = (r > 190) & (g > 50) & (g < 175) & (b < 100)


def bands(mask, x0, x1, y0, y1, minpx=3, gap=3, label=""):
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    counts = sub.sum(axis=1)
    out = []
    st = None
    for i, c in enumerate(counts):
        if c >= minpx and st is None:
            st = i
        elif c < minpx and st is not None:
            if i - st >= 2:
                out.append((st, i - 1))
            st = None
    if st is not None:
        out.append((st, len(counts) - 1))
    merged = []
    for (s, e) in out:
        if merged and s - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    print(f"-- {label} [{x0},{x1}]x[{y0},{y1}]")
    for (s, e) in merged:
        band = sub[s:e + 1]
        cols = np.where(band.sum(axis=0) >= 1)[0]
        if len(cols) == 0:
            continue
        print(f"   y[{y0+s}-{y0+e}] x[{x0+cols[0]}-{x0+cols[-1]}] h={e-s+1}")


# LEFT column (x 45..400)
bands(RED, 45, 400, 155, 540, label="LEFT RED")
bands(BLUE, 45, 400, 155, 540, label="LEFT BLUE")
bands(DARK, 45, 400, 155, 540, label="LEFT DARK")
# RIGHT column (x 401..921)
bands(RED, 401, 921, 185, 540, label="RIGHT RED")
bands(BLUE, 401, 921, 185, 540, label="RIGHT BLUE")
bands(DARK, 401, 921, 185, 540, label="RIGHT DARK")
# TOP region (y 43..190)
bands(RED, 401, 921, 43, 190, label="TOP-R RED")
bands(BLUE, 401, 921, 43, 190, label="TOP-R BLUE")
bands(DARK, 401, 921, 43, 190, label="TOP-R DARK")
bands(ORANGE, 401, 921, 43, 190, label="TOP-R ORANGE")
bands(DARK, 45, 400, 43, 190, label="TOP-L DARK")
bands(BLUE, 45, 400, 43, 190, label="TOP-L BLUE")
bands(ORANGE, 45, 400, 43, 190, label="TOP-L ORANGE")
# header band across
bands(BLUE, 40, 925, 188, 230, minpx=4, label="HEADER BLUE")
bands(DARK, 40, 925, 188, 230, minpx=4, label="HEADER DARK")
