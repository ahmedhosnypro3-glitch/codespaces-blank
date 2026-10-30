#!/usr/bin/env python3
"""Slide 046 — three spiral arms (red inner, blue middle, black outer).

Decision:
  lib      : matplotlib + numpy
  algorithm: parametric Archimedean spirals, 3 arms, even dot spacing
  data     : generated to match the original's concentric spiral topology
  plot     : scatter dots along each spiral arm, no legend/title inside axes
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IMG_X0, IMG_Y0, IMG_W, IMG_H = 40, 30, 700, 500
AXBOX = (100, 80, 640, 480)
XLIM = (0, 35)
YLIM = (-10, 40)
XTICKS = [0, 5, 10, 15, 20, 25, 30, 35]
YTICKS = [-10, 0, 10, 20, 30, 40]
DPI = 300

# centers/radii matched to original's arm positions (judge transcript + image analysis)
# Original: red inner spiral (~r 8-20), blue middle (~r 12-25), black outer (~r 18-33)
ARMS = [
    {"color": "#FF0000", "r0": 8.0, "r1": 20.0, "off": 0.0},   # red inner
    {"color": "#0000FF", "r0": 12.0, "r1": 25.0, "off": 1.2},  # blue middle
    {"color": "#1A1A1A", "r0": 18.0, "r1": 33.0, "off": 2.6},  # black outer
]
CX, CY = 17.5, 15.0


def spiral_points(r0, r1, n=400, turns=2.2, off=0.0):
    t = np.linspace(0, 1, n)
    r = r0 + t * (r1 - r0)
    a = t * turns * 2 * np.pi + off
    return CX + r * np.cos(a), CY + r * np.sin(a)


def build_figure(out):
    fig = plt.figure(figsize=(IMG_W / 72.0, IMG_H / 72.0), dpi=DPI)
    fig.patch.set_facecolor("white")
    l, t, r, b = AXBOX
    ax = fig.add_axes([(l - IMG_X0) / IMG_W, (IMG_H - (b - IMG_Y0)) / IMG_H,
                       (r - l) / IMG_W, (b - t) / IMG_H])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_facecolor("white")
    for arm in ARMS:
        xs, ys = spiral_points(arm["r0"], arm["r1"], off=arm["off"])
        ax.scatter(xs, ys, s=10, c=arm["color"], linewidths=0, alpha=0.9)
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