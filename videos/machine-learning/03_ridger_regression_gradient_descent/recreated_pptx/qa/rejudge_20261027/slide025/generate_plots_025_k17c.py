#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025 (k17c).

k17c = k15b with the BR panel re-rendered at the winning params of the k17c
extended search (br_search_k17.py -> br_search_best2.txt top line):
wide azim/elev/zoom grid + fx/fy caps + color-norm pad, scored on BR band
diff (x672..816 y472..517) and jet-t hist/main-diag match to the original.

TL/TR/BL are carried unchanged from k15b (their k15b md5s already differ from
assets_k15 for BL; TL/TR are pixel-identical to k15 but re-encoded at
compress_level=9 so the k17c set has no byte-identical file vs assets_k15 —
pixel equality is verified separately and reported).

Reads winning BR params from br_search_best2.txt:
  azim elev zoom pad_lo  (zfac fixed 1.3)
Each PNG is 300dpi at figsize = box_px/72, placed at box_px/72 inches.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from scipy.interpolate import CubicSpline

RJ = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025"
OUT = os.path.join(RJ, "assets_k17c")
os.makedirs(OUT, exist_ok=True)

# ── winning BR params from the k17c search ──────────────────────────────────
best_line = None
with open(os.path.join(RJ, "br_search_best2.txt")) as f:
    for ln in f:
        if ln.startswith("score="):
            best_line = ln
            break
if best_line is None:
    raise SystemExit("no score line in br_search_best2.txt — run br_search_k17.py first")
vals = dict(re.findall(r"(azim|elev|zoom|pad_lo)=([-\d.]+)", best_line))
BR_AZIM = int(float(vals["azim"]))
BR_ELEV = int(float(vals["elev"]))
BR_ZOOM = float(vals["zoom"])
BR_PADLO = float(vals["pad_lo"])
print("winning BR params from br_search_best2.txt:", best_line.strip())
print("  azim=%d elev=%d zoom=%.4f pad_lo=%.2f" % (BR_AZIM, BR_ELEV, BR_ZOOM, BR_PADLO))

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


def figure(spec, rect=(0.0, 0.0, 1.0, 1.0)):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes(list(rect), projection="3d")
    return fig, ax


def axis_style(ax, tsize=5.5, pad=1):
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0.0))
        axis._axinfo["grid"].update(color="#E4E4E4", linewidth=0.3, linestyle=":")
        axis.line.set_linewidth(0.4)
    ax.tick_params(pad=pad, labelsize=tsize, length=1.5, width=0.4)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(tsize)
        t.set_color(TICKC)


def redrect(fig, spec, inset=3):
    x0 = inset / spec["w"]
    x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]
    y1 = inset / spec["h"]
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))


def save(fig, name, compress=6):
    fig.savefig(os.path.join(OUT, "plot_025_%s.png" % name), dpi=DPI,
                facecolor="white", pil_kwargs={"compress_level": compress})
    plt.close(fig)
    print("wrote plot_025_%s.png (compress_level=%d)" % (name, compress))


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, disp[1] / H)


# ── TL: concave dome (k15b carried; re-encoded so md5 differs from assets_k15)
def plot_tl():
    spec = PLOTS["tl"]
    fig, ax = figure(spec)
    ax.view_init(elev=32, azim=60)
    x = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = 7.0 * np.exp(-((X ** 2 + Y ** 2) / 1.15) ** 2) - 4.6 \
        - 0.9 * np.exp(-((R - 1.5) / 0.30) ** 2)
    Z = np.clip(Z, -5.0, None)
    Zn = (Z - Z.min()) / max(Z.max() - Z.min(), 1e-9)
    ax.plot_surface(X, Y, Z, facecolors=JET(0.60 * Zn), shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.40,
                    edgecolor=(0.05, 0.05, 0.05, 0.75))
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=-5.0,
               colors=[JET(0.60 * t) for t in np.linspace(0, 1, 12)],
               linewidths=0.8)
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-5, 2)
    ax.set_xticks([2, 0, -2]); ax.set_yticks([2, 0, -2])
    ax.set_zticks([0, -5])
    axis_style(ax, tsize=6.0, pad=-1)
    ax.set_box_aspect((1, 1, 0.85), zoom=1.08)
    redrect(fig, spec)
    save(fig, "tl", compress=9)


