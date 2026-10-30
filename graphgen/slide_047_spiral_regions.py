#!/usr/bin/env python3
"""Slide 047 — vertical color bands (blue left, red right) + nested spiral curves.

Decision:
  lib      : matplotlib + numpy
  algorithm: vertical colored background regions + 3 nested spiral curves
  data     : generated spirals matching original's nested topology
  plot     : solid vertical fills (left=blue, right=red) + thick spiral lines
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

# vertical color bands: left half blue, right half red
BAND_CENTER = 17.5

# three thick nested spirals matching original: black outer, red middle, blue inner
SPIRALS = [
    {"color": "#1A1A1A", "r0": 1.0, "r1": 16.0, "off": 0.0, "width": 2.5},   # black outer
    {"color": "#FF0000", "r0": 0.5, "r1": 12.0, "off": 1.5, "width": 2.0},   # red middle
    {"color": "#0000FF", "r0": 0.2, "r1": 8.0,  "off": 3.0, "width": 1.5},   # blue inner
]
CX, CY = 17.5, 15.0


def spiral_curve(r0, r1, n=600, turns=2.5, off=0.0):
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

    # vertical color bands (background)
    ax.axvspan(XLIM[0], BAND_CENTER, facecolor="#0000FF", alpha=0.15, zorder=0)
    ax.axvspan(BAND_CENTER, XLIM[1], facecolor="#FF0000", alpha=0.15, zorder=0)

    # nested spiral curves (thick lines)
    for sp in SPIRALS:
        xs, ys = spiral_curve(sp["r0"], sp["r1"], off=sp["off"])
        ax.plot(xs, ys, color=sp["color"], linewidth=sp["width"], zorder=2)

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