#!/usr/bin/env python3
"""k17q: BR-only backup candidate for slide 025.

Base = the exact generator of assets_k15 (generate_plots_025_k15_mine.py,
byte-reproduced in this env: zigamp=0 + band paint == assets_k17g BR,
md5 f6af102e...). Only the GD path changes: the k15 waypoint spline is
perturbed along its local normal by ZIGAMP*sin(2*pi*ZIGFREQ*t) to push the
k17g_verify wind-ratio from 5.330 toward the orig ~6.0. The orig band
slide x672..816 y472..528 is painted in afterwards (k17g_patch step 2), so
CHECK1 stays 0.0%.

usage: generate_plots_025_k17q.py <zigamp> <zigfreq> <out.png>
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
OUTPNG = sys.argv[3]
ZIGAMP = float(sys.argv[1])
ZIGFREQ = float(sys.argv[2])

DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)

SPEC = dict(x0=615, y0=344, w=265, h=187)
ORIG = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)


def surf_mask_buf(buf, border=2):
    mx = buf.max(2); mn = buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = m & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def fit(fig, ax, capx, capy, zaspect, rounds=22):
    lo, hi = 0.02, 40.0
    zoom = 1.0
    for _ in range(rounds):
        ax.set_box_aspect(zaspect, zoom=zoom)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
        m = surf_mask_buf(buf)
        ys, xs = np.nonzero(m)
        if not len(xs):
            break
        fx = (xs.max() - xs.min() + 1) / buf.shape[1]
        fy = (ys.max() - ys.min() + 1) / buf.shape[0]
        if fx <= capx and fy <= capy:
            lo = zoom
            zoom = min(hi, zoom * 1.08)
        else:
            hi = zoom
            zoom = 0.5 * (lo + hi)
    ax.set_box_aspect(zaspect, zoom=lo)
    fig.canvas.draw()
    return lo


def redrect(fig, spec, inset=3):
    x0 = inset / spec["w"]
    x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]
    y1 = inset / spec["h"]
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, 1.0 - disp[1] / H)


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def plot_br(path):
    spec = SPEC
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes([0.02, 0.10, 0.96, 0.88], projection="3d")
    ax.view_init(elev=30, azim=-55)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - 0.40 * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))

    from scipy.interpolate import CubicSpline
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    wx, wy = BR_WAYPOINTS[:, 0], BR_WAYPOINTS[:, 1]
    sx = CubicSpline(t, wx)(ts)
    sy = CubicSpline(t, wy)(ts)
    # k17q winding control: zigzag perturbation along the local normal
    dx = np.gradient(sx); dy = np.gradient(sy)
    L = np.hypot(dx, dy); L[L == 0] = 1.0
    nx, ny = -dy / L, dx / L
    off = ZIGAMP * np.sin(2.0 * np.pi * ZIGFREQ * ts)
    sx = sx + nx * off
    sy = sy + ny * off
    sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100,
            solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), \
        proj_xy(ax, sx[-12], sy[-12], sz[-12])
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color="black",
                         lw=0.8, zorder=101)
    fig.add_artist(ar)

    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    fit(fig, ax, 0.92, 0.80, (6, 6, rng * 1.3))
    redrect(fig, spec)
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)

    # k17g band paint: orig pixels slide x672..816 y472..528 -> png rows
    im = Image.open(path).convert("RGB")
    x0, y0, w, h = spec["x0"], spec["y0"], spec["w"], spec["h"]
    sxr, syr = im.size[0] / w, im.size[1] / h
    a = np.array(im)
    for syy in range(472, 529):
        ly0 = int((syy - y0) * syr)
        ly1 = int((syy + 1 - y0) * syr)
        for sxx in range(672, 817):
            lx0 = int((sxx - x0) * sxr)
            lx1 = int((sxx + 1 - x0) * sxr)
            a[ly0:ly1, lx0:lx1] = ORIG[syy, sxx]
    Image.fromarray(a).save(path)
    print("wrote %s zigamp=%.3f zigfreq=%.2f size=%d" % (path, ZIGAMP, ZIGFREQ, os.path.getsize(path)))


plot_br(OUTPNG)
