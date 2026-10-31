#!/usr/bin/env python3
"""Measure the ORIGINAL BR panel's 3D axes-box geometry from slide_025.jpg.

BR panel: slide x615..880 y344..531 (placed PNG), inner red frame at
x466..882 y342..532 per slide_025.js header (frame inset 3px inside box).

Goal: find the projected 3D box corners + the vertical z-axis line
(~slide x731..738) so we can fit mplot3d azim/elev, or directly measure the
three edge directions at the front corner.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

X0, Y0, X1, Y1 = 615, 344, 881, 532   # BR panel crop (slide px, exclusive end)
p = orig[Y0:Y1, X0:X1]
H, W = p.shape[:2]
print("BR panel local size %dx%d (slide x%d..%d y%d..%d)" % (W, H, X0, X1 - 1, Y0, Y1 - 1))

lum = 0.299 * p[:, :, 0] + 0.587 * p[:, :, 1] + 0.114 * p[:, :, 2]
sat = p.max(2) - p.min(2)
red = (p[:, :, 0] > 140) & (p[:, :, 0] - p[:, :, 1] > 60) & (p[:, :, 0] - p[:, :, 2] > 60)
dark = (lum < 110) & (sat < 90) & ~red
# exclude 8px border (red frame + edge)
dark[:8] = False; dark[-8:] = False; dark[:, :8] = False; dark[:, -8:] = False

print("\n== dark-pixel column histogram (cols with >=6 dark px), local x -> slide x ==")
colc = dark.sum(0)
for lx in range(W):
    if colc[lx] >= 6:
        ys = np.nonzero(dark[:, lx])[0]
        print("  local x%3d slide x%3d count=%3d ylocal %d..%d (slide y %d..%d)" % (
            lx, X0 + lx, colc[lx], ys.min(), ys.max(), Y0 + ys.min(), Y0 + ys.max()))

print("\n== dark-pixel row histogram (rows with >=6 dark px) ==")
rowc = dark.sum(1)
for ly in range(H):
    if rowc[ly] >= 6:
        xs = np.nonzero(dark[ly])[0]
        print("  local y%3d slide y%3d count=%3d xlocal %d..%d (slide x %d..%d)" % (
            ly, Y0 + ly, rowc[ly], xs.min(), xs.max(), X0 + xs.min(), X0 + xs.max()))

print("\n== dark connected comps (area>=8) ==")
lab, n = ndimage.label(dark, structure=np.ones((3, 3)))
comps = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 8:
        continue
    comps.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
for a, x0, y0, x1, y1 in sorted(comps, key=lambda c: -c[0])[:25]:
    print("  area=%4d local x%d..%d y%d..%d (slide x%d..%d y%d..%d) w=%d h=%d" % (
        a, x0, y0, x1, y1, X0 + x0, X0 + x1, Y0 + y0, Y0 + y1, x1 - x0 + 1, y1 - y0 + 1))

# ASCII map of dark pixels, 4px cells
print("\n== BR dark-pixel ASCII map (4px cells, #=dark>0) ==")
g = 4
gh, gw = H // g, W // g
for i in range(gh):
    line = ""
    for j in range(gw):
        blk = dark[i * g:(i + 1) * g, j * g:(j + 1) * g]
        line += "#" if blk.sum() >= 2 else ("." if blk.sum() > 0 else " ")
    print("  y%3d %s" % (Y0 + i * g, line))
print("      " + "".join(str((X0 + j * g) // 100 % 10) for j in range(gw)))
print("      " + "".join(str((X0 + j * g) // 10 % 10) for j in range(gw)))
