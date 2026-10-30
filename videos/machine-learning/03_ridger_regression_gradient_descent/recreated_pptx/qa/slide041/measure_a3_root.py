#!/usr/bin/env python3
"""Slide 041 measurement pass A3: marker census for the scatter plot.

Frame-space coordinate system measured in pass A1/A2:
  plot frame (red 1pt box): x313..823, y174..479
  data axes: x = 362.5 + 52.71*X  (X=0..8)
             y = 429.6 - 30.68*Y  (Y=0..7)
  horizontal gridlines y215/245.5/276.5/307/337.5/368/398.5/429.5 (8, Y=7..0)
  vertical gridlines x362/x784 are the only ones drawn (measured)
"""
import json
import os

import numpy as np
from PIL import Image

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
HERE = os.path.dirname(os.path.abspath(__file__))

a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

MASKS = {
    "blue": (B - R > 45) & (B - G > 20) & (B > 90),
    "red": (R - B > 55) & (R - G > 35) & (R > 140),
    "magenta": (R - B > -70) & (R - B < 70) & (R > 120) & (B > 120) & (G < R - 35) & (G < B - 35),
}

X0, X1, Y0, Y1 = 362.5, 784.2, 215.0, 429.6


def components(m):
    H, W = m.shape
    seen = np.zeros_like(m, bool)
    out = []
    for y in range(H):
        for x in range(W):
            if m[y, x] and not seen[y, x]:
                stack = [(y, x)]
                comp = []
                seen[y, x] = True
                while stack:
                    cy, cx = stack.pop()
                    comp.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                stack.append((ny, nx))
                out.append(comp)
    return out


res = {}
for name, m in MASKS.items():
    mm = np.array(m)
    mm[:180] = False
    mm[485:] = False
    mm[:, :320] = False
    mm[:, 820:] = False
    lst = []
    for comp in components(mm):
        if len(comp) < 15:
            continue
        ys = [p[0] for p in comp]
        xs = [p[1] for p in comp]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        xv = (bx0 + bx1) / 2.0
        yv = (by0 + by1) / 2.0
        d = (xv - X0) / ((X1 - X0) / 8.0)
        e = (Y0 - yv) / ((Y0 - Y1) / 7.0)
        px = a[by0:by1 + 1, bx0:bx1 + 1].reshape(-1, 3)
        sat = np.argsort(-(px.max(axis=1) - px.min(axis=1)))[:3]
        shape = []
        for r in range(by0, by1 + 1):
            shape.append(sum(1 for (yy, xx) in comp if yy == r))
        lst.append({
            "bbox": [bx0, by0, bx1, by1], "w": bx1 - bx0 + 1, "h": by1 - by0 + 1,
            "n": len(comp), "cx": round(xv, 2), "cy": round(yv, 2),
            "data": [round(d, 2), round(e, 2)],
            "core": [tuple(int(v) for v in px[i]) for i in sat],
            "rowwidths": shape,
        })
    lst.sort(key=lambda z: (z["data"][0], z["data"][1]))
    res[name] = lst

with open(os.path.join(HERE, "measurements_a3.json"), "w") as f:
    json.dump(res, f, indent=1)

for name, lst in res.items():
    print("###", name, len(lst))
    for d in lst:
        print("   bbox=%s w=%d h=%d n=%d data=(%.2f,%.2f) core=%s widths=%s"
              % (d["bbox"], d["w"], d["h"], d["n"], d["data"][0], d["data"][1], d["core"][0], d["rowwidths"]))
