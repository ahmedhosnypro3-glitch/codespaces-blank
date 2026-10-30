#!/usr/bin/env python3
"""Fine measurement of the 050 'Step eta = 1' element (orig frame x355..435 y52..82)."""
import numpy as np
from PIL import Image

NS = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")).astype(int)

win = o[52:84, 355:435]
lum = win.mean(axis=2)
ink = lum < 190
ys, xs = np.where(ink)
print("ink bbox: x%d..%d y%d..%d  n=%d" % (355+xs.min(), 355+xs.max(), 52+ys.min(), 52+ys.max(), len(ys)))
core = win[lum < 120]
print("core px (lum<120) n=%d mean RGB %s median %s" % (len(core), core.mean(axis=0).round(1) if len(core) else None, np.median(core, axis=0) if len(core) else None))
core2 = win[lum < 100]
print("core px (lum<100) n=%d mean RGB %s" % (len(core2), core2.mean(axis=0).round(1) if len(core2) else None))
red = (win[:,:,0] - win[:,:,1] > 40)
print("red-dominant px n=%d" % red.sum())
# per-row ink to find the underline bar
for yy in range(win.shape[0]):
    n = int(ink[yy].sum())
    if n:
        cols = np.where(ink[yy])[0]
        print("y%-3d n=%-3d x%d..%d  mean=%s" % (52+yy, n, 355+cols[0], 355+cols[-1], win[yy][ink[yy]].mean(axis=0).round(0)))
print()
print("ascii (lum<190, char=1px, x355 y52):")
for yy in range(win.shape[0]):
    print("%3d %s" % (52+yy, "".join("#" if ink[yy, xx] else "." for xx in range(win.shape[1]))))
