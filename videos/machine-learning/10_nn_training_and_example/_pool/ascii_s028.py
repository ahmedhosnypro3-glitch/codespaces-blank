#!/usr/bin/env python3
"""ASCII colour map of a slide_028 region (R=red B=blue K=dark .=#c0c0c0 =white /=cream)."""
import sys
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
a = np.asarray(Image.open(f"{BASE}/slide_028.jpg").convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = a.mean(axis=2)

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
sx = int(sys.argv[5]) if len(sys.argv) > 5 else 4
sy = int(sys.argv[6]) if len(sys.argv) > 6 else 2


def cls(px):
    rr, gg, bb = px[0], px[1], px[2]
    ll = (rr + gg + bb) / 3.0
    if rr - gg > 55 and rr - bb > 55:
        return "R"
    if bb - rr > 45 and bb - gg > 25:
        return "B"
    if bb - rr > 20 and bb > 90:
        return "b"
    if rr - gg > 25 and rr - bb > 25 and rr > 120:
        return "r"
    if ll < 120:
        return "K"
    if ll > 246:
        return "."
    if ll > 225:
        return ","
    if ll > 185:
        return ":"
    return "-"


print(f"region x[{x0}-{x1}] y[{y0}-{y1}] sx={sx} sy={sy}")
hdr = "     " + "".join(str((x0 + i * sx) // 100 % 10) for i in range((x1 - x0) // sx + 1))
print(hdr)
hdr2 = "     " + "".join(str((x0 + i * sx) // 10 % 10) for i in range((x1 - x0) // sx + 1))
print(hdr2)
for yy in range(y0, y1 + 1, sy):
    line = []
    for xx in range(x0, x1 + 1, sx):
        block = a[yy:min(yy + sy, y1 + 1), xx:min(xx + sx, x1 + 1)].reshape(-1, 3)
        if len(block) == 0:
            line.append(" ")
            continue
        m = block.mean(axis=0)
        line.append(cls(m))
    print(f"{yy:4d} " + "".join(line))
