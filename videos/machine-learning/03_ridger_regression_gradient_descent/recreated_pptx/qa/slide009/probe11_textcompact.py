#!/usr/bin/env python3
"""Probe 11b: compact ASCII of the two annotation-box equation texts and the
two 'mm' labels, emitting ONLY rows/cols that contain TEXT ink.

Reads slide_009.jpg (960x540, 1px = 1pt). TEXT-INK predicate excludes every
saturated chart color so only near-black glyph pixels survive:
    not white-ish (r,g,b all >240)
    not panel gray (~233,233,231)
    not pale-blue box fill (~224,240,255 / low-sat blue: b-r < 25)
    not red  (r-g > 50 and r-b > 50)
    not blue (b-r > 50 and b-g > 25)
    not orange (r > 190 and g > 130 and b < 140)
    and sum(rgb) < 620  (dark)
Legend: '#' text ink | ' ' white/box fill | '.' panel gray | ':' other low-sat.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

whiteish = (r > 240) & (g > 240) & (b > 240)
gray = (abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16)
red = (r - g > 50) & (r - b > 50)
blue = (b - r > 50) & (b - g > 25)
orange = (r > 190) & (g > 130) & (b < 140)
paleblue = (b - r > 8) & (b - r < 40) & (b > 225)      # E0F0FF family fill
ink = (~whiteish) & (~gray) & (~red) & (~blue) & (~orange) & (~paleblue) & (r + g + b < 620)


def band(name, x0, x1, y0, y1):
    m = ink[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    print(f"\n===== {name} (window x{x0}..{x1} y{y0}..{y1}) =====")
    if not len(ys):
        print("  no text ink")
        return
    bx0, bx1 = x0 + xs.min(), x0 + xs.max()
    by0, by1 = y0 + ys.min(), y0 + ys.max()
    print(f"  INK BBOX: x {bx0}..{bx1} (w={bx1-bx0+1})  y {by0}..{by1} (h={by1-by0+1})")
    print(f"  center: ({(bx0+bx1)/2:.1f}, {(by0+by1)/2:.1f})")
    X0, X1 = max(bx0 - 2, x0), min(bx1 + 2, x1)
    Y0, Y1 = max(by0 - 2, y0), min(by1 + 2, y1)
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1)))
    for y in range(Y0, Y1 + 1):
        s = []
        for x in range(X0, X1 + 1):
            if ink[y, x]:
                s.append("#")
            elif whiteish[y, x] or paleblue[y, x]:
                s.append(" ")
            elif gray[y, x]:
                s.append(".")
            elif red[y, x]:
                s.append("R")
            elif blue[y, x]:
                s.append("U")
            else:
                s.append(":")
        print(f"  {y:4d} " + "".join(s))


# equation texts inside the two navy-bordered boxes (interior x 98..463 / 489..868)
band("LEFT equation '50.85^2 = 2585'", 98, 463, 108, 188)
band("RIGHT equation '63.64^2 = 4050'", 489, 868, 108, 188)
# the 'mm' labels (dark text beside the axis arrowheads)
band("LEFT '50.85 mm'", 96, 152, 482, 532)
band("RIGHT '63.64 mm'", 490, 548, 482, 532)
