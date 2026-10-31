#!/usr/bin/env python3
"""ROC plot PNG for slide 32 (v3), matched to the measured original frame.

Original 960x540 (1px = 1pt). Measured: blue plot border x[641,895] y[80,386];
red axes x=661 (vertical, arrow up) and y=351 (horizontal, arrow right);
cyan field #EEFEFB; grid; four red OPEN circle markers with white red-bordered
threshold labels offset down-left; no connecting polyline.
Marker/label pixel centers measured in unique_slides/slide_032.jpg.
Image box x[634,902] y[43,390] -> placed at 268/72 x 347/72 in.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DPI = 600
BX0, BY0, BX1, BY1 = 634, 43, 902, 390
W_IN = (BX1 - BX0) / 72.0
H_IN = (BY1 - BY0) / 72.0

# (marker center, label text, label center) in original-frame px, measured
MARKS = [
    ((742, 125), "0.3", (726, 147)),
    ((827, 125), "0.1", (811, 147)),
    ((887, 125), "0.0", (871, 147)),
    ((683, 218), "0.4", (667, 240)),
]
AX_X = 661          # red y-axis
AX_Y = 351          # red x-axis
PLOT = (641, 80, 895, 386)  # blue border: left, top, right, bottom

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(BX0, BX1)
ax.set_ylim(BY1, BY0)  # original-frame pixel coords, y down
ax.axis("off")

lx, ty, rx, by = PLOT
ax.add_patch(plt.Rectangle((lx, by), rx - lx, ty - by, fc="#EEFEFB", ec="none", zorder=1))

# grid at 0.2 steps across the plot
for gx in [708, 755, 802, 848]:
    ax.plot([gx, gx], [ty, by], color="#B9CAD1", lw=0.7, zorder=2)
for gy in [132, 179, 226, 273, 320]:
    ax.plot([lx, rx], [gy, gy], color="#B9CAD1", lw=0.7, zorder=2)

# red axes with arrowheads
ax.annotate("", xy=(AX_X, 52), xytext=(AX_X, AX_Y),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6), zorder=4)
ax.annotate("", xy=(899, AX_Y), xytext=(AX_X, AX_Y),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6), zorder=4)

# open red circle markers + boxed labels
for (mx, my), lab, (tx, ty2) in MARKS:
    ax.scatter([mx], [my], s=90, facecolors="none", edgecolors="#FF0000",
               linewidths=1.8, zorder=5)
    ax.annotate(lab, (mx, my), xytext=(tx, ty2), fontsize=8, color="#000000",
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="#FF0000", lw=0.9))

# axis labels
ax.text(650, 215, "TPR", fontsize=10, color="#000000", rotation=90,
        ha="center", va="center", zorder=6)
ax.text(778, 372, "FPR", fontsize=10, color="#000000", ha="center", va="center", zorder=6)

out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/roc_032_v3.png"
fig.savefig(out, dpi=DPI, transparent=True)
im2 = Image.open(out)
print("saved", out, im2.size, "-> in:", im2.size[0] / DPI, im2.size[1] / DPI)
