#!/usr/bin/env python3
"""Regenerate the slide_054 scatter plot from the original frame's measured pixels.

Draws in original-frame pixel coordinates (960x540 source) so the image can be
placed 1:1 over the plot region. White plot box x 206..753, y 64..501 with a
pinkish border; black left spine x~236 and bottom spine y~467; tick labels
0,5,10,15,20,25 on both axes; 4x4 checkerboard of 2x2 red/blue dot clusters.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ORIG = NS + "/qa/rejudge2/orig_png/slide_054.png"
OUT = NS + "/recreated_pptx/build/slide_054_graph.png"

X0, X1, Y0, Y1 = 206, 753, 64, 501  # white plot box in original px
W_PX, H_PX = X1 - X0, Y1 - Y0
DPI = 300

a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
inner = np.zeros((H, W), bool)
inner[Y0:Y1 + 1, X0:X1 + 1] = True
blue = (B > 140) & (R < 110) & (G < 110) & (B - R > 60) & inner
red = (R > 170) & (G < 90) & (B < 90) & inner
# mouse cursor arrow (dark pixels near x 630-650, y 170-190)
cursor = np.zeros((H, W), bool)
cursor[170:191, 630:651] = (R[170:191, 630:651] < 140) & (G[170:191, 630:651] < 140) & (B[170:191, 630:651] < 140)

fig = plt.figure(figsize=(W_PX / DPI, H_PX / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y1, Y0)
ax.axis("off")
ax.set_facecolor("white")

# pinkish plot border (measured #E8B4B4-ish)
for sx in (X0, X1):
    ax.plot([sx, sx], [Y0, Y1], color="#E8A8A8", lw=0.5, solid_capstyle="butt", zorder=2)
for sy in (Y0, Y1):
    ax.plot([X0, X1], [sy, sy], color="#E8A8A8", lw=0.5, solid_capstyle="butt", zorder=2)

# black left/bottom spines (measured x~236, y~467)
ax.plot([236, 236], [80, 468], color="black", lw=0.45, solid_capstyle="butt", zorder=2)
ax.plot([234, 751], [467, 467], color="black", lw=0.45, solid_capstyle="butt", zorder=2)

# tick marks + labels (measured positions)
x_lab = [(0, 241), (5, 343), (10, 444), (15, 536), (20, 637), (25, 727)]
y_lab = [(25, 83), (20, 161), (15, 237), (10, 315), (5, 391), (0, 467)]
for v, cx in x_lab:
    ax.plot([cx, cx], [467, 472], color="black", lw=0.4, zorder=2)
    ax.text(cx, 479.5, str(v), fontsize=2.6, color="black", ha="center", va="center", zorder=4)
for v, cy in y_lab:
    ax.plot([231, 236], [cy, cy], color="black", lw=0.4, zorder=2)
    ax.text(228, cy, str(v), fontsize=2.6, color="black", ha="right", va="center", zorder=4)

# scatter: every extracted colored pixel as a point (real plot of measured data)
for mask, color in ((blue, "#0000FF"), (red, "#FF0000")):
    ys, xs = np.where(mask)
    ax.scatter(xs, ys, s=0.35, marker="o", c=color, edgecolors="none", zorder=3)
ys, xs = np.where(cursor)
ax.scatter(xs, ys, s=0.5, marker="s", c="black", edgecolors="none", zorder=3)

fig.savefig(OUT, dpi=DPI, facecolor="white")
print("wrote", OUT)
print("size:", Image.open(OUT).size)
