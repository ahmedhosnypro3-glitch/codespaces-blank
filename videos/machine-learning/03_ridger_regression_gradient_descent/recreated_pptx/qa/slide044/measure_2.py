#!/usr/bin/env python3
"""Precise per-element measurement of slide_044.jpg."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def hx(v): return f"#{v[0]:02X}{v[1]:02X}{v[2]:02X}"

# panel E9E9E7 core is (233,232,231); JPEG tolerance +/-10
PANEL = (abs(r - 233) < 10) & (abs(g - 232) < 10) & (abs(b - 231) < 10)
print("panel px:", PANEL.sum())
ys, xs = np.where(PANEL)
print("panel bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())
# panel edges: for each row in a band, find min/max panel col
for yy in (50, 200, 300, 400, 500):
    cols = np.where(PANEL[yy])[0]
    if len(cols): print(f"  row {yy}: panel x {cols.min()}..{cols.max()}")

# interior of the panel only: x 60..900, y 46..536
IN_X0, IN_X1, IN_Y0, IN_Y1 = 61, 900, 46, 536
# ink = differs from panel AND not white-ish
outside = ~PANEL
white = (r > 244) & (g > 244) & (b > 244)
ink = outside & ~white
ink[:, :IN_X0] = False
ink[:, IN_X1:] = False
ink[:IN_Y0] = False
ink[IN_Y1+1:] = False
print("\ninterior ink px:", ink.sum())

def runs_1d(cnt, thr, axis=0):
    out = []
    inr = False
    n = len(cnt)
    for i in range(n):
        if cnt[i] > thr and not inr:
            inr = True; a = i
        elif cnt[i] <= thr and inr:
            inr = False; out.append((a, i - 1))
    if inr: out.append((a, n - 1))
    return out

print("\n=== TEXT ROW BANDS (ink rows, thr=6) ===")
rc = ink.sum(axis=1)
for y0, y1 in runs_1d(rc, 6):
    cols = np.where(ink[y0:y1+1].any(axis=0))[0]
    if len(cols):
        print(f"  y {y0:>3}-{y1:<3} (h{y1-y0+1:>3})  x {cols.min():>3}..{cols.max():>3}  px={int(ink[y0:y1+1].sum())}")

print("\n=== TEXT COLUMN BANDS (ink cols, thr=5) ===")
cc = ink.sum(axis=0)
for x0, x1 in runs_1d(cc, 5):
    rows = np.where(ink[:, x0:x1+1].any(axis=1))[0]
    if len(rows):
        print(f"  x {x0:>3}-{x1:<3} (w{x1-x0+1:>3})  y {rows.min():>3}..{rows.max():>3}  px={int(ink[:,x0:x1+1].sum())}")
