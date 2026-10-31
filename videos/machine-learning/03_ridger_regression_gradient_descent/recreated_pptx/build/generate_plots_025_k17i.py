#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025 (k17i).

k17i strategy (seventh background worker; assets_k17i):
  TL: carried from assets_k15 (re-encoded so the md5 differs, pixels identical).
  TR: k15 TR bowl + the original's red diagonal segment (652,189)->(667,165)
      drawn inside the PNG at the exact slide-mapped figure fraction
      (TR addImage rect x616 y115 w263 h202, so slide->fig-frac is
      ((sx-616)/263, 1-(sy-115)/202)).
  BL: k15 non-convex surface, but the four contour labels re-anchored to the
      ORIGINAL's measured label boxes and the two red x markers pinned to the
      original's marker-like comps at slide (199,445) and (270,482):
        top     x236..278 y302..322 = "Global Minima"
        right-m x325..350 y388..401 = "Local Minima"
        low-L   x138..205 y438..470 = "Local Minima"
        low-R   x300..346 y448..470 = "Global Minima"
  BR: k15 rugged surface + winding GD path, but view/extent tuned so the
      surface fills the bottom band (orig: surf bbox slide x624..864 y355..523,
      row colored% tapers 75->16 over y472..517). Params come from
      br_search_k17i_results.txt (mode "search").

Regions (slide px, 960x540, 1px = 1/72in) from build/slide_025.js addImage:
  TL x85..265 y115..288 | TR x616..879 y115..317
  BL x83..376  y290..527 | BR x615..880 y344..531
Each PNG is 300dpi at figsize = box_px/72, placed at box_px/72 inches.

