"""Generate the ROC/AUC plot asset for slide 037.

Geometry measured from unique_slides/slide_037.jpg (960x540, 1px = 1pt):
plot axes box = px (259,217)-(632,512) -> 373x295 px -> 5.1806x4.0972 in at (3.5972,3.0139).
Rendered at 600 dpi so the PNG embeds at exactly w=px/72 inches.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
OUT = f"{NS}/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

PW, PH = 373.0, 295.0  # plot box size in px == pt
fig = plt.figure(figsize=(PW / 72.0, PH / 72.0), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor("#F0F8FF")
for sp in ax.spines.values():
    sp.set_color("#00008B")
    sp.set_linewidth(1.5)

# light gray grid mesh
for t in [i / 10.0 for i in range(1, 10)]:
    ax.axhline(t, color="#D3D3D3", lw=0.4, alpha=0.6, zorder=0)
    ax.axvline(t, color="#D3D3D3", lw=0.4, alpha=0.6, zorder=0)

# red axes with arrowheads, inset inside the blue plot border
ax.annotate("", xy=(0.985, 0.035), xytext=(0.035, 0.035),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.8,
                            mutation_scale=18), zorder=2)
ax.annotate("", xy=(0.035, 0.985), xytext=(0.035, 0.035),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.8,
                            mutation_scale=18), zorder=2)

# random-guess diagonal (dark blue)
ax.plot([0, 1], [0, 1], color="#404040", lw=1.3, zorder=2)

# thin green lines radiating from the origin
import math
for a in (35, 42, 50, 58):
    r = math.radians(a)
    t = min(1.0 / math.cos(r), 1.0 / math.sin(r))
    ax.plot([0, t * math.cos(r)], [0, t * math.sin(r)], color="#008000", lw=1.0, zorder=2)

# worst (blue) curve, lowest, near the diagonal; small filled-dot markers,
# endpoint pulled inside the frame
bx = [0, 0.10, 0.20, 0.30, 0.45, 0.58, 0.70]
by = [0, 0.08, 0.20, 0.33, 0.48, 0.60, 0.68]
ax.plot(bx, by, color="#0000CD", lw=1.8, marker="o", ms=3.5,
        mfc="#0000CD", mec="#0000CD", zorder=3)

# middle (green) curve — measured polyline from the original frame
gx = [0, 0.080, 0.129, 0.193, 0.257, 0.322, 0.387, 0.451, 0.515, 0.579, 0.611, 0.66]
gy = [0, 0.068, 0.227, 0.336, 0.430, 0.480, 0.544, 0.581, 0.632, 0.678, 0.739, 0.730]
ax.plot(gx, gy, color="#008000", lw=2.0, marker="o", ms=5,
        mfc="white", mec="#008000", zorder=4)

# best (magenta) curve hugging the top-left — measured polyline; endpoint
# pulled inside the frame; pale-yellow AUC fill clearly under THIS curve
mx = [0, 0.080, 0.097, 0.113, 0.129, 0.145, 0.161, 0.177, 0.193, 0.30, 0.45, 0.66]
my = [0, 0.251, 0.508, 0.542, 0.603, 0.651, 0.715, 0.739, 0.749, 0.756, 0.756, 0.756]
ax.fill_between(mx, my, facecolor="none", hatch="//", edgecolor="#E8C800", lw=0.0, alpha=0.55, zorder=1)
ax.plot(mx, my, color="#800080", lw=3.0, marker="o", ms=6,
        mfc="white", mec="#800080", zorder=5)

# annotations (inside the plot, as in the original)
ax.text(0.51, 0.95, "Best Model\nLargest Area Under\nthe Curve)",
        ha="center", va="top", fontsize=11, color="#800080", zorder=6)
# one thick hollow red block arrow from the best-model label down-left to the curve
ax.annotate("", xy=(0.30, 0.775), xytext=(0.43, 0.845),
            arrowprops=dict(arrowstyle="Simple,tail_width=0.035,head_width=0.11,head_length=0.085",
                            color="#C00000", lw=1.4, fc="none",
                            connectionstyle="arc3,rad=0.35"), zorder=6)

# worst-model label on the right side of the plot
ax.text(0.95, 0.74, "Worst Model\nSmallest Area\nUnder the Curve",
        ha="right", va="top", fontsize=11, color="#00008B", zorder=6)
# one thick hollow red block arrow pointing up-right toward the label
ax.annotate("", xy=(0.88, 0.66), xytext=(0.58, 0.36),
            arrowprops=dict(arrowstyle="Simple,tail_width=0.035,head_width=0.11,head_length=0.085",
                            color="#C00000", lw=1.4, fc="none",
                            connectionstyle="arc3,rad=0.35"), zorder=6)

# axis labels (red, inside the plot edges)
ax.text(0.055, 0.67, "TPR", rotation=90, ha="center", va="center",
        fontsize=13, color="#C00000", zorder=6)
ax.text(0.41, 0.045, "FPR", ha="center", va="center",
        fontsize=13, color="#C00000", zorder=6)

path = f"{OUT}/roc_037.png"
fig.savefig(path, dpi=600)
plt.close(fig)
from PIL import Image
print("wrote", path, Image.open(path).size)
