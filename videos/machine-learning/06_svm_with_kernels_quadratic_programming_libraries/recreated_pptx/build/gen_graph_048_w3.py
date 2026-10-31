#!/usr/bin/env python3
# Slide 048 graph PNG drawn in capture-pixel space of the measured original.
# Panel (gray #E9E9E9, maroon #712934 border) = capture [56,42,904,516].
# White axes face = capture [207,63,756,501] with maroon edge; black spines
# left/right/top; gray y=0 line at capture y=467; gridlines every 5 units;
# tick labels inside: x at y~480, y right-aligned at x~239.
# Data mapping: x_px = 246 + 12.1*x (0..40), y_px = 466 - 10.886*y (0..35).
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
PX0, PY0 = 56, 42
PW, PH = 848, 474
DPI = 300

fig = plt.figure(figsize=(PW / 100.0, PH / 100.0), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(PH, 0)
ax.axis("off")
fig.patch.set_facecolor("#E9E9E9")
ax.set_facecolor("#E9E9E9")

ax.add_patch(Rectangle((0.5, 0.5), PW - 1, PH - 1, fill=False,
                       edgecolor="#712934", linewidth=1.5, zorder=5))
ax.add_patch(Rectangle((207 - PX0, 63 - PY0), 756 - 207, 501 - 63,
                       facecolor="white", edgecolor="#712934", linewidth=1.2,
                       zorder=2))

for v in range(0, 41, 5):
    x = 246 + 12.1 * v - PX0
    ax.plot([x, x], [63 - PY0, 501 - PY0], color="#E0E0E0", lw=0.6, zorder=3)
for v in range(0, 36, 5):
    y = 466 - 10.886 * v - PY0
    ax.plot([207 - PX0, 756 - PX0], [y, y], color="#E0E0E0", lw=0.6, zorder=3)

for x in (207 - PX0, 756 - PX0):
    ax.plot([x, x], [63 - PY0, 501 - PY0], color="#000000", lw=1.2, zorder=4)
ax.plot([207 - PX0, 756 - PX0], [63 - PY0, 63 - PY0], color="#000000", lw=1.2, zorder=4)
ax.plot([207 - PX0, 756 - PX0], [467 - PY0, 467 - PY0], color="#8C8C8C", lw=1.0, zorder=4)

for v in range(0, 41, 5):
    x = 246 + 12.1 * v - PX0
    ax.text(x, 480 - PY0, str(v), ha="center", va="center", fontsize=8.5,
            color="#222222", zorder=4)
for v in range(0, 36, 5):
    y = 466 - 10.886 * v - PY0
    ax.text(239 - PX0, y, str(v), ha="right", va="center", fontsize=8.5,
            color="#222222", zorder=4)

pts = json.load(open(BASE + "/eq_048/points_raw.json"))
COLORS = {"red": "#FF0000", "blue": "#0000FF", "black": "#000000"}
for name, color in COLORS.items():
    xs = [p[0] - PX0 for p in pts[name]]
    ys = [p[1] - PY0 for p in pts[name]]
    ax.scatter(xs, ys, s=5, c=color, marker="o", edgecolors="none",
               linewidths=0, zorder=6)

out = BASE + "/slide_048_graph_w3.png"
fig.savefig(out, dpi=DPI, facecolor="#E9E9E9", pad_inches=0)
print("wrote", out)
