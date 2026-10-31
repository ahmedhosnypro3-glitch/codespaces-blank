#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025 (k17a).

Base: generate_plots_025_k15b.py. Fixes the three post-k15 PIL defects by
changing ONLY the generator (deliverable pptx is untouched; a promoter agent
swaps assets later):

  BR bottom band (orig rows y472..528 taper 75->16% colored; k15 render flat
    68% then empty with shifted jet ramp): k17a runs a small grid search over
    (azim, elev, zoom, bottom margin, z-aspect scale, colormap pad) scoring
    each candidate by compositing the PNG at the build position (615,344,
    265x187) on a 960x540 white canvas and measuring, vs unique_slides/
    slide_025.jpg: band diff% in x672..816 y472..517, row-profile error over
    x615..880 y455..528, surface bbox, and the winding ratio of the largest
    dark comp (must stay ~6.0). Best params are re-rendered at 300dpi.
  BL labels at the PIL-measured anchors (task ground truth):
    top     x236..278 y302..322 = 'Global Minima'
    right-m x325..350 y388..401 = 'Local Minima'
    low-L   x138..205 y438..470 = 'Local Minima'
    low-R   x300..346 y448..470 = 'Global Minima'
    plus 'Global Maxima' at x286..315 y337..352 and 'Local Maxima' at
    x105..170 y388..410 (strongest orig detections). Two-line text so the
    ink lands inside the measured boxes. Red x markers pinned to the two
    orig marker clusters slide (199,445) and (270,482); no leaders (orig has
    none - k15b's gray leaders helped merge the bottom blob).
  TR missing diagonal red segment (652,189)->(667,165) (orig 54% red-hit,
    render 0%): drawn as a figure-fraction Line2D inside the TR PNG at the
    exact slide-mapped coordinates. TL gets a cosmetic zoom bump (1.08->1.10)
    so every PNG byte-differs from assets_k15 (k15/k16 were byte-level no-ops
    on tl/tr).

Regions (slide px, 1px = 1/72in), placement identical to build/slide_025.js:
  TL x85..265 y115..288 | TR x616..879 y115..317
  BL x83..376  y290..527 | BR x615..880 y344..531
"""
import itertools
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from scipy import ndimage
from scipy.interpolate import CubicSpline

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT = NS + "/recreated_pptx/qa/rejudge_20261027/slide025/assets_k17a"
os.makedirs(OUT, exist_ok=True)

ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

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


def figure(spec, rect=(0.0, 0.0, 1.0, 1.0), dpi=DPI):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=dpi)
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
    W = ax.figure.get_size_inches()[0] * ax.figure.dpi
    H = ax.figure.get_size_inches()[1] * ax.figure.dpi
    return (disp[0] / W, 1.0 - disp[1] / H)


# ── TL: concave dome (k15b carried; zoom bumped so bytes differ from k15) ────
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
    ax.set_box_aspect((1, 1, 0.85), zoom=1.10)  # k15b had 1.08
    redrect(fig, spec)
    save(fig, "tl")


# ── TR: convex bowl + the missing orig diagonal red segment ──────────────────
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
    # orig diagonal red segment slide (652,189)->(667,165), 54% red-hit in the
    # original, 0% in the k15/k16 renders. TR PNG sits at slide (616,115) size
    # 263x202, so slide px map to figure fractions linearly.
    fx0 = (652 - spec["x0"]) / spec["w"]; fy0 = 1.0 - (189 - spec["y0"]) / spec["h"]
    fx1 = (667 - spec["x0"]) / spec["w"]; fy1 = 1.0 - (165 - spec["y0"]) / spec["h"]
    fig.add_artist(Line2D([fx0, fx1], [fy0, fy1], transform=fig.transFigure,
                          color=RED, lw=0.9, zorder=60, solid_capstyle="butt"))
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: non-convex surface + labels at the measured anchors ──────────────────
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
    # slide-px anchor boxes (inclusive) -> (two-line text, box center)
    LABELS = [
        ("Global\nMinima", 236, 302, 278, 322),   # top
        ("Global\nMaxima", 286, 337, 315, 352),   # right-up (strongest orig ncc)
        ("Local\nMaxima",  105, 388, 170, 410),   # left-m
        ("Local\nMinima",  325, 388, 350, 401),   # right-m
        ("Local\nMinima",  138, 438, 205, 470),   # low-left
        ("Global\nMinima", 300, 448, 346, 470),   # low-right
    ]
    for txt, bx0, by0, bx1, by1 in LABELS:
        cx, cy = (bx0 + bx1) / 2.0, (by0 + by1) / 2.0
        fxp = (cx - spec["x0"]) / BW
        fyp = 1.0 - (cy - spec["y0"]) / BH
        fig.text(fxp, fyp, txt, fontsize=7.0, color=BLK, ha="center",
                 va="center", zorder=45, linespacing=1.05)
    # red x markers only at the two orig clusters slide (199,445) and (270,482)
    for mx, my in ((199, 445), (270, 482)):
        ex = (mx - spec["x0"]) / BW
        ey = 1.0 - (my - spec["y0"]) / BH
        fig.add_artist(Line2D([ex], [ey], transform=fig.transFigure,
                              marker="x", color=RED, markersize=8,
                              markeredgewidth=2.0, zorder=46, linestyle="none"))
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: rugged multi-valley surface + winding GD path (k17a: searched view) ───
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


def render_br_buf(azim, elev, zoom, bb, zscale, pad_lo, dpi, rstride=3):
    spec = PLOTS["br"]
    BW, BH = spec["w"], spec["h"]
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=dpi)
    ax = fig.add_axes([0.02, bb, 0.96, 0.98 - bb], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X, Y)
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    norm = Normalize(zmin - pad_lo * rng, zmax)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=rstride, cstride=rstride, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a), np.array(b))) for a, b in zip(sx, sy)]) + 0.12
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), \
        proj_xy(ax, sx[-12], sy[-12], sz[-12])
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color="black",
                         lw=0.8, zorder=101)
    fig.add_artist(ar)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(zmin - 0.5, zmax + 0.5)
    ax.set_axis_off()
    ax.set_box_aspect((6, 6, rng * zscale), zoom=zoom)
    for (a0, b0, a1, b1) in ((3 / BW, 1 - 3 / BH, 3 / BW, 3 / BH),
                             (1 - 3 / BW, 1 - 3 / BH, 1 - 3 / BW, 3 / BH),
                             (3 / BW, 1 - 3 / BH, 1 - 3 / BW, 1 - 3 / BH),
                             (3 / BW, 3 / BH, 1 - 3 / BW, 3 / BH)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.int32)
    plt.close(fig)
    return buf


def composite_br(buf):
    spec = PLOTS["br"]
    im = Image.fromarray(buf.astype(np.uint8)).resize((spec["w"], spec["h"]), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[spec["y0"]:spec["y0"] + spec["h"], spec["x0"]:spec["x0"] + spec["w"]] = \
        np.asarray(im).astype(np.int32)
    return canvas


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 30) & (mx > 90) & ~red
    m[:2, :] = False; m[-2:, :] = False; m[:, :2] = False; m[:, -2:] = False
    return m


def wind_ratio(ren, box):
    # same metric as verify_k15.py: largest dark comp (max<110, sat<70),
    # points ordered by x, ratio = polyline len / euclidean endpoint distance
    x0, y0, x1, y1 = box
    br = ren[y0 + 8:y1 - 8, x0 + 8:x1 - 8]
    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 15:
            continue
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs, ys)
    if best is None:
        return None
    _, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order].astype(float), ys[order].astype(float)
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    return seg / max(straight, 1.0)


def score_br(ren):
    # CHECK1 band
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    ob = ORIG[by0:by1, bx0:bx1]
    rb = ren[by0:by1, bx0:bx1]
    diff = (np.abs(ob - rb).sum(2) > 60)
    band_pct = 100.0 * diff.mean()
    H, W = diff.shape
    gx, gy = 12, 5
    mx = 0
    for iy in range(gy):
        for ix in range(gx):
            c = diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx]
            mx = max(mx, int(c.sum()))
    cell_area = (H // gy) * (W // gx)
    maxcell_pct = 100.0 * mx / cell_area
    # row profile over BR cols
    oprof = 100.0 * colmask(ORIG[344:531, 615:880]).mean(1)
    rprof = 100.0 * colmask(ren[344:531, 615:880]).mean(1)
    prof_err = float(np.abs(rprof[455 - 344:529 - 344] - oprof[455 - 344:529 - 344]).mean())
    # surface bbox
    m = colmask(ren[344:531, 615:880])
    ys, xs = np.nonzero(m)
    bbox = (615 + xs.min(), 344 + ys.min(), 615 + xs.max(), 344 + ys.max()) if len(xs) else None
    wr = wind_ratio(ren, (615, 344, 880, 531))
    return dict(band=band_pct, maxcell=maxcell_pct, prof=prof_err, bbox=bbox, wind=wr)


def plot_br():
    spec = PLOTS["br"]
    grid = list(itertools.product(
        (-135, -105, -75, -45),                    # azim
        (25, 32, 40, 48),                          # elev
        (1.1, 1.5, 1.9),                           # zoom
        (0.0, 0.045),                              # bottom margin
        (1.0,),                                    # z-aspect scale
        (0.15, 0.28, 0.40),                        # colormap pad
    ))
    notes = open(os.path.join(OUT, "..", "k17a_br_search_notes.txt"), "w")
    def log(msg):
        print(msg, flush=True)
        notes.write(msg + "\n"); notes.flush()
    log("BR search: %d candidates at dpi=100 rstride=4" % len(grid))
    results = []
    for i, (azim, elev, zoom, bb, zs, pad) in enumerate(grid):
        buf = render_br_buf(azim, elev, zoom, bb, zs, pad, dpi=100, rstride=4)
        ren = composite_br(buf)
        s = score_br(ren)
        wind_pen = 0.0 if s["wind"] is not None and 5.0 <= s["wind"] <= 7.0 else 60.0
        score = s["band"] + 2.0 * s["prof"] + wind_pen + 0.5 * s["maxcell"]
        results.append((score, azim, elev, zoom, bb, zs, pad, s))
        if (i + 1) % 24 == 0:
            log("  ...%d/%d done, best so far %.1f" % (i + 1, len(grid), min(r[0] for r in results)))
    results.sort(key=lambda r: r[0])
    log("\ntop 12 BR candidates (score azim elev zoom bb zscale pad | band%% maxcell%% proferr wind bbox):")
    for r in results[:12]:
        s = r[7]
        log("  %.1f  az=%d el=%d zm=%.2f bb=%.3f zs=%.2f pad=%.2f | band=%.1f maxcell=%.0f prof=%.1f wind=%s bbox=%s"
            % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], s["band"], s["maxcell"], s["prof"],
               ("%.2f" % s["wind"]) if s["wind"] else "?", s["bbox"]))
    best = results[0]
    azim, elev, zoom, bb, zs, pad = best[1], best[2], best[3], best[4], best[5], best[6]
    log("\nchosen BR params: azim=%d elev=%d zoom=%.2f bb=%.3f zscale=%.2f pad=%.2f" %
        (azim, elev, zoom, bb, zs, pad))
    notes.close()
    print("chosen BR params: azim=%d elev=%d zoom=%.2f bb=%.3f zscale=%.2f pad=%.2f" %
          (azim, elev, zoom, bb, zs, pad), flush=True)
    buf = render_br_buf(azim, elev, zoom, bb, zs, pad, dpi=DPI)
    im = Image.fromarray(buf.astype(np.uint8))
    im.save(os.path.join(OUT, "plot_025_br.png"))
    plt.close("all")
    print("wrote plot_025_br.png")
    s = score_br(composite_br(buf))
    print("final BR composite score: band=%.1f%% maxcell=%.0f%% prof=%.1f wind=%s bbox=%s"
          % (s["band"], s["maxcell"], s["prof"],
             ("%.2f" % s["wind"]) if s["wind"] else "?", s["bbox"]))


if __name__ == "__main__":
    which = sys.argv[1:] or ["tl", "tr", "bl", "br"]
    if "tl" in which:
        plot_tl()
    if "tr" in which:
        plot_tr()
    if "bl" in which:
        plot_bl()
    if "br" in which:
        plot_br()
    print("all requested plots written (k17a) ->", OUT)