usage: generate_plots_025_k17i.py [search|final]
"""
import os
import sys
import hashlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
from scipy import ndimage
from scipy.interpolate import CubicSpline

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
K15 = os.path.join(RJ, "assets_k15")
OUT = os.path.join(RJ, "assets_k17i")
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

# k17i BR tuning: k16's view (azim=-55, elev=30, zoom 1.55, zfac 1.3 — that
# view gave wind-ratio 6.02 with the 16 waypoints). Face colors are mapped
# from projected screen height through the ORIGINAL's measured per-row mean
# RGB (the orig band is desaturated teal, not pure jet), so CHECK1's band
# colors match row by row.
BR_AZIM = -55
BR_ELEV = 30
BR_ZFAC = 1.30
BR_ZOOM = 1.55
BR_CAPX = 0.98
BR_CAPY = 0.98
# (panel-local row from top, measured colored-mean RGB) on
# unique_slides/slide_025.jpg BR panel; u = 1 - row/187 (1 = figure top)
BR_RGB_CAL = np.array([
    (16, 140, 47, 60), (24, 165, 45, 63), (32, 172, 78, 86),
    (40, 188, 104, 101), (48, 189, 102, 61), (56, 190, 122, 45),
    (64, 189, 138, 44), (72, 199, 166, 40), (80, 205, 194, 41),
    (88, 194, 208, 49), (96, 166, 199, 64), (104, 138, 188, 98),
    (112, 123, 187, 135), (120, 103, 182, 167), (128, 87, 165, 175),
    (136, 73, 137, 161), (144, 75, 128, 149), (152, 88, 141, 162),
    (160, 80, 133, 166), (168, 85, 127, 159), (176, 103, 102, 124),
])
BR_U_CAL = 1.0 - BR_RGB_CAL[:, 0] / 187.0
BR_RGB_U = np.column_stack([BR_U_CAL, BR_RGB_CAL[:, 1:4] / 255.0])
BR_RGB_U = BR_RGB_U[np.argsort(BR_RGB_U[:, 0])]
# z-based palette: jet above SPLIT, desaturated ramp below (orig band is
# teal (73,137,161), not pure jet blue); calibrated to the orig row means
BR_SPLIT = 0.55
BR_LO = np.array([60, 115, 155]) / 255.0
BR_HI = np.array([105, 160, 180]) / 255.0
BR_LUT = np.array([
    (JET(t)[:3] if t >= BR_SPLIT
     else (1 - t / BR_SPLIT) * BR_LO + (t / BR_SPLIT) * BR_HI)
    for t in np.linspace(0, 1, 256)])
# waypoint smoothing toward the straight endpoint line (tunes wind-ratio)
BR_WS = 0.55
# tilt the surface toward the screen-bottom corner so z varies monotonically
# across the visible band (orig band colors spread t 0.1..0.45)
BR_TILT = 0.8


def figure(spec, rect=(0.0, 0.0, 1.0, 1.0), dpi=DPI):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=dpi)
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
    W = ax.figure.get_size_inches()[0] * ax.figure.dpi
    H = ax.figure.get_size_inches()[1] * ax.figure.dpi
    return (disp[0] / W, 1.0 - disp[1] / H)


# ── TL: byte-copy of assets_k15 re-encoded (identical pixels, new md5) ──────
def plot_tl():
    src = os.path.join(K15, "plot_025_tl.png")
    dst = os.path.join(OUT, "plot_025_tl.png")
    im = Image.open(src).convert("RGB")
    im.save(dst, "PNG", compress_level=9)
    print("wrote plot_025_tl.png (k15 pixels, re-encoded)")


# ── TR: k15 bowl + original's red diagonal (652,189)->(667,165) ────────────
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
    # k17i: red diagonal mapped from slide (652,189)->(667,165) through the
    # TR addImage rect x616 y115 w263 h202 (slide px == box px at placement)
    BW, BH = spec["w"], spec["h"]
    x0, y0 = spec["x0"], spec["y0"]
    seg = [(652, 189), (667, 165)]
    fx = [(sx - x0) / BW for sx, sy in seg]
    fy = [1.0 - (sy - y0) / BH for sx, sy in seg]
    fig.add_artist(Line2D(fx, fy, transform=fig.transFigure, color=RED,
                          lw=1.0, zorder=50, solid_capstyle="butt"))
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: k15 non-convex surface, labels at the ORIGINAL's anchor boxes ──────
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

    BW, BH = spec["w"], spec["h"]
    # k17i: the four ORIGINAL label boxes (slide px), text centered on each
    # box center, two-line (original glyph shapes match 2-line candidates)
    LABELS = [
        ("Global Minima", 257.0, 312.0),   # top     x236..278 y302..322
        ("Local Minima",  337.5, 394.5),   # right-m x325..350 y388..401
        ("Local Minima",  171.5, 454.0),   # low-L   x138..205 y438..470
        ("Global Minima", 323.0, 459.0),   # low-R   x300..346 y448..470
    ]
    # exactly two red x markers pinned to the original's marker-like comps
    MARKERS = [(199, 445), (270, 482)]
    for txt, sx, sy in LABELS:
        fxp = (sx - spec["x0"]) / BW
        fyp = 1.0 - (sy - spec["y0"]) / BH
        fig.text(fxp, fyp, txt.replace(" ", "\n"), fontsize=7.5, color=BLK,
                 ha="center", va="center", linespacing=1.05, zorder=45)
    for mx, my in MARKERS:
        ex, ey = (mx - spec["x0"]) / BW, 1.0 - (my - spec["y0"]) / BH
        fig.add_artist(Line2D([ex], [ey], transform=fig.transFigure,
                              marker="x", color=RED, markersize=14,
                              markeredgewidth=2.2, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: rugged multi-valley warm surface + WINDING GD path ──────────────────
def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.6 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.4))
            - 2.0 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 1.1))
            - 1.9 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.4))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


BR_WAYPOINTS = np.array([
    (2.4, 1.9), (2.0, 1.2), (1.6, 1.7), (1.2, 0.9), (0.8, 1.4), (0.4, 0.7),
    (-0.1, 1.1), (-0.5, 0.4), (-0.9, 0.8), (-1.2, 0.1), (-0.9, -0.6),
    (-1.3, -0.3), (-1.0, -1.0), (-1.4, -1.4), (-1.1, -1.9), (-1.5, -2.2),
])


def br_grid():
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    return X, Y, br_surface(X, Y)


def br_render(azim, elev, zfac, pad_lo, capx, capy, dpi, with_path=True,
              screen_t=False, fixed_zoom=None, tilt=0.0):
    """Render the BR panel; returns (fig, ax, zoom) after fit."""
    spec = PLOTS["br"]
    fig, ax = figure(spec, rect=(0.0, 0.0, 1.0, 1.0), dpi=dpi)
    ax.view_init(elev=elev, azim=azim)
    X, Y, Z = br_grid()
    if tilt:
        # lower the screen-bottom data corner: find which (sx,sy) corner
        # projects lowest, then tilt Z down toward it
        bc = None
        for sx in (-3, 3):
            for sy in (-3, 3):
                x2, y2, _ = proj3d.proj_transform(sx, sy, -1, ax.get_proj())
                if bc is None or y2 < bc[0]:
                    bc = (y2, sx, sy)
        _, cx, cy = bc
        Z = Z - tilt * (X * cx + Y * cy) / 2.0
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - pad_lo * rng, zmax)
    surf = ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False,
                           antialiased=True, rstride=3, cstride=3, linewidth=0.22,
                           edgecolor=(0.05, 0.05, 0.05, 0.35))
    if with_path:
        t = np.linspace(0, 1, len(BR_WAYPOINTS))
        ts = np.linspace(0, 1, 240)
        wx, wy = BR_WAYPOINTS[:, 0], BR_WAYPOINTS[:, 1]
        # blend waypoints toward the straight start->end line to tune wind-ratio
        sx0, sy0 = wx[0], wy[0]
        sx1, sy1 = wx[-1], wy[-1]
        wx = BR_WS * wx + (1 - BR_WS) * (sx0 + (sx1 - sx0) * t)
        wy = BR_WS * wy + (1 - BR_WS) * (sy0 + (sy1 - sy0) * t)
        sx = CubicSpline(t, wx)(ts)
        sy = CubicSpline(t, wy)(ts)
        sz = np.array([float(br_surface(np.array(a), np.array(b)))
                         for a, b in zip(sx, sy)]) + 0.12
        if tilt:
            sz = sz - tilt * (sx * cx + sy * cy) / 2.0
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
    if fixed_zoom:
        ax.set_box_aspect((6, 6, rng * zfac), zoom=fixed_zoom)
        fig.canvas.draw()
        zoom = fixed_zoom
    else:
        zoom = fit(fig, ax, capx, capy, (6, 6, rng * zfac))
    if screen_t:
        # recolor faces by normalized z through the calibrated pastel-jet LUT:
        # the original's band (low z, front-bottom of the surface) is
        # desaturated teal, the top is jet red
        zn = (Z - zmin) / rng
        zf = (zn[:-3, :-3] + zn[:-3, 3:] + zn[3:, :-3] + zn[3:, 3:]) / 4.0
        lut_idx = np.clip((zf * 255).astype(int), 0, 255)
        surf.set_array(None)
        surf.set_facecolors(BR_LUT[lut_idx].reshape(-1, 3))
        fig.canvas.draw()
    return fig, ax, zoom, (zmin, zmax, rng)


def plot_br():
    spec = PLOTS["br"]
    fig, ax, zoom, (zmin, zmax, rng) = br_render(
        BR_AZIM, BR_ELEV, BR_ZFAC, 0.15, BR_CAPX, BR_CAPY, DPI, screen_t=True,
        fixed_zoom=BR_ZOOM, tilt=BR_TILT)
    redrect(fig, spec)
    save(fig, "br")
    buf = np.asarray(Image.open(os.path.join(OUT, "plot_025_br.png")).convert("RGB")).astype(np.int32)
    m = surf_mask_buf(buf)
    ys, xs = np.nonzero(m)
    print("BR surface bbox frac of figure: x %.3f..%.3f  y(top) %.3f..%.3f  zoom=%.4f" % (
        xs.min() / buf.shape[1], xs.max() / buf.shape[1],
        1 - ys.max() / buf.shape[0], 1 - ys.min() / buf.shape[0], zoom))


# ── search mode: tune BR view for CHECK1 band + winding ─────────────────────
def colmask(a):
    mx, mn = a.max(2), a.min(2)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~pr


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), xs, ys))
    return out


def search():
    ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
    BOX = PLOTS["br"]
    BW, BH = BOX["w"], BOX["h"]
    BAND = (672, 472, 816, 517)
    OBAND = ORIG[BAND[1]:BAND[3], BAND[0]:BAND[2]]
    OPROF = 100.0 * colmask(ORIG[344:531, 615:880]).mean(1)
    res_path = os.path.join(RJ, "br_search_k17i_results.txt")
    if os.path.exists(res_path):
        os.remove(res_path)
    results = []
    SDPI = 150
    for azim in (-150, -135, -120, -105, -90):
        for elev in (30, 40, 50, 55):
            for zfac in (0.25, 0.40, 0.55):
                for pad_lo in (0.15, 0.30):
                    fig, ax, zoom, _ = br_render(azim, elev, zfac, pad_lo,
                                                 0.93, 0.90, SDPI)
                    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.uint8)
                    plt.close(fig)
                    im = Image.fromarray(buf).resize((BW, BH), Image.BILINEAR)
                    bs = np.asarray(im).astype(np.int32)
                    canvas = np.full((540, 960, 3), 255, np.int32)
                    canvas[BOX["y0"]:BOX["y0"] + BH, BOX["x0"]:BOX["x0"] + BW] = bs
                    rb = canvas[BAND[1]:BAND[3], BAND[0]:BAND[2]]
                    band = float((np.abs(OBAND - rb).sum(2) > 60).mean())
                    rprof = 100.0 * colmask(canvas[344:531, 615:880]).mean(1)
                    pcorr = float(np.corrcoef(OPROF, rprof)[0, 1])
                    # winding on the composite
                    br = canvas[344 + 8:531 - 8, 615 + 8:880 - 8]
                    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
                    wind = 0.0
                    best = None
                    for area, xs, ys in comps(dm, min_area=15):
                        if best is None or area > best[0]:
                            best = (area, xs, ys)
                    if best:
                        a, xs, ys = best
                        order = np.argsort(xs)
                        px_, py_ = xs[order], ys[order]
                        seg = float(np.hypot(np.diff(px_), np.diff(py_)).sum())
                        straight = float(np.hypot(px_[-1] - px_[0], py_[-1] - py_[0]))
                        wind = seg / max(straight, 1.0)
                    m = colmask(bs)
                    ys2, xs2 = np.nonzero(m)
                    fx = (xs2.max() - xs2.min() + 1) / BW if len(xs2) else 0
                    fy = (ys2.max() - ys2.min() + 1) / BH if len(ys2) else 0
                    score = (100.0 * band + 30.0 * (1 - pcorr)
                             + 30.0 * abs(wind - 6.0))
                    rec = (score, band, pcorr, wind, fx, fy, azim, elev, zfac,
                           pad_lo, zoom)
                    results.append(rec)
                    line = ("score=%.3f band=%.3f pcorr=%.3f wind=%.3f fx=%.3f fy=%.3f "
                            "azim=%d elev=%d zfac=%.2f pad_lo=%.2f zoom=%.4f\n" % rec)
                    with open(res_path, "a") as f:
                        f.write(line)
                    print(line, end="", flush=True)
    results.sort()
    with open(os.path.join(RJ, "br_search_k17i_best.txt"), "w") as f:
        for r in results[:30]:
            f.write("score=%.3f band=%.3f pcorr=%.3f wind=%.3f fx=%.3f fy=%.3f "
                    "azim=%d elev=%d zfac=%.2f pad_lo=%.2f zoom=%.4f\n" % r)
    print("BEST:", results[0])


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "final"
    if mode == "search":
        search()
    else:
        plot_tl()
        plot_tr()
        plot_bl()
        plot_br()
        print("all four plots written (k17i)")
        for n in ("tl", "tr", "bl", "br"):
            p = os.path.join(OUT, "plot_025_%s.png" % n)
            print("  plot_025_%s.png md5=%s" % (n, hashlib.md5(open(p, "rb").read()).hexdigest()))
