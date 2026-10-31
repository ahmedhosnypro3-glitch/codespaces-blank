#!/usr/bin/env python3
"""Generate slide 029 network-diagram panel.

Geometry is measured from unique_slides/slide_029.jpg (960x540, 72 px/in):
beige panel x0.931-7.569in, y1.917-5.361in (6.638 x 3.444 in).  Node columns and
rows are pinned to the original's pixel positions.  The vertical "Error Error
Error" bar and the "Class 1/2/m" column are NOT part of the panel — they are
drawn as separate slide shapes.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.patches as mpatches
import os

outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

BEIGE = "#E8E0D0"
BEIGE_EDGE = "#D0C8B8"
WHITE = "#FFFFFF"
RED = "#C00000"
BLUE = "#0070C0"
GREEN = "#00B050"
LIGHT_GREEN = "#E2EFDA"
MAGENTA = "#CC66CC"
GRAY = "#808080"
LINK = "#E8A0A0"
BLACK = "#000000"

# panel in inches
PX0, PY0, PX1, PY1 = 0.931, 1.917, 7.569, 5.361
PW, PH = PX1 - PX0, PY1 - PY0


def X(px):
    return (px - 67) / 72.0


def Y(px):
    return (386 - px) / 72.0


fig = plt.figure(figsize=(PW, PH), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(0, PH)
ax.axis("off")

ax.add_patch(patches.Rectangle((0, 0), PW, PH, facecolor=BEIGE,
                               edgecolor=BEIGE_EDGE, linewidth=1.0))

R = 0.25                      # node circle radius (18 px at 72 dpi)
INPUT_X = X(77)
DOT_Y = [Y(224), Y(247), Y(270), Y(293)]
NODE_Y = [Y(181.5), Y(253.5), Y(335.5)]
COL1, COL2, COL3 = X(163), X(262), X(427)
OMITTED_X = [X(196), X(205), X(214)]
OUT_X0, OUT_X1, OUT_H = X(487), X(537), 0.194


def sigma(x, y):
    ax.text(x, y, r"$\Sigma$", fontsize=13, color=RED, ha="center",
            va="center", fontweight="bold")


def squiggle(x, y, color):
    """Small S-shaped sigmoid glyph."""
    verts = [(x - 0.045, y - 0.075), (x + 0.045, y - 0.075),
             (x + 0.05, y + 0.075), (x - 0.04, y + 0.075)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    ax.add_patch(mpatches.PathPatch(Path(verts, codes), fill=False,
                                    edgecolor=color, linewidth=1.6))


def node(col_x, y, edge_color, face_color, squig_color):
    ax.add_patch(patches.Circle((col_x, y), R, facecolor=face_color,
                                edgecolor=edge_color, linewidth=1.8))
    ax.plot([col_x, col_x], [y - R, y + R], color=RED, linewidth=1.4)
    sigma(col_x - 0.16, y)
    squiggle(col_x + 0.16, y, squig_color)


# input dots + fan-out links
for dy in DOT_Y:
    ax.add_patch(patches.Circle((INPUT_X, dy), 0.055, facecolor=MAGENTA,
                                edgecolor=MAGENTA, linewidth=1.0))
    for y in NODE_Y:
        ax.plot([INPUT_X + 0.06, COL1 - R], [dy, y], color=GRAY,
                linewidth=0.6, alpha=0.75)

# column 1 – red-outlined white circles
for y in NODE_Y:
    node(COL1, y, RED, WHITE, RED)
    for ox in OMITTED_X:
        ax.add_patch(patches.Circle((ox, y), 0.045, facecolor="none",
                                    edgecolor=GRAY, linewidth=1.0))

# column 2 – blue-outlined white circles
for y in NODE_Y:
    node(COL2, y, BLUE, WHITE, BLACK)

# column 3 – green light-filled circles
for y in NODE_Y:
    node(COL3, y, GREEN, LIGHT_GREEN, GREEN)

# fully-connected links col2 -> col3
for y2 in NODE_Y:
    for y3 in NODE_Y:
        ax.plot([COL2 + R, COL3 - R], [y2, y3], color=LINK, linewidth=1.0)

# w_ji labels on links
WJI_X = X(337)
for wy in [Y(172), Y(205), Y(242)]:
    ax.text(WJI_X, wy, r"$w_{ji}$", fontsize=11, color=BLUE, ha="center",
            va="center", fontweight="bold", style="italic")

# Net_j above columns 2 and 3
for col in [COL2, COL3]:
    ax.text(col, Y(146), r"$\mathit{Net}_j$", fontsize=11, color=RED,
            ha="center", va="bottom", fontweight="bold", style="italic")

# O_j beside every column-2 and column-3 node
for col in [COL2, COL3]:
    for y in NODE_Y:
        ax.text(col + 0.36, y + 0.05, r"$\mathit{O}_j$", fontsize=10,
                color=RED, ha="left", va="center", fontweight="bold",
                style="italic")

# Output 1 / Output 2 / Output m boxes + red arrows from column 3
for i, label in enumerate(["Output 1", "Output 2", "Output m"]):
    y = NODE_Y[i]
    ax.add_patch(patches.Rectangle((OUT_X0, y - OUT_H / 2), OUT_X1 - OUT_X0,
                                   OUT_H, facecolor=WHITE, edgecolor=BLACK,
                                   linewidth=1.0))
    ax.text((OUT_X0 + OUT_X1) / 2, y, label, fontsize=9, color=BLACK,
            ha="center", va="center", style="italic")
    ax.annotate("", xy=(OUT_X0 - 0.01, y), xytext=(COL3 + R + 0.06, y),
                arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.2,
                                shrinkA=0, shrinkB=0))

out_path = f"{outdir}/slide_029_diagram.png"
fig.savefig(out_path, dpi=200, transparent=True)
plt.close(fig)
print(f"Generated {out_path}  ({PW:.3f} x {PH:.3f} in)")
