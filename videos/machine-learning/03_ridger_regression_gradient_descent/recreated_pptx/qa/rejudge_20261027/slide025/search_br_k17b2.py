#!/usr/bin/env python3
"""k17b2 BR view search: find (azim, elev, zoom, bb, extent) so the rendered
surface's bottom band (slide x672..816 y472..517) diff vs orig < 50% and the
per-row colored taper matches orig (75%->16% over x615..880, tip ~y519).
Scores a downscaled composite (gray panel + white plot box at 615,344 265x187).
"""
import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from scipy.interpolate import CubicSpline
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
BW, BH = 265, 187
X0, Y0 = 615, 344
PANEL = np.array([233, 233, 231], np.int32)  # E9E9E7

DPI = 150  # search res


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


def surf_mask(buf, border=2):
    mx, mn = buf.max(2), buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = m & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def render(azim, elev, zoom, bb, extent, zfac=1.3, path=True):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.02, bb, 0.96, 0.98 - bb], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    x = np.linspace(-extent, extent, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - 0.40 * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=plt.get_cmap("jet"), norm=norm, shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    if path:
        t = np.linspace(0, 1, len(WAYPOINTS))
        ts = np.linspace(0, 1, 240)
        sx = CubicSpline(t, WAYPOINTS[:, 0])(ts)
        sy = CubicSpline(t, WAYPOINTS[:, 1])(ts)
        sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
        ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    ax.set_xlim(-extent, extent); ax.set_ylim(-extent, extent)
    ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((2 * extent, 2 * extent, rng * zfac), zoom=zoom)
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


def composite(buf):
    im = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[45:540, 54:904] = PANEL
    canvas[Y0:Y0 + BH, X0:X0 + BW] = np.asarray(im).astype(np.int32)
    return canvas


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 60) & (mx > 90) & ~red
    return m


def score(ren):
    # CHECK1 band
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    ob = ORIG[by0:by1, bx0:bx1]
    rb = ren[by0:by1, bx0:bx1]
    diff = (np.abs(ob - rb).sum(2) > 60)
    band = 100.0 * diff.mean()
    H, W = diff.shape
    gx, gy = 12, 5
    mx = max(int(diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx].sum())
             for iy in range(gy) for ix in range(gx))
    # row profile over BR cols
    oprof = 100.0 * colmask(ORIG[344:531, 615:880]).mean(1)
    rprof = 100.0 * colmask(ren[344:531, 615:880]).mean(1)
    prof = float(np.abs(oprof - rprof)[111:].mean())  # rows y455..528
    # surface bbox frac
    m = surf_mask(ren[Y0:Y0 + BH, X0:X0 + BW], border=3)
    ys, xs = np.nonzero(m)
    fx = (xs.max() - xs.min() + 1) / BW
    fy = (ys.max() - ys.min() + 1) / BH
    xtop = xs.min() / BW
    xbot = xs.max() / BW
    ybot = 1 - ys.max() / BH  # frac from top
    return band, mx, prof, fx, fy, xtop, ybot


def wind(ren):
    bl = ren[Y0:Y0 + BH, X0:X0 + BW]
    lum = 0.299 * bl[:, :, 0] + 0.587 * bl[:, :, 1] + 0.114 * bl[:, :, 2]
    sat = bl.max(2) - bl.min(2)
    dm = (lum < 100) & (sat < 80)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 15:
            continue
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs, ys)
    if best is None:
        return None
    _, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    return seg / max(straight, 1.0)


results = []
for extent in (3.0, 3.6):
    for azim in range(-100, 1, 10):
        for elev in (15, 22, 30, 38):
            for bb in (0.08, 0.14):
                # zoom search: surface bbox ~ (0.90, 0.90)
                lo, hi = 0.05, 8.0
                for _ in range(7):
                    zm = 0.5 * (lo + hi)
                    buf = render(azim, elev, zm, bb, extent, path=False)
                    m = surf_mask(buf)
                    ys, xs = np.nonzero(m)
                    if not len(xs):
                        lo = zm; continue
                    fxx = (xs.max() - xs.min() + 1) / buf.shape[1]
                    fyy = (ys.max() - ys.min() + 1) / buf.shape[0]
                    if fxx < 0.90 and fyy < 0.90:
                        lo = zm
                    else:
                        hi = zm
                zm = lo
                buf = render(azim, elev, zm, bb, extent, path=True)
                ren = composite(buf)
                band, mx, prof, fx, fy, xtop, ybot = score(ren)
                w = wind(ren)
                results.append((band + prof, band, mx, prof, azim, elev, zm, bb, extent, fx, fy, xtop, ybot, w))
                print("azim=%4d elev=%2d bb=%.2f ext=%.1f zoom=%.3f | band=%.1f%% maxcell=%d prof=%.1f fx=%.2f fy=%.2f x0=%.2f ybot=%.2f wind=%s" %
                      (azim, elev, bb, extent, zm, band, mx, prof, fx, fy, xtop, ybot,
                       ("%.2f" % w) if w else "-"), flush=True)

results.sort(key=lambda r: r[0])
print("\nTOP 15 (score band prof):")
for r in results[:15]:
    print("score=%.1f band=%.1f maxcell=%d prof=%.1f azim=%d elev=%d zoom=%.3f bb=%.2f ext=%.1f fx=%.2f fy=%.2f x0=%.2f ybot=%.2f wind=%s" %
          (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], ("%.2f" % r[13]) if r[13] else "-"))
with open(os.path.join(RJ, "search_br_k17b2_best.txt"), "w") as f:
    for r in results[:30]:
        f.write("score=%.2f band=%.2f maxcell=%d prof=%.2f azim=%d elev=%d zoom=%.4f bb=%.2f ext=%.1f fx=%.3f fy=%.3f x0=%.3f ybot=%.3f wind=%s\n" %
                (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13]))
print("wrote search_br_k17b2_best.txt")
