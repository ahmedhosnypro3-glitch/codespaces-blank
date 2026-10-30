#!/usr/bin/env python3
"""Slide 041 pass 9: connected-component inventory of the pale panel interior.
Each glyph/stroke = one component with bbox, px count, dominant colour class.
Banks measurements9.json.
"""
import json
import os

import numpy as np
from PIL import Image

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
HERE = os.path.dirname(os.path.abspath(__file__))
a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

dark = (R < 170) & (G < 170) & (B < 170)
red = (R > 110) & ((R - G) > 60) & ((R - B) > 40)
blue = (B - R >= 30) & (B >= 90) & (R <= 140)
green = (G - R >= 30) & (G - B >= 20) & (G >= 80)
ink = dark | red | blue | green

Y0, Y1, X0, X1 = 57, 128, 71, 718
sub = ink[Y0:Y1 + 1, X0:X1 + 1]
subR = red[Y0:Y1 + 1, X0:X1 + 1]
subB = blue[Y0:Y1 + 1, X0:X1 + 1]
subG = green[Y0:Y1 + 1, X0:X1 + 1]
subD = dark[Y0:Y1 + 1, X0:X1 + 1]

# label with 4-connectivity, iterative
lbl = np.zeros(sub.shape, dtype=np.int32)
cur = 0
from collections import deque
for r in range(sub.shape[0]):
    for c in range(sub.shape[1]):
        if sub[r, c] and not lbl[r, c]:
            cur += 1
            q = deque([(r, c)])
            lbl[r, c] = cur
            while q:
                y0, x0 = q.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y0 + dy, x0 + dx
                    if 0 <= yy < sub.shape[0] and 0 <= xx < sub.shape[1] and sub[yy, xx] and not lbl[yy, xx]:
                        lbl[yy, xx] = cur
                        q.append((yy, xx))

comps = []
for lab in range(1, cur + 1):
    ys, xs = np.where(lbl == lab)
    n = len(ys)
    if n < 2:
        continue
    x0, x1 = int(xs.min() + X0), int(xs.max() + X0)
    y0, y1 = int(ys.min() + Y0), int(ys.max() + Y0)
    nr = int(subR[ys, xs].sum())
    nb = int(subB[ys, xs].sum())
    ng = int(subG[ys, xs].sum())
    nd = int(subD[ys, xs].sum())
    tot = nr + nb + ng + nd
    dom = {"red": nr, "blue": nb, "green": ng, "dark": nd}
    domc = max(dom, key=dom.get)
    comps.append({
        "bbox": [x0, y0, x1, y1], "w": x1 - x0 + 1, "h": y1 - y0 + 1, "n": int(n),
        "cx": round(float(xs.mean() + X0), 1), "cy": round(float(ys.mean() + Y0), 1),
        "dom": domc, "frac": round(dom[domc] / max(tot, 1), 2),
        "colors": {"r": nr, "b": nb, "g": ng, "d": nd},
    })
comps.sort(key=lambda c: (c["bbox"][1], c["bbox"][0]))
out = {"components": comps, "count": len(comps)}
with open(os.path.join(HERE, "measurements9.json"), "w") as f:
    json.dump(out, f, indent=1)
for c in comps:
    print(f"x{c['bbox'][0]:>3}-{c['bbox'][2]:>3} y{c['bbox'][1]:>3}-{c['bbox'][3]:>3} "
          f"w{c['w']:>2} h{c['h']:>2} n{c['n']:>4} {c['dom']:>5} {c['frac']:.2f}")
