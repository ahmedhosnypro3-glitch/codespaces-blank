"""Regenerate the ROC/AUC plot asset for slide 037, v2.

v1 stretched a full-canvas 10x10 grid and let the curves/annotations fill the
whole chart box. Pixel-measured original (unique_slides/slide_037.jpg, 960x540):
the blue chart frame spans px (259,217)-(632,512); inside it the actual axes
(grid + red arrows + curves) occupy only the inner box x 290..590, y 291..491
(gridlines at x~290,331,375,417,460,503,~546,~589 and y~291,333,372,412,451,491).
The top band y 219..290 hosts the magenta "Best Model" annotation, the right
band x ~540..630 the blue "Worst Model" annotation. The magenta best-model
curve plateaus flat at the top gridline (TPR=1, y~288) and ends ~x505-518 —
no rising diagonal to the corner. "FPR" sits below the red x-axis (y 493..508).
Asset stays 373x295 px == pt, rendered at 600 dpi, embedded at w=px/72 in.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
OUT = f"{NS}/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

PW, PH = 373.0, 295.0  # chart box size in px == pt

fig = plt.figure(figsize=(PW / 72.0, PH / 72.0), dpi=600, facecolor="#EEFEFB")
fig.patches.append(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             facecolor="#EEFEFB", edgecolor="none", zorder=-10))
# blue chart frame (measured #26246F-ish dark navy border)
fig.patches.append(Rectangle((0.004, 0.006), 0.992, 0.988, transform=fig.transFigure,
                             fill=False, edgecolor="#26246F", lw=2.0, zorder=1))

# inner axes box: abs x 290..590, y 291..491 inside the 259..632 / 217..512 frame
ax = fig.add_axes([31 / PW, 21 / PH, 300 / PW, 200 / PH])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_facecolor("#EEFEFB")
ax.set_xticks([i / 8.0 for i in range(9)])
ax.set_yticks([i / 5.0 for i in range(6)])
ax.grid(True, color="#C8C8C8", lw=0.5, alpha=0.8, zorder=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.tick_params(length=0, labelbottom=False, labelleft=False)

# red axes arrows from the origin
ax.annotate("", xy=(0.93, 0.0), xytext=(0.0, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.8,
                            mutation_scale=18), zorder=2)
ax.annotate("", xy=(0.0, 0.93), xytext=(0.0, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.8,
                            mutation_scale=18), zorder=2)

# thin green lines radiating from the origin (area-fill guides)
for a in (38, 50, 62):
    r = math.radians(a)
    t = 0.62 * min(1.0 / math.cos(r), 1.0 / math.sin(r))
    ax.plot([0, t * math.cos(r)], [0, t * math.sin(r)], color="#008000", lw=0.8,
            alpha=0.8, zorder=2)

# worst (blue) curve — lowest, ends at the (1,1) corner
bx = [0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.88, 1.0]
by = [0, 0.40, 0.62, 0.78, 0.90, 0.96, 0.99, 1.0]
ax.plot(bx, by, color="#0000CD", lw=1.8, marker="o", ms=5,
        mfc="white", mec="#0000CD", mew=1.2, zorder=3)

# middle (green) curve
gx = [0, 0.10, 0.20, 0.30, 0.50, 0.72]
gy = [0, 0.35, 0.60, 0.85, 0.95, 1.0]
ax.plot(gx, gy, color="#008000", lw=2.0, marker="o", ms=6,
        mfc="white", mec="#008000", mew=1.2, zorder=4)

# best (magenta) curve — steep rise then flat plateau at TPR=1, ending ~FPR 0.72
mx = [0, 0.03, 0.07, 0.11, 0.72]
my = [0, 0.70, 0.86, 1.0, 1.0]
# yellow diagonal hatch under the magenta plateau (measured abs x 301..489, y 308..478)
ax.fill_between(mx, my, 0.0, where=[0.04 <= x <= 0.66 for x in mx],
                facecolor="none", hatch="//", edgecolor="#D9B800", lw=0.0,
                alpha=0.9, zorder=1)
ax.plot(mx, my, color="#800080", lw=3.0, marker="o", ms=7,
        mfc="white", mec="#800080", mew=1.5, zorder=5)

# annotations live OUTSIDE the axes: magenta in the top band, blue in the right band
fig.text(0.425, 0.955, "Best Model\nLargest Area Under\nthe Curve)",
         ha="center", va="top", fontsize=13, fontweight="bold",
         color="#800080", zorder=6)
fig.text(0.955, 0.61, "Worst Model\nSmallest Area\nUnder the Curve",
         ha="right", va="top", fontsize=13, fontweight="bold",
         color="#0000FF", zorder=6)

# hollow block arrows (white fill, red outline) from each callout to its curve
fig.patches.append(matplotlib.patches.FancyArrowPatch(
    (0.45, 0.80), (0.40, 0.735), transform=fig.transFigure,
    arrowstyle="Simple,tail_width=0.030,head_width=0.13,head_length=0.10",
    fc="white", ec="#C00000", lw=1.8, zorder=6))
fig.patches.append(matplotlib.patches.FancyArrowPatch(
    (0.72, 0.575), (0.655, 0.665), transform=fig.transFigure,
    arrowstyle="Simple,tail_width=0.030,head_width=0.13,head_length=0.10",
    fc="white", ec="#C00000", lw=1.8, zorder=6))

# axis labels: FPR below the x-axis, TPR rotated left of the y-axis (maroon, bold)
fig.text(0.485, 0.045, "FPR", ha="center", va="center", fontsize=12,
         fontweight="bold", color="#800000", zorder=6)
fig.text(0.016, 0.72, "TPR", rotation=90, ha="center", va="center",
         fontsize=12, fontweight="bold", color="#800000", zorder=6)

path = f"{OUT}/roc_037_v2.png"
fig.savefig(path, dpi=600, facecolor=fig.get_facecolor())
plt.close(fig)
from PIL import Image
print("wrote", path, Image.open(path).size)
