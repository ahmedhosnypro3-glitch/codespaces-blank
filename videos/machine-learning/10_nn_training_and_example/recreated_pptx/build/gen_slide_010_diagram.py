#!/usr/bin/env python3
"""Generate the slide_010 neural-network diagram (600dpi PNG on the beige panel)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

PX, PY, PW, PH = 5.32, 0.75, 5.65, 2.10   # panel origin + size, slide inches (measured from slide_010.jpg: beige x=383..790px, y=54..205px)
DPI = 600
BEIGE = "#D8CFC0"
RED = "#CC0000"
BLUE = "#0000CC"
GREEN = "#008000"
MAGENTA = "#C000C0"
GREY = "#808080"
BLACK = "#000000"

fig = plt.figure(figsize=(PW, PH), dpi=DPI)
fig.patch.set_facecolor(BEIGE)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PW)
ax.set_ylim(PH, 0)
ax.axis("off")
ax.add_patch(Rectangle((0, 0), PW, PH, facecolor=BEIGE, edgecolor="#9A9080", lw=1.0))


def L(x):
    return x - PX


def T(y):
    return y - PY


def txt(x, y, s, size=6, color=BLACK, style="normal", ha="center", va="center",
        weight="normal"):
    ax.text(L(x), T(y), s, fontsize=size, color=color, style=style, ha=ha, va=va,
            weight=weight, zorder=6)


def line(x1, y1, x2, y2, color=GREY, lw=0.6, ls="-", z=2):
    ax.plot([L(x1), L(x2)], [T(y1), T(y2)], color=color, lw=lw, ls=ls, zorder=z,
            solid_capstyle="round")


def sigma(x, y, fill, edge=RED, r=0.095, size=8):
    ax.add_patch(Circle((L(x), T(y)), r, facecolor=fill, edgecolor=edge, lw=1.0,
                        zorder=5))
    txt(x, y, "$\\Sigma$", size=size, color=RED if fill != "#FFFF00" else RED)


def slash_box(x, y):
    ax.add_patch(Rectangle((L(x), T(y) - 0.055), 0.11, 0.11, facecolor="#FFFFFF",
                           edgecolor=RED, lw=0.8, zorder=5))
    txt(x + 0.055, y, "/", size=6, color=RED)


# ---- input dots (purple) -------------------------------------------------
IN_X = 5.40
in_ys = [1.42, 1.60, 1.78, 1.96, 2.14, 2.32]
for y in in_ys:
    ax.add_patch(Circle((L(IN_X), T(y)), 0.035, facecolor=MAGENTA,
                        edgecolor=MAGENTA, zorder=5))

# ---- layer 1: red-outlined Sigma nodes -----------------------------------
COL1_X = 5.88
col_ys = [1.05, 1.65, 2.25]
for y in col_ys:
    line(IN_X, y if y in in_ys else in_ys[0], COL1_X, y, MAGENTA, 0.5, ":")
for y in col_ys:
    sigma(COL1_X, y, "#FFFFFF")
    slash_box(COL1_X + 0.20, y)
    txt(COL1_X + 0.42, y, "O", size=6.5, color=RED)
    for k in range(3):
        ax.add_patch(Circle((L(COL1_X + 0.58 + 0.10 * k), T(y)), 0.022,
                            facecolor="#BFBFBF", edgecolor="#8C8C8C", lw=0.4,
                            zorder=4))

# ---- layer 2: second Sigma column with Net_i labels ----------------------
COL2_X = 7.30
for y in col_ys:
    line(COL1_X + 0.85, y, COL2_X, y, "#909090", 0.7, "-")
for y in col_ys:
    sigma(COL2_X, y, "#FFFFFF")
    txt(COL2_X - 0.02, y - 0.19, "Net$_i$", size=6, color=RED, ha="center")
    slash_box(COL2_X + 0.20, y)
    txt(COL2_X + 0.42, y, "O$_i$", size=6.5, color=RED)

# ---- weighted-input yellow circles (diagonal) ----------------------------
WJ = [(8.50, 0.95), (8.72, 1.22), (8.94, 1.49)]
for wx, wy in WJ:
    ax.add_patch(Circle((L(wx), T(wy)), 0.075, facecolor="#FFFF00",
                        edgecolor="#B0A020", lw=0.7, zorder=5))
    txt(wx + 0.13, wy, "W$_{ij}$", size=5.5, color=BLACK, style="italic")

# ---- col2 -> col5 connections (blue, labelled W_ji) ----------------------
for c2y, (w5y) in [(1.05, 1.67), (1.65, 1.98), (2.25, 2.24)]:
    line(COL2_X + 0.85, c2y, 9.15, w5y, BLUE, 0.7, "-")
txt(8.05, 1.35, "W$_{ji}$", size=5.5, color=BLUE, style="italic")

# ---- layer 3: yellow Sigma nodes + outputs -------------------------------
COL5_X = 9.15
out_ys = [1.67, 1.98, 2.24]
out_names = ["1", "2", "m"]
for i, y in enumerate(out_ys):
    sigma(COL5_X, y, "#FFFF00", edge="#B0A020", r=0.085, size=7.5)
    txt(COL5_X, y - 0.16, "Net$_j$", size=5.5, color=RED)
    txt(COL5_X + 0.17, y, "O$_" + out_names[i] + "$", size=6, color=BLACK)
    txt(9.60, y, "Output " + out_names[i], size=6, color=BLACK, ha="left")

# ---- magenta "1" bias circle + dotted line up to the W circles ----------
ax.add_patch(Circle((L(8.05), T(2.60)), 0.078, facecolor=MAGENTA,
                    edgecolor=MAGENTA, zorder=5))
txt(8.05, 2.60, "1", size=6.5, color="#FFFFFF", weight="bold")
line(8.05, 2.60, 8.50, 0.95, MAGENTA, 0.6, ":", z=1)

# ---- green up arrows ------------------------------------------------------
for gx in (7.30, 9.15):
    ax.add_patch(FancyArrowPatch((L(gx), 2.68), (L(gx), 2.34),
                                 arrowstyle="-|>", mutation_scale=7,
                                 color=GREEN, lw=0.9, zorder=5))

# ---- "Node Bias" badge ----------------------------------------------------
ax.add_patch(Circle((L(5.38), T(2.52)), 0.048, facecolor="#FFFF00",
                    edgecolor="#B0A020", lw=0.6, zorder=5))
txt(5.38, 2.52, "!", size=5.5, color=RED, weight="bold")
txt(5.55, 2.52, "Node Bias", size=6, color=BLACK, ha="left")

# ---- error-feedback curved arrows (right edge -> yellow Sigma nodes) -----
for wy in out_ys:
    ax.add_patch(FancyArrowPatch((9.95, wy - 0.10), (L(COL5_X) + 0.10, T(wy) - 0.10),
                                 connectionstyle="arc3,rad=-0.35", arrowstyle="-|>",
                                 mutation_scale=6, color="#909090", lw=0.7,
                                 linestyle=(0, (2, 2)), zorder=3))

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/diagram_010.png"
fig.savefig(OUT, dpi=DPI, facecolor=fig.patch.get_facecolor())
print("wrote", OUT)
