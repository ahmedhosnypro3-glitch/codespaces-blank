"""Regenerate slide_015 graph asset v2: red y=1/x hyperbola, x ticks -6..6, y ticks -3..3,
yellow translucent oval over the steep branches near the y-axis, light grid, black axes
with arrowheads + x/y labels, 'y = 1/x' caption, red panel border.

Geometry measured from unique_slides/slide_015.jpg (960x540, 1px = 1pt):
  panel red border x 661..859, y 97..273 (198 x 176 px)
  y-axis at frame x ~746.5, x-axis at frame y ~193, grid spacing 16 px/unit
  yellow oval frame x 741..774, y 99..219
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_015_graph_v2.png")

PANEL_W_IN = 198.0 / 72.0
PANEL_H_IN = 176.0 / 72.0

# axes cross fractions inside the panel (measured: y-axis 85.5/199, x-axis 96/177 from top)
AX_X_FRAC = 0.4296
AX_Y_FRAC_FROM_TOP = 0.5424

S = 198.0 / 13.8          # px per data unit, x span 13.8 units
X_SPAN = 13.8
Y_SPAN = 176.0 / (198.0 / X_SPAN)  # keep isotropic
XLIM = (-AX_X_FRAC * X_SPAN, (1 - AX_X_FRAC) * X_SPAN)          # (-5.93, 7.87)
YLIM = (-AX_Y_FRAC_FROM_TOP * Y_SPAN, (1 - AX_Y_FRAC_FROM_TOP) * Y_SPAN)

fig = plt.figure(figsize=(PANEL_W_IN, PANEL_H_IN), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(False)

# graph-paper grid at every integer, light gray
ax.set_xticks(np.arange(np.floor(XLIM[0]), np.ceil(XLIM[1]) + 1))
ax.set_yticks(np.arange(np.floor(YLIM[0]), np.ceil(YLIM[1]) + 1))
ax.grid(True, color="#D9D9D9", linewidth=0.5)
# labeled ticks per spec: x -6..6, y -3..3
ax.set_xticks(range(-6, 7))
ax.set_yticks(range(-3, 4))
ax.tick_params(axis="both", direction="out", length=2.5, labelsize=5.5,
               colors="black", pad=1, width=0.6)

# black axes through origin with arrowheads
ax.axhline(0, color="#404040", linewidth=0.9, zorder=2)
ax.axvline(0, color="#404040", linewidth=0.9, zorder=2)
ax.annotate("", xy=(XLIM[1], 0), xytext=(XLIM[1] - 0.55, 0),
            arrowprops=dict(arrowstyle="-|>", color="#404040", lw=0.9), zorder=2)
ax.annotate("", xy=(0, YLIM[1]), xytext=(0, YLIM[1] - 0.55),
            arrowprops=dict(arrowstyle="-|>", color="#404040", lw=0.9), zorder=2)

# red hyperbola y = 1/x, quadrants I and III
for lo, hi in ((XLIM[0], -0.06), (0.06, XLIM[1])):
    xs = np.linspace(lo, hi, 800)
    ax.plot(xs, 1.0 / xs, color="#C00000", linewidth=1.5,
            solid_capstyle="round", zorder=4)

# translucent yellow oval over the steep branches near the y-axis
# measured frame x 741..774, y 99..219; frame y grows downward, data y grows upward
sx = 198.0 / X_SPAN
sy = 176.0 / Y_SPAN
data_cx = XLIM[0] + ((741 + 774) / 2.0 - 661.0) / sx
data_cy = YLIM[1] - (((99 + 219) / 2.0) - 97.0) / sy
ell = Ellipse((data_cx, data_cy), width=(774 - 741) / sx, height=(219 - 99) / sy,
              facecolor="#FFFF00", alpha=0.42, edgecolor="none", zorder=5)
ax.add_patch(ell)

# caption y = 1/x (stacked-fraction mathtext; safe under ground rule (e)) top right-of-center
ax.text(3.2, YLIM[1] - 0.55, r"$y = \frac{1}{x}$", fontsize=8, color="black",
        ha="left", va="center", zorder=6)

# axis labels at the arrow ends
ax.text(XLIM[1] - 0.25, -0.42, "x", fontsize=8, color="black",
        ha="right", va="center", style="italic", zorder=6)
ax.text(0.28, YLIM[1] - 0.18, "y", fontsize=8, color="black",
        ha="left", va="center", style="italic", zorder=6)

# red panel border
ax.add_patch(plt.Rectangle((XLIM[0], YLIM[0]), XLIM[1] - XLIM[0], YLIM[1] - YLIM[0],
                           fill=False, edgecolor="#C00000", linewidth=1.8,
                           clip_on=False, zorder=10))

fig.savefig(OUT, dpi=600, facecolor="white")
plt.close(fig)
print("wrote", OUT, "xlim", XLIM, "ylim", YLIM, "ellipse center", (round(data_cx, 2), round(data_cy, 2)))
