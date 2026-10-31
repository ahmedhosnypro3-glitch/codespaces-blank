#!/usr/bin/env python3
"""Generate slide 018 assets: 5 charts + 2 2D piecewise equations.

Measured from unique_slides/slide_018.jpg (960x540):
  step panes   : blue-bordered white boxes, arrowed axes, DARK RED step curve,
                 filled translucent yellow saturation ellipses (~#F0F078)
  bottom charts: blue-bordered panels, grey grid, PINK curves (~#F2A6B0);
                 sigmoid carries interior green guide lines, a grey circle
                 marker, a top-left legend box, a green "sigmoid" label and two
                 filled yellow blobs; tanh carries an in-pane "tanh" title;
                 arctan carries "Inverse Tangent Graph" at its top-left
  equations    : red curly brace spanning both case lines, first case red,
                 second case green
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
CHART_DPI = 300
EQ_DPI = 600

RED_STEP = "#C0392B"
PINK = "#F2A6B0"
GREEN = "#2E8B57"
BLUE_BORDER = "#261F7F"
AXIS = "#333333"
GRID = "#CCCCCC"
YELLOW = "#F2E94E"
WHITE = "#FFFFFF"


def step_chart(fname, y_lo, y_hi):
    w_in, h_in = 270 / 72, 106 / 72
    fig = plt.figure(figsize=(w_in, h_in), dpi=CHART_DPI)
    fig.patch.set_facecolor(WHITE)
    fig.patch.set_edgecolor(BLUE_BORDER)
    fig.patch.set_linewidth(2.0)
    ax = fig.add_axes([0.17, 0.20, 0.72, 0.62])
    ax.set_facecolor(WHITE)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-3, 3)
    ax.set_ylim(y_lo, y_hi)

    # arrowed axes
    ax.annotate("", xy=(3.0, 0), xytext=(-3, 0),
                arrowprops=dict(arrowstyle="-|>", color=AXIS, lw=1.4))
    ax.annotate("", xy=(-3, y_hi - 0.1), xytext=(-3, y_lo),
                arrowprops=dict(arrowstyle="-|>", color=AXIS, lw=1.4))

    cases = (0, 1) if y_lo == 0 else (-1, 1)
    xs = np.linspace(-3, 3, 200)
    ys = np.where(xs < 0, cases[0], cases[1])
    ax.plot(xs, ys, color=RED_STEP, lw=2.0, zorder=4)
    ax.plot([0, 0], [cases[0], cases[1]], color=RED_STEP, lw=2.0, zorder=4)

    # small red arrowheads marking the saturated flat branches
    h = y_hi - y_lo
    for xv, yv in ((-1.15, cases[0]), (1.15, cases[1])):
        ax.annotate("", xy=(xv, yv), xytext=(xv - 0.55, yv),
                    arrowprops=dict(arrowstyle="-|>", color=RED_STEP, lw=1.3),
                    zorder=5)

    # filled translucent yellow saturation ellipses
    for yv in cases:
        for xv in (-1.45, 1.45):
            ax.add_patch(plt.matplotlib.patches.Ellipse(
                (xv, yv), width=1.6, height=0.42 * h / 2.2,
                facecolor=YELLOW, edgecolor="#D9C93A", alpha=0.72,
                linewidth=1.0, zorder=6))
    fig.savefig(f"{OUT}/{fname}", dpi=CHART_DPI, facecolor=WHITE,
                edgecolor=BLUE_BORDER)
    plt.close(fig)
    im = Image.open(f"{OUT}/{fname}")
    return {"image": fname, "w_px": im.size[0], "h_px": im.size[1], "dpi": CHART_DPI}


def smooth_chart(fname, kind, xlim, ylim, yticks, ylabels, internal=None,
                 internal_pos="center", annotate=False, legend=False,
                 ylabel_side=False):
    w_in, h_in = 255 / 72, 150 / 72
    fig = plt.figure(figsize=(w_in, h_in), dpi=CHART_DPI)
    fig.patch.set_facecolor(WHITE)
    fig.patch.set_edgecolor(BLUE_BORDER)
    fig.patch.set_linewidth(2.0)
    ax = fig.add_axes([0.20, 0.16, 0.72, 0.66])
    ax.set_facecolor(WHITE)
    xs = np.linspace(xlim[0], xlim[1], 600)
    if kind == "sigmoid":
        ys = 1 / (1 + np.exp(-xs))
    elif kind == "tanh":
        ys = np.tanh(xs)
    else:
        ys = np.arctan(xs)
    ax.plot(xs, ys, color=PINK, lw=2.0, zorder=4)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=5.5, color=AXIS)
    ax.set_xticks([xlim[0], 0, xlim[1]])
    ax.set_xticklabels([f"{t:g}" for t in (xlim[0], 0, xlim[1])],
                       fontsize=5.5, color=AXIS)
    ax.tick_params(length=2, pad=1.5)
    ax.grid(True, color=GRID, lw=0.5)
    for s in ax.spines.values():
        s.set_color(AXIS)
        s.set_linewidth(1.0)
    ax.set_xlabel("x", fontsize=6.5, color=AXIS, labelpad=1)
    if ylabel_side:
        ax.set_ylabel("sigmoid", fontsize=6.5, color=GREEN, labelpad=1)
        ax.yaxis.set_label_position("right")
    else:
        ax.set_ylabel("f(x)", fontsize=6.5, color=AXIS, labelpad=1)
    if internal:
        if internal_pos == "left":
            ax.text(0.02, 0.98, internal, transform=ax.transAxes, fontsize=7,
                    color=AXIS, ha="left", va="top")
        else:
            ax.text(0.5, 0.98, internal, transform=ax.transAxes, fontsize=7,
                    color=AXIS, ha="center", va="top")
    if legend:
        ax.plot([0.03, 0.30], [0.90, 0.90], transform=ax.transAxes,
                color=PINK, lw=2.0, zorder=6)
        ax.add_patch(plt.matplotlib.patches.Rectangle(
            (0.02, 0.82), 0.31, 0.15, transform=ax.transAxes, facecolor=WHITE,
            edgecolor=GRID, lw=0.6, zorder=5))
    if annotate:
        for xv in (1.0, 2.0, 3.0):
            ax.axvline(xv, color=GREEN, lw=1.0, zorder=2)
        xm, ym = 1.0, 1 / (1 + np.exp(-1.0))
        ax.plot([xm], [ym], marker="o", ms=4, color="#888888", zorder=7)
        for (xv, yv) in ((3.6, 0.97), (-3.6, 0.03)):
            ax.add_patch(plt.matplotlib.patches.Ellipse(
                (xv, yv), width=2.6, height=0.30, facecolor=YELLOW,
                edgecolor="#D9C93A", alpha=0.72, linewidth=1.0, zorder=6))
    fig.savefig(f"{OUT}/{fname}", dpi=CHART_DPI, facecolor=WHITE,
                edgecolor=BLUE_BORDER)
    plt.close(fig)
    im = Image.open(f"{OUT}/{fname}")
    return {"image": fname, "w_px": im.size[0], "h_px": im.size[1], "dpi": CHART_DPI}


def piecewise(cases, fname):
    """2D piecewise: red brace spanning both case lines; first case red, second green.

    Sized for the slide directly (1.43 x 0.66 in at 600 dpi) so the build plates
    it at native size: brace ~0.6 in tall, case-line pitch ~0.19 in. Reports the
    measured row fraction of each case line so the build can align them.
    """
    w_in, h_in = 1.43, 0.66
    fig = plt.figure(figsize=(w_in, h_in), dpi=EQ_DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    spans = [0.644, 0.356]
    for (val, cond), y, col in zip(cases, spans, ("#C00000", GREEN)):
        ax.text(0.145, y, val, fontsize=21, color=col, ha="left",
                va="center", fontweight="bold")
        ax.text(0.34, y, f"for {cond}", fontsize=15, color=col,
                ha="left", va="center")
    ax.text(0.045, 0.5, "{", fontsize=50, color="#C00000",
            ha="center", va="center")
    path = f"{OUT}/{fname}"
    fig.savefig(path, dpi=EQ_DPI, transparent=True)
    plt.close(fig)
    im = Image.open(path)
    al = np.asarray(im)[:, :, 3]
    h_px, w_px = im.size[1], im.size[0]
    cond_x0 = int(0.30 * w_px)
    prof = (al[:, cond_x0:] > 10).sum(axis=1)
    bands = []
    cur = None
    for y in range(h_px):
        if prof[y] > 0:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur is not None:
            bands.append(cur)
            cur = None
    if cur is not None:
        bands.append(cur)
    line1_frac = round((bands[0][0] + bands[0][1]) / 2 / h_px, 4)
    line2_frac = round((bands[1][0] + bands[1][1]) / 2 / h_px, 4)
    return {"image": fname, "w_px": w_px, "h_px": h_px, "dpi": EQ_DPI,
            "w_in": round(w_px / EQ_DPI, 5), "h_in": round(h_px / EQ_DPI, 5),
            "line1_frac": line1_frac, "line2_frac": line2_frac}


charts = {
    "unipolar_step": step_chart("slide_018_unipolar_step.png", 0.0, 1.6),
    "bipolar_step": step_chart("slide_018_bipolar_step.png", -1.6, 1.6),
    "sigmoid": smooth_chart("slide_018_sigmoid.png", "sigmoid", (-4, 4),
                            (-0.10, 1.10), [0.0, 0.5, 1.0], ["0.0", "0.5", "1.0"],
                            annotate=True, legend=True, ylabel_side=True),
    "tanh": smooth_chart("slide_018_tanh.png", "tanh", (-4, 4), (-1.1, 1.1),
                         [-1.0, -0.5, 0.0, 0.5, 1.0],
                         ["-1.0", "-0.5", "0", "0.5", "1.0"],
                         internal="tanh", internal_pos="left"),
    "arctan": smooth_chart("slide_018_arctan.png", "arctan", (-4, 4),
                           (-1.65, 1.65),
                           [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5],
                           ["-1.5", "-1.0", "-0.5", "0", "0.5", "1.0", "1.5"],
                           internal="Inverse Tangent Graph", internal_pos="left"),
}
eqs = {
    "unipolar": piecewise([("0", "x<0"), ("1", "x>0")], "eq_018_unipolar.png"),
    "bipolar": piecewise([("-1", "x<0"), ("1", "x>0")], "eq_018_bipolar.png"),
}
manifest = {"charts": charts, "equations": eqs}
with open(f"{OUT}/gen_slide_018_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(json.dumps(manifest, indent=2))
