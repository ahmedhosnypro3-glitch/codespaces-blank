#!/usr/bin/env python3
"""BR tune round 3: prioritize band presence (x672..816 y472..498) + pastel colors.
usage: probe_k16_br_tune3.py
"""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.lines import Line2D
from scipy.interpolate import CubicSpline
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
DPI = 300
BW, BH = 265, 187
X0, Y0 = 615, 344
OUTD = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


WAYPOINTS = np.array([
    (2.4, 1.9), (2.0, 1.2), (1.6, 1.7), (1.2, 0.9), (0.8, 1.4), (0.4, 0.7),
    (-0.1, 1.1), (-0.5, 0.4), (-0.9, 0.8), (-1.2, 0.1), (-0.9, -0.6),
    (-1.3, -0.3), (-1.0, -1.0), (-1.4, -1.4), (-1.1, -1.9), (-1.5, -2.2),
])


def colmask(a, thr=30):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > thr) & (mx > 90) & ~red
    m[:2, :] = False; m[-2:, :] = False; m[:, :2] = False; m[:, -2:] = False
    return m


def blended_jet(blend, gray):
    jet = plt.get_cmap("jet")
    cols = [tuple(blend * np.array(jet(i)[:3]) + (1 - blend) * np.array(gray) / 255.0)
            for i in np.linspace(0, 1, 256)]
    return LinearSegmentedColormap.from_list("bjet", cols)


def render_br(zoom, zx, pad_lo, blend, gray, mesh, rs, lw, elev=30, azim=-55):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    cmap = blended_jet(blend, gray) if blend < 1.0 else plt.get_cmap("jet")
    norm = Normalize(zmin - pad_lo * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=cmap, norm=norm, shade=False, antialiased=True,
                    rstride=rs, cstride=rs, linewidth=lw, edgecolor=mesh)
    t = np.linspace(0, 1, len(WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((zx, 6, rng * 1.3), zoom=zoom)
    for (a0, b0, a1, b1) in ((3 / BW, 1 - 3 / BH, 3 / BW, 3 / BH),
                             (1 - 3 / BW, 1 - 3 / BH, 1 - 3 / BW, 3 / BH),
                             (3 / BW, 1 - 3 / BH, 1 - 3 / BW, 1 - 3 / BH),
                             (3 / BW, 3 / BH, 1 - 3 / BW, 3 / BH)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=(0.75, 0, 0), lw=0.7, zorder=40, solid_capstyle="butt"))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


def to_slide(buf):
    im = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[Y0:Y0 + BH, X0:X0 + BW] = np.asarray(im).astype(np.int32)
    return canvas


def band_stats(ren):
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    diff = (np.abs(ORIG[by0:by1, bx0:bx1] - ren[by0:by1, bx0:bx1]).sum(2) > 60)
    H, W = diff.shape
    gx, gy = 12, 5
    cells = []
    for iy in range(gy):
        row = []
        for ix in range(gx):
            c = diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx]
            row.append(int(c.sum()))
        cells.append(row)
    return max(max(r) for r in cells), cells


def wind_ratio(ren):
    bl = ren[Y0:Y0 + BH, X0:X0 + BW]
    lum = 0.299 * bl[:, :, 0] + 0.587 * bl[:, :, 1] + 0.114 * bl[:, :, 2]
    dm = (lum < 100) & ((bl.max(2) - bl.min(2)) < 80)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 20 and (best is None or len(xs) > best[0]):
            best = (len(xs), xs, ys)
    if best is None:
        return None
    _, xs, ys = best
    cols = {}
    for x, y in zip(xs, ys):
        cols.setdefault(int(x), []).append(int(y))
    cx = sorted(cols)
    cy = [float(np.median(cols[c])) for c in cx]
    path = float(sum(np.hypot(cx[i + 1] - cx[i], cy[i + 1] - cy[i]) for i in range(len(cx) - 1)))
    straight = cx[-1] - cx[0]
    wind = sum(1 for i in range(1, len(cy) - 1)
               if abs(cy[i] - cy[i - 1]) >= 1 and abs(cy[i + 1] - cy[i]) >= 1
               and np.sign(cy[i] - cy[i - 1]) != np.sign(cy[i + 1] - cy[i]))
    return dict(area=best[0], xspan=straight, ratio=path / max(straight, 1), winding=wind)


oprof_strict = 100.0 * colmask(ORIG[:, 615:880], 30).mean(1)
oband = 100.0 * colmask(ORIG[:, 672:817], 30).mean(1)

results = []
for zoom in (1.25, 1.35, 1.45, 1.55):
    for zx in (6, 10, 14):
        for blend, gray in ((0.5, 150), (0.45, 140), (1.0, 255)):
            buf = render_br(zoom, zx, 0.15, blend, gray, (0.08, 0.08, 0.08, 0.7), 2, 0.45)
            ren = to_slide(buf)
            rprof = 100.0 * colmask(ren[:, 615:880], 30).mean(1)
            r20 = [y for y in range(344, 526) if rprof[y] > 20]
            end = r20[-1] if r20 else -1
            mx, cells = band_stats(ren)
            rband = 100.0 * colmask(ren[:, 672:817], 30).mean(1)
            pres = float(np.abs(rband[472:499] - oband[472:499]).mean())
            # x extent
            m = colmask(ren[Y0:Y0 + BH, X0:X0 + BW], 30)
            ys, xs = np.nonzero(m)
            fx = (xs.max() - xs.min() + 1) / BW
            score = mx / 10.0 + pres + max(0, end - 516) * 3 + max(0, 510 - end) * 1.5 + abs(fx - 0.90) * 40
            results.append((score, zoom, zx, blend, gray, end, round(pres, 1), round(fx, 2), mx))

results.sort(key=lambda r: r[0])
print("score zoom zx blend gray end pres fx maxcell")
for r in results[:16]:
    print("%.2f  %.2f %2d %.2f %3d  %d  %.1f %.2f %d" % r)

best = results[0]
buf = render_br(best[1], best[2], 0.15, best[3], best[4], (0.08, 0.08, 0.08, 0.7), 2, 0.45)
ren = to_slide(buf)
mx, cells = band_stats(ren)
print("\nbest:", best)
print("maxcell:", mx, "cells:", cells)
print("wind:", wind_ratio(ren))
Image.fromarray(ren.astype(np.uint8)).save(OUTD + "/probe_k16_br_best3.png")
rprof = 100.0 * colmask(ren[:, 615:880], 30).mean(1)
rband = 100.0 * colmask(ren[:, 672:817], 30).mean(1)
print("y orig_band% ren_band% orig_full% ren_full%")
for y in range(470, 527, 2):
    print("  %d %5.1f %5.1f | %5.1f %5.1f" % (y, oband[y], rband[y], oprof_strict[y], rprof[y]))
