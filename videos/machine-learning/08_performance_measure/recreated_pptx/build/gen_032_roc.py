#!/usr/bin/env python3
"""ROC plot PNG for slide 32, matched to the measured original region.

Original frame (960x540, 1px=1pt). Plot panel box x[634,902] y[43,344];
inner blue-bordered plot area x[641,895] y[80,311]; data area FPR 0->1 maps
x 661->874, TPR 0->1 maps y 311->150. Red axes with arrows, light-cyan field,
red OPEN circle markers, NO connecting line, threshold labels in small white
bordered boxes. Output at 600 dpi; embed with w = px/600 in.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DPI = 600
X0, X1 = 634, 902   # image box, 268 px wide
Y0, Y1 = 344, 43    # y flipped: bottom=344, top=43 (301 px tall)
W_IN = (X1 - X0) / 72.0
H_IN = (Y0 - Y1) / 72.0

# data area (fractions of the image box), measured from the original
LX = (661 - X0) / (X1 - X0)
RX = (874 - X0) / (X1 - X0)
BY = 1 - (311 - Y1) / (Y0 - Y1)
TY = 1 - (150 - Y1) / (Y0 - Y1)

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([LX, BY, RX - LX, TY - BY])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_facecolor("#EEFEFB")  # light cyan plot field (measured)

# grid at 0.2 steps, clipped to the data area
for v in [0.2, 0.4, 0.6, 0.8]:
    ax.axvline(v, color="#B9CAD1", lw=0.7, zorder=1)
    ax.axhline(v, color="#B9CAD1", lw=0.7, zorder=1)
ax.set_axisbelow(True)

# ROC points (no connecting line in the original): (fpr, tpr) with labels
pts = [(0.16, 0.8, "0.4"), (0.33, 1.0, "0.3"), (0.66, 1.0, "0.1"), (1.0, 1.0, "0.0")]
xs = [p[0] for p in pts]
ys = [p[1] for p in pts]
ax.scatter(xs, ys, s=52, facecolors="none", edgecolors="#FF0000", linewidths=1.6, zorder=4)

# threshold labels in small white bordered boxes, offset down-left of each point
for (x, y, lab) in pts:
    ax.annotate(lab, (x, y), xytext=(x - 0.075, y - 0.085), fontsize=7.5,
                color="#000000", zorder=5, ha="center", va="center",
                bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="#FF0000", lw=0.8))

# red axes with arrowheads extending past the data area into the panel margins
for sp in ("left", "bottom"):
    ax.spines[sp].set_color("#C00000")
    ax.spines[sp].set_linewidth(1.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.annotate("", xy=(1.135, 0), xytext=(1.0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.4),
            annotation_clip=False, zorder=6)
ax.annotate("", xy=(0, 1.31), xytext=(0, 1.0),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.4),
            annotation_clip=False, zorder=6)

# no numeric tick labels in the original (grid only)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.tick_params(length=2, pad=1, color="#C00000")

# axis labels: TPR left of the y-axis (outside the blue plot border), FPR below x-axis
ax.set_ylabel("TPR", fontsize=9, color="#000000", labelpad=1)
ax.set_xlabel("FPR", fontsize=9, color="#000000", labelpad=1)

fig.savefig("assets/roc_032_v2.png", dpi=DPI, transparent=True)
print("saved assets/roc_032_v2.png")
from PIL import Image
im = Image.open("assets/roc_032_v2.png")
print("px size:", im.size, "-> in:", im.size[0] / DPI, im.size[1] / DPI)
