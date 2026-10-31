#!/usr/bin/env python3
"""Generate slide_008_graph_v2.png - the one-vs-all class-region plot for slide 008.

Canvas is the original panel grid: inner panel x 167-798, y 120-505 of
unique_slides/slide_008.jpg (960x540, 1px == 1pt == 1/72in) -> 632 x 386 px,
saved at 100 dpi so the pptx addImage rect (632/72 x 386/72 in) is pixel-exact.

Tint regions are painted from the measured lattice slide_008_regions.npy
(extracted from the original frame; labels 0 white, 1 green, 2 lavender,
3 pink, 4 grey). Axes, arrowheads, boundary lines, ticks and point clusters
are drawn at their measured pixel coordinates on the same grid.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

W, H, DPI = 632, 386, 100
OUT = "slide_008_graph_v2.png"

# measured tint centroids (RGB 0-255)
TINT = {1: (220, 248, 213), 2: (196, 194, 240), 3: (251, 219, 225), 4: (231, 231, 231)}
RED = (204, 34, 34)      # #CC2222 family - measured axis + d1 stroke
BLUE = (0, 0, 255)
GREEN = (0, 160, 0)

# hatch strokes per region (direction, spacing px, stroke rgb)
HATCH = {
    1: [(90, 7, (150, 220, 160))],                 # green: horizontal
    2: [(-45, 7, (150, 148, 205))],                # lavender: diagonal /
    3: [(45, 8, (205, 170, 185))],                 # pink: diagonal backslash
    4: [(45, 9, (185, 185, 185)), (-45, 9, (185, 185, 185))],  # grey: cross-hatch
}

# measured decision boundaries (panel-local px endpoints)
BOUNDS = [
    (RED, (108, 423), (90, 370)),    # d1(x)
    (BLUE, (493, 208), (20, 360)),   # d2(x)
    (GREEN, (68, 528), (242, 75)),   # d3(x)
]

# measured point clusters (panel-local px, radius ~7.5 px)
CLUSTERS = [
    (GREEN, [(209, 46), (273, 45), (271, 90), (223, 132), (271, 132), (333, 120), (223, 163)]),
    (BLUE, [(478, 178), (433, 218), (473, 213), (470, 255), (319, 220), (319, 252),
            (370, 248), (406, 270), (435, 268), (433, 220)]),
    (RED, [(193, 225), (158, 253), (185, 253), (158, 278), (190, 278)]),
]

# boundary ticks: thick segment perpendicular to the line at the measured point
TICKS = [
    (RED, 333, 312, 1, 1.192),
    (BLUE, 461, 26, 1, -0.838),
    (GREEN, 131, 198, 460, -167),
]


def hatch_layer(mask, angle_deg, spacing, rgb, width=2.0, alpha=0.5):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    a = np.deg2rad(angle_deg)
    u = np.cos(a) * xx + np.sin(a) * yy
    lines = (np.mod(u, spacing) < width) & mask
    lay = np.zeros((H, W, 3))
    lay[lines] = np.array(rgb, dtype=np.float64) / 255.0
    return lay, lines.astype(np.float64)


labels = np.load("slide_008_regions.npy")

img = np.ones((H, W, 3))
counts = {}
for k, c in TINT.items():
    m = labels == k
    counts[k] = int(m.sum())
    img[m] = np.array(c, dtype=np.float64) / 255.0
counts[0] = int((labels == 0).sum())

# border strokes leaked into the lattice at the panel edge -> white
img[:2, :] = 1.0
img[-2:, :] = 1.0
img[:, :2] = 1.0
img[:, -2:] = 1.0

hatch_total = 0
for k, specs in HATCH.items():
    mask = labels == k
    mask[:2, :] = False
    mask[-2:, :] = False
    mask[:, :2] = False
    mask[:, -2:] = False
    for angle, spacing, rgb in specs:
        lay, alpha = hatch_layer(mask, angle, spacing, rgb)
        img = img * (1.0 - alpha[..., None]) + lay * alpha[..., None]
        hatch_total += int(alpha.sum())

fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)  # image-like coordinates (y down)
ax.axis("off")
ax.imshow(img, extent=[0, W, H, 0], interpolation="nearest", zorder=0, aspect="auto")

# panel border: measured thin red stroke around the inner panel
ax.add_patch(plt.Rectangle((1, 1), W - 2, H - 2, fill=False, ec=np.array(RED) / 255.0,
                           lw=2.0, zorder=6))

# decision boundaries
for color, (x0, x1), (y0, y1) in BOUNDS:
    ax.plot([x0, x1], [y0, y1], color=np.array(color) / 255.0, lw=2.5,
            solid_capstyle="round", zorder=4)

# boundary ticks (thick, perpendicular)
for color, x, y, dx, dy in TICKS:
    n = (dx * dx + dy * dy) ** 0.5
    px, py = -dy / n, dx / n
    ax.plot([x - px * 6, x + px * 6], [y - py * 6, y + py * 6],
            color=np.array(color) / 255.0, lw=4.0, solid_capstyle="butt", zorder=5)

# point clusters
for color, pts in CLUSTERS:
    for x, y in pts:
        ax.add_patch(plt.Circle((x, y), 7.5, fc=np.array(color) / 255.0,
                                ec="none", zorder=5))

# axes: RED shafts with RED arrowheads at the positive ends (measured)
ax.plot([0, 508], [316, 316], color=np.array(RED) / 255.0, lw=3.0,
        solid_capstyle="butt", zorder=6)
ax.add_patch(Polygon([[508, 316], [494, 310.5], [494, 321.5]], closed=True,
                     fc=np.array(RED) / 255.0, ec="none", zorder=6))
ax.plot([142.5, 142.5], [323, 25], color=np.array(RED) / 255.0, lw=3.0,
        solid_capstyle="butt", zorder=6)
ax.add_patch(Polygon([[143, 15], [137.5, 25], [148.5, 25]], closed=True,
                     fc=np.array(RED) / 255.0, ec="none", zorder=6))

fig.savefig(OUT, dpi=DPI)
print("wrote %s" % OUT)
print("canvas %d x %d px" % (W, H))
print("tint px: white %d green %d lavender %d pink %d grey %d"
      % (counts[0], counts[1], counts[2], counts[3], counts[4]))
print("hatch stroke px: %d (%.1f%% of panel)" % (hatch_total, 100.0 * hatch_total / (W * H)))
