#!/usr/bin/env python3
"""Generate slide 012 visuals: OR decision-boundary plot and perceptron diagram.

Colors follow the validated final analysis (analysis/slide_012_final.json):
red Cartesian axes, dark-blue boundary from (0,0.4) to (0.28,0), three green
points at (0,1),(1,1),(1,0), one cyan point at (0,0); blue weight labels,
light-blue Sigma node, plum step box with green/red rule lines.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

BLACK = "#000000"
AXIS_RED = "#c00000"
LINE_BLUE = "#0000ff"
GREEN = "#00ff00"
CYAN = "#00ffff"
PLOT_BG = "#ffffff"

# ---- Decision boundary plot -------------------------------------------------
# Boundary: from (0, 0.4) on the y-axis to (0.28, 0) on the x-axis.
# That is d(X) = -7x1 - 5x2 + 2 = 0  ->  x2 = (2 - 7x1) / 5
def boundary_x2(x1):
    return (2 - 7 * x1) / 5.0

fig, ax = plt.subplots(figsize=(4.6, 4.0), dpi=200)
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)

x1 = np.linspace(-0.08, 0.50, 50)
ax.plot(x1, boundary_x2(x1), color=LINE_BLUE, linewidth=3.0,
        solid_capstyle="round", zorder=2)

# OR data points: class 1 at (0,1),(1,1),(1,0); class 0 at (0,0)
ones = np.array([[0.0, 1.0], [1.0, 1.0], [1.0, 0.0]])
zeros = np.array([[0.0, 0.0]])
ax.scatter(ones[:, 0], ones[:, 1], c=GREEN, s=170, zorder=3,
           edgecolors="white", linewidths=1.0)
ax.scatter(zeros[:, 0], zeros[:, 1], c=CYAN, s=170, zorder=3,
           edgecolors="white", linewidths=1.0)

# L-shaped red axes with arrowheads
ax.annotate("", xy=(1.35, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=AXIS_RED, lw=1.8))
ax.annotate("", xy=(0, 1.35), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=AXIS_RED, lw=1.8))

# Axis labels
ax.text(1.37, -0.10, "x$_1$", fontsize=15, color=BLACK, ha="right", va="top")
ax.text(-0.07, 1.37, "x$_2$", fontsize=15, color=BLACK, ha="right", va="bottom")

# Red annotations at the line's axis crossings
ax.text(-0.10, 0.4, "0.4", fontsize=12, color=AXIS_RED, ha="right", va="center")
ax.text(0.2857, -0.10, "0.28", fontsize=12, color=AXIS_RED, ha="center", va="top")

ax.set_xlim(-0.42, 1.42)
ax.set_ylim(-0.32, 1.44)
ax.set_aspect("equal")
ax.axis("off")
plt.savefig(f"{outdir}/slide_012_decision_boundary.png", dpi=200,
            facecolor=PLOT_BG, bbox_inches="tight", pad_inches=0.05)
plt.close()
print("wrote slide_012_decision_boundary.png")

# ---- Perceptron diagram -----------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(4.8, 2.7), dpi=200)
fig2.patch.set_alpha(0.0)
ax2.set_facecolor("none")
ax2.axis("off")

def node_circle(x, y, r, fc="#add8e6", ec="#000000", lw=1.3, z=2):
    ax2.add_patch(mpatches.Circle((x, y), r, facecolor=fc,
                                  edgecolor=ec, linewidth=lw, zorder=z))

def arrow(x0, y0, x1, y1, color=BLACK, lw=1.3, z=3):
    ax2.annotate("", xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                 shrinkA=0, shrinkB=0), zorder=z)

# Inputs with blue weight labels
inputs = [
    ("x$_1$", "-7", 2.60, 0.98),
    ("x$_2$", "-5", 2.60, 0.00),
    ("1",     "2",  2.60, -0.98),
]
SUM_X, SUM_Y = 3.5, 0.0
for label, w, ix, iy in inputs:
    ax2.text(ix, iy, label, fontsize=13, color=BLACK, ha="center", va="center", zorder=4)
    ax2.text(ix + 0.42, iy, w, fontsize=12, color=LINE_BLUE,
             ha="left", va="center", zorder=4)
    arrow(ix + 0.42, iy, SUM_X - 0.45, SUM_Y)

# Sigma node
node_circle(SUM_X, SUM_Y, 0.44, z=2)
ax2.text(SUM_X, SUM_Y, r"$\Sigma$", fontsize=18, color=BLACK,
         ha="center", va="center", zorder=4)

# Step-function box, plum outline, green/red rule lines
box_x, box_y, box_w, box_h = 4.45, -0.55, 1.65, 1.10
ax2.add_patch(mpatches.FancyBboxPatch((box_x, box_y), box_w, box_h,
                                      boxstyle="round,pad=0.04,rounding_size=0.08",
                                      facecolor="none", edgecolor="#dda0dd",
                                      linewidth=1.6, zorder=2))
ax2.text(box_x + box_w/2, box_y + box_h*0.71, ">0 = 1",
         fontsize=12, color=GREEN, ha="center", va="center", zorder=4)
ax2.text(box_x + box_w/2, box_y + box_h*0.29, "\u22640 = 0",
         fontsize=12, color=AXIS_RED, ha="center", va="center", zorder=4)
arrow(SUM_X + 0.46, SUM_Y, box_x, SUM_Y)

# Output
ax2.text(6.55, 0.0, "O/P", fontsize=13, color=BLACK, ha="center", va="center", zorder=4)
arrow(box_x + box_w, SUM_Y, 6.22, SUM_Y)

ax2.set_xlim(-0.35, 6.95)
ax2.set_ylim(-1.45, 1.45)
ax2.set_aspect("equal")
plt.savefig(f"{outdir}/slide_012_perceptron.png", dpi=200,
            transparent=True, bbox_inches="tight", pad_inches=0.04)
plt.close()
print("wrote slide_012_perceptron.png")
