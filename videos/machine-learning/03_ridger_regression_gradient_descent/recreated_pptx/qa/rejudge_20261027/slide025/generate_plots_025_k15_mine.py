#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025 (k15).

k15 fixes the post-k14 judge_full_fresh.txt FAILs (PIL-confirmed against
unique_slides/slide_025.jpg):
  BL labels: glyph-template PIL on the original shows lower-LEFT text =
    "Local Minima" (anchor ~x158 y456) and lower-RIGHT = "Global Minima"
    (~x314 y459); k14 had them swapped. Local Maxima anchor measured at
    ~(300,345). Red 'x' markers: the original carries only two small red
    clusters at the minima (~(194,443) and (267,481)); no markers at the
    maxima — k15 keeps x markers on the two minima only and thins leaders.
  BR surface: rugged multi-valley gaussian mixture (3 peaks + 3 valleys +
    stronger ripple vs k14's 2+2), so the panel no longer reads as a single
    smooth dome. GD path is an explicit WINDING waypoint spline (11 pts)
    instead of k14's near-straight gradient trace.
  BR containment: axes rect lifted (bottom margin 0.10) and fit cap cut to
    0.80 height — original surface tapers to a tip near slide y521 with a
    white gap before the inner bottom frame at y526-528; k14 ran flush.
  TL/TR: carried unchanged from k14 (TR bowl PIL-verified; TR finding was
    adjudicated secondary).

Regions measured from unique_slides/slide_025.jpg (960x540, 1px = 1/72in):
  TL x85..265 y115..288 | TR x616..879 y115..317
  BL x83..376  y290..527 | BR x615..880 y344..531
Each PNG is 300dpi at figsize = box_px/72 and is placed at box_px/72 inches.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/assets_k15"
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


def figure(spec, rect=(0.0, 0.0, 1.0, 1.0)):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes(list(rect), projection="3d")
    return fig, ax


def surf_mask_buf(buf, border=2):
    mx = buf.max(2); mn = buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = m & ~red  # the redrect frame is figure chrome, not surface
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def fit(fig, ax, capx, capy, zaspect, rounds=22):
    """Binary-search zoom so the surface bbox approaches (capx, capy) from
    either side — zoom IN when too small, OUT when overflowing."""
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
            zoom = min(hi, zoom * 1.08)
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


def redrect(fig, spec, inset=3):
    x0 = inset / spec["w"]
    x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]
    y1 = inset / spec["h"]
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


# ── TL: concave dome (k14 carried) ───────────────────────────────────────────
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
    save(fig, "tl")


# ── TR: convex bowl (k14 carried — PIL-verified bowl sign) ───────────────────
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
    fit(fig, ax, 0.74, 0.68, (200, 200, zmax * 0.9))
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: non-convex two-peak/two-valley, labels PIL-measured from the original ─
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
    # Label anchors PIL-measured on unique_slides/slide_025.jpg (glyph-template
    # matched): lower-LEFT = "Local Minima", lower-RIGHT = "Global Minima".
    LABELS = {
        "GM":  ("Global Maxima", 254, 309, "center"),
        "LMx": ("Local Maxima",  300, 345, "center"),
        "LMn": ("Local Minima",  158, 456, "center"),
        "GMn": ("Global Minima", 314, 459, "center"),
    }
    # red x markers only at the two minima (original shows two small red
    # clusters near the valleys, none at the maxima)
    MARKED = {"LMn", "GMn"}
    for key, (txt, sx, sy, ha) in LABELS.items():
        fxp = (sx - spec["x0"]) / BW
        fyp = 1.0 - (sy - spec["y0"]) / BH
        fig.text(fxp, fyp, txt, fontsize=6.2, color=BLK, ha=ha, va="center",
                 zorder=45)
        px_, py_, pz_ = PEAKS[key]
        ex, ey = proj_xy(ax, px_, py_, pz_)
        fig.add_artist(Line2D([fxp, ex], [fyp, ey], transform=fig.transFigure,
                              color=BLK, lw=0.45, zorder=42))
        if key in MARKED:
            fig.add_artist(Line2D([ex], [ey], transform=fig.transFigure,
                                  marker="x", color=RED, markersize=4,
                                  markeredgewidth=1.3, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: rugged multi-valley warm surface + WINDING GD path (k15) ─────────────
def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


# explicit winding route (data coords): hilltop -> S-curves -> deepest valley
BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def plot_br():
    spec = PLOTS["br"]
    # bottom margin 0.10 lifts the surface off the inner bottom frame
    fig, ax = figure(spec, rect=(0.02, 0.10, 0.96, 0.88))
    ax.view_init(elev=30, azim=-55)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - 0.40 * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))

    # winding path: spline through the waypoints, z hugging the surface
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    wx, wy = BR_WAYPOINTS[:, 0], BR_WAYPOINTS[:, 1]
    # Catmull-Rom-ish smoothing via cubic interpolation per coordinate
    from scipy.interpolate import CubicSpline
    sx = CubicSpline(t, wx)(ts)
    sy = CubicSpline(t, wy)(ts)
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
    fit(fig, ax, 0.92, 0.80, (6, 6, rng * 1.3))
    redrect(fig, spec)
    save(fig, "br")

    # report the surface's vertical extent inside the saved PNG (containment)
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
print("all four plots written (k15)")
