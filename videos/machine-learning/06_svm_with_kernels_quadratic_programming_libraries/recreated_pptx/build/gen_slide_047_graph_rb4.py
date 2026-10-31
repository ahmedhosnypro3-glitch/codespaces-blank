#!/usr/bin/env python3
"""Slide 047 graph (rebuild wave 3, fix round) — full-slide transparent PNG.

Pixel-faithful regeneration of qa/rejudge2/orig_png/slide_047.png plot:
white axes on transparent bg, red top line at y=40, gray dot lattice,
black comb of vertical segments, red/blue class blobs traced from the
original frame's masks. Axes rect from measured spines (px 207..752,
py 63..502 of the 960x540 frame).
Run: python3 gen_slide_047_graph_rb4.py <out.png>
"""
import sys
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
OUT = sys.argv[1] if len(sys.argv) > 1 else "slide_047_graph_rb4.png"
DPI = 200
W_IN, H_IN = 13.33, 7.5

im = np.array(Image.open(NS + "/qa/rejudge2/orig_png/slide_047.png").convert("RGB")).astype(int)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 150) & (G < 110) & (B < 110)
blue = (B > 150) & (R < 110) & (G < 110)
black = (R < 70) & (G < 70) & (B < 70)
gray = (abs(R - G) < 10) & (abs(G - B) < 10) & (R > 170) & (R < 236) & ~red & ~blue & ~black

X0, X1, Y0, Y1 = 208, 751, 66, 501  # plot interior px box (excl. red top spine)
def px2dx(px): return (px - 207) / 545.0 * 35.0
def py2dy(py): return 40.0 - (py - 63) / 439.0 * 50.0

sub = lambda m: m[Y0:Y1, X0:X1]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_alpha(0.0)
AX = [207 / 960.0, (540 - 502) / 540.0, (752 - 207) / 960.0, (502 - 63) / 540.0]
ax = fig.add_axes(AX)
ax.set_xlim(0, 35)
ax.set_ylim(-10, 40)
ax.set_facecolor("white")

# gray dot lattice
gy, gx = np.nonzero(sub(gray)[::2, ::2])
ax.scatter(px2dx(gx * 2 + X0), py2dy(gy * 2 + Y0), s=6, c="#CFCFCF",
           marker="o", linewidths=0, zorder=1)

# black comb: contiguous vertical runs per column -> line segments
segs = []
bm = sub(black)
for c in range(bm.shape[1]):
    col = bm[:, c]
    idx = np.nonzero(col)[0]
    if not len(idx):
        continue
    start = prev = idx[0]
    for i in idx[1:]:
        if i - prev > 1:
            segs.append([(px2dx(c + X0), py2dy(prev + Y0)), (px2dx(c + X0), py2dy(start + Y0))])
            start = i
        prev = i
    segs.append([(px2dx(c + X0), py2dy(prev + Y0)), (px2dx(c + X0), py2dy(start + Y0))])
ax.add_collection(LineCollection(segs, colors="black", linewidths=2.2, zorder=2))

# red / blue class blobs
for m, colr in ((red, "#FF0000"), (blue, "#0000FF")):
    yy, xx = np.nonzero(sub(m)[::2, ::2])
    ax.scatter(px2dx(xx * 2 + X0), py2dy(yy * 2 + Y0), s=12, c=colr,
               marker="o", linewidths=0, zorder=3)

ax.set_xticks(range(0, 36, 5))
ax.set_yticks(range(-10, 41, 10))
ax.tick_params(length=3.5, width=1.0, labelsize=9, colors="black")
for side in ("left", "right", "bottom"):
    ax.spines[side].set_visible(False)
ax.spines["top"].set_visible(True)
ax.spines["top"].set_color("#E60000")
ax.spines["top"].set_linewidth(2.0)

fig.savefig(OUT, dpi=DPI, transparent=True)
plt.close(fig)
print("wrote", OUT, "segments:", len(segs))
