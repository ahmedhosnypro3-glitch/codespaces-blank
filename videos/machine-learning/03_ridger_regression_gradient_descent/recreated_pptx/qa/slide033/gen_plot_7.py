#!/usr/bin/env python3
"""Generate the slide-033 function plot as a 600-dpi PNG (attempt 7).

The original frame's plot is the analytic function f(x) = (x^2 cos(x) - x)/10
over the plotted x-range. The mapping was fitted on the original's teal ink
(177 columns, median residual 0.34 px):
    x_px = 721.5 + 8.95 * x,   y_px = 172.0 - 9.25 * f(x)
Plot box (dark-red border) x607..845, y60..313; inner white area x608..844,
y62..312 (236 x 250 px = 236 x 250 pt -> 1 px = 1 pt at 150-dpi render scale).
Image placed at exact 236/72 x 250/72 in (600 dpi -> 1966 x 2083 px).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DPI = 600
W_IN, H_IN = 236 / 72.0, 250 / 72.0
X0, SX, Y0, SY = 721.5, 8.95, 172.0, 9.25
XLIM = ((608 - X0) / SX, (844 - X0) / SX)      # -12.6816 .. 13.6872
YLIM = ((Y0 - 312) / SY, (Y0 - 62) / SY)       # -15.1351 .. 11.8919
TEAL = "#2FA9AC"

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Liberation Serif", "DejaVu Serif"]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
ax.set_facecolor("white")
ax.axis("off")

# light grid every 2 units
for gx in np.arange(-12, 14, 2):
    ax.plot([gx, gx], [YLIM[0], YLIM[1]], color="#D9D9D9", lw=0.45, zorder=0)
for gy in np.arange(-14, 12, 2):
    ax.plot([XLIM[0], XLIM[1]], [gy, gy], color="#D9D9D9", lw=0.45, zorder=0)

# axes with double arrowheads
ax.annotate("", xy=(13.30, 0), xytext=(-12.25, 0),
            arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.0,
                            mutation_scale=9, shrinkA=0, shrinkB=0), zorder=2)
ax.annotate("", xy=(0, 11.30), xytext=(0, -14.45),
            arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.0,
                            mutation_scale=9, shrinkA=0, shrinkB=0), zorder=2)

# tick marks
for tx in np.arange(-12, 14, 2):
    ax.plot([tx, tx], [-0.45, 0.45], color="black", lw=0.9, zorder=2)
for ty in np.arange(-14, 12, 2):
    ax.plot([-0.45, 0.45], [ty, ty], color="black", lw=0.9, zorder=2)

# tick labels
for tx in range(-10, 12, 2):
    if tx == 0:
        continue
    ax.text(tx, -0.95, str(tx), ha="center", va="top", fontsize=6.6, color="#333333")
for ty in [8, 6, 4, 2, -4, -6, -8, -10, -12]:
    ax.text(-0.60, ty, str(ty), ha="right", va="center", fontsize=6.6, color="#333333")
ax.text(0, 10.45, "y", ha="center", va="bottom", fontsize=8.2, color="#333333")

# the function curve
x = np.linspace(XLIM[0], XLIM[1], 3000)
y = (x * x * np.cos(x) - x) / 10.0
ax.plot(x, y, color=TEAL, lw=2.6, solid_capstyle="round", zorder=3)

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "build", "assets", "slide_033_plot_v7.png")
fig.savefig(out, dpi=DPI, facecolor="white")
print("WROTE", out)
from PIL import Image
print("size", Image.open(out).size)
