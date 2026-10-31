#!/usr/bin/env python3
"""Sweep BR view variants (azim x elev x zoom, pad_lo=0.40 zfac=1.3) at 150dpi,
score band diff% + band colored% + main-diag jet-t dmean vs orig (0.55/0.125).
Prints ranked table; used to pick the k17i2 BR params when CHECK1 > 50.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
BW, BH = 265, 187
DPI = 150
JET = plt.get_cmap("jet")
JET_LUT = (JET(np.linspace(0, 1, 256))[:, :3] * 255.0)


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


_X = np.linspace(-3, 3, 110)
_XG, _YG = np.meshgrid(_X, _X)
_ZG = br_surface(_XG, _YG)
_ZMIN, _ZMAX = float(_ZG.min()), float(_ZG.max())
_ZRNG = _ZMAX - _ZMIN


def render(azim, elev, zoom, pad_lo=0.40, zfac=1.3):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    norm = Normalize(_ZMIN - pad_lo * _ZRNG, _ZMAX)
    ax.plot_surface(_XG, _YG, _ZG, cmap=JET, norm=norm, shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.set_zlim(_ZMIN - 0.5, _ZMAX + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, _ZRNG * zfac), zoom=zoom)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


def colmask(a, border=2):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 60) & (mx > 90) & ~red
    if border > 0:
        m[:border, :] = False; m[-border:, :] = False
        m[:, :border] = False; m[:, -border:] = False
    return m


def jet_t(px):
    d = ((JET_LUT[None, :, :] - px[:, None, :].astype(np.float64)) ** 2).sum(2)
    return d.argmin(1) / 255.0


BAND = (672, 472, 816, 517)
OBAND = orig[BAND[1]:BAND[3], BAND[0]:BAND[2]]
ob_col = 100.0 * colmask(OBAND, border=0).mean()

rows = []
for azim in (-80, -65, -50):
    for elev in (30, 38):
        for zoom in (1.68, 1.72, 1.76, 1.80, 1.8164):
            buf = render(azim, elev, zoom)
            bs = np.array(Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)).astype(np.int32)
            band = 100.0 * (np.abs(OBAND - bs[BAND[1] - 344:BAND[3] - 344, BAND[0] - 615:BAND[2] - 615]).sum(2) > 60).mean()
            r_col = 100.0 * colmask(bs[BAND[1] - 344:BAND[3] - 344, BAND[0] - 615:BAND[2] - 615], border=0).mean()
            m = colmask(bs, border=2)
            if m.sum() > 50:
                ys, xs = np.nonzero(m)
                t = jet_t(bs[ys, xs])
                x0, y0 = xs.min(), ys.min()
                diag = np.abs((xs - x0) - (ys - y0)) <= 2
                dm = float(t[diag].mean()) if diag.sum() > 10 else float("nan")
                ds = float(t[diag].std()) if diag.sum() > 10 else float("nan")
            else:
                dm = ds = float("nan")
            rows.append((band, r_col, dm, ds, azim, elev, zoom))
            print("azim=%4d elev=%2d zoom=%.4f | banddiff=%.2f bandcol=%.1f (orig %.1f) dmean=%.3f dstd=%.3f"
                  % (azim, elev, zoom, band, r_col, ob_col, dm, ds), flush=True)

print("\nranked by banddiff:")
for r in sorted(rows)[:10]:
    print("banddiff=%.2f bandcol=%.1f dmean=%.3f dstd=%.3f azim=%d elev=%d zoom=%.4f" % r)
print("\nranked by |dmean-0.55| among bandcol>=60:")
cand = [r for r in rows if r[1] >= 60.0]
for r in sorted(cand, key=lambda r: abs(r[2] - 0.55))[:10]:
    print("banddiff=%.2f bandcol=%.1f dmean=%.3f dstd=%.3f azim=%d elev=%d zoom=%.4f" % r)
