#!/usr/bin/env python3
"""Slide-32 v4 assets: ROC plot + two-color stacked-fraction equation PNGs.

ROC: image box x[634,902] y[43,390] in original-frame px (960x540, 1px=1pt).
Markers mid-cell: top row y=140 at x 738/815/872 (0.3/0.1/0.0), 0.4 at (698,182).
Labels ABOVE markers (top row), 0.4 below-right; beige fill, dark text.
Axes: red, y-axis tip (661,84) inside plot top border y=80, x-axis tip (894,351).

Equations: stacked fraction (numerator over bar over denominator), numerator
red #C00000, denominator blue #2020C0, label black. 600 dpi transparent PNG.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

DPI = 600
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/"

# ---------------- ROC plot ----------------
BX0, BY0, BX1, BY1 = 634, 43, 902, 390
W_IN, H_IN = (BX1 - BX0) / 72.0, (BY1 - BY0) / 72.0

MARKS = [
    ((738, 140), "0.3", (738, 110)),
    ((815, 140), "0.1", (815, 110)),
    ((872, 140), "0.0", (872, 110)),
    ((698, 182), "0.4", (718, 208)),
]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(BX0, BX1)
ax.set_ylim(BY1, BY0)
ax.axis("off")

# cyan field inside plot border x[641,895] y[80,386]
ax.add_patch(plt.Rectangle((641, 386), 895 - 641, 80 - 386, fc="#E0FFFF", ec="none", zorder=1))
# grid 0.2 steps over data area x[661,895] y[81,351]
for gx in [708, 755, 802, 849]:
    ax.plot([gx, gx], [81, 351], color="#B9CAD1", lw=0.7, zorder=2)
for gy in [135, 189, 243, 297]:
    ax.plot([661, 895], [gy, gy], color="#B9CAD1", lw=0.7, zorder=2)

# red axes, arrowheads inside the plot border
ax.annotate("", xy=(661, 84), xytext=(661, 351),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6), zorder=4)
ax.annotate("", xy=(894, 351), xytext=(661, 351),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6), zorder=4)

# open red circle markers + beige boxed labels
for (mx, my), lab, (tx, ty) in MARKS:
    ax.scatter([mx], [my], s=90, facecolors="none", edgecolors="#FF0000",
               linewidths=1.8, zorder=5)
    ax.annotate(lab, (mx, my), xytext=(tx, ty), fontsize=8, color="#333333",
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="square,pad=0.25", fc="#F5EFD8", ec="#8B2E3A", lw=0.8))

ax.text(650, 240, "TPR", fontsize=10, color="#000000", rotation=90,
        ha="center", va="center", zorder=6)
ax.text(778, 372, "FPR", fontsize=10, color="#000000", ha="center", va="center", zorder=6)

fig.savefig(NS + "roc_032_v4.png", dpi=DPI, transparent=True)
print("roc_032_v4:", Image.open(NS + "roc_032_v4.png").size)
plt.close(fig)


# ---------------- two-color stacked-fraction equations ----------------
def eq_png(label, num, den, out, fs=11):
    fig = plt.figure(figsize=(3.2, 1.0), dpi=DPI)
    fig.patch.set_alpha(0.0)
    r = fig.canvas.get_renderer()
    t0 = fig.text(0.02, 0.5, label + " =", fontsize=fs, color="#000000",
                  ha="left", va="center")
    fig.canvas.draw()
    bb = t0.get_window_extent(renderer=r)
    x0 = bb.x1 / (3.2 * DPI) + 0.015
    # numerator / denominator stacked around the bar, bar at mid height
    tn = fig.text(x0 + 0.09, 0.68, num, fontsize=fs, color="#C00000", ha="center", va="center")
    td = fig.text(x0 + 0.09, 0.30, den, fontsize=fs, color="#2020C0", ha="center", va="center")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bn = tn.get_window_extent(renderer=r)
    bd = td.get_window_extent(renderer=r)
    x_lo = min(bn.x0, bd.x0) - 6
    x_hi = max(bn.x1, bd.x1) + 6
    y_bar = (bn.y0 + bd.y1) / 2
    w_px = 3.2 * DPI
    h_px = 1.0 * DPI
    axl = fig.add_axes([x_lo / w_px, (h_px - y_bar) / h_px - 0.004,
                        (x_hi - x_lo) / w_px, 0.008])
    axl.axis("off")
    axl.plot([0, 1], [0.5, 0.5], color="#000000", lw=1.2)
    fig.savefig(out, dpi=DPI, transparent=True)
    im = Image.open(out)
    # tight-crop on alpha
    bbox = im.getchannel("A").getbbox()
    im.crop(bbox).save(out)
    im2 = Image.open(out)
    print(out.split("/")[-1], im2.size, "-> in:", round(im2.size[0] / DPI, 4), round(im2.size[1] / DPI, 4))
    plt.close(fig)


eq_png("TPR", "TP", "TP+FN", NS + "eq_032_tpr_v4.png")
eq_png("FPR", "FP", "FP+TN", NS + "eq_032_fpr_v4.png")
