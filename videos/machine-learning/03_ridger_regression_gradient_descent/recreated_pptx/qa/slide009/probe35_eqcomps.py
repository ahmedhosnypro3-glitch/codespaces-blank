#!/usr/bin/env python3
"""Probe 35: connected-component breakdown of each equation box's loose ink,
with a small per-component ASCII so every glyph (including a superscript) is
isolated and its vertical extent unambiguous.
"""
import numpy as np
from PIL import Image
from collections import deque

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def comps(name, x0, x1, y0, y1, thr=690, minn=4):
    w = a[y0:y1+1, x0:x1+1]
    ink = w.sum(axis=2) <= thr
    H, W = ink.shape
    seen = np.zeros_like(ink, bool)
    out = []
    for yy in range(H):
        for xx in range(W):
            if ink[yy, xx] and not seen[yy, xx]:
                q = deque([(yy, xx)]); seen[yy, xx] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < H and 0 <= nx < W and ink[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True; q.append((ny, nx))
                    if len(pts) >= minn:
                        ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                        out.append((min(xs)+x0, max(xs)+x0, min(ys)+y0, max(ys)+y0, len(pts), pts))
    out.sort()
    print(f"=== {name}  x{x0}..{x1} y{y0}..{y1}  -> {len(out)} comps ===")
    for i, (X0, X1, Y0, Y1, n, pts) in enumerate(out):
        g = np.zeros((Y1-Y0+1, X1-X0+1), bool)
        for cy, cx in pts:
            g[cy-(Y0-y0), cx-(X0-x0)] = True
        print(f"  comp{i}: x{X0}..{X1} y{Y0}..{Y1} w={X1-X0+1} h={Y1-Y0+1} n={n}")
        for r in range(g.shape[0]):
            print("        " + "".join("#" if v else "." for v in g[r]))
comps("LEFT eq", 220, 312, 150, 169)
comps("RIGHT eq", 639, 726, 151, 169)
