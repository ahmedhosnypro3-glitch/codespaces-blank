#!/usr/bin/env python3
"""PIL census of the W-vector ENTRY area (the 3 stacked numbers inside the parens).

Build places the entries at x0+49..x0+65, gy+2..gy+58 (7pt). The original's
frame-px equivalent is measured, not assumed: the parens sit at x0+37..x0+45 and
x0+67..x0+75, so the entries occupy x0+45..x0+66.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{NS}/recreated_pptx/qa/slide019/render_2.png").convert("RGB")).astype(int)
SY = r.shape[0] / 540.0
SX = r.shape[1] / 960.0

COLX = [124, 384, 644]
GROUPY = [205, 310, 420]


def census(img, sfx, sfy, x0, y0, x1, y1, thresh=175, label=""):
    X0, Y0, X1, Y1 = int(x0 * sfx), int(y0 * sfy), int(x1 * sfx), int(y1 * sfy)
    sub = img[Y0:Y1, X0:X1]
    lum = sub.sum(axis=2) / 3.0
    mask = lum < thresh
    if not mask.sum():
        print(f"  {label}: no ink")
        return
    from collections import Counter
    c = Counter()
    for py, ppx in zip(*np.where(mask)):
        rr, gg, bb = sub[py, ppx]
        if rr > 110 and gg < 105 and bb < 105 and rr - max(gg, bb) > 40:
            c["red"] += 1
        elif bb > 115 and rr < 105 and bb - max(rr, gg) > 30:
            c["blue"] += 1
        elif gg > 100 and rr < 125 and bb < 105 and gg - max(rr, bb) > 35:
            c["green"] += 1
        elif rr < 95 and gg < 95 and bb < 95:
            c["black"] += 1
        else:
            c["other"] += 1
    tot = sum(c.values())
    print(f"  {label}: {tot} px | " + ", ".join(f"{k}:{v}({100*v/tot:.0f}%)" for k, v in c.most_common()))


print("=== W-vector ENTRIES (x0+46..x0+66, gy+2..gy+58) ===")
for ci, x0 in enumerate(COLX):
    for gi, gy in enumerate(GROUPY):
        print(f" col{ci} g{gi}:")
        census(o, 1.0, 1.0, x0 + 46, gy + 2, x0 + 66, gy + 58, label="  orig")
        census(r, SX, SY, x0 + 46, gy + 2, x0 + 66, gy + 58, label="  rend")

print()
print("=== ||W||² norm line (x0+6..x0+82, gy+68..gy+84) ===")
for ci, x0 in enumerate(COLX):
    for gi, gy in enumerate(GROUPY):
        print(f" col{ci} g{gi}:")
        census(o, 1.0, 1.0, x0 + 6, gy + 68, x0 + 82, gy + 84, label="  orig")
        census(r, SX, SY, x0 + 6, gy + 68, x0 + 82, gy + 84, label="  rend")
