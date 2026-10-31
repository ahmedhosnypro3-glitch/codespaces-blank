#!/usr/bin/env python3
"""Slide-32 v5 ROC asset. Pixel-adjudicated vs unique_slides/slide_032.jpg (2026-10-31):
- no cyan fill: original plot interior is white (transparent PNG over white canvas)
- gridlines at measured original lattice: v [704,747,790,833,876], h [120,151,193,232,271,311]
- markers at measured original ring centers: (726,148) (810,148) (874,148) (690,194)
- label chips at measured original centers: top row y=124 above markers, "0.4" at (721,211)
- axis labels TPR/FPR in measured maroon red #8B2E3A at (651,249) / (770,364)
Equations unchanged (eq_032_*_v4.png kept).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DPI = 600
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/"

BX0, BY0, BX1, BY1 = 634, 43, 902, 390
W_IN, H_IN = (BX1 - BX0) / 72.0, (BY1 - BY0) / 72.0

MARKS = [
    ((726, 148), "0.3", (726, 124)),
    ((810, 148), "0.1", (810, 124)),
    ((874, 148), "0.0", (874, 124)),
    ((690, 194), "0.4", (721, 211)),
]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(BX0, BX1)
ax.set_ylim(BY1, BY0)
ax.axis("off")

# faint plot-area fill measured in the original interior: #EEFEFA (near-white)
ax.add_patch(plt.Rectangle((641, 386), 895 - 641, 80 - 386, fc="#EEFEFA", ec="none", zorder=1))
# grid over data area x[661,895] y[81,351]
for gx in [704, 747, 790, 833, 876]:
    ax.plot([gx, gx], [81, 351], color="#B9CAD1", lw=0.7, zorder=2)
for gy in [120, 151, 193, 232, 271, 311]:
    ax.plot([661, 895], [gy, gy], color="#B9CAD1", lw=0.7, zorder=2)

# red axes, arrowheads inside the plot border
ax.annotate("", xy=(661, 84), xytext=(661, 351),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6), zorder=4)
ax.annotate("", xy=(894, 351), xytext=(661, 351),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6), zorder=4)

# open red circle markers + beige boxed labels
for (mx, my), lab, (tx, ty) in MARKS:
    ax.scatter([mx], [my], s=120, facecolors="none", edgecolors="#FF0000",
               linewidths=1.8, zorder=5)
    ax.annotate(lab, (mx, my), xytext=(tx, ty), fontsize=10, color="#333333",
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="square,pad=0.35", fc="#F5EFD8", ec="#8B2E3A", lw=0.8))

ax.text(651, 249, "TPR", fontsize=10, color="#8B2E3A", rotation=90,
        ha="center", va="center", zorder=6)
ax.text(770, 364, "FPR", fontsize=10, color="#8B2E3A", ha="center", va="center", zorder=6)

fig.savefig(NS + "roc_032_v5.png", dpi=DPI, transparent=True)
print("roc_032_v5:", Image.open(NS + "roc_032_v5.png").size)
plt.close(fig)
