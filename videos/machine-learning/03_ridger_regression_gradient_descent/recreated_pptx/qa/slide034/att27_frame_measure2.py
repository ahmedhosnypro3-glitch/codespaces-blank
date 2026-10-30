#!/usr/bin/env python3
"""att27 focused pass 2: column separators, text rows, slope inset boxes, plot grid."""
import numpy as np
from PIL import Image

A = np.asarray(Image.open("unique_slides/slide_034.jpg").convert("RGB")).astype(int)
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)

def clusters(idx, gap=4):
    idx = np.asarray(idx)
    if len(idx) == 0: return []
    br = np.nonzero(np.diff(idx) > gap)[0]
    return [(int(s[0]), int(s[-1])) for s in np.split(idx, br + 1)]

P("### A. vertical separators per band (deviation from band fill, x140..881)")
BANDS = [("band1", 333, 367), ("band2", 376, 408), ("band3", 419, 452)]
for name, y0, y1 in BANDS:
    Z = A[y0:y1, 140:881]
    med = np.median(Z.reshape(-1, 3), axis=0)
    dev = np.abs(Z - med).max(axis=2)
    frac = (dev > 45).mean(axis=0)
    cols = np.nonzero(frac > 0.55)[0]
    cl = clusters(cols, gap=3)
    P(name, "median fill", med.round(0).tolist(), "separator clusters frame-x:",
      [(a + 140, b + 140) for a, b in cl])

P("### B. text ink row bands per table region (dark px per row, x145..870)")
for name, y0, y1 in [("band1", 328, 372), ("band2", 372, 414), ("band3", 415, 457),
                     ("slope", 458, 480), ("nextx", 481, 518)]:
    Z = A[y0:y1, 145:870]
    dk = (Z.max(axis=2) < 120).sum(axis=1)
    rows = [int(y) + y0 for y in np.nonzero(dk > 8)[0]]
    cl = clusters(rows, gap=3)
    P(name, "text row clusters (frame-y):", cl)

P("### C. slope inset boxes (red borders) y459..479")
Z = A[459:480, 140:881]
red = (Z[..., 0] > 130) & (Z[..., 0] - Z[..., 1] > 45) & (Z[..., 0] - Z[..., 2] > 35)
colfrac = red.mean(axis=0)
cols = np.nonzero(colfrac > 0.5)[0]
P("red border col clusters (frame-x):", [(a + 140, b + 140) for a, b in clusters(cols, gap=2)])
rowfrac = red.mean(axis=1)
P("red border row profile y459..479:", {int(y) + 459: round(float(f), 2) for y, f in enumerate(rowfrac) if f > 0.3})
# salmon inset vertical extent at x300 (inside an inset box)
col = A[455:482, 300]
P("x300 y455..482 RGB:", [tuple(v) for v in col])
# label cell fill extent x70..140
col2 = A[455:482, 100]
P("x100 y455..482 RGB:", [tuple(v) for v in col2])

P("### D. plot gridline check (sample expected grid rows/cols)")
X0, SX, Y0, SY = 721.825, 8.9296, 172.336, 8.8443
for k in [-6, -4, -2, 2, 4, 6, 8, 10, 12]:
    gx = int(round(X0 + k * SX))
    seg = A[80:305, gx - 1:gx + 2]
    grayish = ((np.abs(seg[..., 0] - seg[..., 1]) < 14) & (np.abs(seg[..., 1] - seg[..., 2]) < 14)
               & (seg[..., 0] > 175) & (seg[..., 0] < 235)).sum()
    P("vgrid x=%d (unit %d): grayish px %d" % (gx, k, grayish))
for k in [-12, -10, -8, -6, -4, -2, 2, 4, 6, 8, 10]:
    gy = int(round(Y0 - k * SY))
    if 58 <= gy <= 313:
        seg = A[gy - 1:gy + 2, 615:835]
        grayish = ((np.abs(seg[..., 0] - seg[..., 1]) < 14) & (np.abs(seg[..., 1] - seg[..., 2]) < 14)
                   & (seg[..., 0] > 175) & (seg[..., 0] < 235)).sum()
        P("hgrid y=%d (unit %d): grayish px %d" % (gy, k, grayish))

P("### E. insert dashed border color (dark px on insert perimeter)")
Z = A[327:373, 664:792]
dkm = (Z.max(axis=2) < 140) & (Z[..., 0] - Z[..., 2] > 10)
ys, xs = np.nonzero(dkm)
P("dark warm px:", int(dkm.sum()), "mean RGB:", Z[dkm].mean(axis=0).round(1) if dkm.sum() else None)
# where are they? column histogram clusters
if dkm.sum():
    P("dark warm col clusters (frame-x):", [(a + 664, b + 664) for a, b in clusters(np.nonzero(dkm.any(axis=0))[0], gap=3)])
    P("dark warm row clusters (frame-y):", [(a + 327, b + 327) for a, b in clusters(np.nonzero(dkm.any(axis=1))[0], gap=3)])

P("### F. next-x edges y481..505 red rule rows")
Z = A[478:508, 145:870]
red = (Z[..., 0] > 120) & (Z[..., 0] - Z[..., 1] > 55) & (Z[..., 0] - Z[..., 2] > 45)
rowfrac = red.mean(axis=1)
P("next-x red rows:", {int(y) + 478: round(float(f), 2) for y, f in enumerate(rowfrac) if f > 0.5})
P("next-x red core mean:", Z[red].mean(axis=0).round(1) if red.sum() else None)

P("### G. label column separator (x136..146) in band1")
Z = A[333:367, 132:150]
med = np.median(A[333:367, 145:175].reshape(-1, 3), axis=0)
for xx in range(132, 150):
    colm = A[333:367, xx].mean(axis=0).round(0).astype(int)
    P("  x%d:" % xx, tuple(colm))

P("### H. badge area sanity + 'x'/'y' plot labels")
Z = A[160:185, 828:846]
dk = (Z.max(axis=2) < 120)
P("'x' label zone x828..846 y160..185 dark px:", int(dk.sum()))
Z = A[60:80, 712:732]
dk = (Z.max(axis=2) < 120)
P("'y' label zone x712..732 y60..80 dark px:", int(dk.sum()))

with open("att27_frame_measure2.txt", "w") as fh:
    fh.write("\n".join(out) + "\n")
print("WROTE att27_frame_measure2.txt")
