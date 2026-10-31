#!/usr/bin/env python3
"""Slide 019 - activation-function plot panels (sigmoid, tanh, tan, arctan), PIL-matched.

Palette/geometry are PIL-MEASURED from unique_slides/slide_019.jpg:
  panel border core #20197D (2.5 px), interior near-white #FEFFFD
  gridlines        #D3D5D2 light gray, faint dashed
  curves           rose #B86A80 (core #A95F73)
  tan branches    warm taupe #CFC5C5
v1 used #0000CC borders / #D9D9D9 interiors / #E06666 curves; corrected here.
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

ROSE = "#B86A80"
ROSE_DARK = "#A95F73"
TAUPE = "#CFC5C5"
BORDER = "#20197D"
GRID = "#D3D5D2"
INK = "#333333"
PANEL_BG = "#FEFFFD"
AXIS = "#8C8C8C"

PANELS = {
    "sigmoid": (105, 59, 410, 237),
    "tanh":    (499, 59, 804, 237),
    "tan":     (105, 297, 410, 475),
    "arctan":  (499, 297, 804, 475),
}

SIGMOID_XTICKS = [-8, -6, -4, -2, 2, 4, 6, 8]
SIGMOID_YTICKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
TANH_XTICKS = [-4, -2, 2, 4]
TANH_YTICKS = [-1.0, -0.5, 0, 0.5, 1.0]
TAN_XTICKS = [-2 * np.pi, -3 * np.pi / 2, -np.pi, -np.pi / 2, np.pi / 2, np.pi,
              3 * np.pi / 2, 2 * np.pi]
TAN_XLABELS = [r"$-2\pi$", r"$-\frac{3\pi}{2}$", r"$-\pi$", r"$-\frac{\pi}{2}$",
               r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
TAN_YTICKS = [4, 2, -2, -4]
TAN_ASYMPTOTES = [-3 * np.pi / 2, -np.pi / 2, np.pi / 2, 3 * np.pi / 2]
ARCTAN_XTICKS = [-3, -2, -1, 1, 2, 3]
ARCTAN_YTICKS = [1, -1]


def panel_size(key):
    x0, y0, x1, y1 = PANELS[key]
    return x1 - x0, y1 - y0


def axes_frame(w, h, xlim, ylim):
    """Map data coords to panel-local px coords, y inverted (0 = top)."""
    def fx(v):
        return (v - xlim[0]) / (xlim[1] - xlim[0]) * w
    def fy(v):
        return (1 - (v - ylim[0]) / (ylim[1] - ylim[0])) * h
    return fx, fy


def setup(w, h):
    fig = plt.figure(figsize=(w / 72.0, h / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), w, h, facecolor=PANEL_BG, edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0.85, 0.85), w - 1.7, h - 1.7, fill=False,
                           edgecolor=BORDER, linewidth=1.7, zorder=9))
    return fig, ax


def grid_and_axes(ax, w, h, fx, fy, xlim, ylim, xticks, yticks,
                  xlabels=None, tick_fs=6.4):
    for xt in xticks:
        xp = fx(xt)
        ax.plot([xp, xp], [4, h - 4], color=GRID, lw=0.6, ls=(0, (4, 3)), zorder=1)
    for yt in yticks:
        yp = fy(yt)
        ax.plot([4, w - 4], [yp, yp], color=GRID, lw=0.6, ls=(0, (4, 3)), zorder=1)

    ax.plot([4, w - 4], [fy(ylim[0]), fy(ylim[0])], color=AXIS, lw=1.0, zorder=3)
    ax.plot([fx(xlim[0]), fx(xlim[0])], [4, h - 4], color=AXIS, lw=1.0, zorder=3)

    for i, xt in enumerate(xticks):
        label = xlabels[i] if xlabels else f"{xt:g}"
        ax.text(fx(xt), h - 5, label, fontsize=tick_fs, color=INK, ha="center",
                va="bottom", zorder=6, math_fontfamily="dejavusans")
    for i, yt in enumerate(yticks):
        ax.text(fx(xlim[0]) - 4, fy(yt), f"{yt:g}", fontsize=tick_fs, color=INK,
                ha="right", va="center", zorder=6)


def render_sigmoid(w, h):
    fig, ax = setup(w, h)
    fx, fy = axes_frame(w, h, (-8, 8), (0.0, 1.0))
    grid_and_axes(ax, w, h, fx, fy, (-8, 8), (0.0, 1.0), SIGMOID_XTICKS, SIGMOID_YTICKS)
    xd = np.linspace(-8, 8, 600)
    ax.plot(fx(xd), fy(1 / (1 + np.exp(-xd))), color=ROSE, lw=1.5, zorder=4,
            solid_capstyle="round")
    ax.plot([16, 30], [16, 16], color=ROSE, lw=1.5, zorder=7)
    ax.text(33, 16, r"$\sigma(z) = 1/(1+e^{-z})$", fontsize=6.0, color=ROSE_DARK,
            ha="left", va="center", zorder=7, math_fontfamily="dejavusans")
    ax.text(fx(-8) + 6, 4, r"$\sigma(z)=1$", fontsize=6.0, color=INK, ha="left",
            va="top", zorder=6, math_fontfamily="dejavusans")
    return fig


def render_tanh(w, h):
    fig, ax = setup(w, h)
    fx, fy = axes_frame(w, h, (-5, 5), (-1.0, 1.0))
    grid_and_axes(ax, w, h, fx, fy, (-5, 5), (-1.0, 1.0), TANH_XTICKS, TANH_YTICKS)
    xd = np.linspace(-5, 5, 600)
    ax.plot(fx(xd), fy(np.tanh(xd)), color=ROSE, lw=1.5, zorder=4, solid_capstyle="round")
    ax.text(fx(-5) + 6, 4, "tanh x", fontsize=8.0, color=INK, ha="left", va="top", zorder=6)
    return fig


def render_tan(w, h):
    fig, ax = setup(w, h)
    fx, fy = axes_frame(w, h, (-2 * np.pi, 2 * np.pi), (-4, 4))
    grid_and_axes(ax, w, h, fx, fy, (-2 * np.pi, 2 * np.pi), (-4, 4),
                  TAN_XTICKS, TAN_YTICKS, xlabels=TAN_XLABELS, tick_fs=6.4)
    for asym in TAN_ASYMPTOTES:
        xp = fx(asym)
        ax.plot([xp, xp], [4, h - 4], color=ROSE, lw=1.0, ls=(0, (5, 4)), zorder=2)
    xd = np.linspace(-2 * np.pi, 2 * np.pi, 4000)
    yd = np.tan(xd)
    keep = np.abs(yd) <= 4
    idx = np.nonzero(keep)[0]
    breaks = np.nonzero(np.diff(idx) > 1)[0]
    starts = [0] + (breaks + 1).tolist()
    ends = (breaks + 1).tolist() + [len(idx)]
    for s, e in zip(starts, ends):
        if e - s > 1:
            ax.plot(fx(xd[idx[s:e]]), fy(yd[idx[s:e]]), color=TAUPE, lw=1.0,
                    zorder=3, solid_capstyle="round")
    ax.text(fx(-2 * np.pi) + 6, 4, "tan x", fontsize=8.0, color=INK, ha="left",
            va="top", zorder=6)
    return fig


def render_arctan(w, h):
    fig, ax = setup(w, h)
    fx, fy = axes_frame(w, h, (-3, 3), (-1, 1))
    grid_and_axes(ax, w, h, fx, fy, (-3, 3), (-1, 1), ARCTAN_XTICKS, ARCTAN_YTICKS)
    xd = np.linspace(-3, 3, 600)
    ax.plot(fx(xd), fy(np.arctan(xd)), color=ROSE, lw=1.5, zorder=4, solid_capstyle="round")
    ax.plot([fx(0)], [fy(0)], "o", ms=3.4, mfc="white", mec=ROSE_DARK, mew=1.0,
            ls="none", zorder=5)
    ax.text(8, 10, "Inverse Tangent Graph", fontsize=6.6, color=INK, ha="left",
            va="top", zorder=6)
    return fig


RENDERERS = {
    "sigmoid": render_sigmoid,
    "tanh": render_tanh,
    "tan": render_tan,
    "arctan": render_arctan,
}


def main():
    for key, fn in RENDERERS.items():
        w, h = panel_size(key)
        fig = fn(w, h)
        out = os.path.join(OUTDIR, f"graph_{key}.png")
        fig.savefig(out, dpi=DPI, facecolor=PANEL_BG)
        plt.close(fig)
        print(f"rendered {key}: {w}x{h}px -> {out}")


if __name__ == "__main__":
    main()
