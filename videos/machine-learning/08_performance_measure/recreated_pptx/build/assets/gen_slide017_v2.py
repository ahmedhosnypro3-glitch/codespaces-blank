#!/usr/bin/env python3
"""Slide 17 F1-vs-recall chart, regenerated from PIL measurements of the original frame.

Frame 960x540, 1px = 1pt. Measured geometry (px):
  chart container red rect: x 184-766, y 104-503
  plot bbox: x 256-746, y 116-446  ->  data x(r) = 274.2 + 454.6*r, y(f) = 433.5 - 306*f
  (R-style 4% axis extension: spines map to -0.04..1.04)
Output PNG covers exactly the container rect; embedded at 582/72 x 399/72 in.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
DPI = 300

# container rect in px -> inches (1px = 1/72 in)
CX0, CY0, CX1, CY1 = 184, 104, 766, 503
W_IN, H_IN = (CX1 - CX0) / 72.0, (CY1 - CY0) / 72.0
# plot bbox in px
PX0, PY0, PX1, PY1 = 256, 116, 746, 446

recall = np.round(np.arange(0.0, 1.01, 0.1), 10)
series = [
    (0.1, "#FF9999", "o"),
    (0.2, "#FFB366", "^"),
    (0.3, "#E8C800", "v"),
    (0.4, "#66CC66", "<"),
    (0.5, "#66CCCC", ">"),
    (0.6, "#3FA8A0", "D"),
    (0.7, "#6699FF", "s"),
    (0.8, "#FF66FF", "+"),
    (0.9, "#9966FF", "D"),
    (1.0, "#B266FF", "x"),
]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_facecolor("white")
# red container border baked into the image
fig.patches.append(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             fill=False, edgecolor="#C00000", linewidth=1.2))

ax = fig.add_axes([
    (PX0 - CX0) / (CX1 - CX0),
    (CY1 - PY1) / (CY1 - CY0),
    (PX1 - PX0) / (CX1 - CX0),
    (PY1 - PY0) / (CY1 - CY0),
])
ax.set_facecolor("white")

for p, color, marker in series:
    with np.errstate(divide="ignore", invalid="ignore"):
        f1 = np.where(recall > 0, 2 * p * recall / (p + recall), 0.0)
    if marker == "+":
        ax.plot(recall, f1, color=color, marker=marker, linewidth=0.7,
                markersize=3.6, markeredgewidth=0.9, markerfacecolor=color,
                markeredgecolor=color)
    else:
        ax.plot(recall, f1, color=color, marker=marker, linewidth=0.7,
                markersize=3.6, markerfacecolor="none", markeredgecolor=color,
                markeredgewidth=0.8)

ax.set_xlim(-0.04, 1.04)
ax.set_ylim(-0.04, 1.04)
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=9, color="black")
ax.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=9, color="black")
ax.set_xlabel("recall", fontsize=13, color="black", labelpad=2)
ax.set_ylabel("F1", fontsize=13, color="black", labelpad=8)
for spine in ax.spines.values():
    spine.set_color("black")
    spine.set_linewidth(0.8)
ax.tick_params(length=3, width=0.8, colors="black")

handles = [
    plt.Line2D([], [], color=c, marker=m, linestyle="-", linewidth=1.0,
               markersize=4.5, markerfacecolor=("none" if m != "+" else c),
               markeredgecolor=c, markeredgewidth=1.0)
    for _, c, m in series
]
# Legend measured from the original: box x255-405, y115-269 px -> spans
# recall -0.04..0.29 (31% of plot width), F1 0.54..1.04 (47% of plot height),
# 10 rows ~13.8px apart. Large enough to occlude the green/red overlay lines.
ax.legend(handles, [f"precision = {p:g}" for p, _, _ in series],
          loc="upper left", fontsize=12, frameon=True, facecolor="white",
          edgecolor="gray", framealpha=1.0, borderpad=0.6, labelspacing=0.25,
          handlelength=2.2, markerscale=1.0, borderaxespad=0.0)

GREEN = "#2E7D32"
RED = "#FF0000"
# green solid guides (measured: H F1=0.592 r0->0.60 + V r=0.60 down;
# H F1=0.176 r0->0.917 + V r=0.917 down)
ax.plot([0.0, 0.60], [0.592, 0.592], color=GREEN, linewidth=1.4, solid_capstyle="butt")
ax.plot([0.60, 0.60], [-0.04, 0.592], color=GREEN, linewidth=1.4, solid_capstyle="butt")
ax.plot([0.0, 0.917], [0.176, 0.176], color=GREEN, linewidth=1.4, solid_capstyle="butt")
ax.plot([0.917, 0.917], [-0.04, 0.176], color=GREEN, linewidth=1.4, solid_capstyle="butt")
# green short solid L near origin (H F1=0.209 r0->0.12; V r=0.12 down to axis)
ax.plot([0.0, 0.12], [0.209, 0.209], color=GREEN, linewidth=1.4, solid_capstyle="butt")
ax.plot([0.12, 0.12], [-0.04, 0.209], color=GREEN, linewidth=1.4, solid_capstyle="butt")
# red dashed annotations with left-pointing arrowheads at r=0 (xy must stay
# inside the axes or annotation_clip drops the whole arrow)
ax.annotate("", xy=(0.0, 0.645), xytext=(0.645, 0.645),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2, linestyle=(0, (4, 3))))
ax.plot([0.645, 0.645], [-0.04, 0.645], color=RED, linewidth=1.2, linestyle=(0, (4, 3)))
ax.annotate("", xy=(0.0, 0.46), xytext=(1.0, 0.46),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2, linestyle=(0, (4, 3))))
ax.plot([1.0, 1.0], [-0.04, 0.46], color=RED, linewidth=1.2, linestyle=(0, (4, 3)))

out = f"{NS}/recreated_pptx/build/assets/slide017_f1chart_v2.png"
fig.savefig(out, dpi=DPI, facecolor="white")
from PIL import Image
im = Image.open(out)
print("saved", out, im.size, "embed in:", W_IN, H_IN)
