#!/usr/bin/env python3
"""Fast winding probe for a k17q BR candidate png: resize to the build
placement 265x187 (as k17g_verify composites it) and run the same largest-
dark-comp wind-ratio metric on slide region x615..880 y344..531 inset 8.
usage: k17q_wind_probe.py <br.png>   prints one line: wind-ratio etc.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

p = sys.argv[1]
im = Image.open(p).convert("RGB").resize((265, 187), Image.NEAREST)
REN = np.asarray(im).astype(np.int32)
P8 = 8
br = REN[P8:187 - P8, P8:265 - P8]
dmk = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
lab, n = ndimage.label(dmk, structure=np.ones((3, 3)))
best = None
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) >= 15 and (best is None or len(xs) > best[0]):
        best = (len(xs), xs, ys)
if best:
    aa, xs, ys = best
    spanx = xs.max() - xs.min() + 1
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    ratio = seg / max(straight, 1.0)
    print("%s area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f" % (
        p.split("/")[-2] + "/" + p.split("/")[-1], aa, spanx, seg, straight, ratio))
else:
    print("%s no dark comp" % p)
