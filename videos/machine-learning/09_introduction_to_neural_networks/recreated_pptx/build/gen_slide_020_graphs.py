#!/usr/bin/env python3
"""Generate slide_020 activation-function plots (ReLU, PReLU, ELU, SoftPlus).

Real closed-form activation functions rendered with matplotlib at the panel
sizes measured from the original 960x540 frame. The thin blue frame is baked
into each PNG (measured 1 px blue stroke) so the pptx places frames exactly.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/graphs_slide_020"
os.makedirs(OUT, exist_ok=True)

BLUE = "#0000FF"
RED = "#FF0000"
GRAY_GRID = "#D3D3D3"
BLACK = "#000000"
WHITE = "#FFFFFF"

Four thin blue #0000FF frames measured in the 960x540 original (1 px = 1 pt).
TOP = (318, 114, 616, 277)   # w 298, h 163
BL = (84, 336, 320, 475)     # w 236, h 139
BC = (362, 336, 592, 474)    # w 230, h 138
BR = (638, 336, 876, 474)    # w 238, h 138

# Axes (data area) fractions inside each panel, from measured gridlines:
#   TOP: x ticks 379.5/427.75/476/524.25/572.5, y rows 129/193.5/258
#        left=41.5/278, right=100/278, top=15/163, bottom=(163-144)/163
AX = {
    "top": dict(left=41.5 / 278, right=100 / 278, top=15 / 163, bottom=(163 - 144) / 163),
    "bl": dict(left=0.19, right=0.055, top=0.30, bottom=0.30),
    "bc": dict(left=0.19, right=0.075, top=0.32, bottom=0.30),
    "br": dict(left=0.185, right=0.185, top=0.30, bottom=0.30),
}

DPI = 72


def make_panel(name, path, box, draw_fn, xlim=(-10, 10), ylim=(0, 10),
               xticks=(-10, -5, 0, 5, 10), yticks=(0, 5, 10),
               xlabel="x", ylabel="f"):
    x0, y0, x1, y1 = box
    w_px, h_px = x1 - x0, y1 - y0
    axf = AX[name]
    fig = plt.figure(figsize=(w_px / 72, h_px / 72), dpi=DPI)
    ax = fig.add_axes([axf["left"], axf["bottom"], 1 - axf["left"] - axf["right"],
                       1 - axf["bottom"] - axf["top"]])
    ax.set_facecolor(WHITE)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.grid(True, color=GRAY_GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_visible(False)
    draw_fn(ax, x0, y0, x1, y1, w_px, h_px)
    ax.tick_params(labelsize=6, colors=BLACK, length=2, width=0.6, pad=1.0)
    # thin blue panel frame, inscribed so the stroke straddles the measured box
    fig.add_artist(plt.Rectangle(
        (x0 + 1.0 / (DPI * 1.0) * 0, y0), 0.0, 0.0, fill=False))
    frame = fig.add_artist(plt.Rectangle(
        (0, 0), 1, 1, transform=fig.transFigure, fill=False,
        edgecolor=BLUE, linewidth=1.0, joinstyle="miter"))
    fig.savefig(path, dpi=DPI, facecolor=WHITE)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- ReLU (top)
def draw_relu(ax, px0, py0, px1, py1, w, h):
    x = np.linspace(-10, 10, 400)
    ax.plot(x, np.maximum(0, x), color=RED, linewidth=1.8, solid_capstyle="butt",
            zorder=3)
    # measured axis labels: "x" right of x-axis, "f" top of y-axis
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("top", f"{OUT}/graph_relu.png", TOP, draw_relu)


# --------------------------------------------------------------- PReLU (BL)
def draw_prelu(ax, px0, py0, px1, py1, w, h):
    x = np.linspace(-10, 10, 400)
    ax.plot(x, np.where(x >= 0, x, 0.1 * x), color=RED, linewidth=1.8,
            solid_capstyle="butt")
    # small red left-pointing arrow along the slightly-negative flat segment
    ax.annotate("", xy=(-8.0, -0.85), xytext=(-3.0, -0.35),
                arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=6))
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("bl", f"{OUT}/graph_prelu.png", BL, draw_prelu)


# --------------------------------------------------------------- ELU (center)
def draw_elu(ax, px0, py0, px1, py1, w, h):
    x = np.linspace(-5, 5, 500)
    curves = []
    for a, col in [(0.1, "#E8383D"), (0.5, "#00B050"), (1.0, "#0000FF"), (2.0, "#ED7D31")]:
        y = np.where(x >= 0, x, a * (np.exp(x) - 1.0))
        curves.append(ax.plot(x, y, color=col, linewidth=1.3)[0])
    ax.legend(curves, ["a = 0.1", "a = 0.5", "a = 1.0", "a = 2.0"], loc="upper left",
              fontsize=5.2, frameon=True, fancybox=False, edgecolor="#808080",
              handlelength=1.2, handletextpad=0.4, borderpad=0.3, labelspacing=0.25)
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("bc", f"{OUT}/graph_elu.png", BC, draw_elu, xlim=(-5, 5), ylim=(-2, 2),
           xticks=(-5, -2, 0, 2, 5), yticks=(-2, 0, 2))


# ----------------------------------------------------------- SoftPlus (right)
def draw_softplus(ax, px0, py0, px1, py1, w, h):
    x = np.linspace(-10, 10, 600)
    y = np.logaddexp(0, x)
    ax.plot(x, y, color=RED, linewidth=1.8, solid_capstyle="butt")
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("br", f"{OUT}/graph_softplus.png", BR, draw_softplus)
print("done")
