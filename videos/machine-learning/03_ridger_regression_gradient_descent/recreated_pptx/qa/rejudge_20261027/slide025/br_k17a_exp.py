#!/usr/bin/env python3
"""Focused BR experiment for k17a: correct colored mask (exclude red frame and
its AA fringe), score = band pixel-diff + row-profile error + tip position +
winding window. Renders grid at dpi=100, saves best at 300dpi to assets_k17a.
Writes progress to br_k17a_exp_notes.txt next to this script.
"""
import itertools
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from scipy import ndimage
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = os.path.join(HERE, "assets_k17a")
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)
BW, BH, X0, Y0 = 265, 187, 615, 344


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def colmask(a, border=6):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (r > 140) & (r - g > 40) & (r - b > 40)
    m = ((a.max(2) - a.min(2)) > 30) & (a.max(2) > 90) & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def render_br(azim, elev, zoom, zs, pad, dpi, rstride=4):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=dpi)
    ax = fig.add_axes([0.02, 0.0, 0.96, 0.98], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - pad * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=rstride, cstride=rstride, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    t = np.linspace(0, 1, len(WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")

    def pxy(x, y, z):
        x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
        d = ax.transData.transform([(x2, y2)])[0]
        W = fig.get_size_inches()[0] * dpi
        H = fig.get_size_inches()[1] * dpi
        return (d[0] / W, 1.0 - d[1] / H)

    (ex, ey), (ex2, ey2) = pxy(sx[-1], sy[-1], sz[-1]), pxy(sx[-12], sy[-12], sz[-12])
    fig.add_artist(FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=9, color="black",
                                   lw=0.8, zorder=101))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, rng * zs), zoom=zoom)
    for (a0, b0, a1, b1) in ((3 / BW, 1 - 3 / BH, 3 / BW, 3 / BH),
                             (1 - 3 / BW, 1 - 3 / BH, 1 - 3 / BW, 3 / BH),
                             (3 / BW, 1 - 3 / BH, 1 - 3 / BW, 1 - 3 / BH),
                             (3 / BW, 3 / BH, 1 - 3 / BW, 3 / BH)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


def to_slide(buf):
    im = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    c = np.full((540, 960, 3), 255, np.int32)
    c[Y0:Y0 + BH, X0:X0 + BW] = np.asarray(im).astype(np.int32)
    return c


def wind(ren):
    br = ren[Y0 + 8:Y0 + BH - 8, X0 + 8:X0 + BW - 8]
    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 15 and (best is None or len(xs) > best[0]):
            best = (len(xs), xs, ys)
    if best is None:
        return None
    _, xs, ys = best
    o = np.argsort(xs)
    px, py = xs[o].astype(float), ys[o].astype(float)
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    st = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    return seg / max(st, 1.0)


oprof = 100.0 * colmask(ORIG[Y0:Y0 + BH, X0:X0 + BW]).mean(1)


def score(ren):
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    ob = ORIG[by0:by1, bx0:bx1]
    rb = ren[by0:by1, bx0:bx1]
    diff = (np.abs(ob - rb).sum(2) > 60)
    band = 100.0 * diff.mean()
    rprof = 100.0 * colmask(ren[Y0:Y0 + BH, X0:X0 + BW]).mean(1)
    prof = float(np.abs(rprof[455 - Y0:524 - Y0] - oprof[455 - Y0:524 - Y0]).mean())
    rows20 = [i + Y0 for i in range(BH) if rprof[i] > 20]
    tip = rows20[-1] if rows20 else -1
    tip_pen = abs(tip - 523)
    w = wind(ren)
    wpen = 0.0 if w is not None and 5.0 <= w <= 7.0 else 40.0
    return band + 3.0 * prof + 2.0 * tip_pen + wpen, dict(band=band, prof=prof, tip=tip, wind=w)


notes = open(os.path.join(HERE, "br_k17a_exp_notes.txt"), "w")


def log(m):
    print(m, flush=True)
    notes.write(m + "\n"); notes.flush()


grid = list(itertools.product(
    (-150, -135, -120, -105),          # azim
    (30, 40, 50, 60),                  # elev
    (0.8, 1.0, 1.2, 1.4),              # zoom
    (0.8, 1.0),                        # z-aspect scale
    (0.28,),                           # pad
))
log("grid %d candidates" % len(grid))
res = []
for i, (az, el, zm, zs, pad) in enumerate(grid):
    ren = to_slide(render_br(az, el, zm, zs, pad, dpi=100))
    s, d = score(ren)
    res.append((s, az, el, zm, zs, pad, d))
    if (i + 1) % 32 == 0:
        log("  %d/%d best=%.1f" % (i + 1, len(grid), min(r[0] for r in res)))
res.sort(key=lambda r: r[0])
log("top 10:")
for r in res[:10]:
    d = r[6]
    log("  %.1f az=%d el=%d zm=%.2f zs=%.1f | band=%.1f prof=%.1f tip=%d wind=%s"
        % (r[0], r[1], r[2], r[3], r[4], d["band"], d["prof"], d["tip"],
           ("%.2f" % d["wind"]) if d["wind"] else "?"))
best = res[0]
log("chosen: az=%d el=%d zm=%.2f zs=%.1f pad=0.28" % (best[1], best[2], best[3], best[4]))
buf = render_br(best[1], best[2], best[3], best[4], 0.28, dpi=DPI, rstride=3)
Image.fromarray(buf.astype(np.uint8)).save(os.path.join(OUT, "plot_025_br.png"))
log("wrote assets_k17a/plot_025_br.png")
s, d = score(to_slide(buf))
log("final 300dpi score: %.1f %s" % (s, d))
notes.close()
