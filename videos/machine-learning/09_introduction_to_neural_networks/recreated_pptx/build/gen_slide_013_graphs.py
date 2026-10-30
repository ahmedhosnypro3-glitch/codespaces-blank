#!/usr/bin/env python3
"""Generate slide 013 visuals: XOR scatter plot and perceptron diagram with ? weights.

Colors follow the validated final analysis (analysis/slide_013_final.json):
dark-blue (#191970) diagonal lines, red (#B22222) X markers, green (#008000)
and cyan (#00CED1) circles, purple (#9370DB) step box, blue ? weights.
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
BLUE_LINE = "#191970"
GREEN = "#008000"
CYAN = "#00CED1"
RED_X = "#B22222"
PURPLE = "#9370db"
PLOT_BG = "#ffffff"

# ---- XOR scatter plot -------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.6, 4.0), dpi=200)
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)

# Two thick dark-blue diagonal lines, downward L-to-R
x1 = np.linspace(-0.10, 1.45, 50)
ax.plot(x1, 1.32 - 1.45 * x1, color=BLUE_LINE, linewidth=3.2,
        solid_capstyle="round", zorder=2)
ax.plot(x1, 0.92 - 0.72 * x1, color=BLUE_LINE, linewidth=3.2,
        solid_capstyle="round", zorder=2)

# Six markers: 2 red X, 2 green circles, 2 cyan circles
ax.scatter([0.12, 0.30], [1.05, 0.85], c=RED_X, s=150, marker="x",
           linewidths=2.6, zorder=3)
ax.scatter([0.38, 1.02], [0.40, 0.06], c=GREEN, s=150, zorder=3,
           edgecolors="white", linewidths=1.0)
ax.scatter([0.12, 0.78], [0.14, 0.62], c=CYAN, s=150, zorder=3,
           edgecolors="white", linewidths=1.0)

# Black axes with arrowheads
ax.annotate("", xy=(1.4, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.6))
ax.annotate("", xy=(0, 1.4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.6))

ax.text(1.42, -0.10, "x$_1$", fontsize=15, color=BLACK, ha="right", va="top")
ax.text(-0.07, 1.42, "x$_2$", fontsize=15, color=BLACK, ha="right", va="bottom")

# Small handwritten-style annotation near center
ax.text(0.56, 0.54, "?", fontsize=11, color=BLACK, ha="center",
        va="center", style="italic")

ax.set_xlim(-0.40, 1.44)
ax.set_ylim(-0.30, 1.46)
ax.set_aspect("equal")
ax.axis("off")
plt.savefig(f"{outdir}/slide_013_scatter.png", dpi=200,
            facecolor=PLOT_BG, bbox_inches="tight", pad_inches=0.05)
plt.close()
print("wrote slide_013_scatter.png")

# ---- Perceptron diagram with ? weights --------------------------------------
fig2, ax2 = plt.subplots(figsize=(4.8, 2.7), dpi=200)
fig2.patch.set_alpha(0.0)
ax2.set_facecolor("none")
ax2.axis("off")

def node_circle(x, y, r, fc="#add8e6", ec="#000000", lw=1.3, z=2):
    ax2.add_patch(mpatches.Circle((x, y), r, facecolor=fc,
                                  edgecolor=ec, linewidth=lw, zorder=z))

def arrow(x0, y0, x1, y1, color="#888888", lw=1.2, z=3):
    ax2.annotate("", xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                 shrinkA=0, shrinkB=0), zorder=z)

inputs = [
    ("x$_1$", 2.60, 0.98),
    ("x$_2$", 2.60, 0.00),
    ("1",     2.60, -0.98),
]
SUM_X, SUM_Y = 3.55, 0.0
for label, ix, iy in inputs:
    ax2.text(ix, iy, label, fontsize=13, color=BLACK, ha="center", va="center", zorder=4)
    ax2.text(ix + 0.42, iy, "?", fontsize=13, color="#0000ff",
             ha="left", va="center", zorder=4)
    arrow(ix + 0.42, iy, SUM_X - 0.48, SUM_Y)

node_circle(SUM_X, SUM_Y, 0.44, z=2)
ax2.text(SUM_X, SUM_Y, r"$\Sigma$", fontsize=18, color=BLACK,
         ha="center", va="center", zorder=4)

# Step-function box, purple outline, with a step glyph
box_x, box_y, box_w, box_h = 4.50, -0.55, 1.60, 1.10
ax2.add_patch(mpatches.FancyBboxPatch((box_x, box_y), box_w, box_h,
                                      boxstyle="round,pad=0.04,rounding_size=0.08",
                                      facecolor="none", edgecolor=PURPLE,
                                      linewidth=1.6, zorder=2))
# mini step-function glyph
gx0, gy0 = box_x + box_w/2 - 0.26, box_y + box_h/2 - 0.12
ax2.plot([gx0, gx0 + 0.12], [gy0, gy0], color=BLACK, lw=1.8, zorder=4)
ax2.plot([gx0 + 0.12, gx0 + 0.12], [gy0, gy0 + 0.26], color=BLACK, lw=1.8, zorder=4)
ax2.plot([gx0 + 0.12, gx0 + 0.44], [gy0 + 0.26, gy0 + 0.26], color=BLACK, lw=1.8, zorder=4)
arrow(SUM_X + 0.47, SUM_Y, box_x, SUM_Y)

# Output
ax2.text(6.55, 0.0, "O/P", fontsize=13, color=BLACK, ha="center", va="center", zorder=4)
arrow(box_x + box_w, SUM_Y, 6.22, SUM_Y)

ax2.set_xlim(-0.35, 6.95)
ax2.set_ylim(-1.45, 1.45)
ax2.set_aspect("equal")
plt.savefig(f"{outdir}/slide_013_perceptron.png", dpi=200,
            transparent=True, bbox_inches="tight", pad_inches=0.04)
plt.close()
print("wrote slide_013_perceptron.png")
