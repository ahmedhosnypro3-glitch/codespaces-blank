#!/usr/bin/env python3
"""Probe 6: y-vector delimiter bars (color/extent), pure chip fills, matrix right-zone ink (#46)."""
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
r = np.asarray(Image.open(Q + "/render_33.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(D + "/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
SRX, SRY = 2001 / 960.0, 1125 / 540.0
def rimg(x0, y0, x1, y1): return r[int(y0 * SRY):int(y1 * SRY), int(x0 * SRX):int(x1 * SRX)]

print("=== LEFT delimiter bar x104..111, per-y dark/sat columns ===")
for yy in range(360, 490, 10):
    seg = o[yy, 102:112]
    dk = np.where(seg.max(axis=1) < 140)[0]
    print(f"  y{yy}: dark cols " + (str([102 + int(i) for i in dk]) if len(dk) else "none") + " vals " + " ".join(",".join(str(v) for v in seg[i]) for i in dk[:3]))
print("=== LEFT bar color: dark px in x104..110 y370..475 ===")
im = o[370:475, 104:110]
mx = im.max(axis=2)
ink = mx < 160
if ink.sum():
    px = im[ink]
    print(f"  n={int(ink.sum())} mean=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) darkest={px[px.sum(axis=1).argmin()]}")
print("=== RIGHT bar x132..141: red px per row (r>g+40 & r>b+40) ===")
rows = []
for yy in range(350, 500):
    seg = o[yy, 132:141]
    red = (seg[:, 0] > seg[:, 1] + 40) & (seg[:, 0] > seg[:, 2] + 40) & (seg[:, 0] > 120)
    if red.sum() >= 1:
        rows.append(yy)
if rows:
    runs, start = [], rows[0]
    for a, b in zip(rows, rows[1:]):
        if b - a > 4: runs.append((start, a)); start = b
    runs.append((start, rows[-1]))
    print(f"  red rows y-runs: {runs}")
    ymid = (rows[0] + rows[-1]) // 2
    seg = o[rows[0]:rows[-1], 132:141]
    redm = (seg[:, :, 0] > seg[:, :, 1] + 40) & (seg[:, :, 0] > seg[:, :, 2] + 40)
    px = seg[redm]
    print(f"  red px mean=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) n={int(redm.sum())} darkest={px[px.sum(axis=1).argmin()]}")
    xs = np.where(redm.any(axis=0))[0]
    print(f"  red x-cols: {[132 + int(i) for i in xs]}")

print("=== chip PURE fills (top strips away from glyphs) ===")
for tag, y0, y1 in [("chip1", 368, 373), ("chip2", 399, 404), ("chip3", 455, 460)]:
    im = o[y0:y1, 112:132]
    px = im.reshape(-1, 3)
    print(f"  {tag}: mean=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})")

print("=== matrix right-zone x355..400: per-band dark-ink col counts, ORIG vs REND ===")
bands = [("row1", 368, 392), ("row2", 397, 423), ("row3", 427, 452), ("row4", 456, 478)]
for tag, y0, y1 in bands:
    for img, lab, conv in ((o, "ORIG", 1.0), (r, "REND", None)):
        if conv is None:
            im = rimg(355, y0, 400, y1)
        else:
            im = img[y0:y1, 355:400]
        dark = im.max(axis=2) < 120
        cols = np.where(dark.sum(axis=0) > 0)[0]
        print(f"  {lab} {tag}: dark n={int(dark.sum())} cols " + (str([355 + int(c) for c in cols][:12]) if len(cols) else "none"))

print("=== matrix LEFT delimiter x192..200 per-band (ORIG) ===")
for tag, y0, y1 in bands:
    im = o[y0:y1, 190:202]
    dark = im.max(axis=2) < 140
    cols = np.where(dark.sum(axis=0) > 1)[0]
    print(f"  {tag}: dark cols " + (str([190 + int(c) for c in cols]) if len(cols) else "none"))
