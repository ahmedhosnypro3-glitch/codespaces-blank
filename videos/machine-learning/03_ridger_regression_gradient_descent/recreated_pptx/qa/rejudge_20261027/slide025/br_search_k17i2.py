#!/usr/bin/env python3
"""k17i BR focused search: corner-on views + corner-tilted surface so the
silhouette bottom is a TIP (orig tapers 75->16% over y472..517).

mplot3d fits the 3D box into a centered square of side min(W,H), so fx caps
at H/W=0.707 in the 265x187 box — fine, the band x672..816 (local 57..201)
is inside the centered span. What matters is the row profile in the band.

Grid: azim in {-135,-45,45,135}, elev {35,45,55}, zfac {0.3,0.5},
pad_lo {0.15,0.30}, tilt corner = the screen-bottom corner at that azim
(computed via proj3d), tilt strength {0.4, 0.8} per unit.
Zoom: cap-search fy<=0.92 only (fx free up to 0.707).

Metrics (slide space, panel pasted at 615,344 265x187):
  band  : CHECK1 diff fraction in x672..816 y472..517 (target <0.50)
  proferr: mean |row colored% diff| over y455..528, x615..880
  wind  : path-only render (no surface), largest dark comp wind-ratio
          (promoter gate 5.5..6.5)
score = 100*band + proferr + 25*|wind-6.0|
Writes ranked rows to br_search_k17i2_results.txt (+ _best.txt).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
from scipy import ndimage
from scipy.interpolate import CubicSpline

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

BW, BH = 265, 187
BX, BY = 615, 344
BAND = (672, 472, 816, 517)
OBAND = ORIG[BAND[1]:BAND[3], BAND[0]:BAND[2]]

JET = plt.get_cmap("jet")
DPI = 150


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~pr


OPROF = 100.0 * colmask(ORIG[344:531, 615:880]).mean(1)


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.6 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.4))
            - 2.0 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 1.1))
            - 1.9 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.4))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])

_X = np.linspace(-3, 3, 120)
_XG, _YG = np.meshgrid(_X, _X)


def bottom_corner(azim, elev):
    """which data corner (sx,sy) in {+-3}^2 projects lowest on screen."""
    fig = plt.figure(figsize=(1, 1), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-1, 1)
    ax.set_axis_off()
    best = None
    for sx in (-3, 3):
        for sy in (-3, 3):
            x2, y2, _ = proj3d.proj_transform(sx, sy, -1, ax.get_proj())
            if best is None or y2 < best[0]:
                best = (y2, sx, sy)
    plt.close(fig)
    return best[1], best[2]


def render(azim, elev, zfac, pad_lo, tilt, with_path=True, with_surf=True):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    Z = br_surface(_XG, _YG)
    if tilt:
        cx, cy = bottom_corner(azim, elev)
        Z = Z - tilt * (0.5 * _XG * cx / 3.0 + 0.5 * _YG * cy / 3.0) * 3.0
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    if with_surf:
        norm = Normalize(zmin - pad_lo * rng, zmax)
        ax.plot_surface(_XG, _YG, Z, cmap=JET, norm=norm, shade=False,
                        antialiased=True, rstride=3, cstride=3, linewidth=0.22,
                        edgecolor=(0.05, 0.05, 0.05, 0.35))
    if with_path:
        t = np.linspace(0, 1, len(BR_WAYPOINTS))
        ts = np.linspace(0, 1, 240)
        sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
        sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
        sz = np.array([float(br_surface(np.array(a), np.array(b)))
                         for a, b in zip(sx, sy)])
        if tilt:
            cx, cy = bottom_corner(azim, elev)
            sz = sz - tilt * (0.5 * sx * cx / 3.0 + 0.5 * sy * cy / 3.0) * 3.0
        sz = sz + 0.12
        ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100,
                solid_capstyle="round")
        x2a, y2a, _ = proj3d.proj_transform(sx[-1], sy[-1], sz[-1], ax.get_proj())
        x2b, y2b, _ = proj3d.proj_transform(sx[-12], sy[-12], sz[-12], ax.get_proj())
        W = fig.get_size_inches()[0] * DPI
        H = fig.get_size_inches()[1] * DPI
        fa = (x2a / W, 1.0 - y2a / H) if False else None
        # use transData like the generator
        da = ax.transData.transform([(x2a, y2a)])[0]
        db = ax.transData.transform([(x2b, y2b)])[0]
        ar = FancyArrowPatch(posA=(db[0] / W, 1 - db[1] / H),
                             posB=(da[0] / W, 1 - da[1] / H),
                             transform=fig.transFigure, arrowstyle="-|>",
                             mutation_scale=9, color="black", lw=0.8, zorder=101)
        fig.add_artist(ar)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    # cap-search zoom on fy only
    lo, hi = 0.02, 40.0
    zoom = 1.0
    for _ in range(12):
        ax.set_box_aspect((6, 6, rng * zfac), zoom=zoom)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
        mx = buf.max(2); mn = buf.min(2)
        m = ((mx - mn) > 60) & (mx > 90)
        red = (buf[:, :, 0] > 140) & (buf[:, :, 0] - buf[:, :, 1] > 60) & (buf[:, :, 0] - buf[:, :, 2] > 60)
        m = m & ~red
        m[:4, :] = False; m[-4:, :] = False; m[:, :4] = False; m[:, -4:] = False
        ys, xs = np.nonzero(m)
        if not len(xs):
            break
        fy = (ys.max() - ys.min() + 1) / buf.shape[0]
        if fy <= 0.92:
            lo = zoom
            zoom = min(hi, zoom * 1.10)
        else:
            hi = zoom
            zoom = 0.5 * (lo + hi)
    ax.set_box_aspect((6, 6, rng * zfac), zoom=lo)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.uint8)
    plt.close(fig)
    return buf, lo


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), xs, ys))
    return out


def wind_of(path_buf):
    im = Image.fromarray(path_buf).resize((BW, BH), Image.BILINEAR)
    bs = np.asarray(im).astype(np.int32)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[BY:BY + BH, BX:BX + BW] = bs
    br = canvas[344 + 8:531 - 8, 615 + 8:880 - 8]
    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    best = None
    for area, xs, ys in comps(dm, min_area=15):
        if best is None or area > best[0]:
            best = (area, xs, ys)
    if not best:
        return 0.0
    a, xs, ys = best
    order = np.argsort(xs)
    px_, py_ = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px_), np.diff(py_)).sum())
    straight = float(np.hypot(px_[-1] - px_[0], py_[-1] - py_[0]))
    return seg / max(straight, 1.0)


def evaluate(azim, elev, zfac, pad_lo, tilt):
    buf, zoom = render(azim, elev, zfac, pad_lo, tilt, with_path=True, with_surf=True)
    im = Image.fromarray(buf).resize((BW, BH), Image.BILINEAR)
    bs = np.asarray(im).astype(np.int32)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[BY:BY + BH, BX:BX + BW] = bs
    rb = canvas[BAND[1]:BAND[3], BAND[0]:BAND[2]]
    band = float((np.abs(OBAND - rb).sum(2) > 60).mean())
    rprof = 100.0 * colmask(canvas[344:531, 615:880]).mean(1)
    proferr = float(np.abs(rprof[455 - 344:529 - 344] - OPROF[455 - 344:529 - 344]).mean())
    pbuf, _ = render(azim, elev, zfac, pad_lo, tilt, with_path=True, with_surf=False)
    wind = wind_of(pbuf)
    m = colmask(bs)
    ys2, xs2 = np.nonzero(m)
    fx = (xs2.max() - xs2.min() + 1) / BW if len(xs2) else 0
    fy = (ys2.max() - ys2.min() + 1) / BH if len(ys2) else 0
    score = 100.0 * band + proferr + 25.0 * abs(wind - 6.0)
    return (score, band, proferr, wind, fx, fy, azim, elev, zfac, pad_lo, tilt, zoom)


if __name__ == "__main__":
    res_path = os.path.join(RJ, "br_search_k17i2_results.txt")
    if os.path.exists(res_path):
        os.remove(res_path)
    results = []
    for azim in (-135, -45, 45, 135):
        for elev in (35, 45, 55):
            for zfac in (0.3, 0.5):
                for pad_lo in (0.15, 0.30):
                    for tilt in (0.4, 0.8):
                        rec = evaluate(azim, elev, zfac, pad_lo, tilt)
                        results.append(rec)
                        line = ("score=%.3f band=%.3f proferr=%.2f wind=%.3f fx=%.3f fy=%.3f "
                                "azim=%d elev=%d zfac=%.2f pad_lo=%.2f tilt=%.1f zoom=%.4f\n" % rec)
                        with open(res_path, "a") as f:
                            f.write(line)
                        print(line, end="", flush=True)
    results.sort()
    with open(os.path.join(RJ, "br_search_k17i2_best.txt"), "w") as f:
        for r in results[:40]:
            f.write("score=%.3f band=%.3f proferr=%.2f wind=%.3f fx=%.3f fy=%.3f "
                    "azim=%d elev=%d zfac=%.2f pad_lo=%.2f tilt=%.1f zoom=%.4f\n" % r)
    print("BEST:", results[0])
