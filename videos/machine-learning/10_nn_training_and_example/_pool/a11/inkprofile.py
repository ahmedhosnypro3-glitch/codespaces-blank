#!/usr/bin/env python3
"""Ink-column profile inside the slide-019 diagram band (a11).
Tan bg + white = non-ink; everything else = diagram ink."""
import sys
import numpy as np
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
scale = W / 13.333
# tan/white/cream background detection
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
istam = (r > 175) & (g > 165) & (b < r) & ((r - b) < 80)
iswh = (r > 235) & (g > 235) & (b > 225)
isbg = istam | iswh
ink = ~isbg

y0, y1 = float(sys.argv[2]) * scale, float(sys.argv[3]) * scale
band = ink[int(y0):int(y1), :]
colsum = band.sum(axis=0)
rowsum = ink[:, int(0.40 * scale):int(0.95 * scale)].sum(axis=1)

def peaks(v, lo, hi, minv):
    out = []
    cur = []
    for i in range(lo, min(hi, len(v))):
        if v[i] >= minv:
            cur.append(i)
        else:
            if cur:
                out.append((cur[0], cur[-1]))
                cur = []
    if cur:
        out.append((cur[0], cur[-1]))
    return out

inkthr = max(3, (y1 - y0) * 0.05)
print(f"== {sys.argv[1]} band y={sys.argv[2]}..{sys.argv[3]}in  inkthr={inkthr}")
print("COLUMN bands (x.in : w.in : inkpx) -- node columns:")
for a0, b0 in peaks(colsum, 0, W, inkthr):
    print(f"   x={a0/scale:6.2f}..{b0/scale:6.2f} w={(b0-a0+1)/scale:5.2f} n={colsum[a0:b0+1].sum()}")
print("ROW bands (y.in : inkpx) -- node rows:")
for a0, b0 in peaks(rowsum, 0, H, max(2, inklevel := 0.02 * (0.55 * W))):
    print(f"   y={a0/scale:6.2f}..{b0/scale:6.2f} h={(b0-a0+1)/scale:5.2f} n={rowsum[a0:b0+1].sum()}")
