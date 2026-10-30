#!/usr/bin/env python3
"""Slide 019 — Activation function plots (sigmoid, tanh, tan, arctan) generator.

Decision (lib / function / algorithm / data) per the graphgen protocol:
  lib      : numpy + matplotlib (Agg)
  function : matplotlib.axes.Axes.plot for 4 canonical activation functions
  algorithm: standard activation functions (sigmoid = 1/(1+e^-x), tanh, tan, arctan)
  data     : computed function values on the domains shown by the original slide

Geometry is PIL-MEASURED from the original frame
(videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg,
960x540, 1px = 1pt = 1/72in) — see the measured values below.

Measured panel borders (blue #0000CC, 1.5pt):
  TL (sigmoid)   x 105..410  y  59..237
  TR (tanh)      x 499..804  y  59..237
  BL (tan)       x 105..410  y 297..475
  BR (arctan)    x 499..804  y 297..475
Measured caption boxes:
  sigmoid peach  x 142..380  y 243..292
  tanh    peach  x 530..768  y 243..292
  arctan  peach  x 577..693  y 484..512
  tan     gray   x 169..320  y 484..512
Measured badge (yellow #FFFF99): x 859..893, y 56..85
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = "/home/codespace/ai_llm_slides"
VIDEO = "videos/machine-learning/09_introduction_to_neural_networks"
OUTDIR = os.path.join(ROOT, VIDEO, "recreated_pptx", "build", "graphs_slide_019")
os.makedirs(OUTDIR, exist_ok=True)

DPI = 300  # render at 300dpi for clean embedding

RED_CURVE = "#E06666"
BLUE_BORDER = "#0000CC"
GRAY_GRID = "#BFBFBF"
GRAY_GRID_TAN = "#A6A6A6"
DARK_AXES = "#404040"
PANEL_BG = "#D9D9D9"

PANELS = {
    "sigmoid": {"x0": 105, "y0": 59, "x1": 410, "y1": 237},
    "tanh":    {"x0": 499, "y0": 59, "x1": 804, "y1": 237},
    "tan":     {"x0": 105, "y0": 297, "x1": 410, "y1": 475},
    "arctan":  {"x0": 499, "y0": 297, "x1": 804, "y1": 475},
}

# Axis specs (verbatim tick labels from the vision analysis)
SIGMOID_X, SIGMOID_Y = (-8, 8), (0.0, 1.0)
SIGMOID_XTICKS = [-8, -6, -4, -2, 2, 4, 6, 8]
SIGMOID_YTICKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
SIGMOID_YLABEL = "sig(x)"
SIGMOID_LEGEND = "sig(x) = 1/(1+e^-x)"

TANH_X, TANH_Y = (-5, 5), (-1.0, 1.0)
TANH_XTICKS = [-4, -2, 2, 4]
TANH_YTICKS = [-1.0, -0.5, 0, 0.5, 1.0]
TANH_YLABEL = "tanh x"

TAN_X, TAN_Y = (-2 * np.pi, 2 * np.pi), (-4, 4)
TAN_XTICKS = [-2 * np.pi, -3 * np.pi / 2, -np.pi, -np.pi / 2, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
TAN_XTICK_LABELS = [r"$-2\pi$", r"$-3\pi/2$", r"$-\pi$", r"$-\pi/2$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"]
TAN_YTICKS = [4, 2, -2, -4]
TAN_YLABEL = "tan x"
TAN_ASYMPTOTES = [-3 * np.pi / 2, -np.pi / 2, np.pi / 2, 3 * np.pi / 2]

ARCTAN_X, ARCTAN_Y = (-3, 3), (-1, 1)
ARCTAN_XTICKS = [-3, -2, -1, 1, 2, 3]
ARCTAN_YTICKS = [1, -1]
ARCTAN_TITLE = "Inverse Tangent Graph"


def _axes_frame(w_px, h_px, xlim, ylim, x0, x1):
    """Map data coords to panel-local pixel coords (y flipped: 0 = top)."""
    def fx(v):
        return (v - xlim[0]) / (xlim[1] - xlim[0]) * w_px

    def fy(v):
        return (1 - (v - ylim[0]) / (ylim[1] - ylim[0])) * h_px

    return fx, fy


def _frame(ax, w_px, h_px, border=BLUE_BORDER, bg=PANEL_BG):
    ax.add_patch(Rectangle((0, 0), w_px, h_px, facecolor=bg, edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0.75, 0.75), w_px - 1.5, h_px - 1.5, fill=False,
                           edgecolor=border, linewidth=1.5, zorder=9))


def _axes(ax, w_px, h_px, fx, fy, xlim, ylim, xticks, yticks,
          xlabels=None, ylabels=None, grid=GRAY_GRID, tick_fs=4.2):
    """Draw gridlines, L-axes, tick labels."""
    for xt in xticks:
        xp = fx(xt)
        ax.plot([xp, xp], [0, h_px], color=grid, lw=0.4, zorder=1)
    for yt in yticks:
        yp = fy(yt)
        ax.plot([0, w_px], [yp, yp], color=grid, lw=0.4, zorder=1)

    # horizontal axis at y = ylim[0], vertical axis at x = xlim[0]
    ax.plot([0, w_px], [fy(ylim[0]), fy(ylim[0])], color=DARK_AXES, lw=1.0, zorder=3)
    ax.plot([fx(xlim[0]), fx(xlim[0])], [0, h_px], color=DARK_AXES, lw=1.0, zorder=3)

    # x tick labels below the horizontal axis
    for i, xt in enumerate(xticks):
        label = xlabels[i] if xlabels else f"{xt:g}"
        ax.text(fx(xt), h_px - 1, label, fontsize=tick_fs, color=DARK_AXES,
                ha="center", va="bottom", zorder=6)
    # y tick labels left of the vertical axis
    for i, yt in enumerate(yticks):
        label = ylabels[i] if ylabels else f"{yt:g}"
        ax.text(fx(xlim[0]) - 1, fy(yt), label, fontsize=tick_fs, color=DARK_AXES,
                ha="right", va="center", zorder=6)


def render_panel(key, spec, out_png):
    x0, y0, x1, y1 = spec["x0"], spec["y0"], spec["x1"], spec["y1"]
    w_px, h_px = x1 - x0, y1 - y0
    w_in, h_in = w_px / 72.0, h_px / 72.0

    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_px)
    ax.set_ylim(h_px, 0)
    ax.axis("off")
    _frame(ax, w_px, h_px)

    if key == "sigmoid":
        fx, fy = _axes_frame(w_px, h_px, SIGMOID_X, SIGMOID_Y, x0, x1)
        xd = np.linspace(*SIGMOID_X, 400)
        yd = 1 / (1 + np.exp(-xd))
        _axes(ax, w_px, h_px, fx, fy, SIGMOID_X, SIGMOID_Y, SIGMOID_XTICKS, SIGMOID_YTICKS)
        ax.plot(fx(xd), fy(yd), color=RED_CURVE, lw=1.4, zorder=4, solid_capstyle="round")
        # y-axis title at the top of the vertical axis
        ax.text(fx(SIGMOID_X[0]) + 2, 2, SIGMOID_YLABEL, fontsize=5.2, color=DARK_AXES,
                ha="left", va="bottom", zorder=6)
        # legend: red line swatch + label, upper-left inside the plot area
        ax.plot([14, 26], [14, 14], color=RED_CURVE, lw=1.4, zorder=7)
        ax.text(28, 14, SIGMOID_LEGEND, fontsize=5.0, color=RED_CURVE,
                ha="left", va="center", zorder=7)

    elif key == "tanh":
        fx, fy = _axes_frame(w_px, h_px, TANH_X, TANH_Y, x0, x1)
        xd = np.linspace(*TANH_X, 400)
        yd = np.tanh(xd)
        _axes(ax, w_px, h_px, fx, fy, TANH_X, TANH_Y, TANH_XTICKS, TANH_YTICKS)
        ax.plot(fx(xd), fy(yd), color=RED_CURVE, lw=1.4, zorder=4, solid_capstyle="round")
        ax.text(fx(TANH_X[0]) + 2, 2, TANH_YLABEL, fontsize=5.2, color=DARK_AXES,
                ha="left", va="bottom", zorder=6)

    elif key == "tan":
        fx, fy = _axes_frame(w_px, h_px, TAN_X, TAN_Y, x0, x1)
        _axes(ax, w_px, h_px, fx, fy, TAN_X, TAN_Y, TAN_XTICKS, TAN_YTICKS,
              xlabels=TAN_XTICK_LABELS, grid=GRAY_GRID_TAN)
        # four dashed red asymptotes
        for asym in TAN_ASYMPTOTES:
            xp = fx(asym)
            ax.plot([xp, xp], [0, h_px], color=RED_CURVE, lw=0.9, ls="--", zorder=2)
        # tangent branches (light gray), clipped to the plot window
        xd = np.linspace(*TAN_X, 3000)
        yd = np.tan(xd)
        keep = np.abs(yd) <= TAN_Y[1]
        for xs, ys in _split_branches(xd, yd, keep):
            ax.plot(fx(xs), fy(ys), color=GRAY_GRID_TAN, lw=0.9, zorder=3, solid_capstyle="round")
        ax.text(fx(TAN_X[0]) + 2, 2, TAN_YLABEL, fontsize=5.2, color=DARK_AXES,
                ha="left", va="bottom", zorder=6)

    elif key == "arctan":
        fx, fy = _axes_frame(w_px, h_px, ARCTAN_X, ARCTAN_Y, x0, x1)
        xd = np.linspace(*ARCTAN_X, 400)
        yd = np.arctan(xd)
        _axes(ax, w_px, h_px, fx, fy, ARCTAN_X, ARCTAN_Y, ARCTAN_XTICKS, ARCTAN_YTICKS)
        ax.plot(fx(xd), fy(yd), color=RED_CURVE, lw=1.4, zorder=4, solid_capstyle="round")
        ax.plot([fx(0)], [fy(0)], "o", ms=3.2, mfc="white", mec=RED_CURVE, mew=1.0,
                ls="none", zorder=5)
        ax.text(6, 8, ARCTAN_TITLE, fontsize=5.2, color=DARK_AXES,
                ha="left", va="top", zorder=6)

    fig.savefig(out_png, dpi=DPI, facecolor=PANEL_BG)
    plt.close(fig)
    return out_png


def _split_branches(xd, yd, keep):
    """Split a clipped tangent curve into contiguous branches."""
    idx = np.nonzero(keep)[0]
    if not len(idx):
        return []
    breaks = np.nonzero(np.diff(idx) > 1)[0]
    starts = [0] + (breaks + 1).tolist()
    ends = (breaks + 1).tolist() + [len(idx)]
    return [(xd[idx[s:e]], yd[idx[s:e]]) for s, e in zip(starts, ends) if e - s > 1]


def main():
    facts = {"panels": PANELS, "dpi": DPI}
    for key, spec in PANELS.items():
        out_png = os.path.join(OUTDIR, f"graph_{key}.png")
        render_panel(key, spec, out_png)
        facts[key] = {"png": out_png, "w_px": spec["x1"] - spec["x0"], "h_px": spec["y1"] - spec["y0"]}
        print(f"Rendered {key} -> {out_png}")

    facts_path = os.path.join(OUTDIR, "graphgen_facts.json")
    with open(facts_path, "w") as f:
        json.dump(facts, f, indent=2, default=str)
    print(f"Facts saved to {facts_path}")


if __name__ == "__main__":
    main()
