#!/usr/bin/env python3
# Slide 048 graph PNG, regenerated in capture-pixel space of the measured original
# (qa/rejudge2/orig_png/slide_048.png, 960x540).
# Measured panel (gray fill, maroon border): capture [58,42,902,518].
# White axes box with black spines: capture x[207,757], y[63,501]; extra black
# x-axis line at y=467 (data y=0). Gridlines every 5 data units:
#   x_px = 246 + 12.1*x (x 0..40), y_px = 466 - 10.886*y (y 0..35).
# Tick labels below/left of the box. Scatter points come from
# eq_048/points_raw.json (capture px, one entry per source pixel), plotted as
# 1-px markers so dot size/shape matches the original exactly.
# PNG covers the panel only; slide_048.js places it at exact size.
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
PX0, PY0 = 58, 42          # panel origin in capture px
PW, PH = 844, 476          # panel size in capture px (902-58, 518-42)
DPI = 72  # 1 png px = 1 capture px = 1 pt, so all sizes below are capture px

fig = plt.figure(figsize=(PW / DPI, PH / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(PH, 0)
ax.axis("off")
fig.patch.set_facecolor("#E7E9E6")
ax.set_facecolor("#E7E9E6")

# maroon panel border (capture cols 58-59 / rows 42-44 / 516-518)
ax.add_patch(Rectangle((1, 1), PW - 2, PH - 2, fill=False,
                       edgecolor="#712934", linewidth=2.0, zorder=5))

# white axes box: capture x[207,757], y[63,501] -> panel-local
BX0, BY0 = 207 - PX0, 63 - PY0
BW, BH = 757 - 207, 501 - 63
ax.add_patch(Rectangle((BX0, BY0), BW, BH, facecolor="white",
                       edgecolor="none", zorder=2))

# gridlines every 5 data units, inside the axes box
for v in range(0, 41, 5):
    x = 246 + 12.1 * v - PX0
    ax.plot([x, x], [BY0, BY0 + BH], color="#E8E8E8", lw=0.8, zorder=3)
for v in range(0, 36, 5):
    y = 466 - 10.886 * v - PY0
    ax.plot([BX0, BX0 + BW], [y, y], color="#E8E8E8", lw=0.8, zorder=3)

# black spines on all four sides + the y=0 x-axis line (capture row 467)
for x in (BX0, BX0 + BW):
    ax.plot([x, x], [BY0, BY0 + BH], color="#000000", lw=1.6, zorder=4)
for y in (BY0, BY0 + BH):
    ax.plot([BX0, BX0 + BW], [y, y], color="#000000", lw=1.6, zorder=4)
ax.plot([BX0, BX0 + BW], [467 - PY0, 467 - PY0], color="#000000", lw=1.2, zorder=4)

# tick marks outside the box (capture: bottom y 501..505, left x 203..207)
for v in range(0, 41, 5):
    x = 246 + 12.1 * v - PX0
    ax.plot([x, x], [BY0 + BH, BY0 + BH + 4], color="#000000", lw=1.2, zorder=4)
for v in range(0, 36, 5):
    y = 466 - 10.886 * v - PY0
    ax.plot([BX0 - 4, BX0], [y, y], color="#000000", lw=1.2, zorder=4)

# tick labels: x below the box, y left of the box
for v in range(0, 41, 5):
    x = 246 + 12.1 * v - PX0
    ax.text(x, BY0 + BH + 6, str(v), ha="center", va="top", fontsize=8.5,
            color="#222222", zorder=4)
for v in range(0, 36, 5):
    y = 466 - 10.886 * v - PY0
    ax.text(BX0 - 6, y, str(v), ha="right", va="center", fontsize=8.5,
            color="#222222", zorder=4)

# scatter series: every source pixel as a ~1px marker (capture px -> panel-local)
pts = json.load(open(BASE + "/eq_048/points_raw.json"))
COLORS = {"red": "#FF0000", "blue": "#0000FF", "black": "#000000"}
for name, color in COLORS.items():
    xs = [p[0] - PX0 for p in pts[name]]
    ys = [p[1] - PY0 for p in pts[name]]
    ax.scatter(xs, ys, s=3.0, c=color, marker="o", edgecolors="none",
               linewidths=0, zorder=6)  # ~2 px dots; neighbors overlap -> solid cores

out = BASE + "/slide_048_graph_rb5.png"
fig.savefig(out, dpi=DPI, facecolor="#E7E9E6", pad_inches=0)
print("wrote", out)
