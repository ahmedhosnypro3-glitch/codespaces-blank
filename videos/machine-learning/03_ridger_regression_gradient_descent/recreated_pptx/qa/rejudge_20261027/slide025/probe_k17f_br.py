#!/usr/bin/env python3
"""BR-only tuning probe: try view/pit combos, report taper corr vs orig + wind-ratio."""
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
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
DPI = 300
JET = plt.get_cmap("jet")

spec = dict(x0=615, y0=344, w=265, h=187)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return m & ~pr


rows = list(range(472, 529, 2))
po = []
for y in rows:
    po.append(100 * colmask(orig[y, 620:876][None, :, :])[0].mean())
po = np.array(po)


def br_surface(X, Y, pit):
    Z = (3.4 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
         + 2.1 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
         + 1.4 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
         - 2.8 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.4))
         - 2.2 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 1.1))
         - 2.1 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.4))
         + 0.40 * np.sin(2.1 * X) * np.cos(2.3 * Y))
    if pit is not None:
        px, py = pit
        Z = Z - 3.6 * np.exp(-(((X - px) ** 2 + (Y - py) ** 2) / 0.5))
    return Z


WP = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def try_cfg(elev, azim, zaspect, pit, zoom):
    fig = plt.figure(figsize=(spec["w"] / 72, spec["h"] / 72), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y, pit)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - 0.15 * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    t = np.linspace(0, 1, len(WP))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, WP[:, 0])(ts)
    sy = CubicSpline(t, WP[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b), pit)) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.3, zorder=100)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect(zaspect, zoom=zoom)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    # composite to slide px
    im = Image.fromarray(buf.astype(np.uint8)).resize((spec["w"], spec["h"]), Image.BILINEAR)
    ren = np.array(im).astype(np.int32)
    pr = np.array([100 * colmask(ren[y - spec["y0"], 5:261][None, :, :])[0].mean() for y in rows])
    corr = float(np.corrcoef(po, pr)[0, 1])
    # wind ratio on the full-size buffer region mapped to slide
    bx0, by0 = 8, 8
    br = ren[by0:spec["h"] - 8, bx0:spec["w"] - 8]
    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 15:
            continue
        o = np.argsort(xs); px, py = xs[o], ys[o]
        seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
        st = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
        r = seg / max(st, 1.0)
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs.max() - xs.min() + 1, r)
    wr = best[2] if best else 0.0
    col = 100 * colmask(ren).mean()
    print("elev=%d azim=%d z=%s pit=%s zoom=%.2f: taper corr=%.3f wind=%.2f spanx=%s colored=%.1f"
          % (elev, azim, zaspect, pit, zoom, corr, wr, best[1] if best else 0, col))
    return corr, wr


for elev, azim in [(36, -130), (32, -130), (36, -115), (30, -140)]:
    for pit in [None, (2.8, 2.8), (-2.8, -2.8), (2.8, -2.8), (-2.8, 2.8)]:
        try_cfg(elev, azim, (9.0, 5.0, 4.0), pit, 2.0)
