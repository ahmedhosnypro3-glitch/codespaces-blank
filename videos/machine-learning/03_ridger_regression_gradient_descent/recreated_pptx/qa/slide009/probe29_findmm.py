#!/usr/bin/env python3
"""Probe 29: find ALL dark-ink components in each panel outside the annotation
box, to locate the 'mm' labels (and any other text) exactly.
"""
import numpy as np
from PIL import Image
from collections import deque

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
SAT = mx - mn
INK = (~((r > 244) & (g > 244) & (b > 243))) & ((r + g + b) < 470) & (SAT <= 55)

BOXES = {
    "LEFT": (216, 317, 147, 175),
    "RIGHT": (632, 733, 147, 175),
}
for nm, xr in (("LEFT", (98, 462)), ("RIGHT", (489, 866))):
    x0, x1 = xr
    bx0, bx1, by0, by1 = BOXES[nm]
    sub = INK[113:470, x0:x1 + 1].copy()
    # blank the annotation box + the red/blue axes regions handled by mask
    sub[(by0 - 113):(by1 - 113 + 1), (bx0 - x0):(bx1 - x0 + 1)] = False
    H, W = sub.shape
    seen = np.zeros_like(sub, bool)
    comps = []
    for yy in range(H):
        for xx in range(W):
            if sub[yy, xx] and not seen[yy, xx]:
                q = deque([(yy, xx)])
                seen[yy, xx] = True
                pts = []
                while q:
                    cy, cx = q.popleft()
                    pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and sub[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                q.append((ny, nx))
                if len(pts) >= 8:
                    ys = [p[0] for p in pts]
                    xss = [p[1] for p in pts]
                    comps.append((len(pts), x0 + min(xss), x0 + max(xss),
                                  113 + min(ys), 113 + max(ys)))
    comps.sort(key=lambda c: -c[0])
    print(f"\n########## {nm} dark-ink components outside the annotation box "
          f"({len(comps)} with n>=8) ##########")
    for n, xa, xb, ya, yb in comps[:60]:
        print(f"  n={n:5d}  x {xa}..{xb}  y {ya}..{yb}   w={xb-xa+1} h={yb-ya+1}")
