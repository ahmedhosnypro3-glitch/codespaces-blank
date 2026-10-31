#!/usr/bin/env python3
"""k17f — re-derive slide 025's four subplot PNGs from measured original pixels.

Unlike k15 (hand-tuned analytic surfaces), every surface parameter here is
driven by a measurement taken from unique_slides/slide_025.jpg (960x540,
1px = 1pt) in qa/rejudge_20261027/slide025/probe_k17f_measure.py:

  panel rects (slide px, from build/slide_025.js addImage calls):
    TL x85..265  y115..288 (180x173)  TR x616..879 y115..317 (263x202)
    BL x83..376  y290..527 (293x237)  BR x615..880 y344..531 (265x187)
  measured orig stats:
    TL colored 20.1%, jet-t mean .62 std .33, row profile [15,5,35,40,32,14,4,15]
    TR colored 23.3%, jet-t mean .57 std .23, row profile [10,9,32,58,44,20,2,13]
    BL colored 20.1%, jet-t mean .53 std .23, row profile [ 9,5,23,54,47,13, 4, 8]
    BR colored 43.3%, jet-t mean .54 std .22, bottom band y472..528 tapers
       colored% 75 -> 16 (per-row measured); single hot-rim bowl t-field
  TR diagonal red segment slide (652,189)->(667,165): 170 red px, 53.3% red-hit
  BL labels (slide anchors): 'Local Minima' x138..205 y438..470,
    'Global Minima' x300..346 y448..470, 'Local Minima' x325..350 y388..401,
    'Global Minima' x236..278 y302..322
  BL red x markers: slide (199,445) area 67, (270,482) area 60
  BR winding GD path: wind-ratio 6.02 (verify_k15 metric on largest dark comp)

Each PNG is 300dpi at figsize = panel_px/72, placed unscaled at panel_px/72
inches, so figure-fraction coords map 1:1 to slide px:
  fx = (sx - x0)/w,  fy = 1 - (sy - y0)/h

Output: qa/rejudge_20261027/slide025/assets_k17f/plot_025_{tl,tr,bl,br}.png
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

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025/assets_k17f")
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

# measured orig row profiles (8 bands top->bottom, colored %) and colored share
TARGET = {
    "tl": dict(col=0.201, prof=[15, 5, 35, 40, 32, 14, 4, 15]),
    "tr": dict(col=0.233, prof=[10, 9, 32, 58, 44, 20, 2, 13]),
    "bl": dict(col=0.201, prof=[9, 5, 23, 54, 47, 13, 4, 8]),
    "br": dict(col=0.433, prof=[16, 5, 43, 70, 81, 70, 40, 22]),
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
    return float(100.0 * m.mean()), prof


def fit_profile(fig, ax, name, zaspect, zooms):
    """Pick the zoom whose rendered (colored%, 8-band row profile) best matches
    the measured original panel stats (min profile MSE + colored% penalty)."""
    tgt = TARGET[name]
    best = None
    for z in zooms:
        ax.set_box_aspect(zaspect, zoom=z)
        col, prof = measure(fig)
        err = float(np.sum((np.array(prof) - np.array(tgt["prof"])) ** 2)) \
            + 20000.0 * (col / 100.0 - tgt["col"]) ** 2
        if best is None or err < best[0]:
            best = (err, z, col, prof)
    err, z, col, prof = best
    ax.set_box_aspect(zaspect, zoom=z)
    print("  %s fit zoom=%.3f colored=%.1f%% (target %.1f%%) prof=%s err=%.1f"
          % (name, z, col, 100 * tgt["col"], ["%.0f" % v for v in prof], err))
    return z


def fit_bbox(fig, ax, capx, capy, zaspect, rounds=20):
    """Binary-search zoom so the surface bbox approaches (capx, capy) from
    either side — zoom IN when too small, OUT when overflowing (k15 method)."""
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
    col, prof = measure(fig)
    print("  br bbox-cap fit zoom=%.3f colored=%.1f%% (target 43.3%%) prof=%s"
          % (lo, col, ["%.0f" % v for v in prof]))
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


# ── TL: concave dome with contour base, matched to orig t-hist (peaks at
#    t~0 blue skirt, t~.5, t~.75, t~1 red cap) and row profile ────────────────
def plot_tl():
    spec = PLOTS["tl"]
    fig, ax = figure(spec)
    ax.view_init(elev=32, azim=60)
    x = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, x)
    R2 = X ** 2 + Y ** 2
    # measured hist is bimodal (blue skirt + red cap): steep dome, wide flat base
    Z = 8.0 * np.exp(-(R2 / 0.62) ** 1.6) - 5.2
    Z = np.clip(Z, -5.2, None)
    Zs = np.where(Z > -4.9, Z, np.nan)  # thin dome shell; base shows contour lines only
    Zn = (Z - Z.min()) / max(Z.max() - Z.min(), 1e-9)
    Zn = np.where(Z > -4.9, Zn, np.nan)
    ax.plot_surface(X, Y, Zs, facecolors=JET(Zn), shade=True,
                    antialiased=True, rstride=3, cstride=3, linewidth=0.40,
                    edgecolor=(0.05, 0.05, 0.05, 0.75))
    ax.contour(X, Y, Z, levels=12, zdir="z", offset=-5.2,
               colors=[JET(t) for t in np.linspace(0, 1, 12)],
               linewidths=0.8)
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-5.2, 3)
    ax.set_xticks([2, 0, -2]); ax.set_yticks([2, 0, -2])
    ax.set_zticks([0, -5])
    axis_style(ax, tsize=6.0, pad=-1)
    # orig TL surface bbox 178x167px (aspect 1.07), spans ~0.98 x 0.96 of panel
    fit_bbox(fig, ax, 0.96, 0.95, (1.3, 1.0, 0.9), rounds=18)
    redrect(fig, spec)
    save(fig, "tl")


# ── TR: convex bowl, hot rim (orig bin15 red peak) + cold center, with the
#    diagonal red segment (652,189)->(667,165) embedded in-PNG (53% red-hit) ─
def plot_tr():
    spec = PLOTS["tr"]
    fig, ax = figure(spec)
    ax.view_init(elev=38, azim=60)
    x = np.linspace(-100, 100, 100)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    # measured ring: rim high (red), center low (blue/green) -> steep-sided bowl
    Z = 3.1 * np.clip((R - 8.0) / 92.0, 0, 1) ** 0.7 \
        + 0.55 * np.exp(-(R ** 2) / (30.0 ** 2))
    zmax = 3.65
    zmin = 0.0
    norm = Normalize(zmin, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=True, antialiased=True,
                    rstride=5, cstride=5, linewidth=0.25,
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
    # orig TR surface bbox 256x194px (aspect 1.32), spans ~0.97 x 0.96
    fit_bbox(fig, ax, 0.96, 0.94, (300, 200, zmax * 0.95), rounds=18)
    # diagonal red segment, measured slide (652,189)->(667,165), drawn in-PNG
    # as 3 short ticks with wide gaps: the orig stroke is broken (53% red-hit
    # over a 5px sampling window), so a solid line would over-hit
    (fx0, fy0) = slide_to_fig(spec, 652, 189)
    (fx1, fy1) = slide_to_fig(spec, 667, 165)
    for f in (0.10, 0.60):
        fa, fb = f, f + 0.12
        fig.add_artist(Line2D([fx0 + (fx1 - fx0) * fa, fx0 + (fx1 - fx0) * fb],
                              [fy0 + (fy1 - fy0) * fa, fy0 + (fy1 - fy0) * fb],
                              transform=fig.transFigure, color=RED, lw=1.0,
                              zorder=41, solid_capstyle="butt"))
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: non-convex two-peak/two-valley surface + 4 labels at measured slide
#    anchors + 2 red x markers at (199,445) and (270,482) ─────────────────────
def plot_bl():
    spec = PLOTS["bl"]
    fig, ax = figure(spec, rect=(0.01, 0.02, 0.98, 0.96))
    ax.view_init(elev=28, azim=-62)
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    # measured t-field: two hot caps up-top, one deep cold pool low-center-right
    Z = (5.2 * np.exp(-((X - 0.2) ** 2 + (Y - 0.4) ** 2) * 0.9)
         + 3.8 * np.exp(-((X + 1.9) ** 2 + (Y - 1.7) ** 2) * 1.5)
         - 5.4 * np.exp(-((X + 0.7) ** 2 + (Y + 1.6) ** 2) * 1.1)
         - 4.0 * np.exp(-((X - 1.8) ** 2 + (Y + 1.3) ** 2) * 1.4))
    ax.plot_surface(X, Y, Z, cmap=JET, shade=True, antialiased=True,
                    rstride=6, cstride=6, linewidth=0.28,
                    edgecolor=(0.05, 0.05, 0.05, 0.55))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-6.5, 9)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_zticks([-6, -4, -2, 0, 2, 4, 6, 8])
    axis_style(ax, tsize=5.5, pad=0.5)
    ax.set_xlabel("X", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_ylabel("Y", fontsize=5.5, color=TICKC, labelpad=0)
    # orig BL surface bbox 291x232px (aspect 1.25), spans ~0.99 x 0.98
    fit_bbox(fig, ax, 0.96, 0.95, (1.6, 1.0, 1.0), rounds=18)

    # labels at the measured slide anchor centers (figure coords)
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
    # red x markers at the two measured marker centroids
    for (mx, my) in ((199, 445), (270, 482)):
        fx, fy = slide_to_fig(spec, mx, my)
        fig.add_artist(Line2D([fx], [fy], transform=fig.transFigure,
                              marker="x", color=RED, markersize=5.2,
                              markeredgewidth=1.7, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: single hot-rim bowl filling the bottom band (taper 75%->16% over
#    y472..528) + winding GD path with wind-ratio 6.02 ───────────────────────
def br_surface(X, Y):
    return (3.4 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.1 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.4 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.8 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.4))
            - 2.2 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 1.1))
            - 2.1 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.4))
            - 3.6 * np.exp(-(((X - 2.8) ** 2 + (Y - 2.8) ** 2) / 0.5))
            + 0.40 * np.sin(2.1 * X) * np.cos(2.3 * Y))


BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
])


def plot_br():
    spec = PLOTS["br"]
    fig, ax = figure(spec, rect=(0.0, 0.0, 1.0, 1.0))
    ax.view_init(elev=34, azim=-125)
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - 0.15 * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))

    from scipy.interpolate import CubicSpline
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b)))
                   for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.3, zorder=100,
            solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), \
        proj_xy(ax, sx[-12], sy[-12], sz[-12])
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color="black",
                         lw=0.8, zorder=101)
    fig.add_artist(ar)

    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    # orig BR surface bbox 260x182px (aspect 1.43), spans ~0.996 x 0.968:
    # wide flat diamond, so the box is much wider than tall. Zoom pinned from
    # the pixel probe (probe_k17f_br.py): elev=34/azim=-125/pit(2.8,2.8)/zoom~1.9
    # gives taper corr ~0.47 and wind-ratio ~7 (orig 6.02).
    fit_bbox(fig, ax, 0.96, 0.95, (9.0, 5.0, rng * 0.7), rounds=16)
    ax.set_box_aspect((9.0, 5.0, rng * 0.7), zoom=1.9)
    redrect(fig, spec)
    save(fig, "br")

    from PIL import Image
    buf = np.asarray(Image.open(os.path.join(OUT, "plot_025_br.png"))
                     .convert("RGB")).astype(np.int32)
    m = surf_mask_buf(buf)
    ys, xs = np.nonzero(m)
    print("  br surface bbox frac of figure: x %.3f..%.3f  y(top) %.3f..%.3f" % (
        xs.min() / buf.shape[1], xs.max() / buf.shape[1],
        1 - ys.max() / buf.shape[0], 1 - ys.min() / buf.shape[0]))


plot_tl()
plot_tr()
plot_bl()
plot_br()
print("all four plots written (k17f) ->", OUT)
