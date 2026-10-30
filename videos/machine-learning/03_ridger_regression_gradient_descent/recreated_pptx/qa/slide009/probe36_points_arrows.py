#!/usr/bin/env python3
"""Probe 36: definitive ORANGE scatter-point census + RED residual-arrow census
for both chart panels, using measured color signatures.

Orange signature (from samples): r 160..255, g 85..150, b <=120, r-b >=70.
  red y-axis core is (112,40,51) -> b=51, g=40 -> g<85 so excluded.
  blue fitted line is dark navy/blue -> b>150 so excluded.
  caption red keyword (129,37,41) -> r<160 and g<85 -> excluded.
Red residual arrow signature: the arrow stroke color family. Measured nearby
  arrow samples are the C00000 family; use r>=90, r-b>=55, g<=95.
Panels (white interiors): LEFT x98..463 y111..470, RIGHT x489..867 y111..470.
"""
import numpy as np
from PIL import Image
from collections import deque

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

ORA = (r >= 160) & (g >= 85) & (g <= 155) & (b <= 125) & ((r - b) >= 70)
RED = (r >= 90) & ((r - b) >= 55) & (g <= 95) & (g >= 15)

def blobs(mask, x0, x1, y0, y1, minn=8, label=""):
    m = mask[y0:y1+1, x0:x1+1]
    H, W = m.shape
    seen = np.zeros_like(m, bool)
    out = []
    for yy in range(H):
        for xx in range(W):
            if m[yy, xx] and not seen[yy, xx]:
                q = deque([(yy, xx)]); seen[yy, xx] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True; q.append((ny, nx))
                if len(pts) >= minn:
                    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                    out.append((min(xs)+x0, max(xs)+x0, min(ys)+y0, max(ys)+y0, len(pts)))
    out.sort()
    print(f"  {label}: {len(out)} blobs, total px {int(m.sum())}")
    for X0, X1, Y0, Y1, n in out:
        cx = (X0+X1)/2; cy = (Y0+Y1)/2
        print(f"    n={n:5d} x {X0:4d}..{X1:4d} y {Y0:4d}..{Y1:4d} w={X1-X0+1:3d} h={Y1-Y0+1:3d} c=({cx:6.1f},{cy:6.1f})")
    return out

print("########## ORANGE SCATTER POINTS ##########")
print("-- LEFT panel interior x98..463 y111..470")
L_ORA = blobs(ORA, 98, 463, 111, 470, 8, "LEFT orange")
print("-- RIGHT panel interior x489..867 y111..470")
R_ORA = blobs(ORA, 489, 867, 111, 470, 8, "RIGHT orange")

print()
print("########## RED RESIDUAL ARROWS ##########")
print("-- LEFT panel (excluding red axes cols 125..127 and row 433..435)")
m = RED.copy()
m[:, 125:128] = False
m[433:436, :] = False
L_RED = blobs(m, 98, 463, 111, 470, 8, "LEFT red-arrow")
print("-- RIGHT panel (excluding red axes cols 539..541 and row 433..435)")
m2 = RED.copy()
m2[:, 539:542] = False
m2[433:436, :] = False
R_RED = blobs(m2, 489, 867, 111, 470, 8, "RIGHT red-arrow")
