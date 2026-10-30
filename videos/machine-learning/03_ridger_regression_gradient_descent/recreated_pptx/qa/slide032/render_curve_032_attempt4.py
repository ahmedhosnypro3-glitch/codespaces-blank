#!/usr/bin/env python3
"""Render the slide-032 loss curve f(x)=(x-5)^2+1 as a transparent PNG.

Vectors aren't needed: the plot's data->px calibration is fixed
(x0=630.5 + 11.5*x, y0=266 - 12*y).  We rasterize the curve at 600 dpi
so the PNG's own pixels carry the analytic shape, then the builder
places it as ONE addImage over the plot box.  Rendered tight to the ink.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

# --- plot calibration, frame px (1 frame px = 1 pt) -----------------------
XC, SX = 630.5, 11.5
YC, SY = 266.0, 12.0
PLOT_X0, PLOT_X1 = 573.0, 810.0
PLOT_Y0, PLOT_Y1 = 66.0, 265.0

DPI = 600
PXW = 2            # curve stroke width in frame px (~2pt)

# visible span: (x-5)^2+1 <= yMax at plot top
YMAX = (YC - PLOT_Y0) / SY
XVIS_LO = 5 - (YMAX - 1) ** 0.5
XVIS_HI = 5 + (YMAX - 1) ** 0.5

N = 3000
xs = np.linspace(XVIS_LO, XVIS_HI, N)
ys = (xs - 5) ** 2 + 1
px = XC + SX * xs
py = YC - SY * ys
# keep only inside the plot box
keep = (px >= PLOT_X0) & (px <= PLOT_X1) & (py >= PLOT_Y0) & (py <= PLOT_Y1)
px, py = px[keep], py[keep]

X0, X1 = px.min(), px.max()
Y0, Y1 = py.min(), py.max()
W = int(round((X1 - X0) * DPI / 72.0)) + 4 * PXW
H = int(round((Y1 - Y0) * DPI / 72.0)) + 4 * PXW
sc = DPI / 72.0

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
pts = [((p - X0) * sc + 2 * PXW, (q - Y0) * sc + 2 * PXW) for p, q in zip(px, py)]
d.line(pts, fill=(0, 0, 255, 255), width=int(round(PXW * sc)), joint="curve")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "curve_032.png")
img.save(out)

# ink bbox for placement
a = np.asarray(img)
m = a[:, :, 3] > 0
ys2, xs2 = np.where(m)
meta = {
    "path": "curve_032.png",
    "w_px": W,
    "h_px": H,
    "ink_x0": int(xs2.min()),
    "ink_y0": int(ys2.min()),
    "ink_x1": int(xs2.max()),
    "ink_y1": int(ys2.max()),
    "frame_x0": X0,
    "frame_y0": Y0,
    "frame_x1": X1,
    "frame_y1": Y1,
    "x_in": W / DPI,
    "y_in": H / DPI,
    "dpi": DPI,
}
print(json.dumps(meta, indent=2))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "curve_032.json"), "w") as f:
    json.dump(meta, f)

# --- second-difference ripple check on the analytic sampler ---------------
t = np.linspace(0, 1, N)
u = XVIS_LO + (XVIS_HI - XVIS_LO) * t
v = (u - 5) ** 2 + 1
d2 = np.diff(v, 2)
ripple = float(np.max(np.abs(d2)))
print("second-difference max ripple: %.6g frame-px (verify is ~0 for a quadratic)" % ripple)
