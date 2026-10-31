#!/usr/bin/env python3
"""Regenerate the slide_051 scatter plot from the original frame's measured pixels.

Draws in original-frame pixel coordinates (960x540 source) so the image can be
placed 1:1 over the plot region. White plot area x 211..728, y 66..496.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ORIG = NS + "/qa/rejudge2/orig_png/slide_051.png"
OUT = NS + "/recreated_pptx/build/slide_051_graph.png"

X0, X1, Y0, Y1 = 211, 728, 66, 496  # white plot region in original px
W_PX, H_PX = X1 - X0, Y1 - Y0
DPI = 300

a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
inner = np.zeros((H, W), bool)
inner[Y0:Y1 + 1, X0:X1 + 1] = True
blue = (B > 140) & (R < 110) & (G < 110) & (B - R > 60) & inner
red = (R > 170) & (G < 90) & (B < 90) & inner

fig = plt.figure(figsize=(W_PX / DPI, H_PX / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y1, Y0)
ax.axis("off")
ax.set_facecolor("white")

# gridlines measured from the original frame
vlines = [247, 327.5, 407, 487.5, 567, 647.5, 727]
hlines = [85, 161, 237.5, 315, 390.5, 467.5]
for gx in vlines:
    ax.plot([gx, gx], [Y0, 486], color="#E0E0E0", lw=0.22, solid_capstyle="butt", zorder=1)
for gy in hlines:
    ax.plot([X0, X1], [gy, gy], color="#E0E0E0", lw=0.22, solid_capstyle="butt", zorder=1)

# scatter: every extracted colored pixel as a point (real plot of measured data)
for mask, color in ((blue, "#0000FF"), (red, "#FF0000")):
    ys, xs = np.where(mask)
    ax.scatter(xs, ys, s=0.12, marker="o", c=color, edgecolors="none", zorder=3)

# tick labels measured from the original (two x rows exist in the source)
FS = 1.9
x_row1 = [(-10, 238.9), (0, 327.4), (10, 407.1), (20, 487.4), (30, 567.0), (40, 647.3)]
x_row2 = [(-10, 250.0), (0, 327.0), (10, 407.0), (20, 487.0), (30, 567.0), (40, 647.0), (50, 727.5)]
y_lab = [(40, 85.4), (30, 162.0), (20, 238.9), (10, 314.8), (0, 391.9), (-10, 467.4)]
for v, cx in x_row1:
    ax.text(cx, 467.5, str(v), fontsize=FS, color="black", ha="center", va="center", zorder=4)
for v, cx in x_row2:
    ax.text(cx, 481.0, str(v), fontsize=FS, color="black", ha="center", va="center", zorder=4)
for v, cy in y_lab:
    ax.text(245, cy, str(v), fontsize=FS, color="black", ha="right", va="center", zorder=4)

fig.savefig(OUT, dpi=DPI, facecolor="white")
print("wrote", OUT)
im = Image.open(OUT)
print("size:", im.size, "expected:", (W_PX * DPI // 300, H_PX * DPI // 300))
