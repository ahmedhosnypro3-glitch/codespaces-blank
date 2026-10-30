#!/usr/bin/env python3
"""Generate the ROC plot PNG for slide 32, matched to the measured original region.

Original frame (960x540, 1px=1pt): plot box x[634,902] y[43,344]; grid lines at
x=702,745,788,831,874 (0.2..0.8) and y=150,193,232,271,311 (0.2..0.8); red points
(fpr,tpr) = (0.16,0.8),(0.33,1),(0.66,1),(1,1) at px ~(651,242),(690,194),(726,148),
(811,148),(875,148); threshold labels 0.4/0.3/0.1/0.0 near points; axes with arrows,
TPR y-label, FPR x-label. Output PNG is rendered at 600 dpi so that 1px@600dpi =
1/600 in, placed with w = px/600 in.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DPI = 600
# plot box in original px -> inches (1px = 1pt = 1/72 in)
X0, X1 = 634, 902   # 268 px wide
Y0, Y1 = 344, 43    # y flipped: bottom=344, top=43 (301 px tall)
W_IN = (X1 - X0) / 72.0
H_IN = (Y0 - Y1) / 72.0

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# grid (light gray) at 0.2 steps
for v in [0.2, 0.4, 0.6, 0.8]:
    ax.axvline(v, color="#B0B0B0", lw=0.8, zorder=1)
    ax.axhline(v, color="#B0B0B0", lw=0.8, zorder=1)

# ROC points + connecting line (red), order lower-left -> upper-right
fpr = [0.16, 0.33, 0.66, 1.0]
tpr = [0.8, 1.0, 1.0, 1.0]
ax.plot(fpr, tpr, color="#FF0000", lw=1.6, zorder=3)
ax.scatter(fpr, tpr, s=42, color="#FF0000", zorder=4, edgecolors="#FF0000")

# threshold labels near points (white boxes like the original)
labels = ["0.4", "0.3", "0.1", "0.0"]
offsets = [(-0.055, -0.075), (-0.05, -0.075), (-0.05, -0.075), (-0.045, -0.075)]
for (x, y, lab, (dx, dy)) in zip(fpr, tpr, labels, offsets):
    ax.annotate(lab, (x, y), xytext=(x + dx, y + dy), fontsize=7.5,
                color="#000000", zorder=5,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))

# axes on left/bottom with arrows (black)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.spines["left"].set_color("#000000")
ax.spines["bottom"].set_color("#000000")
ax.spines["left"].set_linewidth(1.2)
ax.spines["bottom"].set_linewidth(1.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# arrowheads
ax.plot(0, 1, "^", color="#000000", ms=7, clip_on=False, zorder=6)
ax.plot(1, 0, ">", color="#000000", ms=7, clip_on=False, zorder=6)

# tick labels 0..1
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1"], fontsize=6.5)
ax.set_yticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1"], fontsize=6.5)
ax.tick_params(length=2, pad=1, color="#000000")

# axis labels
ax.set_ylabel("TPR", fontsize=9, color="#000000", labelpad=2)
ax.set_xlabel("FPR", fontsize=9, color="#000000", labelpad=2)

fig.savefig("roc_032.png", dpi=DPI, transparent=True)
print("saved roc_032.png")
from PIL import Image
im = Image.open("roc_032.png")
print("px size:", im.size, "-> in:", im.size[0] / DPI, im.size[1] / DPI)
