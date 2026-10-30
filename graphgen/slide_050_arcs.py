#!/usr/bin/env python3
"""Slide 050 — blue upper arc + red U-shape below (two clean separated arcs).

Decision:
  lib      : matplotlib + numpy
  algorithm: parametric arc curves (upper arc + U-shape) with minimal jitter
  data     : generated to match original's clean two-arc topology
  plot     : two dense scatter clusters following arc paths, NO boundary line, no legend
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IMG_X0, IMG_Y0, IMG_W, IMG_H = 40, 30, 700, 500
AXBOX = (100, 80, 640, 480)
XLIM = (-10, 50)
YLIM = (-10, 40)
XTICKS = [-10, 0, 10, 20, 30, 40, 50]
YTICKS = [-10, 0, 10, 20, 30, 40]
DPI = 300

RNG = np.random.RandomState(7)


def arc_points(n=180, jitter=0.5):
    """Blue upper arc: from (-5, 30) curving over to (45, 28)."""
    t = np.linspace(0, 1, n)
    xs = -5 + t * 50
    ys = 28 + 5 * np.sin(np.pi * t) - 4 * t + RNG.normal(0, jitter, n)
    return xs, ys


def ushape_points(n=180, jitter=0.5):
    """Red U-shape below: dips down from (-2, 18) to (48, 14)."""
    t = np.linspace(0, 1, n)
    xs = -2 + t * 50
    ys = 17 - 12 * np.sin(np.pi * t * 0.9) + 2 * t + RNG.normal(0, jitter, n)
    return xs, ys


def build_figure(out):
    fig = plt.figure(figsize=(IMG_W / 72.0, IMG_H / 72.0), dpi=DPI)
    fig.patch.set_facecolor("white")
    l, t, r, b = AXBOX
    ax = fig.add_axes([(l - IMG_X0) / IMG_W, (IMG_H - (b - IMG_Y0)) / IMG_H,
                       (r - l) / IMG_W, (b - t) / IMG_H])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_facecolor("white")

    bx, by = arc_points()
    rx, ry = ushape_points()
    ax.scatter(bx, by, s=14, c="#0000FF", linewidths=0, alpha=0.75, zorder=2)
    ax.scatter(rx, ry, s=14, c="#FF0000", linewidths=0, alpha=0.75, zorder=2)

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