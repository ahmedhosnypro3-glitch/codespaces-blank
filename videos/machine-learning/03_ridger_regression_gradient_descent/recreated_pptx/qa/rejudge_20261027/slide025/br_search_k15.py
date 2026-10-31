#!/usr/bin/env python3
"""Search BR panel view params (azim/elev/zoom) so the rendered surface silhouette
matches the original slide_025.jpg BR box. Scores each candidate by pasting the
surface-only PNG into a 960x540 canvas at box (615,344,265,187) and diffing the
BR interior vs the original; also compares per-row colored% profiles.
Writes best params to br_search_best.txt and candidate PNGs to br_cand_<tag>.png.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
DPI = 150  # search resolution; final render stays 300
JET = plt.get_cmap("jet")
BOX = dict(x0=615, y0=344, w=265, h=187)

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

# original BR interior stats (box pad 8)
P = 8
ob = orig[BOX["y0"] + P:BOX["y0"] + BOX["h"] - P, BOX["x0"] + P:BOX["x0"] + BOX["w"] - P]
mx, mn = ob.max(2), ob.min(2)
OM = ((mx - mn) > 60) & (mx > 90)
OPR = (ob[:, :, 0] > 170) & (ob[:, :, 1] < 90) & (ob[:, :, 2] < 90)
OM = OM & ~OPR
OROW = 100.0 * OM.mean(1)


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.6 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.4))
            - 2.0 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 1.1))
            - 1.9 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.4))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


def surf_mask(buf, border=2):
    mx = buf.max(2); mn = buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = m & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def render(azim, elev, zoom, zfac=1.3):
    w, h = BOX["w"], BOX["h"]
    fig = plt.figure(figsize=(w / 72.0, h / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - 0.15 * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, rng * zfac), zoom=zoom)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


def score(buf):
    # buf is the box at DPI: downsample to slide px and paste into canvas
    bh, bw = buf.shape[:2]
    im = Image.fromarray(buf.astype(np.uint8)).resize((BOX["w"], BOX["h"]), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[BOX["y0"]:BOX["y0"] + BOX["h"], BOX["x0"]:BOX["x0"] + BOX["w"]] = np.array(im).astype(np.int32)
    rb = canvas[BOX["y0"] + P:BOX["y0"] + BOX["h"] - P, BOX["x0"] + P:BOX["x0"] + BOX["w"] - P]
    mx, mn = rb.max(2), rb.min(2)
    RM = ((mx - mn) > 60) & (mx > 90)
    RPR = (rb[:, :, 0] > 170) & (rb[:, :, 1] < 90) & (rb[:, :, 2] < 90)
    RM = RM & ~RPR
    diff = (np.abs(ob - rb).sum(2) > 60)
    rrow = 100.0 * RM.mean(1)
    prof_err = float(np.abs(rrow - OROW).mean())
    return float(diff.mean()), prof_err, RM, rrow


results = []
for zfac in (0.7, 0.9, 1.1):
  for azim in (-90, -80, -70):
    for elev in (15, 22, 28):
        # auto-zoom: binary search zoom so surface bbox height ~ orig (0.064..0.952 fig frac => 0.888)
        lo, hi = 0.05, 6.0
        best = None
        for _ in range(8):
            zm = 0.5 * (lo + hi)
            buf = render(azim, elev, zm, zfac)
            m = surf_mask(buf)
            ys, xs = np.nonzero(m)
            if not len(xs):
                lo = zm; continue
            fy = (ys.max() - ys.min() + 1) / buf.shape[0]
            fx = (xs.max() - xs.min() + 1) / buf.shape[1]
            # want fx ~0.90, fy ~0.89 (orig bbox fracs)
            if fx < 0.90 and fy < 0.89:
                lo = zm
            else:
                hi = zm
        zm = lo
        buf = render(azim, elev, zm, zfac)
        d, pe, RM, rrow = score(buf)
        m = surf_mask(buf)
        ys, xs = np.nonzero(m)
        fx = (xs.max() - xs.min() + 1) / buf.shape[1]
        fy = (ys.max() - ys.min() + 1) / buf.shape[0]
        results.append((d + pe / 100.0, d, pe, azim, elev, zm, fx, fy, zfac))
        print("zfac=%.1f azim=%4d elev=%2d zoom=%.3f fx=%.3f fy=%.3f diff=%.3f proferr=%.2f" %
              (zfac, azim, elev, zm, fx, fy, d, pe), flush=True)

results.sort()
print("\nBEST:", results[0])
with open(os.path.join(RJ, "br_search_best.txt"), "w") as f:
    for r in results:
        f.write("score=%.4f diff=%.3f proferr=%.2f azim=%d elev=%d zoom=%.4f fx=%.3f fy=%.3f zfac=%.1f\n" % r)
best = results[0]
buf = render(best[3], best[4], best[5], best[8], "best")
Image.fromarray(buf.astype(np.uint8)).save(os.path.join(RJ, "br_cand_best.png"))
print("wrote br_cand_best.png br_search_best.txt")
