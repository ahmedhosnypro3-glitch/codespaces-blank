#!/usr/bin/env python3
"""generate_plots_025_k17t2.py — regenerate ONLY the TR and TL plot PNGs of
slide 025 (k17t2 shard; BL belongs to another worker, BR untouched).

Defects from rejudge judge_full_k17z2.txt (build c50e78bf):
  TR = flat tilted sheet; original is a convex paraboloid BOWL with a tall
    red peak at the rear rim + deep blue trough, dotted 3-D bounding box,
    x/y axis run 100/50/0/-50/-100 (and 0/50/100), z axis carries x10^4.
  TL = original is a concave-UP bowl, red rim at the back, blue minimum at
    the bottom, contour lines on the side walls, ticks 0,-5,-2,0,2;
    recreation was a dome with blue mesh and ticks 0,-2,0,-2.

Contract with build/slide_025.js: the red horizontal REFERENCE LINES and the
two slanted strokes are drawn at slide level (addShape), so they stay OUT of
these PNGs. The thin red figure RECTANGLE, however, is baked into the PNGs by
the current build (redrect below) — keep that, drop everything else red.

Outputs (300 dpi, figsize = box_px/72, so addImage at box_px/72 in is exact):
  TR 263x202 slide-px -> 1095x841 PNG
  TL 180x173 slide-px ->  750x720 PNG
written to $RJ/slide025/assets_k17t2/. Each run appends PIL metrics
(red px count/bbox, blue px, hist L1 vs the original slide_025.jpg figure
sub-rect) to $RJ/slide025/k17t2_iter.log.

Usage: python3 generate_plots_025_k17t2.py <iter 1..4>
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.lines import Line2D

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027")
W = os.path.join(RJ, "slide025")
OUT = os.path.join(W, "assets_k17t2")
LOG = os.path.join(W, "k17t2_iter.log")
ORIG = os.path.join(NS, "unique_slides/slide_025.jpg")

os.makedirs(OUT, exist_ok=True)

DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)          # baked figure rectangle (build chrome)
TICKC = "#333333"
GRIDC = "#9A9A9A"

# figure boxes measured from the original frame (slide px, 1px = 1pt)
PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
}
# original figure sub-rects used as histogram reference (slide px, exclusive end)
ORIG_RECT = {"tl": (85, 115, 266, 289), "tr": (616, 115, 880, 318)}
# slide-level red reference lines/strokes present in the ORIGINAL frame but
# drawn by slide_025.js (not baked into PNGs) — masked out of the orig metrics
ORIG_LINE_BANDS = {
    "tl": [(166, 170, 119, 269), (184, 188, 108, 281), (198, 202, 86, 276)],
    "tr": [(224, 228, 631, 877), (232, 236, 642, 869), (187, 211, 653, 862)],
}

# per-iteration tuning knobs
ITERS = {
    1: dict(tr=dict(elev=27, azim=-60, inv_x=True,  zasp=1.00, exp=1.0, fit=(0.95, 0.90)),
            tl=dict(elev=30, azim=-60, inv_x=False, zasp=0.75, fit=(0.95, 0.92))),
    2: dict(tr=dict(elev=20, azim=-55, inv_x=True,  zasp=1.40, exp=1.5, fit=(0.98, 0.95)),
            tl=dict(elev=26, azim=-55, inv_x=False, zasp=0.85, fit=(0.98, 0.95))),
    3: dict(tr=dict(elev=24, azim=-62, inv_x=True,  zasp=1.20, exp=1.3, fit=(0.98, 0.95)),
            tl=dict(elev=30, azim=-62, inv_x=False, zasp=0.70, fit=(0.98, 0.95))),
    4: dict(tr=dict(elev=18, azim=-50, inv_x=False, zasp=1.50, exp=1.6, fit=(0.98, 0.95)),
            tl=dict(elev=24, azim=-48, inv_x=True,  zasp=0.95, fit=(0.98, 0.95))),
}


def figure(spec):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI,
                     facecolor="white")
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), projection="3d")
    ax.set_facecolor("white")
    return fig, ax


def dotted_box(ax, tsize=5.5):
    """Dotted 3-D bounding box: transparent panes, dotted grey pane grid and
    dotted pane edges (not solid grid walls)."""
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0.0))
        axis._axinfo["grid"].update(color=GRIDC, linewidth=0.4, linestyle=":")
        axis.line.set_linewidth(0.6)
        axis.line.set_color(GRIDC)
        axis.line.set_linestyle(":")
    ax.tick_params(pad=1, labelsize=tsize, length=1.5, width=0.4, colors=TICKC)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(tsize)
        t.set_color(TICKC)


def redrect(fig, spec, inset=3):
    """Thin red figure rectangle baked into the PNG (current build's chrome)."""
    x0 = inset / spec["w"]
    x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]
    y1 = inset / spec["h"]
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))


