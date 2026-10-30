#!/usr/bin/env python3
"""Slide 053 — dense red band top-center + dense blue vertical U-shape.

Decision:
  lib      : matplotlib + numpy
  algorithm: high-density scatter on band + U-shape curves
  data     : generated to match original's dense filled regions
  plot     : very dense red band (y 25-31) + dense blue U columns
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IMG_X0, IMG_Y0, IMG_W, IMG_H = 40, 30, 700, 500
AXBOX = (100, 80, 640, 480)
XLIM = (-5, 20)
YLIM = (0, 35)
XTICKS = [-5, 0, 5, 10, 15, 20]
YTICKS = [0, 5, 10, 15, 20, 25, 30, 35]
DPI = 300

RNG = np.random.RandomState(17)


def red_band(n=800, jitter=0.4):
    """Dense red band at top-center: x -2..12, y 25-31."""
    xs = RNG.uniform(-2, 12, n)
    ys = RNG.uniform(25, 31, n)
    return xs, ys


def blue_ushape(n=800, jitter=0.3):
    """Dense blue vertical U: two columns at x≈-2 and x≈12, y 12-26, connected at bottom."""
    # left column
    n2 = n // 2
    xl = RNG.normal(-2, jitter, n2)
    yl = RNG.uniform(12, 26, n2)
    # right column
    xr = RNG.normal(12, jitter, n2)
    yr = RNG.uniform(12, 26, n2)
    # bottom connection
    xb = RNG.uniform(-2, 12, n // 4)
    yb = RNG.normal(12, jitter, n // 4)
    return np.concatenate([xl, xr, xb]), np.concatenate([yl, yr, yb])


def build_figure(out):
    fig = plt.figure(figsize=(IMG_W / 72.0, IMG_H / 72.0), dpi=DPI)
    fig.patch.set_facecolor("white")
    l, t, r, b = AXBOX
    ax = fig.add_axes([(l - IMG_X0) / IMG_W, (IMG_H - (b - IMG_Y0)) / IMG_H,
                       (r - l) / IMG_W, (b - t) / IMG_H])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_facecolor("white")

    rx, ry = red_band()
    bx, by = blue_ushape()
    ax.scatter(rx, ry, s=6, c="#FF0000", linewidths=0, alpha=0.7, zorder=2)
    ax.scatter(bx, by, s=6, c="#0000FF", linewidths=0, alpha=0.7, zorder=2)

    ax.set_xticks(XTICKS)
    ax.set_yticks(YTICKS)
    ax.tick_params(length=3.5, width=1.0, labelsize=13, colors="black")
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color("black")
    ax.grid(True, linestyle=":", linewidth=0.5, color="#CCCCCC", alpha=0.5)
    fig.savefig(out, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    build_figure(args.out)