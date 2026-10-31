#!/usr/bin/env python3
"""Slide 047 graph (rebuild wave 3, fix round 2) — full-slide transparent PNG.

Like rb4 (pixel-faithful tracing of qa/rejudge2/orig_png/slide_047.png:
white axes on transparent bg, red top spine at y=40, gray dot lattice,
black comb of vertical segments, red/blue class clouds traced from the
original frame's masks), plus the gray dot lattice extended over the whole
inner slide area outside the axes box, as in the original frame.
Axes rect from measured spines (px 207..752, py 63..502 of the 960x540 frame).
Run: python3 gen_slide_047_graph_rb5.py <out.png>
"""
import sys
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
OUT = sys.argv[1] if len(sys.argv) > 1 else "slide_047_graph_rb5.png"
DPI = 200
W_IN, H_IN = 13.33, 7.5

im = np.array(Image.open(NS + "/qa/rejudge2/orig_png/slide_047.png").convert("RGB")).astype(int)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 150) & (G < 110) & (B < 110)
blue = (B > 150) & (R < 110) & (G < 110)
black = (R < 70) & (G < 70) & (B < 70)
gray = (abs(R - G) < 10) & (abs(G - B) < 10) & (R > 170) & (R < 236) & ~red & ~blue & ~black

X0, X1, Y0, Y1 = 208, 751, 66, 501  # plot interior px box (excl. red top spine)
AX0, AX1, AY0, AY1 = 207, 752, 63, 502  # axes spines px box


def px2dx(px):
    return (px - AX0) / (AX1 - AX0 - 1.0) * 35.0


def py2dy(py):
    return 40.0 - (py - AY0) / (AY1 - AY0 - 1.0) * 50.0


sub = lambda m: m[Y0:Y1, X0:X1]

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_alpha(0.0)

# full-figure background axes in pixel coordinates: gray lattice outside the axes box
bg = fig.add_axes([0, 0, 1, 1])
bg.set_xlim(0, 960)
bg.set_ylim(540, 0)
bg.axis("off")
gy, gx = np.nonzero(gray[::3, ::3])
outside = ~((gx * 3 >= AX0) & (gx * 3 <= AX1) & (gy * 3 >= AY0) & (gy * 3 <= AY1))
bg.scatter(gx[outside] * 3 + 1, gy[outside] * 3 + 1, s=5, c="#CFCFCF",
           marker="o", linewidths=0, zorder=0)

AX = [AX0 / 960.0, (540 - AY1) / 540.0, (AX1 - AX0) / 960.0, (AY1 - AY0) / 540.0]
ax = fig.add_axes(AX)
ax.set_xlim(0, 35)
ax.set_ylim(-10, 40)
ax.set_facecolor("white")

# gray dot lattice inside the plot
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

# red / blue class clouds
for m, colr in ((red, "#FF0000"), (blue, "#0000FF")):
    yy, xx = np.nonzero(sub(m)[::2, ::2])
    ax.scatter(px2dx(xx * 2 + X0), py2dy(yy * 2 + Y0), s=13, c=colr,
               marker="o", linewidths=0, zorder=3)

ax.set_xticks(range(0, 36, 5))
ax.set_yticks(range(-10, 41, 10))
ax.tick_params(length=3.5, width=1.0, labelsize=9, colors="black")
for side in ("left", "right", "bottom"):
    ax.spines[side].set_visible(False)
# original frame has no visible top spine (only a faint 1px antialiased edge)
for side in ("top",):
    ax.spines[side].set_visible(False)

fig.savefig(OUT, dpi=DPI, transparent=True)
plt.close(fig)
print("wrote", OUT, "segments:", len(segs))
