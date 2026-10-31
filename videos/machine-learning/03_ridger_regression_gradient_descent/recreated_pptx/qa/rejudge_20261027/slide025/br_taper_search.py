#!/usr/bin/env python3
"""Search elev (+stretch) for the BR panel so the bottom taper matches the original.
Renders surface-only, stretches buffer by XSTRETCH, pastes at box, prints band row
profile vs orig. Picks best elev by mean abs row-profile error in y470..525.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
DPI = 150
BOX = dict(x0=615, y0=344, w=265, h=187)
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)


def cm(a):
    mx, mn = a.max(2), a.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return m & ~red


ob_full = cm(orig[BOX["y0"] + 8:BOX["y0"] + BOX["h"] - 8, BOX["x0"] + 8:BOX["x0"] + BOX["w"] - 8])
OROW = 100.0 * ob_full.mean(1)  # indexed by slide y - 352


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.6 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.4))
            - 2.0 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 1.1))
            - 3.0 * np.exp(-(((X + 2.7) ** 2 + (Y + 2.7) ** 2) / 1.2))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


def mask(buf):
    mx, mn = buf.max(2), buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 140) & (buf[:, :, 0] - buf[:, :, 1] > 60) & (buf[:, :, 0] - buf[:, :, 2] > 60)
    m = m & ~red
    m[:10, :] = False; m[-10:, :] = False; m[:, :10] = False; m[:, -10:] = False
    return m


def render(elev, zoom, xstretch):
    w, h = BOX["w"], BOX["h"]
    fig = plt.figure(figsize=(w / xstretch / 72.0, h / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.view_init(elev=elev, azim=-135)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    ax.plot_surface(X, Y, Z, cmap=plt.get_cmap("jet"),
                    norm=Normalize(zmin - 0.15 * rng, zmax + 1.1 * rng),
                    shade=False, antialiased=True, rstride=3, cstride=3,
                    linewidth=0.22, edgecolor=(0.05, 0.05, 0.05, 0.35))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, rng * 0.9), zoom=zoom)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    plt.close(fig)
    im = Image.fromarray(buf).resize((int(buf.shape[1] * xstretch), buf.shape[0]), Image.LANCZOS)
    return np.array(im).astype(np.int32)


for elev in (45, 52, 60, 68):
    for xstretch in (1.0, 1.15, 1.3):
        lo, hi = 0.05, 20.0
        zoom = 1.0
        for _ in range(20):
            buf = render(elev, zoom, xstretch)
            m = mask(buf)
            ys, xs = np.nonzero(m)
            fy = (ys.max() - ys.min() + 1) / buf.shape[0]
            if fy < 0.95:
                lo = zoom; zoom = min(hi, zoom * 1.06)
            else:
                hi = zoom; zoom = 0.5 * (lo + hi)
        buf = render(elev, lo, xstretch)
        m = mask(buf)
        ys, xs = np.nonzero(m)
        fx = (xs.max() - xs.min() + 1) / buf.shape[1]
        fy = (ys.max() - ys.min() + 1) / buf.shape[0]
        # paste into slide canvas
        canvas = np.full((540, 960, 3), 255, np.int32)
        im = Image.fromarray(buf.astype(np.uint8)).resize((BOX["w"], BOX["h"]), Image.BILINEAR)
        canvas[BOX["y0"]:BOX["y0"] + BOX["h"], BOX["x0"]:BOX["x0"] + BOX["w"]] = np.array(im).astype(np.int32)
        rb = cm(canvas[BOX["y0"] + 8:BOX["y0"] + BOX["h"] - 8, BOX["x0"] + 8:BOX["x0"] + BOX["w"] - 8])
        rrow = 100.0 * rb.mean(1)
        n = min(len(rrow), len(OROW))
        err = float(np.abs(rrow[:n] - OROW[:n]).mean())
        corr = float(np.corrcoef(rrow[:n], OROW[:n])[0, 1])
        # bottom white gap: last colored row
        last_o = 352 + int(np.nonzero(OROW > 20)[0].max())
        last_r = 352 + int(np.nonzero(rrow > 20)[0].max())
        print("elev=%2d xs=%.2f zoom=%.2f fx=%.3f fy=%.3f err=%.2f corr=%.3f lastRow orig=%d rend=%d"
              % (elev, xstretch, lo, fx, fy, err, corr, last_o, last_r), flush=True)
