#!/usr/bin/env python3
"""Generate slide_021 activation-function plots (ReLU, PReLU, ELU, SoftPlus).

All geometry is measured from the original 960x540 frame
(videos/.../unique_slides/slide_021.jpg) with PIL; see probe_021_*.py in this
directory for the measurement scripts and verify_021.py for the closed-loop
check that re-measures both images.

Real closed-form activation functions (numpy) are rendered at the exact panel
sizes measured from the original frame; the thin blue border is baked into each
PNG so the pptx places frames exactly.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
OUT = BUILD + "/graphs_slide_021"
os.makedirs(OUT, exist_ok=True)

BLUE = "#0000FF"
RED = "#FF0000"
GRAY_GRID = "#D3D3D3"
BLACK = "#000000"
WHITE = "#FFFFFF"

# Blue graph frames measured in the 960x540 original (1 px = 1 pt).
TL = (121, 109, 400, 272)   # w 279, h 163  ReLU
TR = (563, 109, 842, 275)   # w 279, h 166  PReLU
BL = (121, 346, 400, 508)   # w 279, h 162  ELU
BR = (564, 346, 842, 508)   # w 278, h 162  SoftPlus

# Axes (data area) fractions inside each panel, from measured gridlines:
#   TL: verticals 163, 211.5, 260, 308.5, 356.5 (ticks -10..10, zero at 260)
#       horizontals 124 (10), 189 (5), 253 (0)
#   TR: x-axis at row 215 (px 718); verticals 597..802 spacing ~24.3 (ticks -4..4)
#       horizontals 145..263 spacing ~11.9 (ticks 1,2,3,-1)
#   BL: verticals 158.5, 264.5, 370.5 (ticks -3,0,3)
#       horizontals 358.5 (3), 455.5 (0), 486.5 (-1)
#   BR: vertical axis px 705, horizontal axis row 429; x ticks -4..4, y ticks 1,2,3
AX = {
    "tl": dict(left=(163 - 121) / 279.0, right=(400 - 356.5) / 279.0,
               top=(124 - 109) / 163.0, bottom=(272 - 253) / 163.0),
    "tr": dict(left=(597 - 563) / 279.0, right=(842 - 802.5) / 279.0,
               top=(145 - 109) / 166.0, bottom=(275 - 263.5) / 166.0),
    "bl": dict(left=(158.5 - 121) / 279.0, right=(400 - 370.5) / 279.0,
               top=(358.5 - 346) / 162.0, bottom=(508 - 455.5) / 162.0),
    "br": dict(left=(577 - 564) / 278.0, right=(842 - 831) / 278.0,
               top=(357 - 346) / 162.0, bottom=(508 - 429) / 162.0),
}

DPI = 72


def make_panel(name, path, box, draw_fn, xlim, ylim, xticks, yticks,
               axisfs=6.0):
    x0, y0, x1, y1 = box
    w_px, h_px = x1 - x0, y1 - y0
    axf = AX[name]
    fig = plt.figure(figsize=(w_px / 72, h_px / 72), dpi=DPI)
    ax = fig.add_axes([axf["left"], axf["bottom"], 1 - axf["left"] - axf["right"],
                       1 - axf["bottom"] - axf["top"]])
    ax.set_facecolor(WHITE)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(list(xticks))
    ax.set_yticks(list(yticks))
    ax.grid(True, color=GRAY_GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_visible(False)
    draw_fn(ax, x0, y0, x1, y1, w_px, h_px)
    ax.tick_params(labelsize=axisfs, colors=BLACK, length=2, width=0.6, pad=1.0)
    frame = fig.add_artist(plt.Rectangle(
        (0, 0), 1, 1, transform=fig.transFigure, fill=False,
        edgecolor=BLUE, linewidth=1.0, joinstyle="miter"))
    fig.savefig(path, dpi=DPI, facecolor=WHITE)
    plt.close(fig)
    print("wrote", path)


# ------------------------------------------------------------------ ReLU (TL)
def draw_tl(ax, px0, py0, px1, py1, w, h):
    """Top-left Rectified Linear Unit.

    Measured: red curve flat along the x-axis (row 253) from px 165 to 263,
    then a 45-degree rise to the upper-right (356,124). x ticks -10..10,
    y ticks 0,5,10. Axis letters 'f' (top of y-axis) and 'x' (right end).
    """
    x = np.linspace(-10, 10, 400)
    ax.plot(x, np.maximum(0.0, x), color=RED, linewidth=1.8,
            solid_capstyle="butt", zorder=3)
    ax.text(1.05, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.0, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


# ----------------------------------------------------------------- PReLU (TR)
def draw_tr(ax, px0, py0, px1, py1, w, h):
    """Top-right Parametric ReLU.

    Measured: shallow red segment just below the zero line from px 684 to 719
    (negative branch, slope alpha ~0.1), then a 45-degree rise from (719,215)
    to (812,123). x ticks -4..4, y ticks -1,1,2,3.
    """
    x = np.linspace(-4, 4, 400)
    ax.plot(x, np.where(x >= 0, x, 0.1 * x), color=RED, linewidth=1.8,
            solid_capstyle="butt", zorder=3)
    ax.text(1.05, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.0, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


# ------------------------------------------------------------------- ELU (BL)
def draw_bl(ax, px0, py0, px1, py1, w, h):
    """Bottom-left Exponential LU.

    Measured: red curve for alpha=1 running from the upper-right (356,374)
    down through the origin region to the lower-left asymptote near
    px 193..210, row 478..481; legend glyphs at px x 183..204, rows 366..394
    (four entries); rotated y-label 'f(x, alpha)'; dashed grey guides at f=3
    and x=3.
    """
    x = np.linspace(-3, 3, 500)
    for a, col in [(0.1, "#E8383D"), (0.2, "#00B050"), (0.5, "#0000FF"), (1.0, "#A05050")]:
        y = np.where(x >= 0, x, a * (np.exp(x) - 1.0))
        ax.plot(x, y, color=col, linewidth=1.2, zorder=3)
    # legend swatch block, measured at px x 183..204, rows 366..394
    ax.plot([183 - px0, 204 - px0], [370 - py0, 370 - py0], color="#E8383D",
            linewidth=1.2)
    ax.plot([183 - px0, 204 - px0], [378 - py0, 378 - py0], color="#00B050",
            linewidth=1.2)
    ax.plot([183 - px0, 204 - px0], [386 - py0, 386 - py0], color="#0000FF",
            linewidth=1.2)
    ax.plot([183 - px0, 204 - px0], [394 - py0, 394 - py0], color="#A05050",
            linewidth=1.2)
    # dashed grey guides measured at f=3 and x=3
    ax.axhline(3.0, color=GRAY_GRID, linewidth=0.7, linestyle="--")
    ax.axvline(3.0, color=GRAY_GRID, linewidth=0.7, linestyle="--")
    # rotated y-axis label, measured rotated text around px x 142..158
    ax.text(150 - px0, 418 - py0, "f(x, \u03b1)", fontsize=6.2, rotation=90,
            ha="center", va="center", color=BLACK)
    ax.text(1.05, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.0, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


# --------------------------------------------------------------- SoftPlus (BR)
def draw_br(ax, px0, py0, px1, py1, w, h):
    """Bottom-right SoftPlus.

    Measured: red S-curve crossing the x-axis (px 705, row 416) -> f(0)~0.69;
    'Softplus' label at px x 671..698, rows 361..367 at the top of the plot.
    x ticks -4..4, y ticks 1,2,3.
    """
    x = np.linspace(-4, 4, 600)
    y = np.logaddexp(0.0, x)
    ax.plot(x, y, color=RED, linewidth=1.8, solid_capstyle="butt", zorder=3)
    ax.text(671 - px0, 361 - py0, "Softplus", fontsize=6.2, color=BLACK,
            ha="left", va="baseline")
    ax.text(1.05, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.0, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("tl", f"{OUT}/graph_relu.png", TL, draw_tl,
           xlim=(-10, 10), ylim=(0, 10), xticks=(-10, -5, 0, 5, 10), yticks=(0, 5, 10))
make_panel("tr", f"{OUT}/graph_prelu.png", TR, draw_tr,
           xlim=(-4, 4), ylim=(-1, 3), xticks=(-4, -2, 0, 2, 4), yticks=(-1, 1, 2, 3))
make_panel("bl", f"{OUT}/graph_elu.png", BL, draw_bl,
           xlim=(-3, 3), ylim=(-1, 3), xticks=(-3, 0, 3), yticks=(-1, 0, 3))
make_panel("br", f"{OUT}/graph_softplus.png", BR, draw_br,
           xlim=(-4, 4), ylim=(1, 3), xticks=(-4, -2, 0, 2, 4), yticks=(1, 2, 3))
print("done")
