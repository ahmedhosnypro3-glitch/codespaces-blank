#!/usr/bin/env python3
"""Generate slide 018 assets: 5 charts + 2D piecewise equations.

Measured from unique_slides/slide_018.jpg (960x540):
  step panes  : blue-bordered white boxes (270x106 px), black arrowed axes,
                RED step curve, yellow saturation ellipses
  bottom charts: blue-bordered white panels (~255x150 px), gray grid, RED curves;
                sigmoid has green vertical guides + yellow tail highlights and an
                internal title; arctan panel carries an internal
                "Inverse Tangent Graph" title
  equations  : red curly brace spanning two lines, red "for x<0" case,
                green "for x>=0" case
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

RED = "#C0392B"
GREEN = "#2E8B57"
BLUE_BORDER = "#261F7F"
AXIS = "#333333"
GRID = "#CCCCCC"
YELLOW = "#F2E94E"
WHITE = "#FFFFFF"


def _save_trimmed(fig, path, pad=3):
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        plt.close(fig)
        return 0, 0
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad + 1, buf.shape[0])
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad + 1, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(path)
    w, h = x1 - x0, y1 - y0
    plt.close(fig)
    return int(w), int(h)


def _arrow(ax, x0, y0, x1, y1, color, lw=1.4, head=0.20, halfw=0.10):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle="butt", zorder=3)
    d = np.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    ax.fill([x1, x1 - head * ux + halfw * -uy, x1 - head * ux - halfw * -uy],
            [y1, y1 - head * uy + halfw * ux, y1 - head * uy - halfw * ux],
            color=color, lw=0, zorder=3)


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

    _arrow(ax, -3, 0, 2.85, 0, AXIS)
    _arrow(ax, -3, y_lo, -3, y_hi - 0.15, AXIS)
    ax.text(2.8, y_lo + (y_hi - y_lo) * 0.06, "x", fontsize=6.5, color=AXIS,
            ha="right", va="bottom")
    ax.text(-3.25, (y_lo + y_hi) / 2, "f(x)", fontsize=6.5, color=AXIS,
            ha="center", va="center", rotation=90)

    cases = (0, 1) if y_lo == 0 else (-1, 1)
    xs = np.linspace(-3, 3, 200)
    ys = np.where(xs < 0, cases[0], cases[1])
    ax.plot(xs, ys, color=RED, lw=2.0, zorder=4)
    ax.plot([0, 0], [cases[0], cases[1]], color=RED, lw=2.0, zorder=4)

    h = y_hi - y_lo
    for yv in cases:
        for xv in (-1.6, 1.6):
            ax.add_patch(plt.matplotlib.patches.Ellipse(
                (xv, yv), width=1.25, height=0.55 * h / 2.2,
                fill=False, edgecolor=YELLOW, linewidth=2.4, zorder=5))
    fig.savefig(f"{OUT}/{fname}", dpi=CHART_DPI, facecolor=WHITE,
                edgecolor=BLUE_BORDER)
    plt.close(fig)
    im = Image.open(f"{OUT}/{fname}")
    return {"image": fname, "w_px": im.size[0], "h_px": im.size[1],
            "dpi": CHART_DPI}


def smooth_chart(fname, kind, xlim, ylim, yticks, ylabels, internal=None,
                 annotate=False):
    w_in, h_in = 255 / 72, 150 / 72
    fig = plt.figure(figsize=(w_in, h_in), dpi=CHART_DPI)
    fig.patch.set_facecolor(WHITE)
    fig.patch.set_edgecolor(BLUE_BORDER)
    fig.patch.set_linewidth(2.0)
    ax = fig.add_axes([0.18, 0.16, 0.74, 0.66])
    ax.set_facecolor(WHITE)
    xs = np.linspace(xlim[0], xlim[1], 500)
    if kind == "sigmoid":
        ys = 1 / (1 + np.exp(-xs))
    elif kind == "tanh":
        ys = np.tanh(xs)
    else:
        ys = np.arctan(xs)
    ax.plot(xs, ys, color=RED, lw=2.0, zorder=4)
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
    ax.set_ylabel("f(x)", fontsize=6.5, color=AXIS, labelpad=1)
    if internal:
        ax.text(0.5, 0.98, internal, transform=ax.transAxes, fontsize=7,
                color=AXIS, ha="center", va="top")
    if annotate:
        for xv in (xlim[0], xlim[1]):
            ax.axvline(xv, color=GREEN, lw=1.0)
        for xv, yv in ((xlim[0] + 0.6, ylim[0] + 0.05),
                       (xlim[1] - 0.6, ylim[1] - 0.05)):
            ax.add_patch(plt.matplotlib.patches.Ellipse(
                (xv, yv), width=1.7, height=0.16, fill=False,
                edgecolor=YELLOW, linewidth=2.4, zorder=5))
    fig.savefig(f"{OUT}/{fname}", dpi=CHART_DPI, facecolor=WHITE,
                edgecolor=BLUE_BORDER)
    plt.close(fig)
    im = Image.open(f"{OUT}/{fname}")
    return {"image": fname, "w_px": im.size[0], "h_px": im.size[1],
            "dpi": CHART_DPI}


def piecewise(cases, fname, w_in, h_in, fs_val, fs_cond, fs_brace):
    """2D piecewise: red brace spanning all lines; red negative case, green x>=0."""
    fig = plt.figure(figsize=(w_in, h_in), dpi=EQ_DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    n = len(cases)
    tops = [0.80 - i * (0.60 / max(n - 1, 1)) for i in range(n)]
    for (val, cond), y, col in zip(cases, tops, (RED, GREEN)):
        ax.text(0.42, y, val, fontsize=fs_val, color=col, ha="right",
                va="center", fontweight="bold")
        ax.text(0.46, y, f"for {cond}", fontsize=fs_cond, color=col,
                ha="left", va="center")
    ax.text(0.12, (tops[0] + tops[-1]) / 2, "{", fontsize=fs_brace, color=RED,
            ha="center", va="center")
    w, h = _save_trimmed(fig, f"{OUT}/{fname}")
    return {"image": fname, "w_px": w, "h_px": h, "dpi": EQ_DPI,
            "w_in": round(w / EQ_DPI, 5), "h_in": round(h / EQ_DPI, 5)}


charts = {
    "unipolar_step": step_chart("slide_018_unipolar_step.png", 0.0, 1.6),
    "bipolar_step": step_chart("slide_018_bipolar_step.png", -1.6, 1.6),
    "sigmoid": smooth_chart("slide_018_sigmoid.png", "sigmoid", (-4, 4),
                            (-0.08, 1.08), [0.0, 0.5, 1.0],
                            ["0.0", "0.5", "1.0"],
                            internal="f(x) = Sigmoid(x)", annotate=True),
    "tanh": smooth_chart("slide_018_tanh.png", "tanh", (-4, 4), (-1.1, 1.1),
                         [-1.0, -0.5, 0.0, 0.5, 1.0],
                         ["-1.0", "-0.5", "0", "0.5", "1.0"]),
    "arctan": smooth_chart("slide_018_arctan.png", "arctan", (-4, 4),
                           (-1.65, 1.65), [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5],
                           ["-1.5", "-1.0", "-0.5", "0", "0.5", "1.0", "1.5"],
                           internal="Inverse Tangent Graph"),
}
eqs = {
    "unipolar": piecewise([("0", "x<0"), ("1", "x>=0")], "eq_018_unipolar.png",
                          1.30, 0.40, 8, 6.5, 24),
    "bipolar": piecewise([("-1", "x<0"), ("1", "x>=0")], "eq_018_bipolar.png",
                         1.30, 0.40, 8, 6.5, 24),
}
manifest = {"charts": charts, "equations": eqs}
with open(f"{OUT}/gen_slide_018_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(json.dumps(manifest, indent=2))
