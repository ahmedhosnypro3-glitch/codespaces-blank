#!/usr/bin/env python3
"""Slide 15/16 network diagram, v2. Canvas == placed area: x=0.5,y=1.3,w=12.3,h=4.4
Placed in pptx at (0.5,1.3) size 12.3x4.4 -> local lx = slide_x-0.5, ly = 5.7-slide_y.
Geometry measured from unique_slides/slide_015.jpg (72px/in):
 cols slide x 2.00/5.93/8.10, rows slide y 2.52/3.54/4.68, R=0.25.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

W_IN, H_IN = 12.3, 4.4
fig = plt.figure(figsize=(W_IN, H_IN), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_IN)
ax.set_ylim(0, H_IN)
ax.axis("off")
fig.patch.set_alpha(0.0)

SIGMA = "#C0392B"
WTXT = "#2980B9"
BIAS = "#8E44AD"
R = 0.25
COL1, COL2, COL3 = 1.50, 5.43, 7.60          # local x
ROWS = [3.18, 2.16, 1.02]                     # local y (top, mid, bot)

def node(col, y, fill):
    ax.add_patch(Circle((col, y), R, facecolor=fill, edgecolor="black", linewidth=1.3, zorder=5))
    ax.text(col, y, r"$\Sigma$", fontsize=20, fontweight="bold", color=SIGMA,
            ha="center", va="center", zorder=6)
    ax.add_patch(FancyBboxPatch((col + 0.42, y - 0.13), 0.34, 0.26,
                                boxstyle="round,pad=0.02", facecolor="white",
                                edgecolor="black", linewidth=1.0, zorder=4))
    ax.text(col + 0.59, y, "f", fontsize=10, fontweight="bold", color="black",
            ha="center", va="center", zorder=5)

for y in ROWS:
    node(COL1, y, "white")
for y in ROWS:
    node(COL2, y, "#90EE90")
    ax.text(COL2 - 0.72, y + 0.40, r"$Net_j$", fontsize=11, fontweight="bold",
            color=SIGMA, ha="center", va="center", zorder=6)
    ax.text(COL2 + 0.95, y + 0.40, r"$O_j$", fontsize=11, color="black",
            ha="center", va="center", zorder=6)
for y in ROWS:
    node(COL3, y, "#FFA07A")
    ax.text(COL3 - 0.72, y + 0.40, r"$Net_k$", fontsize=11, fontweight="bold",
            color=SIGMA, ha="center", va="center", zorder=6)
    ax.text(COL3 + 0.95, y + 0.40, r"$O_k$", fontsize=11, color="black",
            ha="center", va="center", zorder=6)

# inter-layer arrows
for iy in ROWS:
    for hy in ROWS:
        ax.add_patch(FancyArrowPatch((COL1 + R + 0.42, iy), (COL2 - R, hy),
                                     connectionstyle="arc3,rad=0.05", arrowstyle="->",
                                     mutation_scale=7, linewidth=0.6, color="#808080", zorder=3))
for hy in ROWS:
    for oy in ROWS:
        ax.add_patch(FancyArrowPatch((COL2 + R + 0.42, hy), (COL3 - R, oy),
                                     connectionstyle="arc3,rad=-0.05", arrowstyle="->",
                                     mutation_scale=7, linewidth=0.6, color="#808080", zorder=3))
ax.text((COL1 + COL2) / 2, ROWS[0] + 0.55, r"$w_{ji}$", fontsize=10, fontweight="bold",
        color=WTXT, ha="center", va="center", zorder=6)
ax.text((COL1 + COL2) / 2 + 0.3, ROWS[2] - 0.55, r"$w_{ji}$", fontsize=10, fontweight="bold",
        color=WTXT, ha="center", va="center", zorder=6)
ax.text((COL2 + COL3) / 2, ROWS[0] + 0.55, r"$w_{kj}$", fontsize=10, fontweight="bold",
        color=WTXT, ha="center", va="center", zorder=6)
ax.text((COL2 + COL3) / 2 - 0.3, ROWS[2] - 0.55, r"$w_{kj}$", fontsize=10, fontweight="bold",
        color=WTXT, ha="center", va="center", zorder=6)
# bias: purple circled-1 markers + Node Bias label (slide y~5.2-5.45 -> local ~0.25-0.45)
for bx in (0.57, 3.97, 6.28):
    ax.add_patch(Circle((bx, 0.45), 0.16, facecolor=BIAS, edgecolor="black", linewidth=1, zorder=5))
    ax.text(bx, 0.45, "1", fontsize=8, fontweight="bold", color="white",
            ha="center", va="center", zorder=6)
ax.text(0.57, 0.75, "Node Bias", fontsize=10, color="black", ha="center", va="center", zorder=6)

# output label boxes (slide x 8.79..9.17 -> local 8.29..8.67)
for y, lab in zip(ROWS, ["Output 1", "Output 2", "Output m"]):
    ax.add_patch(FancyBboxPatch((COL3 + 0.72, y - 0.16), 0.42, 0.32,
                                boxstyle="round,pad=0.02", facecolor="#FFA07A",
                                edgecolor="#FF4500", linewidth=1.2, zorder=4))
    ax.text(COL3 + 0.93, y, lab, fontsize=7, fontweight="bold", color="#FF4500",
            ha="center", va="center", zorder=5)

# dashed red backprop arrows from output column back to hidden column
for oy, hy in zip(ROWS, ROWS):
    ax.add_patch(FancyArrowPatch((COL3 + 0.55, oy), (COL2 - 0.4, hy),
                                 connectionstyle="arc3,rad=0.35", arrowstyle="->",
                                 mutation_scale=7, linewidth=1.0, color="#C00000",
                                 linestyle="--", zorder=3))

# arrow from Input Sample box (drawn in JS at slide 0.89..1.79, y 1.33..1.74) to input col
ax.add_patch(FancyArrowPatch((1.35, 4.15), (COL1 - R, ROWS[1]),
                             connectionstyle="arc3,rad=-0.2", arrowstyle="->",
                             mutation_scale=10, linewidth=1.4, color=BIAS, zorder=3))
# arrow from output col to Target Label box (slide 11.36..12.25, y 1.32..1.74)
ax.add_patch(FancyArrowPatch((COL3 + 1.15, ROWS[1]), (10.9, 4.2),
                             connectionstyle="arc3,rad=-0.25", arrowstyle="->",
                             mutation_scale=10, linewidth=1.4, color=BIAS, zorder=3))

import sys
out = sys.argv[1] if len(sys.argv) > 1 else "slide_diagram_v2.png"
fig.savefig(out, dpi=600, transparent=True)
plt.close(fig)
print("ok", out)
