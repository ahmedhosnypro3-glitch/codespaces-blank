#!/usr/bin/env python3
"""k17h BR search v2: silhouette-only scoring (row colored% profile), faster."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from scipy.interpolate import CubicSpline
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
DPI = 100
BOX = dict(x0=615, y0=344, w=265, h=187)
BW, BH = BOX["w"], BOX["h"]
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ORIG_PROF = np.array([82,82,82,82,82,83,83,85,85,85,82,81,79,76,76,76,76,75,74,74,
                      73,73,72,72,71,70,66,56,55,50,46,46,46,45,45,45,44,44,44,43,46,
                      46,45,45,42,41,41,41,43,44,41,41,41,39,37,36,36,30,26,22,18,17,
                      16,18,16,12,10,12,9,2,2], dtype=np.float64)  # y455..525
ORIG_BBOX = (624, 355, 864, 523)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~red


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


_X = np.linspace(-3, 3, 100)
_XG, _YG = np.meshgrid(_X, _X)
_ZG = br_surface(_XG, _YG)
_ZMIN, _ZMAX = float(_ZG.min()), float(_ZG.max())
_ZRNG = _ZMAX - _ZMIN

BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def fit(fig, ax, capx, capy, zaspect, rounds=10):
    lo, hi = 0.02, 40.0
    zoom = 1.0
    for _ in range(rounds):
        ax.set_box_aspect(zaspect, zoom=zoom)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
        m = colmask(buf)
        m[:2] = False; m[-2:] = False; m[:, :2] = False; m[:, -2:] = False
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


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, 1.0 - disp[1] / H)


def render_br(azim, elev, bmargin, capx, capy, zfac=0.7):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.02, bmargin, 0.96, 0.98 - bmargin], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    norm = Normalize(_ZMIN - 0.40 * _ZRNG, _ZMAX)
    ax.plot_surface(_XG, _YG, _ZG, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(_ZMIN - 0.5, _ZMAX + 0.5)
    ax.set_axis_off()
    zoom = fit(fig, ax, capx, capy, (6, 6, _ZRNG * zfac))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf, zoom


def score(buf):
    img = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    reg = np.array(img).astype(np.int32)
    m = colmask(reg)
    prof = 100.0 * m[455 - 344:526 - 344].mean(1)
    prof_err = np.abs(prof - ORIG_PROF).mean()
    ys, xs = np.nonzero(m)
    bbox = (615 + xs.min(), 344 + ys.min(), 615 + xs.max(), 344 + ys.max()) if len(xs) else (0, 0, 0, 0)
    bbox_err = sum(abs(a - b) for a, b in zip(bbox, ORIG_BBOX))
    return prof_err, bbox_err, bbox, prof


if __name__ == "__main__":
    out = open(os.path.join(RJ, "br_search_k17h3_results.txt"), "w")
    results = []
    combos = []
    for azim in (-70, -55, -40):
        for elev in (22, 28, 34, 40):
            for bm in (0.02, 0.06):
                for zfac in (0.5, 0.7, 0.9, 1.1):
                    combos.append((azim, elev, bm, 0.95, 0.98, zfac))
    for (azim, elev, bm, capx, capy, zfac) in combos:
        buf, zoom = render_br(azim, elev, bm, capx, capy, zfac)
        pe, be, bbox, prof = score(buf)
        sc = pe + 0.1 * be
        results.append((sc, pe, be, azim, elev, bm, capx, capy, zoom, bbox, prof, zfac))
        out.write("score=%.3f prof=%.2f bboxerr=%d azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zfac=%.1f zoom=%.3f bbox=%s\n"
                  % (sc, pe, be, azim, elev, bm, capx, capy, zfac, zoom, bbox))
        out.flush()
    results.sort(key=lambda r: r[0])
    print("== top 12 by silhouette ==")
    for r in results[:12]:
        print("score=%.3f prof=%.2f bboxerr=%d azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zfac=%.1f zoom=%.3f bbox=%s" % (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[11],r[8],r[9]))
    print("best prof:", " ".join("%.0f" % v for v in results[0][10]))
    print("orig prof:", " ".join("%.0f" % v for v in ORIG_PROF))
    out.write("== TOP ==\n")
    for r in results[:12]:
        out.write("score=%.3f prof=%.2f bboxerr=%d azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zfac=%.1f zoom=%.3f bbox=%s\n" % (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[11],r[8],r[9]))
    out.close()
    r = results[0]
    buf, _ = render_br(r[3], r[4], r[5], r[6], r[7], r[11])
    img = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    canvas = Image.fromarray(orig.astype(np.uint8)).copy()
    canvas.paste(img, (BOX["x0"], BOX["y0"]))
    canvas.save(os.path.join(RJ, "br_cand_k17h3_best.png"))
    print("BEST azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zfac=%.1f score=%.3f prof=%.2f bbox=%s"
          % (r[3], r[4], r[5], r[6], r[7], r[11], r[0], r[1], r[9]))
    print("DONE")
