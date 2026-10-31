#!/usr/bin/env python3
"""Slide 019 - activation-function plot panels v3 (PIL-measured plot interiors).

v2 mapped the data range onto the whole panel, so the axes sat on the panel
border and the y-tick labels were placed at x=-4 (outside the canvas).
v3 uses each panel's measured data rect, so the axes, tick labels, axis
titles, legend and asymptotes land where the original has them.

Measured anchors (original frame 960x540, panel-relative px, panel 305x178):
  sigmoid  data rect x 30..230, y 22..133   axes x=130, y=133
  tanh     data rect x 26..268, y 18..166   axes x=147, y= 92
  tan      data rect x 22..245, y 30..176   axes x=133.5, y=103
  arctan   data rect x 27..281, y 12..160   axes x=154, y= 86
"""
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

DPI = 300
W, H = 305, 178

ROSE = "#B86A80"
ROSE_DARK = "#A95F73"
ASYM = "#E24B4B"
TAUPE = "#CFC5C5"
BORDER = "#20197D"
GRID = "#D3D5D2"
INK = "#333333"
BLACK = "#111111"
PANEL_BG = "#FEFFFD"
AXIS = "#8C8C8C"

TICK_FS = 7.0

PANELS = {
    "sigmoid": dict(rect=(30, 22, 230, 133), xlim=(-8, 8), ylim=(0.0, 1.0),
                    xticks=[-8, -6, -4, -2, 2, 4, 6, 8],
                    yticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                    xlabels=None, ylabels=None),
    "tanh": dict(rect=(26, 18, 268, 166), xlim=(-5, 5), ylim=(-1.0, 1.0),
                 xticks=[-4, -2, 2, 4], yticks=[-1.0, -0.5, 0, 0.5, 1.0],
                 xlabels=None, ylabels=None),
    "tan": dict(rect=(22, 30, 245, 176), xlim=(-2 * np.pi, 2 * np.pi), ylim=(-4, 4),
                xticks=[-2 * np.pi, -3 * np.pi / 2, -np.pi, -np.pi / 2,
                        np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
                yticks=[4, 2, -2, -4],
                xlabels=[r"$-2\pi$", r"$-\frac{3\pi}{2}$", r"$-\pi$",
                         r"$-\frac{\pi}{2}$", r"$\frac{\pi}{2}$", r"$\pi$",
                         r"$\frac{3\pi}{2}$", r"$2\pi$"],
                ylabels=None, stacked={1, 3, 4, 6}),
    "arctan": dict(rect=(27, 12, 281, 160), xlim=(-3, 3), ylim=(-1, 1),
                   xticks=[-3, -2, -1, 1, 2, 3], yticks=[1, 0, -1],
                   xlabels=None, ylabels=None),
}


def setup():
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, facecolor=PANEL_BG, edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((1.0, 1.0), W - 2.0, H - 2.0, fill=False,
                           edgecolor=BORDER, linewidth=2.0, zorder=9))
    return fig, ax


def mapper(spec):
    x0, y0, x1, y1 = spec["rect"]
    xlim, ylim = spec["xlim"], spec["ylim"]

    def fx(v):
        return x0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * (x1 - x0)

    def fy(v):
        return y1 - (v - ylim[0]) / (ylim[1] - ylim[0]) * (y1 - y0)

    return fx, fy


def arrow_line(ax, x0, y0, x1, y1, color=AXIS, lw=1.0, head=5.0, zorder=4):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle="butt", zorder=zorder)
    dx, dy = x1 - x0, y1 - y0
    n = (dx * dx + dy * dy) ** 0.5
    if n < 1e-6:
        return
    ux, uy = dx / n, dy / n
    for sgn in (1, -1):
        ax.plot([x1 - ux * head * 0.9 - uy * head * 0.45 * sgn,
                 x1 - ux * head * 0.9 + uy * head * 0.45 * sgn],
                [y1 - uy * head * 0.9 + ux * head * 0.45 * sgn,
                 y1 - uy * head * 0.9 - ux * head * 0.45 * sgn],
                color=color, lw=lw, solid_capstyle="butt", zorder=zorder)


def draw_scaffold(ax, spec, fx, fy, x_end=None):
    x0, y0, x1, y1 = spec["rect"]
    ax_x = fx(0.0)
    ax_y = fy(0.0)

    for xt in spec["xticks"]:
        ax.plot([fx(xt), fx(xt)], [y0, y1], color=GRID, lw=0.6, ls=(0, (4, 3)), zorder=1)
    for yt in spec["yticks"]:
        ax.plot([x0, x1], [fy(yt), fy(yt)], color=GRID, lw=0.6, ls=(0, (4, 3)), zorder=1)

    right = x_end if x_end is not None else x1
    arrow_line(ax, x0, ax_y, right, ax_y)
    arrow_line(ax, ax_x, y1, ax_x, y0 - 4)

    stacked = spec.get("stacked", set())
    for i, xt in enumerate(spec["xticks"]):
        label = spec["xlabels"][i] if spec["xlabels"] else f"{xt:g}"
        if i in stacked:
            ax.text(fx(xt), ax_y + 1, label, fontsize=TICK_FS, color=INK,
                    ha="center", va="center", zorder=6, math_fontfamily="dejavusans")
        else:
            ax.text(fx(xt), ax_y + 3.5, label, fontsize=TICK_FS, color=INK,
                    ha="center", va="top", zorder=6, math_fontfamily="dejavusans")
    for yt in spec["yticks"]:
        lab = f"{yt:g}" if spec["ylabels"] is None else spec["ylabels"][yt]
        ax.text(ax_x - 5, fy(yt), lab, fontsize=TICK_FS, color=INK,
                ha="right", va="center", zorder=6, math_fontfamily="dejavusans")

    ax.text(right + 2.5, ax_y + 1, "x", fontsize=TICK_FS, color=INK,
            ha="left", va="center", zorder=6)
    return ax_x, ax_y


