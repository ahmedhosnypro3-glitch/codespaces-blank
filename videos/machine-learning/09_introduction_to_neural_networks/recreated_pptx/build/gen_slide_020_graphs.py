#!/usr/bin/env python3
"""Generate slide_020 activation-function plots (ReLU, PReLU, ELU, SoftPlus).

All geometry is measured from the original 960x540 frame
(unique_slides/slide_020.jpg) with PIL; see build/verify_020.py for the
closed-loop check that re-measures both images.

Real closed-form activation functions are rendered with matplotlib at the
panel sizes measured from the original frame. The thin blue frame is baked
into each PNG so the pptx places frames exactly.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/graphs_slide_020"
os.makedirs(OUT, exist_ok=True)

BLUE = "#0000FF"
RED = "#FF0000"
GRAY_GRID = "#D3D3D3"
BLACK = "#000000"
WHITE = "#FFFFFF"
YELLOW = "#FFFF00"
PALE_YELLOW = "#FFFF80"      # measured ellipse interior (255,255,128)
DARK_RED = "#A05050"         # measured SoftPlus curve
PINK = "#F08080"             # measured PReLU branch
GRAY = "#808080"

# Four thin blue #0000FF frames measured in the 960x540 original (1 px = 1 pt).
TOP = (338, 114, 616, 277)   # w 278, h 163
BL = (83, 335, 320, 475)     # w 237, h 140
BC = (362, 337, 592, 473)    # w 230, h 136
BR = (638, 337, 875, 473)    # w 237, h 136

# Axes (data area) fractions inside each panel, from measured gridlines.
# Fractions are (distance from panel left, distance from panel bottom,
# width, height) in matplotlib add_axes() convention.
#
#   TOP: vertical gridlines at px 379/427/476/524/572 -> x ticks -10..10,
#        zero line at px 476; horizontal gridlines at rows 129/193/258 -> y 0..10.
#   BL:  vertical gridlines at px 128/170/213 -> x ticks; rows 383/423/463.
#   BC:  vertical gridlines at px 394/483/557; rows 346/426.
#   BR:  vertical gridlines at px 664/696/727/758/790; rows 364/446.
def _frac(px0, py0, px1, py1, dx0, dy0, dx1, dy1):
    """Data-area rect (dx0,dy0)-(dx1,dy1) in panel px -> matplotlib add_axes."""
    w = float(px1 - px0)
    h = float(py1 - py0)
    left = (dx0 - px0) / w
    width = (dx1 - dx0) / w
    bottom = (py1 - dy1) / h
    height = (dy1 - dy0) / h
    return dict(left=left, bottom=bottom, width=width, height=height)


AX = {
    "top": _frac(*TOP, 379, 129, 572, 258),
    "bl": _frac(*BL, 106, 345, 299, 424),
    "bc": _frac(*BC, 368, 346, 576, 455),
    "br": _frac(*BR, 654, 364, 846, 447),
}

DPI = 72


def make_panel(name, path, box, draw_fn, xlim=(-10, 10), ylim=(0, 10),
               xticks=(-10, -5, 0, 5, 10), yticks=(0, 5, 10),
               xlabel="x", ylabel="f"):
    x0, y0, x1, y1 = box
    w_px, h_px = x1 - x0, y1 - y0
    axf = AX[name]
    fig = plt.figure(figsize=(w_px / 72, h_px / 72), dpi=DPI)
    ax = fig.add_axes([axf["left"], axf["bottom"], axf["width"], axf["height"]])
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
    frame = fig.add_artist(plt.Rectangle(
        (0, 0), 1, 1, transform=fig.transFigure, fill=False,
        edgecolor=BLUE, linewidth=1.0, joinstyle="miter"))
    fig.savefig(path, dpi=DPI, facecolor=WHITE)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- ReLU (top)
def draw_relu(ax, px0, py0, px1, py1, w, h):
    """Top ReLU plot.

    Measured facts from the original frame:
      * zero line at px x=476, row 258; x ticks -10..10 at px 379..572.
      * red curve: flat at y=0 for x<=0, then 45-degree rise to (10,10).
      * pale-yellow filled ellipse centred on the flat segment,
        px x 355..490, row 250..266 (measured yellow rows 253..269).
      * thin black diagonal leader near the top-centre of the panel.
    """
    x = np.linspace(-10, 10, 400)
    ax.plot(x, np.maximum(0, x), color=RED, linewidth=1.8, solid_capstyle="butt",
            zorder=3)
    # measured yellow highlight ellipse over the flat negative-x segment
    # (px x 355..490 -> data -10.5..0.6 ; px rows 250..266 -> data 0.9..-0.7)
    ax.add_patch(Ellipse(
        xy=(-5.0, 0.1), width=11.2, height=1.55,
        facecolor=PALE_YELLOW, edgecolor="none", zorder=2, alpha=1.0))
    # small black diagonal leader near the top-centre of the panel
    ax.annotate("", xy=(2.6, 9.3), xytext=(1.2, 10.0),
                arrowprops=dict(arrowstyle="-|>", color=BLACK, linewidth=0.9,
                                shrinkA=0, shrinkB=0, mutation_scale=5))
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("top", f"{OUT}/graph_relu.png", TOP, draw_relu)


# --------------------------------------------------------------- PReLU (BL)
def draw_prelu(ax, px0, py0, px1, py1, w, h):
    """Bottom-left Parametric ReLU.

    Measured: flat red segment slightly BELOW the zero line (row ~424 vs
    zero row 424) spanning px x 128..213, with a small red left-pointing
    arrowhead at its left end near px x 128; pink-red rising branch.
    """
    x = np.linspace(-10, 10, 400)
    y = np.where(x >= 0, x, 0.1 * x)
    ax.plot(x, y, color=PINK, linewidth=1.8, solid_capstyle="butt")
    # the flat negative-x segment is drawn in solid red, distinct from the
    # lighter pink rising branch (both measured in the original frame)
    xneg = x[x < 0]
    ax.plot(xneg, 0.1 * xneg, color=RED, linewidth=1.8, solid_capstyle="butt")
    # small red left-pointing arrow along the flat negative-x segment
    # (measured arrowhead near px x 128, i.e. data x ≈ -9.1)
    ax.annotate("", xy=(-9.1, -0.30), xytext=(-4.2, -0.60),
                arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=7))
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("bl", f"{OUT}/graph_prelu.png", BL, draw_prelu)


# --------------------------------------------------------------- ELU (center)
def draw_elu(ax, px0, py0, px1, py1, w, h):
    """Bottom-centre ELU with its inset sub-plot.

    Measured in the original frame:
      * legend swatch column at px x 394-395, four entries on rows
        346/352/359/366/373 with labels at px 400..424.
      * INSET: its own grey rectangle in the upper-right quadrant with a
        vertical y-axis at px x 481 (rows 351..413), a horizontal x-axis at
        row 404-405, a rising red curve, and a grey connector.
    """
    x = np.linspace(-5, 5, 500)
    curves = []
    for a, col in [(0.1, "#E8383D"), (0.5, "#00B050"), (1.0, "#0000FF"), (2.0, "#ED7D31")]:
        y = np.where(x >= 0, x, a * (np.exp(x) - 1.0))
        curves.append(ax.plot(x, y, color=col, linewidth=1.3)[0])
    ax.legend(curves, ["a = 0.1", "a = 0.5", "a = 1.0", "a = 2.0"], loc="upper left",
              fontsize=5.2, frameon=True, fancybox=False, edgecolor=GRAY,
              handlelength=1.2, handletextpad=0.4, borderpad=0.3, labelspacing=0.25)

    # ---- inset sub-plot (measured upper-right quadrant of the ELU panel) ----
    # inset frame: px x 455..535, rows 345..410
    ins_x0, ins_x1 = 455, 535
    ins_y0, ins_y1 = 345, 410
    ins_l = (ins_x0 - px0) / w
    ins_r = (ins_x1 - px0) / w
    ins_b = (py1 - ins_y1) / h
    ins_t = (py1 - ins_y0) / h
    axins = ax.inset_axes([ins_l, ins_b, ins_r - ins_l, ins_t - ins_b])
    axins.set_facecolor(WHITE)
    axins.set_xlim(-5, 5)
    axins.set_ylim(-2, 2)
    axins.set_xticks([-5, 0, 5])
    axins.set_yticks([-2, 0, 2])
    axins.grid(True, color=GRAY_GRID, linewidth=0.5)
    axins.set_axisbelow(True)
    for sp in axins.spines.values():
        sp.set_visible(False)
    xi = np.linspace(-5, 5, 300)
    for a, col in [(0.1, "#E8383D"), (0.5, "#00B050"), (1.0, "#0000FF"), (2.0, "#ED7D31")]:
        yi = np.where(xi >= 0, xi, a * (np.exp(xi) - 1.0))
        axins.plot(xi, yi, color=col, linewidth=1.1)
    axins.tick_params(labelsize=4.2, colors=BLACK, length=1.5, width=0.5, pad=0.8)
    axins.patch.set_edgecolor(GRAY)
    axins.patch.set_linewidth(0.7)

    # grey connector from the main curves into the inset (measured curve
    # running from the inset's lower-left down toward the main ELU family)
    ax.plot([-0.2, 0.9], [1.1, 1.9], color=GRAY, linewidth=0.8, zorder=4)

    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("bc", f"{OUT}/graph_elu.png", BC, draw_elu, xlim=(-5, 5), ylim=(-2, 2),
           xticks=(-5, -2, 0, 2, 5), yticks=(-2, 0, 2))


# ----------------------------------------------------------- SoftPlus (right)
def draw_softplus(ax, px0, py0, px1, py1, w, h):
    """Bottom-right SoftPlus.

    Measured: dark red/brown (#A05050) S-curve; in-plot black title
    'SoftPlus' at px x 730..754, rows 348..351 (top-centre of the panel).
    """
    x = np.linspace(-10, 10, 600)
    y = np.logaddexp(0, x)
    ax.plot(x, y, color=DARK_RED, linewidth=1.6, solid_capstyle="butt")
    # in-plot title, measured at px x 730..754, rows 347..352
    ax.text(730 - px0, 351 - py0, "SoftPlus", fontsize=6.2, color=BLACK,
            ha="left", va="baseline")
    ax.text(1.045, 0.0, "x", transform=ax.transAxes, fontsize=7, style="italic",
            ha="left", va="center")
    ax.text(0.02, 1.02, "f", transform=ax.transAxes, fontsize=7, style="italic",
            ha="center", va="bottom")


make_panel("br", f"{OUT}/graph_softplus.png", BR, draw_softplus)
print("done")