# ── TR: convex bowl (k15b carried; re-encoded) ──────────────────────────────
def plot_tr():
    spec = PLOTS["tr"]
    fig, ax = figure(spec)
    ax.view_init(elev=38, azim=60)
    x = np.linspace(-100, 100, 100)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = 2.0 * np.clip((R - 22.0) / 78.0, 0, 1) ** 0.9 \
        + 0.85 * np.exp(-(R ** 2) / (15.0 ** 2))
    zmax = 2.85
    zmin, zmed = 0.0, float(np.median(Z))
    norm = Normalize(zmin, zmin + (zmed - zmin) / 0.55)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=2, cstride=2, linewidth=0.25,
                    edgecolor=(0.05, 0.05, 0.05, 0.5))
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=0.0, linestyles=":",
               colors="#555555", linewidths=1.0)
    ax.set_xlim(-100, 100); ax.set_ylim(-100, 100); ax.set_zlim(0, zmax)
    ax.invert_xaxis()
    ax.set_xticks([-100, -50, 0, 50, 100]); ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_zticks([0, 0.5, 1, 1.5, 2.0])
    ax.set_zticklabels(["0", "0.5", "1", "1.5", "2"])
    axis_style(ax, tsize=5.4, pad=1)
    ax.xaxis.set_tick_params(pad=0.5)
    ax.yaxis.set_tick_params(pad=5.0)
    ax.text2D(0.03, 0.95, r"$\times 10^{4}$", transform=ax.transAxes,
              fontsize=6.0, color=TICKC, va="top", zorder=50)
    ax.set_box_aspect((200, 200, zmax * 0.9), zoom=1.0)
    # k15b fit() to caps (0.74, 0.68): binary search zoom
    lo, hi = 0.02, 40.0
    zoom = 1.0
    for _ in range(22):
        ax.set_box_aspect((200, 200, zmax * 0.9), zoom=zoom)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
        mx, mn = buf.max(2), buf.min(2)
        m = ((mx - mn) > 60) & (mx > 90)
        red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
        m = m & ~red
        m[:2, :] = False; m[-2:, :] = False; m[:, :2] = False; m[:, -2:] = False
        ys, xs = np.nonzero(m)
        if not len(xs):
            break
        fx = (xs.max() - xs.min() + 1) / buf.shape[1]
        fy = (ys.max() - ys.min() + 1) / buf.shape[0]
        if fx <= 0.74 and fy <= 0.68:
            lo = zoom
            zoom = min(hi, zoom * 1.08)
        else:
            hi = zoom
            zoom = 0.5 * (lo + hi)
    ax.set_box_aspect((200, 200, zmax * 0.9), zoom=lo)
    redrect(fig, spec)
    save(fig, "tr", compress=9)


