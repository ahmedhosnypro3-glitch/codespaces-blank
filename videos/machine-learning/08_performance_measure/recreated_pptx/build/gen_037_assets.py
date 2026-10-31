"""Generate the ROC/AUC plot asset for slide 037.

Geometry measured from unique_slides/slide_037.jpg (960x540, 1px = 1pt):
plot canvas box = px (259,217)-(632,512) -> 373x295 px -> 5.1806x4.0972 in at (3.5972,3.0139).
Inside the canvas the graph (grid + ROC curves) occupies the left ~62% and its top
coincides with the magenta curve's plateau; the right band carries the "Worst Model"
annotation, matching the original frame.
Rendered at 600 dpi so the PNG embeds at exactly w=px/72 inches.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
OUT = f"{NS}/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

PW, PH = 373.0, 295.0  # plot canvas size in px == pt
GRID_R = 0.62          # graph region right edge (fraction of canvas)
GRID_T = 0.756         # graph region top (magenta plateau)

fig = plt.figure(figsize=(PW / 72.0, PH / 72.0), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor("#F0F8FF")
for sp in ax.spines.values():
    sp.set_color("#4A4AA0")
    sp.set_linewidth(1.2)

# light gray grid mesh inside the graph region only
for i in range(1, 11):
    ax.plot([i * GRID_R / 10, i * GRID_R / 10], [0, GRID_T],
            color="#D3D3D3", lw=0.4, alpha=0.6, zorder=0)
for j in range(1, 11):
    ax.plot([0, GRID_R], [j * GRID_T / 10, j * GRID_T / 10],
            color="#D3D3D3", lw=0.4, alpha=0.6, zorder=0)

# red axes with arrowheads, inset inside the canvas with a clear margin
ax.annotate("", xy=(0.90, 0.115), xytext=(0.075, 0.115),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.8,
                            mutation_scale=18), zorder=2)
ax.annotate("", xy=(0.075, 0.93), xytext=(0.075, 0.115),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.8,
                            mutation_scale=18), zorder=2)

# best (magenta) curve: steep rise, then flat plateau at the grid top
mx = [0, 0.080, 0.097, 0.113, 0.129, 0.145, 0.161, 0.177, 0.193, 0.30, 0.45, 0.62]
my = [0, 0.251, 0.508, 0.542, 0.603, 0.651, 0.715, 0.739, 0.749, 0.756, 0.756, 0.756]
# middle (green) curve — measured polyline from the original frame
gx = [0, 0.080, 0.129, 0.193, 0.257, 0.322, 0.387, 0.451, 0.515, 0.579, 0.611, 0.62]
gy = [0, 0.068, 0.227, 0.336, 0.430, 0.480, 0.544, 0.581, 0.632, 0.678, 0.739, 0.750]
# worst (blue) curve, lowest, near the diagonal
bx = [0, 0.10, 0.20, 0.30, 0.45, 0.58, 0.62]
by = [0, 0.08, 0.20, 0.33, 0.48, 0.60, 0.63]

# pale-yellow AUC band hugging the magenta curve (upper-left of the graph region)
band = [0.0, 0.13, 0.16]
ax.fill_between(mx[2:8], [my[i] for i in range(2, 8)],
                [my[i] - 0.16 for i in range(2, 8)],
                facecolor="none", hatch="/", edgecolor="#E8C800", lw=0.0,
                alpha=0.6, zorder=1)

# green area lines under the green ROC, plus a short parallel set lower-right
ax.plot(gx[1:9], [gy[i] - 0.10 for i in range(1, 9)],
        color="#008000", lw=0.8, alpha=0.75, zorder=1)
for k in range(3):
    x0 = 0.44 + 0.05 * k
    ax.plot([x0, x0 + 0.07], [0.10 + 0.03 * k, 0.24 + 0.03 * k],
            color="#008000", lw=0.9, alpha=0.8, zorder=1)

ax.plot(bx, by, color="#0000CD", lw=1.8, marker="o", ms=5,
        mfc="white", mec="#0000CD", zorder=3)
ax.plot(gx, gy, color="#008000", lw=2.0, marker="o", ms=6,
        mfc="#008000", mec="#008000", zorder=4)
ax.plot(mx, my, color="#800080", lw=3.0, marker="o", ms=7,
        mfc="white", mec="#800080", zorder=5)

label_bg = dict(facecolor="#F0F8FF", alpha=0.92, edgecolor="none", pad=2.0)

# best-model annotation (magenta) above the plateau
ax.text(0.31, 0.95, "Best Model\nLargest Area Under\nthe Curve)",
        ha="center", va="top", fontsize=11, color="#800080", zorder=6, bbox=label_bg)
# thick hollow block arrow pointing down-left onto the magenta plateau
ax.annotate("", xy=(0.22, 0.775), xytext=(0.30, 0.845),
            arrowprops=dict(arrowstyle="Simple,tail_width=0.045,head_width=0.16,head_length=0.12",
                            color="#C00000", lw=2.5, fc="#FFFFFF"), zorder=6)

# worst-model annotation in the clean right band of the canvas
ax.text(0.97, 0.62, "Worst Model\nSmallest Area\nUnder the Curve",
        ha="right", va="top", fontsize=11, color="#0000FF", zorder=6, bbox=label_bg)
# thick hollow block arrow pointing up-left onto the blue curve
ax.annotate("", xy=(0.63, 0.66), xytext=(0.80, 0.55),
            arrowprops=dict(arrowstyle="Simple,tail_width=0.045,head_width=0.16,head_length=0.12",
                            color="#C00000", lw=2.5, fc="#FFFFFF"), zorder=6)

# axis labels (red): FPR below the x-axis, TPR left of the y-axis
ax.text(0.40, 0.045, "FPR", ha="center", va="center",
        fontsize=13, color="#C00000", zorder=6, bbox=label_bg)
ax.text(0.028, 0.55, "TPR", rotation=90, ha="center", va="center",
        fontsize=13, color="#C00000", zorder=6, bbox=label_bg)

path = f"{OUT}/roc_037.png"
fig.savefig(path, dpi=600)
plt.close(fig)
from PIL import Image
print("wrote", path, Image.open(path).size)
