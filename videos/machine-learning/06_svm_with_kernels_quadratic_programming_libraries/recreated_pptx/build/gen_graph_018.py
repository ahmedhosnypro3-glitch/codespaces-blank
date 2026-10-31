#!/usr/bin/env python3
"""Slide 018 diagram v3: 2-D matplotlib scene drawn directly at the spec's
measured normalized coordinates (region [0.300,0.283,0.788,0.902])."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
W, H = 13.33, 7.5
GX0, GY0, GX1, GY1 = 0.300, 0.283, 0.788, 0.902
FIG_W, FIG_H = (GX1 - GX0) * W, (GY1 - GY0) * H
DPI = 600
RED = "#CC0000"

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor("none")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(GX0, GX1)
ax.set_ylim(GY1, GY0)  # y down, matching normalized slide coords
ax.set_axis_off()

# orange decision plane parallelogram spanning [0.300,0.418,0.788,0.846]
plane = Polygon(
    [(0.300, 0.560), (0.610, 0.418), (0.788, 0.660), (0.478, 0.846)],
    closed=True, facecolor="#EE9944", edgecolor="none", alpha=0.92, zorder=1)
ax.add_patch(plane)

# pale-yellow translucent ellipsoid region [0.383,0.302,0.616,0.663], tilted
ell = Ellipse((0.4995, 0.4825), 0.233, 0.361, angle=-18,
              facecolor="#FFFCC5", edgecolor="none", alpha=0.55, zorder=2)
ax.add_patch(ell)

# red decision-boundary line on the plane [0.414,0.902 -> 0.678,0.523]
ax.plot([0.414, 0.678], [0.902, 0.523], color=RED, lw=2.6, zorder=3,
        solid_capstyle="round")

# cyan points (spec centres) inside the yellow region
cyan = [
    (0.522, 0.377), (0.555, 0.399), (0.480, 0.398), (0.565, 0.467), (0.452, 0.443),
    (0.430, 0.507), (0.477, 0.573), (0.525, 0.573), (0.434, 0.573), (0.475, 0.600),
]
ax.scatter([p[0] for p in cyan], [p[1] for p in cyan], s=130, c="#33CCFF",
           edgecolors="#0099CC", linewidths=1.4, zorder=4)

# orange-red points (spec centres) on the plane
orange = [
    (0.538, 0.640), (0.545, 0.690), (0.465, 0.700), (0.497, 0.645),
    (0.522, 0.747), (0.475, 0.765),
]
ax.scatter([p[0] for p in orange], [p[1] for p in orange], s=130, c="#EE5500",
           edgecolors="#CC3300", linewidths=1.4, zorder=4)

# red 3-D axes anchored at a common origin (0.510, 0.775)
arrow = dict(arrowstyle="-|>", color=RED, lw=2.2, mutation_scale=22,
             shrinkA=0, shrinkB=0)
ax.annotate("", xy=(0.510, 0.283), xytext=(0.510, 0.775), arrowprops=arrow, zorder=5)
ax.annotate("", xy=(0.733, 0.775), xytext=(0.510, 0.775), arrowprops=arrow, zorder=5)
ax.annotate("", xy=(0.415, 0.902), xytext=(0.510, 0.775), arrowprops=arrow, zorder=5)
for lbl, (lx, ly) in [("z", (0.503, 0.270)), ("x", (0.726, 0.789)), ("y", (0.407, 0.870))]:
    ax.text(lx, ly, lbl, color=RED, fontsize=13, fontweight="bold",
            fontstyle="italic", ha="center", va="center", zorder=5)

out = BASE + "/slide_018_graph.png"
fig.savefig(out, dpi=DPI, transparent=True)
plt.close(fig)

from PIL import Image
im = Image.open(out)
info = {"path": "slide_018_graph.png", "w_px": im.size[0], "h_px": im.size[1],
        "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5),
        "dpi": DPI}
with open(out + ".json", "w") as f:
    json.dump(info, f, indent=2)
print(json.dumps(info))
