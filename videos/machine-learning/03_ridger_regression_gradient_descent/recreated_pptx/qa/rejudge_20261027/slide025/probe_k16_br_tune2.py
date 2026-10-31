#!/usr/bin/env python3
"""Focused BR tune for k16: zoom/zaspect/mesh/cmap-blend grid; scores vs orig.
Writes best PNG to probe_k16_br_best.png and prints metrics.
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


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 30) & (mx > 90) & ~red
    m[:2, :] = False; m[-2:, :] = False; m[:, :2] = False; m[:, -2:] = False
    return m


def row_profile(a, x0, x1):
    return 100.0 * colmask(a[:, x0:x1]).mean(1)


def blended_jet(blend, gray):
    jet = plt.get_cmap("jet")
    cols = [tuple(blend * np.array(jet(i)[:3]) + (1 - blend) * np.array(gray) / 255.0)
            for i in np.linspace(0, 1, 256)]
    return LinearSegmentedColormap.from_list("bjet", cols)


def render_br(zoom, zx, pad_lo, blend, gray, mesh, rs, lw):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=30, azim=-55)
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


def band_maxcell(ren):
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    diff = (np.abs(ORIG[by0:by1, bx0:bx1] - ren[by0:by1, bx0:bx1]).sum(2) > 60)
    H, W = diff.shape
    gx, gy = 12, 5
    mx = 0
    for iy in range(gy):
        for ix in range(gx):
            c = diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx]
            mx = max(mx, int(c.sum()))
    return mx


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


oprof = row_profile(ORIG, 615, 880)

results = []
for zoom in (1.10, 1.15, 1.20, 1.25):
    for zx in (6, 8, 10):
        for blend, gray in ((1.0, 255), (0.62, 200), (0.55, 160)):
            for mesh, rs, lw in (((0.45, 0.45, 0.45, 0.5), 3, 0.22),
                                 ((0.08, 0.08, 0.08, 0.75), 2, 0.5)):
                buf = render_br(zoom, zx, 0.15, blend, gray, mesh, rs, lw)
                ren = to_slide(buf)
                rprof = row_profile(ren, 615, 880)
                r20 = [y for y in range(344, 526) if rprof[y] > 20]
                end = r20[-1] if r20 else -1
                start = r20[0] if r20 else -1
                prof_err = float(np.abs(rprof[455:526] - oprof[455:526]).mean())
                mx = band_maxcell(ren)
                score = prof_err + max(0, end - 515) * 3 + max(0, 515 - end) * 1.0 + mx / 10.0
                results.append((score, zoom, zx, blend, gray, mesh[3], rs, lw,
                                start, end, round(prof_err, 1), mx))

results.sort(key=lambda r: r[0])
print("score zoom zx blend gray malpha rs lw start end prof_err maxcell")
for r in results[:20]:
    print("%.2f  %.2f %2d %.2f %3d %.2f %d %.2f  %d  %d  %.1f  %d" % r)

best = results[0]
buf = render_br(best[1], best[2], 0.15, best[3], best[4],
                (0.45, 0.45, 0.45, best[5]) if best[5] == 0.5 else (0.08, 0.08, 0.08, best[5]),
                best[6], best[7])
ren = to_slide(buf)
print("\nbest:", best)
print("wind:", wind_ratio(ren))
Image.fromarray(ren.astype(np.uint8)).save(
    "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/probe_k16_br_best.png")
# per-row colored% comparison
rprof = row_profile(ren, 615, 880)
print("y, orig%, render% (rows 470..528):")
for y in range(470, 529, 2):
    print("  %d %5.1f %5.1f" % (y, oprof[y], rprof[y]))
