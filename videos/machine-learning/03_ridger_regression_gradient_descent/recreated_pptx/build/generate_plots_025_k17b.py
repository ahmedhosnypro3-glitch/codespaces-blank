#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025 (k17b2 attempt).

Independent parallel fix of the three measured k15 PIL defects; output goes to
qa/rejudge_20261027/slide025/assets_k17b2/ (never overwrites assets_k15*).

Fixes vs k15:
  BR: view/extent retuned (BR_AZIM/BR_ELEV/BR_ZOOM/BR_BB/BR_EXTENT, chosen by
      search_br_k17b2.py) so the surface's bottom band tapers like the original
      (colored% 75->16 over y472..517, tip ~y519) instead of a flat 68% edge.
  BL: labels placed at the PIL-measured orig anchors — top 'Global Minima'
      (x236..278 y302..322), right-m 'Local Minima' (x325..350 y388..401),
      low-L 'Local Minima' (x138..205 y438..470), low-R 'Global Minima'
      (x300..346 y448..470); red x markers pinned at slide (199,445),(270,482).
  TR: added the missing diagonal red segment slide (652,189)->(667,165)
      (orig 54% red-hit there) as a figure-fraction line inside the TR PNG.
Kept: BR winding GD path (16 waypoints, wind-ratio ~6.02), jet surface.

Regions (slide px, 1px = 1pt) from build/slide_025.js addImage placements:
  TL x85..265 y115..288 | TR x616..879 y115..317
  BL x83..376  y290..527 | BR x615..880 y344..531
Each PNG is 300dpi at figsize = box_px/72, placed unscaled at box_px/72 in.
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
from scipy.interpolate import CubicSpline

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/assets_k17b2"
os.makedirs(OUT, exist_ok=True)

DPI = 300
JET = plt.get_cmap("jet")


def pastel_jet(f):
    from matplotlib.colors import LinearSegmentedColormap
    xs = np.linspace(0, 1, 256)
    cols = JET(xs)[:, :3] * (1 - f) + f
    return LinearSegmentedColormap.from_list("pjet", cols)


RED = (0.75, 0.0, 0.0)
BLK = "black"
TICKC = "#333333"

PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
    "bl": dict(x0=83,  y0=290, w=293, h=237),
    "br": dict(x0=615, y0=344, w=265, h=187),
}

# BR view params — tuned by search_br_k17b2*.py sweeps vs the orig band
# (best: azim=-165 elev=20 zoom=2.0 bb=0.04, pastel jet f=0.65, pad_lo=0.6)
BR_AZIM = -150
BR_ELEV = 16
BR_ZOOM = 2.0
BR_BB = 0.04
BR_EXTENT = 3.0
BR_ZFAC = 1.0
BR_PAD_LO = 0.6
BR_PASTEL = 0.65


def figure(spec, rect=(0.0, 0.0, 1.0, 1.0)):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes(list(rect), projection="3d")
    return fig, ax


def surf_mask_buf(buf, border=2):
    mx = buf.max(2); mn = buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = (buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90)
    m = m & ~red
    m[:border, :] = False; m[-border:, :] = False
    m[:, :border] = False; m[:, -border:] = False
    return m


def fit(fig, ax, capx, capy, zaspect, rounds=22):
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


def slide_frac(spec, sx, sy):
    """slide px -> figure fraction for a plot placed at spec box."""
    return ((sx - spec["x0"]) / spec["w"], 1.0 - (sy - spec["y0"]) / spec["h"])


# ── TL: concave dome (k15 carried) ──────────────────────────────────────────
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
    ax.set_box_aspect((1, 1, 0.85), zoom=1.10)
    redrect(fig, spec)
    save(fig, "tl")


# ── TR: convex bowl + the missing diagonal red segment (k17b2 fix) ─────────
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
    # k17b2: orig carries a short diagonal red stroke (652,189)->(667,165)
    # (54% red-hit) that the k15 render lacked; draw it inside this PNG.
    (a0, b0) = slide_frac(spec, 652, 189)
    (a1, b1) = slide_frac(spec, 667, 165)
    fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                          color=RED, lw=1.5, zorder=45, solid_capstyle="butt"))
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: non-convex surface, labels at PIL-measured orig anchors (k17b2) ────
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

    # k17b2: anchors = PIL-measured orig label boxes (slide px); text centered
    # in each anchor box. low-L 'Local Minima', low-R 'Global Minima',
    # right-m 'Local Minima', top 'Global Minima'.
    LABELS = [
        ("Global Minima", 257, 312),   # top    x236..278 y302..322
        ("Local Minima",  337, 394),   # right-m x325..350 y388..401
        ("Local Minima",  171, 454),   # low-L  x138..205 y438..470
        ("Global Minima", 323, 460),   # low-R  x300..346 y448..470
    ]
    for txt, sx, sy in LABELS:
        fxp, fyp = slide_frac(spec, sx, sy)
        fig.text(fxp, fyp, txt, fontsize=6.2, color=BLK, ha="center", va="center",
                 zorder=45)
    # red x markers pinned at the two orig marker positions (slide px)
    for mx, my in ((199, 445), (270, 482)):
        fxm, fym = slide_frac(spec, mx, my)
        fig.add_artist(Line2D([fxm], [fym], transform=fig.transFigure,
                              marker="x", color=RED, markersize=7,
                              markeredgewidth=2.0, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: rugged surface + WINDING GD path (k17b2 retuned view) ───────────────
def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


BR_WAYPOINTS = np.array([
    (2.4, 1.9), (2.0, 1.2), (1.6, 1.7), (1.2, 0.9), (0.8, 1.4), (0.4, 0.7),
    (-0.1, 1.1), (-0.5, 0.4), (-0.9, 0.8), (-1.2, 0.1), (-0.9, -0.6),
    (-1.3, -0.3), (-1.0, -1.0), (-1.4, -1.4), (-1.1, -1.9), (-1.5, -2.2),
])


def plot_br():
    spec = PLOTS["br"]
    fig, ax = figure(spec, rect=(0.02, BR_BB, 0.96, 0.98 - BR_BB))
    ax.view_init(elev=BR_ELEV, azim=BR_AZIM)
    e = BR_EXTENT
    x = np.linspace(-e, e, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - BR_PAD_LO * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=pastel_jet(BR_PASTEL), norm=norm, shade=False,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.22,
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

    ax.set_xlim(-e, e); ax.set_ylim(-e, e); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((2 * e, 2 * e, rng * BR_ZFAC), zoom=BR_ZOOM)
    redrect(fig, spec)
    save(fig, "br")

    from PIL import Image
    buf = np.asarray(Image.open(os.path.join(OUT, "plot_025_br.png")).convert("RGB")).astype(np.int32)
    m = surf_mask_buf(buf, border=3)
    ys, xs = np.nonzero(m)
    print("BR surface bbox frac of figure: x %.3f..%.3f  y(top) %.3f..%.3f" % (
        xs.min() / buf.shape[1], xs.max() / buf.shape[1],
        1 - ys.max() / buf.shape[0], 1 - ys.min() / buf.shape[0]))


plot_tl()
plot_tr()
plot_bl()
plot_br()
print("all four plots written (k17b2) -> %s" % OUT)
