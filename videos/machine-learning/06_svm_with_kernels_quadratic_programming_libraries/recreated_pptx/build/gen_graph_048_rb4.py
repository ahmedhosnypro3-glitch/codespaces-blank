#!/usr/bin/env python3
# Slide 048 scatter panel PNG, fix round 1 (judge FAIL on rb3 build).
# Pixel-forensics of the original 960x540 frame: plot panel frame at
# x 207..757, y 63..518; x tick labels at y 500..514; black bar from y~515.
# So the panel normalized box is [0.2156,0.1167,0.7885,0.9593] and the
# bottom bar must start below y=514 (0.9519) to keep x labels visible.
# Points from eq_048/points_raw.json are already in 960x540 capture px and
# are placed RAW (no rescaling) through the axes mapping below.
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
W, H = 13.33, 7.5
CAPW, CAPH = 960, 540
# panel (white fill, dark frame) measured from the original frame
PX0, PY0, PX1, PY1 = 207, 63, 757, 518
# axes box inside the panel: x labels end at y~514, y labels left of x~225
AX0, AY0, AX1, AY1 = 225, 66, 750, 498
COLORS = {"red": "#FF0000", "blue": "#0000FF", "black": "#000000"}

pts = json.load(open(BASE + "/eq_048/points_raw.json"))

pw = (PX1 - PX0) / CAPW * W
ph = (PY1 - PY0) / CAPH * H
DPI = 200
fig = plt.figure(figsize=(pw, ph), dpi=DPI)
axbg = fig.add_axes([0, 0, 1, 1])
axbg.set_xlim(PX0, PX1)
axbg.set_ylim(PY1, PY0)
axbg.axis("off")
axbg.set_facecolor("white")
fig.patch.set_facecolor("white")
axbg.add_patch(mpatches.Rectangle((PX0 + 1, PY0 + 1), PX1 - PX0 - 2, PY1 - PY0 - 2,
                                  fill=False, edgecolor="#781F2D", linewidth=1.6, zorder=10))

ax = fig.add_axes([(AX0 - PX0) / (PX1 - PX0), (PY1 - AY1) / (PY1 - PY0),
                   (AX1 - AX0) / (PX1 - PX0), (AY1 - AY0) / (PY1 - PY0)])
ax.set_xlim(0, 40)
ax.set_ylim(0, 35)
ax.set_xticks(range(0, 45, 5))
ax.set_yticks(range(0, 40, 5))
ax.grid(True, color="#C8C8C8", linewidth=0.7)
ax.set_axisbelow(True)
for sp in ax.spines.values():
    sp.set_color("#000000")
    sp.set_linewidth(1.0)
ax.tick_params(colors="#000000", labelsize=7, length=3, width=1.0, pad=2)
ax.set_facecolor("white")

for name, xy in pts.items():
    X = [(p[0] - AX0) / (AX1 - AX0) * 40 for p in xy]
    Y = [(AY1 - p[1]) / (AY1 - AY0) * 35 for p in xy]
    ax.scatter(X, Y, s=4, c=COLORS[name], marker="o", edgecolors="none", linewidths=0)

out = BASE + "/slide_048_graph_rb4.png"
fig.savefig(out, dpi=DPI, facecolor="white", pad_inches=0)
print("wrote", out)
