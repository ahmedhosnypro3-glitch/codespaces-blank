#!/usr/bin/env python3
"""Slide 024: per-column dominant-class runs for equation panels (fine)."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

def runs(name, x0, x1, y0, y1, xstep=1):
    print(f"\n=== {name} x{x0}-{x1} y{y0}-{y1} ===")
    for y in range(y0, y1, 3):
        seq = []
        cur = None; start = None
        for x in range(x0, x1, xstep):
            R, G, B = r[y, x], g[y, x], b[y, x]
            if R > 235 and G > 235 and B > 235: c = "."
            elif R < 100 and G < 100 and B < 100: c = "#"
            elif R - G > 55 and R - B > 55 and B < 100: c = "r"
            elif B - R > 40 and B - G > 35: c = "u"
            elif R > 200 and R - G > 50 and G - B > 35: c = "o"
            elif R > 220 and G > 95 and B > 95 and R - G > 50: c = "p"
            else: c = " "
            if c != cur:
                if cur not in (None, ".") and start is not None:
                    seq.append((cur, start, x - xstep))
                cur = c; start = x
        if cur not in (None, ".") and start is not None:
            seq.append((cur, start, x1 - 1))
        seq = [s for s in seq if s[2] - s[1] >= 2]
        if seq:
            print(f" y{y}: " + " ".join(f"{c}[{a}-{z}]" for c, a, z in seq))

runs("P1 sigmoid eq", 78, 330, 104, 152, xstep=2)
runs("P2 remember", 592, 850, 104, 150, xstep=2)
runs("P7 final", 498, 820, 426, 456, xstep=2)
