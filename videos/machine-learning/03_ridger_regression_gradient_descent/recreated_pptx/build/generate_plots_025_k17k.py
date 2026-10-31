#!/usr/bin/env python3
"""k17k — slide 025 four subplot PNGs -> build/assets_k17k/.

k17k answers the crop_dense_judge_k15b FAILs on the BR 3D surface with a real
axis-on mplot3d render instead of the axis-off flat mesh used by k15..k17i2:

  BR (rewritten):
    (a) full z-axis ON: zticks [0, 0.5, 1, 1.5], x/y tick labels
        [-100, -50, 0, 50, 100] on both base axes (orig shows -100..100);
    (b) panes + grid walls ON (light-gray panes, gray gridlines) — orig has
        the 3D grid walls, k15's axis-off render did not;
    (c) view from the banked br_search_best (azim=-80 elev=38 zoom=1.8164,
        band=1.000 dmean=0.550), then zoom re-fit so the surface bbox matches
        the orig bbox measured from unique_slides/slide_025.jpg
        (slide x625..864 y356..523 inside panel x615..880 y344..531);
    (d) jet with vmin above the low tail (Normalize(vmin=z_q12, vmax=zmax))
        so the lowest ~12% of the surface clips to t=0 dark blue — orig
        jet-t hist has 1647 px in the lowest bin.
    winding GD path kept (wind-ratio target ~6.02, verify_k15 metric).
  TL/TR/BL: carried from k17f (PIL-measured): TR red diagonal slide
    (652,189)->(667,165); BL labels at slide anchors x138..205 y438..470
    'Local Minima', x300..346 y448..470 'Global Minima', x325..350 y388..401
    'Local Minima', x236..278 y302..322 'Global Minima'; BL red x markers at
    (199,445) and (270,482).

Panel rects (slide px, 960x540, 1px = 1/72in, from build/slide_025.js):
  TL x85..265 y115..288 | TR x616..879 y115..317
  BL x83..376 y290..527 | BR x615..880 y344..531
Each PNG is 300dpi at figsize = panel_px/72; slide->fig-frac:
  fx = (sx - x0)/w,  fy = 1 - (sy - y0)/h
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
from scipy.interpolate import CubicSpline

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = os.path.join(NS, "recreated_pptx/build/assets_k17k")
os.makedirs(OUT, exist_ok=True)

DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)
BLK = "black"
TICKC = "#333333"

PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
    "bl": dict(x0=83,  y0=290, w=293, h=237),
    "br": dict(x0=615, y0=344, w=265, h=187),
}

TARGET = {
    "tl": dict(col=0.201, prof=[15, 5, 35, 40, 32, 14, 4, 15]),
    "tr": dict(col=0.233, prof=[10, 9, 32, 58, 44, 20, 2, 13]),
    "bl": dict(col=0.201, prof=[9, 5, 23, 54, 47, 13, 4, 8]),
}


def figure(spec, rect=(0.0, 0.0, 1.0, 1.0)):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes(list(rect), projection="3d")
    return fig, ax


def surf_mask_buf(buf, border=10):
    mx = buf.max(2); mn = buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 140) & (buf[:, :, 0] - buf[:, :, 1] > 60) \
        & (buf[:, :, 0] - buf[:, :, 2] > 60)
    m = m & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def measure(fig, nbands=8):
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    m = surf_mask_buf(buf)
    H, W = m.shape
    prof = [100.0 * m[i * H // nbands:(i + 1) * H // nbands].mean()
            for i in range(nbands)]
    return float(100.0 * m.mean()), prof, m


def fit_profile(fig, ax, name, zaspect, zooms):
    tgt = TARGET[name]
    best = None
    for z in zooms:
        ax.set_box_aspect(zaspect, zoom=z)
        col, prof, _ = measure(fig)
        err = float(np.sum((np.array(prof) - np.array(tgt["prof"])) ** 2)) \
            + 20000.0 * (col / 100.0 - tgt["col"]) ** 2
        if best is None or err < best[0]:
            best = (err, z, col, prof)
    err, z, col, prof = best
    ax.set_box_aspect(zaspect, zoom=z)
    print("  %s fit zoom=%.3f colored=%.1f%% (target %.1f%%) prof=%s err=%.1f"
          % (name, z, col, 100 * tgt["col"], ["%.0f" % v for v in prof], err))
    return z


def fit_bbox_frac(fig, ax, capx, capy, zaspect, rounds=20):
    """Binary-search zoom so the colored-surface bbox fills up to (capx, capy)
    of the figure without overflowing (k15 method)."""
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
            zoom = min(hi, zoom * 1.10)
        else:
            hi = zoom
            zoom = 0.5 * (lo + hi)
    ax.set_box_aspect(zaspect, zoom=lo)
    fig.canvas.draw()
    return lo


def axis_style(ax, tsize=5.5, pad=1):
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0.0))
        axis._axinfo["grid"].update(color="#E4E4E4", linewidth=0.3, linestyle=":")
        axis.line.set_linewidth(0.4)
    ax.tick_params(pad=pad, labelsize=tsize, length=1.5, width=0.4)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(tsize)
        t.set_color(TICKC)


def axis_style_walls(ax, tsize=5.0, pad=1):
    """k17k: panes + grid walls ON (orig BR shows the 3D grid walls)."""
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((0.95, 0.95, 0.95, 1.0))
        axis._axinfo["grid"].update(color="#A8A8A8", linewidth=0.45,
                                     linestyle="-")
        axis.line.set_linewidth(0.5)
    ax.tick_params(pad=pad, labelsize=tsize, length=1.5, width=0.4)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(tsize)
        t.set_color(TICKC)


def redrect(fig, spec, inset=3):
    x0 = inset / spec["w"]; x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]; y1 = inset / spec["h"]
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))


def save(fig, name):
    fig.savefig(os.path.join(OUT, "plot_025_%s.png" % name), dpi=DPI,
                facecolor="white")
    plt.close(fig)
    print("wrote plot_025_%s.png" % name)


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, 1.0 - disp[1] / H)


def slide_to_fig(spec, sx, sy):
    return ((sx - spec["x0"]) / spec["w"], 1.0 - (sy - spec["y0"]) / spec["h"])


# ── TL: carried from k17f ────────────────────────────────────────────────────
def plot_tl():
    spec = PLOTS["tl"]
    fig, ax = figure(spec)
    ax.view_init(elev=32, azim=60)
    x = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, x)
    R2 = X ** 2 + Y ** 2
    Z = 8.0 * np.exp(-(R2 / 0.62) ** 1.6) - 5.2
    Z = np.clip(Z, -5.2, None)
    Zn = (Z - Z.min()) / max(Z.max() - Z.min(), 1e-9)
    ax.plot_surface(X, Y, Z, facecolors=JET(0.62 * Zn), shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.40,
                    edgecolor=(0.05, 0.05, 0.05, 0.75))
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=-5.2,
               colors=[JET(0.62 * t) for t in np.linspace(0, 1, 12)],
               linewidths=0.8)
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-5.2, 3)
    ax.set_xticks([2, 0, -2]); ax.set_yticks([2, 0, -2])
    ax.set_zticks([0, -5])
    axis_style(ax, tsize=6.0, pad=-1)
    fit_profile(fig, ax, "tl", (1, 1, 0.85), np.linspace(0.40, 3.2, 24))
    redrect(fig, spec)
    save(fig, "tl")


# ── TR: carried from k17f (incl. red diagonal (652,189)->(667,165)) ──────────
def plot_tr():
    spec = PLOTS["tr"]
    fig, ax = figure(spec)
    ax.view_init(elev=38, azim=60)
    x = np.linspace(-100, 100, 100)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = 3.1 * np.clip((R - 8.0) / 92.0, 0, 1) ** 1.25 \
        + 0.55 * np.exp(-(R ** 2) / (30.0 ** 2))
    zmax = 3.65
    norm = Normalize(0.0, 0.0 + (zmax - 0.0) * 0.42)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=2, cstride=2, linewidth=0.25,
                    edgecolor=(0.05, 0.05, 0.05, 0.5))
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=0.0, linestyles=":",
               colors="#555555", linewidths=1.0)
    ax.set_xlim(-100, 100); ax.set_ylim(-100, 100); ax.set_zlim(0, zmax)
    ax.invert_xaxis()
    ax.set_xticks([-100, -50, 0, 50, 100]); ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_zticks([0, 1, 2, 3])
    ax.set_zticklabels(["0", "1", "2", "3"])
    axis_style(ax, tsize=5.4, pad=1)
    ax.xaxis.set_tick_params(pad=0.5)
    ax.yaxis.set_tick_params(pad=5.0)
    ax.text2D(0.03, 0.95, r"$\times 10^{4}$", transform=ax.transAxes,
              fontsize=6.0, color=TICKC, va="top", zorder=50)
    fit_profile(fig, ax, "tr", (200, 200, zmax * 0.9), np.linspace(0.05, 3.0, 26))
    (fx0, fy0) = slide_to_fig(spec, 652, 189)
    (fx1, fy1) = slide_to_fig(spec, 667, 165)
    fig.add_artist(Line2D([fx0, fx1], [fy0, fy1], transform=fig.transFigure,
                          color=RED, lw=1.1, zorder=41, solid_capstyle="butt"))
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: carried from k17f (4 labels at measured anchors + 2 red x markers) ───
def plot_bl():
    spec = PLOTS["bl"]
    fig, ax = figure(spec, rect=(0.05, 0.09, 0.90, 0.88))
    ax.view_init(elev=28, azim=-62)
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    Z = (5.2 * np.exp(-((X - 0.2) ** 2 + (Y - 0.4) ** 2) * 0.9)
         + 3.8 * np.exp(-((X + 1.9) ** 2 + (Y - 1.7) ** 2) * 1.5)
         - 5.4 * np.exp(-((X + 0.7) ** 2 + (Y + 1.6) ** 2) * 1.1)
         - 4.0 * np.exp(-((X - 1.8) ** 2 + (Y + 1.3) ** 2) * 1.4))
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=4, cstride=4, linewidth=0.28,
                    edgecolor=(0.05, 0.05, 0.05, 0.55))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-6.5, 9)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_zticks([-6, -4, -2, 0, 2, 4, 6, 8])
    axis_style(ax, tsize=5.5, pad=0.5)
    ax.set_xlabel("X", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_ylabel("Y", fontsize=5.5, color=TICKC, labelpad=0)
    fit_profile(fig, ax, "bl", (1, 1, 0.95), np.linspace(0.35, 2.6, 24))

    LABELS = [
        ("Local Minima",  (138 + 205) / 2, (438 + 470) / 2),
        ("Global Minima", (300 + 346) / 2, (448 + 470) / 2),
        ("Local Minima",  (325 + 350) / 2, (388 + 401) / 2),
        ("Global Minima", (236 + 278) / 2, (302 + 322) / 2),
    ]
    for txt, sx, sy in LABELS:
        fx, fy = slide_to_fig(spec, sx, sy)
        fig.text(fx, fy, txt, fontsize=6.2, color=BLK, ha="center", va="center",
                 zorder=45)
    for (mx, my) in ((199, 445), (270, 482)):
        fx, fy = slide_to_fig(spec, mx, my)
        fig.add_artist(Line2D([fx], [fy], transform=fig.transFigure,
                              marker="x", color=RED, markersize=4.5,
                              markeredgewidth=1.4, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR k17k: axis-ON mplot3d surface, -100..100 base, z ticks 0/0.5/1/1.5,
#    panes+grid walls ON, view azim=-80 elev=38 (banked best), jet vmin above
#    the low tail so the lowest area clips to dark blue ──────────────────────
def br_surface(X, Y):
    return (0.38
            + 1.05 * np.exp(-(((X - 25.0) ** 2 + (Y + 20.0) ** 2) / 45.0 ** 2))
            + 0.75 * np.exp(-(((X + 45.0) ** 2 + (Y - 30.0) ** 2) / 35.0 ** 2))
            + 0.55 * np.exp(-(((X - 60.0) ** 2 + (Y - 55.0) ** 2) / 25.0 ** 2))
            - 0.50 * np.exp(-(((X + 15.0) ** 2 + (Y + 40.0) ** 2) / 30.0 ** 2))
            - 0.42 * np.exp(-(((X - 30.0) ** 2 + (Y + 60.0) ** 2) / 28.0 ** 2))
            - 0.38 * np.exp(-(((X + 60.0) ** 2 + (Y + 55.0) ** 2) / 30.0 ** 2))
            + 0.12 * np.sin(X / 18.0) * np.cos(Y / 21.0))


# winding GD route in -100..100 data coords (k17f waypoints scaled x30)
BR_WAYPOINTS = np.array([
    (72, 57), (51, 33), (27, 43.5), (6, 18), (-15, 28.5),
    (-30, 9), (-18, -18), (-39, -27), (-24, -51), (-45, -66),
])


def plot_br():
    spec = PLOTS["br"]
    fig, ax = figure(spec, rect=(0.0, 0.0, 1.0, 1.0))
    # banked br_search_best view: azim=-80 elev=38 zoom=1.8164
    ax.view_init(elev=38, azim=-80)
    x = np.linspace(-100, 100, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    # (d) vmin above the low tail: lowest ~12% of surface clips to jet t=0
    # (dark blue) — orig jet-t hist has 1647 px in the lowest bin
    vmin = float(np.quantile(Z, 0.12))
    norm = Normalize(vmin, zmax)
    print("  br zmin=%.3f zmax=%.3f vmin=%.3f (q12) -> clipped dark-blue frac=%.3f"
          % (zmin, zmax, vmin, float((Z <= vmin).mean())))
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))

    # winding GD path hugging the surface
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b)))
                   for a, b in zip(sx, sy)]) + 4.0
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100,
            solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), \
        proj_xy(ax, sx[-12], sy[-12], sz[-12])
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color="black",
                         lw=0.8, zorder=101)
    fig.add_artist(ar)

    # (a) full axes ON with orig tick sets
    ax.set_xlim(-100, 100); ax.set_ylim(-100, 100); ax.set_zlim(0.0, 1.75)
    ax.set_xticks([-100, -50, 0, 50, 100])
    ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_zticks([0, 0.5, 1, 1.5])
    ax.set_zticklabels(["0", "0.5", "1", "1.5"])
    # (b) panes + grid walls ON
    axis_style_walls(ax, tsize=5.0, pad=1)
    ax.set_xlabel("x", fontsize=5.0, color=TICKC, labelpad=0)
    ax.set_ylabel("y", fontsize=5.0, color=TICKC, labelpad=0)
    ax.set_zlabel("J", fontsize=5.0, color=TICKC, labelpad=0)
    # (c) box aspect: square base, moderate height; zoom re-fit to orig bbox
    # orig surf bbox in panel frac: x 0.038..0.940, y(top) 0.064..0.957
    zoom = fit_bbox_frac(fig, ax, 0.955, 0.975, (4, 4, 1.6), rounds=22)
    print("  br zoom=%.4f (banked best was 1.8164)" % zoom)
    redrect(fig, spec)
    save(fig, "br")

    buf = np.asarray(Image.open(os.path.join(OUT, "plot_025_br.png"))
                     .convert("RGB")).astype(np.int32)
    m = surf_mask_buf(buf)
    ys, xs = np.nonzero(m)
    print("  br surface bbox frac of figure: x %.3f..%.3f  y(top) %.3f..%.3f"
          % (xs.min() / buf.shape[1], xs.max() / buf.shape[1],
             1 - ys.max() / buf.shape[0], 1 - ys.min() / buf.shape[0]))


plot_tl()
plot_tr()
plot_bl()
plot_br()
print("all four plots written (k17k) ->", OUT)
