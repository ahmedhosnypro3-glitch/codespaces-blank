#!/usr/bin/env python3
"""Generate the slide-034 function plot as a 600-dpi PNG (attempt 27).

Same analytic function as slide 033, fitted to THIS frame's teal ink
(att27_frame_measure.txt: X0=721.825 SX=8.9296 Y0=172.336 SY=8.8443,
residual median 0.912 px):
    x_px = 721.825 + 8.9296 * x,   y_px = 172.336 - 8.8443 * f(x)
Plot box (dark-red border) x607..846, y60..313; asset covers x608..845,
y59..313 (237 x 254 pt -> 1975 x 2117 px at 600 dpi).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DPI = 600
W_IN, H_IN = 237 / 72.0, 254 / 72.0
X0, SX, Y0, SY = 721.825, 8.9296, 172.336, 8.8443
XLIM = ((608 - X0) / SX, (845 - X0) / SX)      # -12.7460 .. 13.7952
YLIM = ((Y0 - 313) / SY, (Y0 - 59) / SY)       # -15.9037 .. 12.8125
TEAL = "#45C0CC"

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

# axes with double arrowheads (frame-measured extents)
ax.annotate("", xy=(12.34, 0), xytext=(-11.85, 0),
            arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.0,
                            mutation_scale=9, shrinkA=0, shrinkB=0), zorder=2)
ax.annotate("", xy=(0, 10.668), xytext=(0, -15.108),
            arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.0,
                            mutation_scale=9, shrinkA=0, shrinkB=0), zorder=2)

# tick marks at the labeled values only
XT = [-10, -8, -6, -4, 2, 6, 8, 10]
YT = [8, 6, 4, 2, -4, -6, -8, -10, -12]
for tx in XT:
    ax.plot([tx, tx], [-0.25, 0.25], color="black", lw=0.9, zorder=2)
for ty in YT:
    ax.plot([-0.25, 0.25], [ty, ty], color="black", lw=0.9, zorder=2)

# tick labels (0 / -2 / 4 absent on the frame)
for tx in XT:
    ax.text(tx, -0.95, str(tx), ha="center", va="top", fontsize=6.6, color="#333333")
for ty in YT:
    ax.text(-0.60, ty, str(ty), ha="right", va="center", fontsize=6.6, color="#333333")
ax.text(0, 11.05, "y", ha="center", va="bottom", fontsize=8.2,
        color="#333333", fontstyle="italic")
ax.text(12.8, 0, "x", ha="center", va="center", fontsize=8.2,
        color="#333333", fontstyle="italic")

# the function curve
x = np.linspace(XLIM[0], XLIM[1], 3000)
y = (x * x * np.cos(x) - x) / 10.0
ax.plot(x, y, color=TEAL, lw=2.6, solid_capstyle="round", zorder=3)

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "build", "assets", "slide_034_plot_v27.png")
fig.savefig(out, dpi=DPI, facecolor="white")
print("WROTE", out)
from PIL import Image
print("size", Image.open(out).size)
