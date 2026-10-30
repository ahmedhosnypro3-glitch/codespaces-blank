#!/usr/bin/env python3
"""Tight-window darkest-ink colour reads on the ORIGINAL for the remaining
elements judge_2 mentioned, so the next build is grounded in pixels.

Windows (frame px, from the build's measured geometry):
  * "W =" label      : x0+14..x0+34, gy+22..gy+38   (the 'W' glyph + '=')
  * TestN header     : v0..v0+colW,   gy+5..gy+20
  * x1 value row     : v0..v0+colW,   gy+23..gy+38
  * x2 value row     : v0..v0+colW,   gy+45..gy+60
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)

COLX = [124, 384, 644]
GROUPY = [205, 310, 420]
GX1 = {0: 380, 1: 640, 2: 888}


def hue(p):
    r, g, b = p[:, 0].mean(), p[:, 1].mean(), p[:, 2].mean()
    if r - b > 22:
        return f"RED({r:.0f},{g:.0f},{b:.0f})"
    if b - r > 22:
        return f"BLUE({r:.0f},{g:.0f},{b:.0f})"
    if g - min(r, b) > 22:
        return f"GREEN({r:.0f},{g:.0f},{b:.0f})"
    return f"NEUTRAL({r:.0f},{g:.0f},{b:.0f})"


def read(x0, y0, x1, y1, pct=12, label=""):
    sub = o[int(y0):int(y1), int(x0):int(x1)]
    lum = sub.sum(axis=2) / 3
    p = sub[lum < np.percentile(lum, pct)]
    print(f"   {label}: {hue(p)}  n={p.shape[0]}")


for ci, x0 in enumerate(COLX):
    v0 = x0 + 142
    colW = (GX1[ci] - v0) / 3
    for gi, gy in enumerate(GROUPY):
        print(f" col{ci} g{gi}:")
        read(x0 + 14, gy + 22, x0 + 34, gy + 38, 12, "W= label ")
        for ti in range(3):
            read(v0 + ti * colW, gy + 5, v0 + (ti + 1) * colW, gy + 20, 15, f"Test{ti+1} hdr ")
        read(v0, gy + 23, v0 + colW, gy + 38, 15, "x1 Test1 val")
        read(v0, gy + 45, v0 + colW, gy + 60, 15, "x2 Test1 val")
