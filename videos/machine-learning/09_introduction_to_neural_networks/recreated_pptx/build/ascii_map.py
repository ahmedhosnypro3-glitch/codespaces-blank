#!/usr/bin/env python3
"""Color-class ASCII map of a region — precise geometry without a vision call.

Usage: ascii_map.py <img> <x0> <y0> <x1> <y1> [cols]
"""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1]
x0, y0, x1, y1 = map(int, sys.argv[2:6])
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 120

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
x1, y1 = min(x1, W), min(y1, H)

reg = a[y0:y1, x0:x1]
h, w, _ = reg.shape
step = max(1, w // cols)
rows_out = []

# classify
R, G, B = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
mx = reg.max(axis=2)
mn = reg.min(axis=2)

cls = np.full((h, w), ".", dtype="<U1")
cls[(mx > 246) & (mn > 242)] = " "          # near white
cls[(mx > 232) & (mn > 226)] = ","          # light gray
cls[(mx > 205) & (mn > 198)] = ":"          # mid gray

# dark blue / navy
cls[(B > 70) & (B - R > 35) & (B - G > 45) & (R < 140)] = "B"
# pure blue ? marks
cls[(B > 120) & (R < 120) & (G < 130) & (B - G > 60) & (B - R > 60)] = "b"
# green
cls[(G > 70) & (G - R > 35) & (G - B > 35)] = "G"
# cyan
cls[(G > 140) & (B > 140) & (R < 120) & (G - R > 55) & (B - R > 55)] = "C"
# light cyan fill
cls[(R > 170) & (G > 225) & (B > 225) & (B - R > 12) & (G - R > 25)] = "c"
# light green fill
cls[(R > 160) & (G > 215) & (B > 160) & (B < 235) & (G - B > 18) & (G - R > 20)] = "g"
# red / firebrick
cls[(R > 120) & (R - G > 55) & (R - B > 55)] = "R"
# peach fill (pinkish white)
cls[(R > 245) & (G > 220) & (G < 250) & (B > 220) & (B < 250) & (R - G > 4) & (R - B > 4)] = "p"
# yellow
cls[(R > 195) & (G > 165) & (B < 190) & (R - B > 45) & (G - B > 30)] = "Y"
# black ink
cls[(mx < 95)] = "#"
# purple
cls[(R > 80) & (R < 205) & (B > 130) & (B - G > 35) & (R - G > 12)] = "P"

# priority fix: black wins over other masks when very dark
cls[(mx < 80)] = "#"

print(f"{SRC} region x{x0}..{x1} y{y0}..{y1}  ({w}x{h})  step={step}")
hdr = "     " + "".join(str((x0 + c * step) // 100 % 10) for c in range((w + step - 1) // step))
hdr2 = "     " + "".join(str((x0 + c * step) // 10 % 10) for c in range((w + step - 1) // step))
print(hdr)
print(hdr2)
for r in range(0, h, step):
    line = ""
    for c in range(0, w, step):
        block = cls[r:r + step, c:c + step]
        vals, cnt = np.unique(block, return_counts=True)
        if len(vals) == 0:
            line += " "
            continue
        best = vals[np.argmax(cnt)]
        line += best
    print(f"{y0+r:4d} {line}")
