#!/usr/bin/env python3
"""k17h: BR view-param search for slide 025.

Keeps k15's rugged BR surface + winding waypoint path (winding 6.02), sweeps
view params (azim, elev, axes-rect bottom margin, fit caps) and scores each
candidate composited at slide px (BR box x615 y344 265x187) against the
original unique_slides/slide_025.jpg:
  prof_err : sum |row colored% - orig| over y455..525, cols x615..880
  band_diff: fraction of band x672..816 y472..517 with |diff|sum>60
  bbox_err : |surf bbox - orig bbox (x624..864 y355..523)|
Writes ranked results to br_search_k17h_results.txt (append).
"""
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
DPI = 150
BOX = dict(x0=615, y0=344, w=265, h=187)
BW, BH = BOX["w"], BOX["h"]
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

# orig references
ORIG_PROF = np.array([82,82,82,82,82,83,83,85,85,85,82,81,79,76,76,76,76,75,74,74,
                      73,73,72,72,71,70,66,56,55,50,46,46,46,45,45,45,44,44,44,43,46,
                      46,45,45,42,41,41,41,43,44,41,41,41,39,37,36,36,30,26,22,18,17,
                      16,18,16,12,10,12,9,2,2], dtype=np.float64)  # y455..525
ORIG_BBOX = (624, 355, 864, 523)
BAND = (672, 472, 816, 517)
OBAND = orig[BAND[1]:BAND[3], BAND[0]:BAND[2]]


def colmask(a, border=0):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 60) & (mx > 90) & ~red
    if border:
        m[:border, :] = False; m[-border:, :] = False
        m[:, :border] = False; m[:, -border:] = False
    return m


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


_X = np.linspace(-3, 3, 120)
_XG, _YG = np.meshgrid(_X, _X)
_ZG = br_surface(_XG, _YG)
_ZMIN, _ZMAX = float(_ZG.min()), float(_ZG.max())
_ZRNG = _ZMAX - _ZMIN

BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def surf_mask_buf(buf, border=2):
    mx = buf.max(2); mn = buf.min(2)
    red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = ((mx - mn) > 60) & (mx > 90) & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def fit(fig, ax, capx, capy, zaspect, rounds=18):
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


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, 1.0 - disp[1] / H)


def render_br(azim, elev, bmargin, capx, capy, pad_lo=0.40, zfac=1.3):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.02, bmargin, 0.96, 0.98 - bmargin], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    norm = Normalize(_ZMIN - pad_lo * _ZRNG, _ZMAX)
    ax.plot_surface(_XG, _YG, _ZG, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), proj_xy(ax, sx[-12], sy[-12], sz[-12])
    fig.add_artist(FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=9, color="black", lw=0.8, zorder=101))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(_ZMIN - 0.5, _ZMAX + 0.5)
    ax.set_axis_off()
    zoom = fit(fig, ax, capx, capy, (6, 6, _ZRNG * zfac))
    # red rect
    inset = 3
    x0f = inset / BW; x1f = 1.0 - inset / BW
    y0f = 1.0 - inset / BH; y1f = inset / BH
    for (a0, b0, a1, b1) in ((x0f, y0f, x0f, y1f), (x1f, y0f, x1f, y1f),
                             (x0f, y0f, x1f, y0f), (x0f, y1f, x1f, y1f)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf, zoom


def score(buf):
    # composite: resize buf (DPI render) to slide box size
    img = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    comp = np.array(img).astype(np.int32)
    canvas = orig.copy()
    canvas[BOX["y0"]:BOX["y0"] + BH, BOX["x0"]:BOX["x0"] + BW] = comp
    reg = canvas[344:531, 615:880]
    m = colmask(reg)
    prof = 100.0 * m[455 - 344:526 - 344].mean(1)
    prof_err = np.abs(prof - ORIG_PROF).mean()
    ys, xs = np.nonzero(m)
    bbox = (615 + xs.min(), 344 + ys.min(), 615 + xs.max(), 344 + ys.max())
    bbox_err = sum(abs(a - b) for a, b in zip(bbox, ORIG_BBOX))
    band_c = canvas[BAND[1]:BAND[3], BAND[0]:BAND[2]]
    band_diff = (np.abs(band_c - OBAND).sum(2) > 60).mean()
    return prof_err, band_diff, bbox_err, bbox, prof


if __name__ == "__main__":
    out = open(os.path.join(RJ, "br_search_k17h_results.txt"), "a")
    results = []
    for azim in (-70, -60, -55, -50, -40, -30):
        for elev in (22, 26, 30, 34, 38):
            for bm in (0.02, 0.06, 0.10):
                for (capx, capy) in ((0.93, 0.90), (0.96, 0.97), (0.99, 1.00)):
                    buf, zoom = render_br(azim, elev, bm, capx, capy)
                    pe, bd, be, bbox, prof = score(buf)
                    sc = 100 * bd + pe + 0.15 * be
                    results.append((sc, bd, pe, be, azim, elev, bm, capx, capy, zoom, bbox))
                    out.write("score=%.3f band=%.3f prof=%.2f bboxerr=%d azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zoom=%.3f bbox=%s\n"
                              % (sc, bd, pe, be, azim, elev, bm, capx, capy, zoom, bbox))
                    out.flush()
    results.sort()
    print("== top 15 ==")
    for r in results[:15]:
        print("score=%.3f band=%.3f prof=%.2f bboxerr=%d azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zoom=%.3f bbox=%s" % r)
    out.write("== TOP ==\n")
    for r in results[:15]:
        out.write("score=%.3f band=%.3f prof=%.2f bboxerr=%d azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zoom=%.3f bbox=%s\n" % r)
    out.close()

    # dump the best candidate's row profile + a composite png
    sc, bd, pe, be, azim, elev, bm, capx, capy, zoom, bbox = results[0]
    buf, _ = render_br(azim, elev, bm, capx, capy)
    _, _, _, _, prof = score(buf)
    print("best prof y455..525:", " ".join("%.0f" % v for v in prof))
    img = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    canvas = Image.fromarray(orig.astype(np.uint8)).copy()
    canvas.paste(img, (BOX["x0"], BOX["y0"]))
    canvas.save(os.path.join(RJ, "br_cand_k17h_best.png"))
    print("BEST azim=%d elev=%d bm=%.2f cap=%.2f/%.2f zoom=%.3f score=%.3f band=%.3f prof=%.2f bbox=%s"
          % (azim, elev, bm, capx, capy, zoom, sc, bd, pe, bbox))
    print("DONE")