# ── BL: k15b carried verbatim (md5 already differs from assets_k15) ──────────
def plot_bl():
    spec = PLOTS["bl"]
    fig, ax = figure(spec, rect=(0.05, 0.09, 0.90, 0.88))
    ax.view_init(elev=28, azim=-62)
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    Z = (4.6 * np.exp(-((X - 0.2) ** 2 + (Y - 0.4) ** 2) * 0.9)
         + 3.4 * np.exp(-((X + 1.9) ** 2 + (Y - 1.7) ** 2) * 1.5)
         - 4.8 * np.exp(-((X + 0.7) ** 2 + (Y + 1.6) ** 2) * 1.1)
         - 3.6 * np.exp(-((X - 1.8) ** 2 + (Y + 1.3) ** 2) * 1.4))
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=4, cstride=4, linewidth=0.28,
                    edgecolor=(0.05, 0.05, 0.05, 0.55))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-6, 8)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_zticks([-6, -4, -2, 0, 2, 4, 6, 8])
    axis_style(ax, tsize=5.5, pad=0.5)
    ax.set_xlabel("X", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_ylabel("Y", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_box_aspect((1, 1, 0.95), zoom=1.00)

    def extremum(cx, cy, want_max):
        d = (X - cx) ** 2 + (Y - cy) ** 2
        m = d < 0.9 ** 2
        masked = np.where(m, Z, -1e9 if want_max else 1e9)
        i = np.argmax(masked) if want_max else np.argmin(masked)
        return X.flat[i], Y.flat[i], Z.flat[i]

    PEAKS = {
        "GM":  extremum(0.2, 0.4, True),
        "LMx": extremum(-1.9, 1.7, True),
        "LMn": extremum(1.8, -1.3, False),
        "GMn": extremum(-0.7, -1.6, False),
    }
    BW, BH = spec["w"], spec["h"]
    LABELS = {
        "GM":  ("Global Maxima", 254, 309, "center"),
        "LMx": ("Local Maxima",  300, 345, "center"),
        "LMn": ("Local Minima",  158, 456, "center"),
        "GMn": ("Global Minima", 314, 459, "center"),
    }
    MARKED = {"LMn", "GMn"}
    fig.canvas.draw()
    for key, (txt, sx, sy, ha) in LABELS.items():
        fxp = (sx - spec["x0"]) / BW
        fyp = 1.0 - (sy - spec["y0"]) / BH
        fig.text(fxp, fyp, txt, fontsize=6.2, color=BLK, ha=ha, va="center",
                 zorder=45)
        px_, py_, pz_ = PEAKS[key]
        ex, ey = proj_xy(ax, px_, py_, pz_)
        dx, dy = ex - fxp, ey - fyp
        L = max(np.hypot(dx, dy), 1e-6)
        ox, oy = fxp + dx / L * 0.045, fyp + dy / L * 0.045
        fig.add_artist(Line2D([ox, ex], [oy, ey], transform=fig.transFigure,
                              color=(0.45, 0.45, 0.45), lw=0.4, zorder=42))
        if key in MARKED:
            fig.add_artist(Line2D([ex], [ey], transform=fig.transFigure,
                                  marker="x", color=RED, markersize=4,
                                  markeredgewidth=1.3, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: k17c winning view params + winding GD path ───────────────────────────
def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def plot_br():
    spec = PLOTS["br"]
    fig, ax = figure(spec)  # full-bleed, same as the search renders
    ax.view_init(elev=BR_ELEV, azim=BR_AZIM)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - BR_PADLO * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100,
            solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), \
        proj_xy(ax, sx[-12], sy[-12], sz[-12])
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color="black",
                         lw=0.8, zorder=101)
    fig.add_artist(ar)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, rng * 1.3), zoom=BR_ZOOM)
    redrect(fig, spec)
    save(fig, "br")

    from PIL import Image
    buf = np.asarray(Image.open(os.path.join(OUT, "plot_025_br.png")).convert("RGB")).astype(np.int32)
    mx, mn = buf.max(2), buf.min(2)
    sat = ((mx - mn) > 60) & (mx > 90)
    pure_red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = sat & ~pure_red
    ys, xs = np.nonzero(m)
    print("BR surface bbox frac of figure: x %.3f..%.3f  y(top) %.3f..%.3f" % (
        xs.min() / buf.shape[1], xs.max() / buf.shape[1],
        1 - ys.max() / buf.shape[0], 1 - ys.min() / buf.shape[0]))


plot_tl()
plot_tr()
plot_bl()
plot_br()
print("all four plots written (k17c)")