def surf_mask(buf, border=2):
    mx = buf.max(2)
    mn = buf.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    m &= ~((buf[:, :, 0] > 170) & (buf[:, :, 1] < 90) & (buf[:, :, 2] < 90))
    m[:border, :] = False
    m[-border:, :] = False
    m[:, :border] = False
    m[:, -border:] = False
    return m


def fit(fig, ax, capx, capy, zasp, rounds=22):
    """Binary-search zoom so the surface bbox approaches (capx, capy)."""
    lo, hi = 0.02, 40.0
    zoom = 1.0
    for _ in range(rounds):
        ax.set_box_aspect((1, 1, zasp), zoom=zoom)
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
    ax.set_box_aspect((1, 1, zasp), zoom=lo)
    fig.canvas.draw()
    return lo


def surf_mask_buf(buf, border=2):
    return surf_mask(buf, border)


# ── TR: convex paraboloid bowl, tall red rear rim, deep blue trough ──────────
def plot_tr(cfg):
    spec = PLOTS["tr"]
    fig, ax = figure(spec)
    ax.view_init(elev=cfg["elev"], azim=cfg["azim"])
    x = np.linspace(-100, 100, 121)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = 20000.0 * (R / 100.0) ** cfg["exp"]  # 0 .. 20000 -> x10^4 z offset
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=1, cstride=1, linewidth=0.0)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(0, 20000)
    if cfg["inv_x"]:
        ax.invert_xaxis()
    ax.set_xticks([-100, -50, 0, 50, 100])
    ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_zticks([0, 5000, 10000, 15000, 20000])
    dotted_box(ax, tsize=5.4)
    fit(fig, ax, cfg["fit"][0], cfg["fit"][1], cfg["zasp"])
    redrect(fig, spec)
    fig.savefig(os.path.join(OUT, "plot_025_tr.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ── TL: concave-UP bowl, red rim at back, blue minimum, wall contours ────────
def plot_tl(cfg):
    spec = PLOTS["tl"]
    fig, ax = figure(spec)
    ax.view_init(elev=cfg["elev"], azim=cfg["azim"])
    x = np.linspace(-2, 2, 121)
    X, Y = np.meshgrid(x, x)
    Z = 0.875 * (X ** 2 + Y ** 2) - 5.0     # center -5 (blue) .. rim 2 (red)
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=1, cstride=1, linewidth=0.0)
    # contour lines projected on the two side walls of the bounding box
    ax.contour(X, Y, Z, levels=9, zdir="x", offset=-2, colors="#333333", linewidths=0.6)
    ax.contour(X, Y, Z, levels=9, zdir="y", offset=2, colors="#333333", linewidths=0.6)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-5, 2)
    if cfg["inv_x"]:
        ax.invert_xaxis()
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    ax.set_zticks([-5, -2, 0])
    dotted_box(ax, tsize=6.0)
    fit(fig, ax, cfg["fit"][0], cfg["fit"][1], cfg["zasp"])
    redrect(fig, spec)
    fig.savefig(os.path.join(OUT, "plot_025_tl.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ── PIL metrics vs the original frame ────────────────────────────────────────
def surface_red(a, ring):
    H, W = a.shape[:2]
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (r >= 100) & (r <= 185) & (g < 60) & (b < 60)
    m[:ring, :] = False
    m[-ring:, :] = False
    m[:, :ring] = False
    m[:, -ring:] = False
    return m


def blue_mask(a, ring):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (b > 120) & (r < 80) & (g < 120)
    m[:ring, :] = False
    m[-ring:, :] = False
    m[:, :ring] = False
    m[:, -ring:] = False
    return m


def hist_l1(a, b):
    """Normalized 16-bin/channel RGB hist L1 over non-chrome pixels."""
    def h(im):
        r, g, bl = im[:, :, 0], im[:, :, 1], im[:, :, 2]
        chrome = (r > 185) & (g < 70) & (bl < 70)
        px = im[~chrome].astype(np.int32)
        idx = (px[:, 0] >> 4) * 256 + (px[:, 1] >> 4) * 16 + (px[:, 2] >> 4)
        hist = np.bincount(idx, minlength=4096).astype(float)
        return hist / hist.sum()
    return float(np.abs(h(a) - h(b)).sum())


def white_frac(a):
    return float(((a[:, :, 0] > 235) & (a[:, :, 1] > 235) & (a[:, :, 2] > 235)).mean())


def metrics():
    orig = np.array(Image.open(ORIG).convert("RGB")).astype(int)
    lines = []
    for name in ("tr", "tl"):
        cand = np.array(Image.open(os.path.join(OUT, "plot_025_%s.png" % name))
                        .convert("RGB")).astype(int)
        x0, y0, x1, y1 = ORIG_RECT[name]
        ref = orig[y0:y1, x0:x1].copy()
        # mask the original's slide-level red line/stroke bands
        for (by0, by1, bx0, bx1) in ORIG_LINE_BANDS[name]:
            ref[max(0, by0 - y0):by1 - y0 + 1, max(0, bx0 - x0):bx1 - x0 + 1] = 255
        # candidate: 300dpi PNG of the figure box -> ring 16px ~ 4 slide px
        cr = surface_red(cand, 16)
        cb = blue_mask(cand, 16)
        rr = surface_red(ref, 6)     # orig frame lines are chrome-red (r>185)
        rb = blue_mask(ref, 6)
        cys, cxs = np.nonzero(cr)
        rys, rxs = np.nonzero(rr)
        bys, bxs = np.nonzero(cb)
        bysr, bxr = np.nonzero(rb)
        CH, CW = cand.shape[:2]
        RH, RW = ref.shape[:2]
        l1 = hist_l1(cand, ref)
        lines.append(
            "%s cand size=%dx%d | red_px=%d bbox=x%d..%d y%d..%d (fx%.2f..%.2f fy%.2f..%.2f) | "
            "blue_px=%d bbox=x%d..%d y%d..%d | white=%.3f | histL1=%.4f || "
            "ORIG ref=%dx%d | red_px=%d bbox=x%d..%d y%d..%d (fx%.2f..%.2f fy%.2f..%.2f) | "
            "blue_px=%d bbox=x%d..%d y%d..%d | white=%.3f"
            % (name, CW, CH,
               int(cr.sum()), cxs.min(), cxs.max(), cys.min(), cys.max(),
               cxs.min() / CW, cxs.max() / CW, cys.min() / CH, cys.max() / CH,
               int(cb.sum()), bxs.min(), bxs.max(), bys.min(), bys.max(),
               white_frac(cand), l1,
               RW, RH,
               int(rr.sum()), rxs.min(), rxs.max(), rys.min(), rys.max(),
               rxs.min() / RW, rxs.max() / RW, rys.min() / RH, rys.max() / RH,
               int(rb.sum()), bxr.min(), bxr.max(), bysr.min(), bysr.max(),
               white_frac(ref)))
    return lines


def main():
    it = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cfg = ITERS[it]
    plot_tr(cfg["tr"])
    plot_tl(cfg["tl"])
    lines = metrics()
    with open(LOG, "a") as f:
        f.write("=== k17t2 iter %d | tr: %s | tl: %s ===\n"
                % (it, cfg["tr"], cfg["tl"]))
        for ln in lines:
            f.write(ln + "\n")
        f.write("\n")
    print("iter %d done" % it)
    for ln in lines:
        print(ln)


if __name__ == "__main__":
    main()