def render_sigmoid():
    spec = PANELS["sigmoid"]
    fig, ax = setup()
    fx, fy = mapper(spec)
    draw_scaffold(ax, spec, fx, fy)
    xd = np.linspace(-8, 8, 600)
    ax.plot(fx(xd), fy(1 / (1 + np.exp(-xd))), color=ROSE, lw=1.6, zorder=4,
            solid_capstyle="round")
    # legend box with rose line swatch (original legend at rel x 11..68, y 15..27)
    ax.add_patch(Rectangle((11, 15), 57, 12, facecolor=PANEL_BG, edgecolor=AXIS,
                           linewidth=0.7, zorder=7))
    ax.plot([14, 27], [21, 21], color=ROSE, lw=1.4, zorder=8)
    ax.text(29.5, 21, r"$\sigma(z) = 1/(1+e^{-z})$", fontsize=6.4, color=INK,
            ha="left", va="center", zorder=8, math_fontfamily="dejavusans")
    # axis note above the y-axis (original ink at rel x 129..148, y 15..23)
    ax.text(133, 15, r"$\sigma(z)=1$", fontsize=6.4, color=INK, ha="left",
            va="top", zorder=6, math_fontfamily="dejavusans")
    return fig


def render_tanh():
    spec = PANELS["tanh"]
    fig, ax = setup()
    fx, fy = mapper(spec)
    ax_x, _ = draw_scaffold(ax, spec, fx, fy)
    xd = np.linspace(-5, 5, 600)
    ax.plot(fx(xd), fy(np.tanh(xd)), color=ROSE, lw=1.6, zorder=4, solid_capstyle="round")
    # horizontal axis title above the y-axis (original ink rel x 144..155, y 8..10)
    ax.text(ax_x, 7, "tanh x", fontsize=9.0, color=INK, ha="center", va="top", zorder=8)
    return fig


def render_tan():
    spec = PANELS["tan"]
    fig, ax = setup()
    fx, fy = mapper(spec)
    ax_x, _ = draw_scaffold(ax, spec, fx, fy, x_end=279)
    # four rose dashed vertical asymptotes (data x = +-pi/2, +-3pi/2)
    for asym in (-3 * np.pi / 2, -np.pi / 2, np.pi / 2, 3 * np.pi / 2):
        xp = fx(asym)
        ax.plot([xp, xp], [30, 176], color=ASYM, lw=1.4, ls=(0, (5, 3)), zorder=2)
    xd = np.linspace(-2 * np.pi, 2 * np.pi, 4000)
    yd = np.tan(xd)
    keep = np.abs(yd) <= 4
    idx = np.nonzero(keep)[0]
    breaks = np.nonzero(np.diff(idx) > 1)[0]
    starts = [0] + (breaks + 1).tolist()
    ends = (breaks + 1).tolist() + [len(idx)]
    for s, e in zip(starts, ends):
        if e - s > 1:
            ax.plot(fx(xd[idx[s:e]]), fy(yd[idx[s:e]]), color=TAUPE, lw=1.1,
                    zorder=3, solid_capstyle="round")
    # horizontal axis title above the y-axis (original ink rel x 139..144, y 7..11)
    ax.text(ax_x + 7, 7, "tan x", fontsize=9.5, color=INK, ha="center", va="top", zorder=8)
    return fig


def render_arctan():
    spec = PANELS["arctan"]
    fig, ax = setup()
    fx, fy = mapper(spec)
    draw_scaffold(ax, spec, fx, fy)
    xd = np.linspace(-3, 3, 600)
    ax.plot(fx(xd), fy(np.arctan(xd)), color=ROSE, lw=1.6, zorder=4, solid_capstyle="round")
    ax.plot([fx(0)], [fy(0)], "o", ms=3.4, mfc="white", mec=ROSE_DARK, mew=1.0,
            ls="none", zorder=5)
    # in-panel title: original ink x 530..639, y 309..318 -> rel x 31..140, y 12..21
    ax.text(31, 12, "Inverse Tangent Graph", fontsize=11.0, color=BLACK,
            ha="left", va="top", zorder=8)
    return fig


RENDERERS = {
    "sigmoid": render_sigmoid,
    "tanh": render_tanh,
    "tan": render_tan,
    "arctan": render_arctan,
}


def main():
    for key, fn in RENDERERS.items():
        fig = fn()
        out = os.path.join(OUTDIR, f"graph_{key}.png")
        fig.savefig(out, dpi=DPI, facecolor=PANEL_BG)
        plt.close(fig)
        print(f"rendered {key} -> {out}")


if __name__ == "__main__":
    main()
