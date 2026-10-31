#!/usr/bin/env python3
"""W5 probe 2 for slide012: is the outlier-label digit '5' or '8' in ORIG vs
RENDER? Align the two label strips (slide space) and xor; also print glyph
cluster widths of the digit zone."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide012"
r = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_012.jpg").convert("RGB")).astype(int)
sc = r.shape[1] / 960.0

def label_strip(a, y0=320, y1=352, x0=66, x1=210):
    s = a.shape[1] / 960.0
    sub = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    g = sub.sum(axis=2)
    ink = g < 600
    return ink

ir = label_strip(r)
io = label_strip(o)
# orig is 1x, render is 2.0844x: downscale render ink to orig size
rr = np.asarray(Image.fromarray((ir * 255).astype(np.uint8)).resize((io.shape[1], io.shape[0]), Image.LANCZOS)) > 60
print("render-label downscaled ink:", int(rr.sum()), " orig-label ink:", int(io.sum()))

# best integer shift alignment
best = None
for dy in range(-3, 4):
    for dx in range(-6, 7):
        shifted = np.roll(np.roll(rr, dy, axis=0), dx, axis=1)
        xor = int((shifted ^ io).sum())
        if best is None or xor < best[0]:
            best = (xor, dx, dy)
print(f"best-shift xor={best[0]} dx={best[1]} dy={best[2]} (of {io.size} px)")

# glyph clusters in digit zone: find 'X' then next cluster (the digit).
# print col profiles of both strips
for name, ink in (("orig", io), ("render-ds", rr)):
    cols = ink.sum(axis=0)
    prof = "".join("#" if c >= 2 else ("+" if c > 0 else ".") for c in cols)
    print(f"{name}: {prof}")
    # cluster boundaries
    clusters = []
    inC = False
    for i, c in enumerate(cols):
        if c > 0 and not inC:
            st = i; inC = True
        elif c == 0 and inC:
            clusters.append((st, i - 1, i - st)); inC = False
    if inC:
        clusters.append((st, len(cols) - 1, len(cols) - st))
    print(f"  clusters (x0,x1,w): {clusters}")
