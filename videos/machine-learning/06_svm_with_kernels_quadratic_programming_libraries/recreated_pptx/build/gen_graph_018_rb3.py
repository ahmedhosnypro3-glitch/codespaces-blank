#!/usr/bin/env python3
"""Slide 018 diagram (rebuild wave 3): 2-D scene drawn at the reanalysis2 spec's
normalized coords inside region [0.300,0.283,0.788,0.902]. Plane corners measured
from the original frame's orange mask; point centers from the spec."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, FancyArrowPatch
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
W, H = 13.33, 7.5
X0, Y0, X1, Y1 = 0.300, 0.265, 0.788, 0.902
FW, FH = (X1 - X0) * W, (Y1 - Y0) * H
DPI = 600
RED = "#CC0000"

fig = plt.figure(figsize=(FW, FH), dpi=DPI)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y1, Y0)
ax.axis("off")

# pale-yellow ellipsoid region [0.383,0.302,0.616,0.663], tilted like the original
ax.add_patch(Ellipse((0.4995, 0.4825), 0.233, 0.361, angle=20,
                     facecolor="#FFFCC5", edgecolor="none", zorder=1))

# orange decision plane parallelogram (corners from original frame hull)
plane = [(0.615, 0.427), (0.781, 0.424), (0.467, 0.837), (0.308, 0.812)]
ax.add_patch(Polygon(plane, closed=True, facecolor="#EE9944",
                     edgecolor="none", zorder=2))

# red linear decision boundary on the plane [0.414,0.902 -> 0.678,0.523]
ax.plot([0.414, 0.678], [0.902, 0.523], color=RED, lw=3.0,
        solid_capstyle="round", zorder=3)

# red 3-D axes with arrowheads, origin ~(0.510,0.775)
def arrow(p0, p1):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=20,
                                 color=RED, lw=2.2, zorder=4))
arrow((0.510, 0.780), (0.510, 0.285))  # z vertical
arrow((0.505, 0.775), (0.735, 0.775))  # x horizontal
arrow((0.510, 0.775), (0.413, 0.900))  # y diagonal lower-left
for lbl, x, y in [("z", 0.510, 0.276), ("x", 0.748, 0.798), ("y", 0.414, 0.883)]:
    ax.text(x, y, lbl, color=RED, fontsize=14, fontweight="bold",
            fontstyle="italic", ha="center", va="center", zorder=5)

# 10 cyan points in the yellow region (spec centers)
cyan = [(0.522, 0.377), (0.555, 0.399), (0.480, 0.398), (0.565, 0.467),
        (0.452, 0.443), (0.430, 0.507), (0.477, 0.573), (0.525, 0.573),
        (0.434, 0.573), (0.475, 0.600)]
ax.scatter(*zip(*cyan), s=170, c="#33CCFF", edgecolors="#0099CC",
           linewidths=1.4, zorder=6)

# 6 orange-red points on the plane (spec centers)
orange = [(0.538, 0.640), (0.545, 0.690), (0.465, 0.700), (0.497, 0.645),
          (0.522, 0.747), (0.475, 0.765)]
ax.scatter(*zip(*orange), s=170, c="#EE5500", edgecolors="#CC3300",
           linewidths=1.4, zorder=7)

out = BASE + "/slide_018_graph_rb4.png"
fig.savefig(out, dpi=DPI, transparent=True)
plt.close(fig)

im = Image.open(out)
info = {"path": "slide_018_graph_rb4.png", "w_px": im.size[0], "h_px": im.size[1],
        "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5),
        "dpi": DPI}
with open(out + ".json", "w") as f:
    json.dump(info, f, indent=2)
print(json.dumps(info))
