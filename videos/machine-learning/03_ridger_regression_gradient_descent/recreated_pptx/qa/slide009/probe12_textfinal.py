#!/usr/bin/env python3
"""Probe 12 (FINAL text geometry): per-region ink bboxes + ASCII for every
text element on slide_009.jpg, each region using a predicate TAILORED to that
element's color so chart geometry cannot contaminate the bbox.

Regions and predicates (frame px, 960x540, 1px = 1pt):
  LEQ / REQ   near-black equation text inside the navy-bordered annotation
              boxes, x-window clipped past the red y-axis (x>=140 / x>=510)
  LMM / RMM   near-black 'mm' labels left of each panel's red x-axis origin
  LCAP1/2     RED caption text (left panel), RCAP1/2 (right panel)
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

whiteish = (r > 240) & (g > 240) & (b > 240)
gray = (abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16)
redfam = (r - g > 45) & (r - b > 45) & (r > 90)
bluefam = (b - r > 45) & (b - g > 20) & (b > 120)
orangefam = (r > 190) & (g > 130) & (b < 140) & (r - b > 70)
paleblue = (b - r > 8) & (b - r < 45) & (b > 220)
nearblack = (~whiteish) & (~gray) & (~redfam) & (~bluefam) & (~orangefam) & (~paleblue) & (r + g + b < 620)


def band(name, mask, x0, x1, y0, y1):
    m = mask[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    print(f"\n===== {name} (window x{x0}..{x1} y{y0}..{y1}) =====")
    if not len(ys):
        print("  no ink")
        return
    bx0, bx1 = x0 + xs.min(), x0 + xs.max()
    by0, by1 = y0 + ys.min(), y0 + ys.max()
    print(f"  INK BBOX: x {bx0}..{bx1} (w={bx1-bx0+1})  y {by0}..{by1} (h={by1-by0+1})"
          f"  center ({(bx0+bx1)/2:.1f}, {(by0+by1)/2:.1f})")
    X0, X1 = max(bx0 - 2, x0), min(bx1 + 2, x1)
    Y0, Y1 = max(by0 - 2, y0), min(by1 + 2, y1)
    if (X1 - X0) > 200:
        print(f"  (too wide to print: {X1-X0+1} cols)")
        return
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1)))
    for y in range(Y0, Y1 + 1):
        s = []
        for x in range(X0, X1 + 1):
            if mask[y, x]:
                s.append("#")
            elif whiteish[y, x] or paleblue[y, x]:
                s.append(" ")
            elif gray[y, x]:
                s.append(".")
            elif redfam[y, x]:
                s.append("R")
            elif bluefam[y, x]:
                s.append("U")
            elif orangefam[y, x]:
                s.append("O")
            else:
                s.append(":")
        print(f"  {y:4d} " + "".join(s))


band("LEQ '50.85^2 = 2585'", nearblack, 140, 460, 108, 188)
band("REQ '63.64^2 = 4050'", nearblack, 510, 865, 108, 188)
band("LMM '50.85 mm'", nearblack, 96, 150, 484, 532)
band("RMM '63.64 mm'", nearblack, 492, 548, 484, 532)
# captions are RED text (r-g>45). full-width rows per panel, y 482..532.
for nm, xa, xb in (("LCAP", 100, 472), ("RCAP", 480, 875)):
    capmask = redfam & (~orangefam)
    m = capmask[482:533, xa:xb]
    ys, xs = np.where(m)
    if not len(ys):
        print(f"\n===== {nm}: no red ink")
        continue
    print(f"\n===== {nm} red ink bbox: x {xa+xs.min()}..{xa+xs.max()} "
          f"y {482+ys.min()}..{482+ys.max()}")
    # split into lines by row gaps
    rows = np.where(m.sum(axis=1) > 0)[0]
    lines, start, prev = [], rows[0], rows[0]
    for v in rows[1:]:
        if v - prev > 2:
            lines.append((start, prev))
            start = v
        prev = v
    lines.append((start, prev))
    for (l0, l1) in lines:
        sub = m[l0:l1 + 1]
        ys2, xs2 = np.where(sub)
        print(f"  LINE y {482+l0}..{482+l1}: x {xa+xs2.min()}..{xa+xs2.max()} "
              f"(w={xa+xs2.max()-(xa+xs2.min())+1}, h={l1-l0+1})")
