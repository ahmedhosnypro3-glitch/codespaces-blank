#!/usr/bin/env python3
"""Generate slide 025 graphs: Linear, Unipolar Unit Step, Bipolar Unit Step.

Geometry follows measurements taken from unique_slides/slide_025.jpg (960x540):
  - each plot is a blue-bordered box
  - black axes with arrowheads at the positive ends
  - no numeric tick labels, only the text labels f(x) and x
  - red curves; the step functions are flat on the x-axis left of the y-axis,
    jump vertically at the y-axis, then stay flat to the right
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUTDIR = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
          "09_introduction_to_neural_networks/recreated_pptx/build")
os.makedirs(OUTDIR, exist_ok=True)

RED = "#ff0000"
BLUE_BORDER = "#0000ff"
WHITE_BG = "#ffffff"
AXIS = "#000000"


def style_axes(ax, xlim, ylim, arrow_frac=0.045):
    """Black axes with arrowheads at the positive ends; no tick labels."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    x0, x1 = xlim
    y0, y1 = ylim
    dx = arrow_frac * (x1 - x0)
    dy = arrow_frac * (y1 - y0)

    # x-axis: from left edge to right edge, arrowhead at the right
    ax.annotate("", xy=(x1, y0), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=AXIS, linewidth=1.4,
                                mutation_scale=14, shrinkA=0, shrinkB=0))
    # y-axis: from bottom edge to top edge, arrowhead at the top
    ax.annotate("", xy=(x0, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=AXIS, linewidth=1.4,
                                mutation_scale=14, shrinkA=0, shrinkB=0))

    ax.text(x1 - dx * 0.55, y0 - dy * 0.30, "x", fontsize=11, color=AXIS,
            ha="center", va="top")
    ax.text(x0 - dx * 0.20, y1 - dy * 0.35, "f(x)", fontsize=11, color=AXIS,
            ha="center", va="bottom")


def finish(fig, ax, path):
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(BLUE_BORDER)
        spine.set_linewidth(1.6)
    ax.set_facecolor(WHITE_BG)
    fig.patch.set_facecolor(WHITE_BG)
    plt.tight_layout(pad=0.12)
    plt.savefig(path, dpi=200, facecolor=WHITE_BG, edgecolor="none")
    plt.close(fig)


def plot_linear(path):
    fig, ax = plt.subplots(figsize=(3.0, 1.95), dpi=200)
    x = np.linspace(-3, 3, 400)
    ax.plot(x, x, color=RED, linewidth=2.0, solid_capstyle="round")
    style_axes(ax, (-3.0, 3.0), (-3.0, 3.0))
    finish(fig, ax, path)


def plot_step(path, low, high):
    fig, ax = plt.subplots(figsize=(3.0, 1.95), dpi=200)
    x = np.linspace(-3, 3, 800)
    y = np.where(x < 0, low, high)
    ax.plot(x, y, color=RED, linewidth=2.0, solid_capstyle="round")
    ax.plot([0, 0], [low, high], color=RED, linewidth=2.0)
    style_axes(ax, (-3.0, 3.0), (-1.5, 1.5))
    finish(fig, ax, path)


if __name__ == "__main__":
    plot_linear(f"{OUTDIR}/slide_025_linear.png")
    plot_step(f"{OUTDIR}/slide_025_unipolar_step.png", 0.0, 1.0)
    plot_step(f"{OUTDIR}/slide_025_bipolar_step.png", -1.0, 1.0)
    print("Generated slide_025 graphs")
