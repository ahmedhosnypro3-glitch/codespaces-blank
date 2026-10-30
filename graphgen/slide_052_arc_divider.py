#!/usr/bin/env python3
"""Slide 052 — red center/inner + blue outer U-shape + vertical black line at x=0.

Decision:
  lib      : matplotlib + numpy
  algorithm: U-shaped non-linearly-separable topology (blue surrounds red on bottom/sides)
  data     : generated matching original's specific point distribution
  plot     : red dense cluster in center, blue U-shape wrapping around bottom/sides, vertical line at x=0
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

RNG = np.random.RandomState(42)


def red_center(n=300, jitter=0.8):
    """Red points in center/inner region: x ~ 2-12, y ~ 22-28."""
    xs = RNG.uniform(2, 12, n)
    ys = RNG.uniform(22, 28, n)
    return xs, ys


def blue_ushape(n=400, jitter=0.6):
    """Blue points forming U-shape (outer ring) at lower y: wraps around red on bottom and sides."""
    # Left arm of U
    n_left = n // 3
    xl = RNG.uniform(-4, 2, n_left)
    yl = RNG.uniform(15, 25, n_left)
    # Right arm of U
    n_right = n // 3
    xr = RNG.uniform(10, 16, n_right)
    yr = RNG.uniform(15, 25, n_right)
    # Bottom of U
    n_bottom = n - n_left - n_right
    xb = RNG.uniform(2, 10, n_bottom)
    yb = RNG.uniform(15, 18, n_bottom)
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

    rx, ry = red_center()
    bx, by = blue_ushape()
    ax.scatter(bx, by, s=12, c="#0000FF", linewidths=0, alpha=0.7, zorder=1)
    ax.scatter(rx, ry, s=12, c="#FF0000", linewidths=0, alpha=0.8, zorder=2)

    # vertical black line at x=0
    ax.axvline(x=0, color="#000000", linewidth=2.0, zorder=3)

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