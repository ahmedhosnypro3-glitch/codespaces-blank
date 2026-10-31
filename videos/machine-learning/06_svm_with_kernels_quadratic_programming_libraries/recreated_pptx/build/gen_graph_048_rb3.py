#!/usr/bin/env python3
# Slide 048 scatter panel PNG matched to the reanalysis2 spec geometry.
# Spec regions (normalized [x0,y0,x1,y1] of the 960x540 capture):
#   white panel w/ red border [0.227,0.122,0.974,0.967]
#   axes/grid area            [0.235,0.126,0.971,0.952]
#   red ring   [0.222,0.142,0.978,0.955]  #FF0000
#   blue cl.   [0.261,0.232,0.393,0.616]  #0000FF
#   black cl.  [0.429,0.272,0.716,0.647]  #000000
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
W, H = 13.33, 7.5
CAPW, CAPH = 960, 540
PANEL = (0.227, 0.122, 0.974, 0.967)
AXES = (0.235, 0.126, 0.971, 0.952)
SERIES = {
    "red": (0.222, 0.142, 0.978, 0.955),
    "blue": (0.261, 0.232, 0.393, 0.616),
    "black": (0.429, 0.272, 0.716, 0.647),
}
COLORS = {"red": "#FF0000", "blue": "#0000FF", "black": "#000000"}

pts = json.load(open(BASE + "/eq_048/points_raw.json"))

pw = (PANEL[2] - PANEL[0]) * W
ph = (PANEL[3] - PANEL[1]) * H
DPI = 200
fig = plt.figure(figsize=(pw, ph), dpi=DPI)
axbg = fig.add_axes([0, 0, 1, 1])
axbg.set_xlim(0, CAPW)
axbg.set_ylim(CAPH, 0)
axbg.axis("off")
axbg.set_facecolor("white")
fig.patch.set_facecolor("white")
axbg.add_patch(mpatches.Rectangle((1.5, 1.5), CAPW - 3, CAPH - 3, fill=False,
                                  edgecolor="#FF0000", linewidth=1.1, zorder=10))

ax0x, ax0y = AXES[0] * CAPW, AXES[1] * CAPH
ax1x, ax1y = AXES[2] * CAPW, AXES[3] * CAPH
ax = fig.add_axes([ax0x / CAPW, (CAPH - ax1y) / CAPH,
                   (ax1x - ax0x) / CAPW, (ax1y - ax0y) / CAPH])
ax.set_xlim(0, 40)
ax.set_ylim(0, 35)
ax.set_xticks(range(0, 45, 5))
ax.set_yticks(range(0, 40, 5))
ax.grid(True, color="#C8C8C8", linewidth=0.5)
ax.set_axisbelow(True)
for sp in ax.spines.values():
    sp.set_color("#000000")
    sp.set_linewidth(0.8)
ax.tick_params(colors="#000000", labelsize=7, length=3, width=0.8)
ax.set_facecolor("white")

for name, bb in SERIES.items():
    xy = pts[name]
    xs = [p[0] for p in xy]
    ys = [p[1] for p in xy]
    sx0, sx1, sy0, sy1 = min(xs), max(xs), min(ys), max(ys)
    dx0, dy0 = bb[0] * CAPW, bb[1] * CAPH
    dx1, dy1 = bb[2] * CAPW, bb[3] * CAPH
    X = [(dx0 + (x - sx0) / (sx1 - sx0) * (dx1 - dx0) - ax0x) / (ax1x - ax0x) * 40 for x in xs]
    Y = [(ax1y - (dy0 + (y - sy0) / (sy1 - sy0) * (dy1 - dy0))) / (ax1y - ax0y) * 35 for y in ys]
    ax.scatter(X, Y, s=8, c=COLORS[name], marker="o", edgecolors="none", linewidths=0)

out = BASE + "/slide_048_graph_rb3.png"
fig.savefig(out, dpi=DPI, facecolor="white", pad_inches=0)
print("wrote", out)
