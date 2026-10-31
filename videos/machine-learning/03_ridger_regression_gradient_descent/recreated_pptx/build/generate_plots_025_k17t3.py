#!/usr/bin/env python3
"""k17t3: slide 025 BL-panel-only regeneration (shard: BL; TR/TL owned elsewhere).

Ground truth (task + build/slide_025.js header + analysis/slide_025_final.json,
PIL-verified against unique_slides/slide_025.jpg 2026-10-31):
  BL image placed at slide x83 y290 w293 h237 -> asset 1220x987 @300dpi
  (scale 4.1638 asset px per slide px). Red rect measured x86..372 y294..524,
  red line y418 x126..381, red X comps centered ~(199.5,445) and (270,482.5).
  Four two-line black labels (slide px anchor boxes):
    "Global Maxima" x242..268 y304..319 | "Local Maxima" x286..315 y337..352
    "Local Minima"  x286..311 y390..399 | "Global Minima" x145..201 y439..465
  Judge k17z2 additionally wants: grey dotted 3D bounding box-wire grid,
  numeric z-axis -6..6 and x/y numerals 6/4/2/0/-2/-4.
  Labels SMALL (~15 slide-px box height, two lines), red X must not overlap
  label ink.

Writes $W/assets_k17t3/plot_025_bl.png (exactly 1220x987) and appends a
PIL-compare block vs the original BL crop x60..470 y296..527 to
$W/k17t3_iter.log. No pptx promotion.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx", "qa", "rejudge_20261027")
W = os.path.join(RJ, "slide025")
OUT = os.path.join(W, "assets_k17t3")
LOG = os.path.join(W, "k17t3_iter.log")
os.makedirs(OUT, exist_ok=True)

DPI = 300
# promoted asset pixel size (PIL-checked build/assets/plot_025_bl.png)
AW, AH = 1220, 987
# slide placement of the BL image (slide_025.js): x83 y290 293x237 slide px
SX0, SY0, SW, SH = 83, 290, 293, 237
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)
BLK = (0.0, 0.0, 0.0)
TICKC = "#333333"

# slide-px anchor boxes (task ground truth) -> centers
LABELS = [
    ("Global\nMaxima", (242 + 268) / 2, (304 + 319) / 2),
    ("Local\nMaxima", (286 + 315) / 2, (337 + 352) / 2),
    ("Local\nMinima", (286 + 311) / 2, (390 + 399) / 2),
    ("Global\nMinima", (145 + 201) / 2, (439 + 465) / 2),
]
LABEL_BOXES = {  # slide px, for the PIL compare
    "Global Maxima": (242, 304, 268, 319),
    "Local Maxima": (286, 337, 315, 352),
    "Local Minima": (286, 390, 311, 399),
    "Global Minima": (145, 439, 201, 465),
}
MARKERS = [(199, 445), (270, 482)]       # slide px red X centers
REDLINE = (124, 418, 381, 418)            # slide px red horizontal line
REDRECT = (86, 294, 372, 524)             # slide px red rectangle (PIL-measured)

# tunables (adjusted across iterations)
CFG = dict(
    fontsize=8.6,
    label_dx=0.0, label_dy=0.0,
    gm_dx=-9.0,           # shift "Global Minima" left so the X at (199,445) clears the glyphs
    axes_rect=(0.135, 0.095, 0.835, 0.85),
    zpad=-3.0,
    elev=30, azim=-60,
    zoom=1.0,
    tick_fs=6.4,
    marker_ms=13.0, marker_mew=2.2,
    line_lw=1.1,
)


def s2f(sx, sy):
    """slide px -> figure fraction (image placed at SX0,SY0 size SW,SH)."""
    return ((sx - SX0) / SW, 1.0 - (sy - SY0) / SH)


def bl_surface(X, Y):
    return (6.0 * np.exp(-((X - 1.0) ** 2 + (Y - 2.0) ** 2) / 6.0)
            + 4.0 * np.exp(-((X + 2.0) ** 2 + (Y - 5.0) ** 2) / 5.0)
            - 6.0 * np.exp(-((X + 2.0) ** 2 + (Y + 2.0) ** 2) / 4.0)
            - 4.5 * np.exp(-((X - 4.0) ** 2 + (Y + 1.0) ** 2) / 5.0)
            + 0.5 * np.sin(0.9 * X) * np.cos(0.8 * Y))


def plot_bl():
    fig = plt.figure(figsize=(SW / 72.0, SH / 72.0), dpi=DPI)
    ax = fig.add_axes(CFG["axes_rect"], projection="3d")
    ax.view_init(elev=CFG["elev"], azim=CFG["azim"])
    x = np.linspace(-5, 7, 110)
    X, Y = np.meshgrid(x, x)
    Z = np.clip(bl_surface(X, Y), -6.0, 6.0)
    ax.plot_surface(X, Y, Z, cmap=JET, norm=Normalize(-6, 6.5), shade=False,
                    antialiased=True, rstride=2, cstride=2, linewidth=0.15,
                    edgecolor=(0.55, 0.55, 0.55, 0.35))
    ax.set_xlim(-5, 7); ax.set_ylim(-5, 7); ax.set_zlim(-6, 6.8)
    ax.set_xticks([-4, -2, 0, 2, 4, 6])
    ax.set_yticks([-4, -2, 0, 2, 4, 6])
    ax.set_zticks([-6, -4, -2, 0, 2, 4, 6])
    # grey dotted bounding box-wire grid + numerals (judge k17z2)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0.0))
        axis._axinfo["grid"].update(color="#9A9A9A", linewidth=0.5,
                                    linestyle=":")
        axis.line.set_linewidth(0.6)
        axis.line.set_color("#8A8A8A")
    ax.grid(True)
    ax.tick_params(pad=0.5, labelsize=CFG["tick_fs"], length=2.0, width=0.5,
                   colors=TICKC)
    ax.zaxis.set_tick_params(pad=CFG["zpad"])
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(CFG["tick_fs"])
        t.set_color(TICKC)
    ax.set_box_aspect((1, 1, 0.82), zoom=CFG["zoom"])

    # leader lines: label -> its extremum projection on the surface
    feats = [(1.0, 2.0, 6.0), (-2.0, 5.0, 4.0), (-2.0, 2.0, -6.0), (4.0, -1.0, -4.5)]
    fig.canvas.draw()
    for (txt, sx, sy), (fx, fy, fz) in zip(LABELS, feats):
        x2, y2, _ = proj3d.proj_transform(fx, fy, fz, ax.get_proj())
        disp = ax.transData.transform([(x2, y2)])[0]
        Wp = ax.figure.get_size_inches()[0] * DPI
        Hp = ax.figure.get_size_inches()[1] * DPI
        pf = (disp[0] / Wp, 1.0 - disp[1] / Hp)
        lf = s2f(sx, sy)
        fig.add_artist(Line2D([lf[0], pf[0]], [lf[1], pf[1]],
                              transform=fig.transFigure, color=BLK, lw=0.55,
                              zorder=44, solid_capstyle="butt", alpha=0.85))

    # four small two-line black labels at the anchor centers
    for txt, sx, sy in LABELS:
        dx = CFG["label_dx"] + (CFG["gm_dx"] if txt == "Global\nMinima" else 0.0)
        fx, fy = s2f(sx + dx, sy + CFG["label_dy"])
        fig.text(fx, fy, txt, fontsize=CFG["fontsize"], color=BLK,
                 ha="center", va="center", zorder=45, linespacing=1.05,
                 fontweight="normal")

    # red horizontal reference line (slide y418 x124..381)
    (ax0, ay0), (ax1, ay1) = s2f(REDLINE[0], REDLINE[1]), s2f(REDLINE[2], REDLINE[3])
    fig.add_artist(Line2D([ax0, ax1], [ay0, ay1], transform=fig.transFigure,
                          color=RED, lw=CFG["line_lw"], zorder=46,
                          solid_capstyle="butt"))
    # two red X markers at the measured slide coords
    for mx, my in MARKERS:
        fx, fy = s2f(mx, my)
        ln = Line2D([fx], [fy], transform=fig.transFigure, marker="x",
                    color=RED, markersize=CFG["marker_ms"],
                    markeredgewidth=CFG["marker_mew"], zorder=47,
                    linestyle="none")
        fig.add_artist(ln)
    # thin red rectangle (PIL-measured x86..372 y294..524)
    x0, y1 = s2f(REDRECT[0], REDRECT[1])
    x1, y0 = s2f(REDRECT[2], REDRECT[3])
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=48,
                              solid_capstyle="butt"))
    path = os.path.join(OUT, "plot_025_bl.png")
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    im = Image.open(path).convert("RGB")
    if im.size != (AW, AH):
        im = im.resize((AW, AH), Image.LANCZOS)
        im.save(path, dpi=(DPI, DPI))
    return path


# ── PIL compare vs original BL crop x60..470 y296..527 ──────────────────────
CROP = (60, 296, 470, 527)  # slide px x0,y0,x1,y1 (exclusive x1/y1 -> 411x231)


def red_mask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R > 110) & (G < 120) & (B < 120) & (R - G > 50) & (R - B > 50)


def dark_mask(a):
    return a.max(2) < 180


def compare(gen_path, iter_tag):
    orig = np.asarray(Image.open(os.path.join(NS, "unique_slides", "slide_025.jpg"))
                      .convert("RGB")).astype(int)
    cx0, cy0, cx1, cy1 = CROP
    ocrop = orig[cy0:cy1 + 1, cx0:cx1 + 1]
    gen = Image.open(gen_path).convert("RGB")
    g = np.asarray(gen.resize((SW, SH), Image.LANCZOS)).astype(int)
    # paste generated (slide x83..376 y290..527) into the crop frame (x60..470 y296..527)
    gcanvas = np.full(ocrop.shape, 255, dtype=int)
    ox, oy = SX0 - cx0, SY0 - cy0
    gh, gw = g.shape[:2]
    r0, r1 = max(0, oy), min(ocrop.shape[0], oy + gh)
    c0, c1 = max(0, ox), min(ocrop.shape[1], ox + gw)
    gcanvas[r0:r1, c0:c1] = g[r0 - oy:r1 - oy, c0 - ox:c1 - ox]

    lines = [f"== k17t3 iter {iter_tag} ==", f"asset {gen_path} size {gen.size}"]
    for name, a in (("orig", ocrop), ("gen", gcanvas)):
        rm = red_mask(a)
        ys, xs = np.nonzero(rm)
        if len(xs):
            lines.append(f"{name}: red px={len(xs)} bbox slide x{cx0+xs.min()}..{cx0+xs.max()} "
                         f"y{cy0+ys.min()}..{cy0+ys.max()}")
        else:
            lines.append(f"{name}: red px=0")
    for name, box in LABEL_BOXES.items():
        bx0, by0, bx1, by1 = box
        sub_o = ocrop[by0 - cy0:by1 - cy0 + 1, bx0 - cx0:bx1 - cx0 + 1]
        sub_g = gcanvas[by0 - cy0:by1 - cy0 + 1, bx0 - cx0:bx1 - cx0 + 1]
        out = []
        for tag, sub in (("orig", sub_o), ("gen", sub_g)):
            dm = dark_mask(sub)
            ys, xs = np.nonzero(dm)
            if len(xs):
                out.append(f"{tag}: ink={len(xs)} bbox x{bx0+xs.min()}..{bx0+xs.max()} "
                           f"y{by0+ys.min()}..{by0+ys.max()}")
            else:
                out.append(f"{tag}: ink=0")
        lines.append(f"label '{name}' box x{bx0}..{bx1} y{by0}..{by1}: " + " | ".join(out))
    for i, (mx, my) in enumerate(MARKERS):
        win = 10
        sub_o = ocrop[my - win - cy0:my + win - cy0 + 1, mx - win - cx0:mx + win - cx0 + 1]
        sub_g = gcanvas[my - win - cy0:my + win - cy0 + 1, mx - win - cx0:mx + win - cx0 + 1]
        ro, rg = red_mask(sub_o), red_mask(sub_g)
        lines.append(f"marker{i} slide({mx},{my}) +-{win}: orig red px={int(ro.sum())} "
                     f"gen red px={int(rg.sum())}")
    # overlap: red px inside gen label ink bbox (expanded 2px)
    rg = red_mask(gcanvas)
    for name, box in LABEL_BOXES.items():
        bx0, by0, bx1, by1 = box
        sub = gcanvas[by0 - cy0:by1 - cy0 + 1, bx0 - cx0:bx1 - cx0 + 1]
        dm = dark_mask(sub)
        if dm.sum() == 0:
            lines.append(f"overlap '{name}': no gen ink")
            continue
        ys, xs = np.nonzero(dm)
        r0, r1 = max(0, ys.min() - 2), min(dm.shape[0], ys.max() + 3)
        c0, c1 = max(0, xs.min() - 2), min(dm.shape[1], xs.max() + 3)
        n = int(rg[by0 - cy0 + r0:by0 - cy0 + r1, bx0 - cx0 + c0:bx0 - cx0 + c1].sum())
        lines.append(f"overlap '{name}': red px within gen ink bbox+2 = {n}")
    # z-numeral strip (left edge inside frame): dark ink count, slide scale
    strip_o = ocrop[300 - cy0:520 - cy0, 88 - cx0:125 - cx0]
    strip_g = gcanvas[300 - cy0:520 - cy0, 88 - cx0:125 - cx0]
    lines.append(f"z-strip dark ink: orig={int(dark_mask(strip_o).sum())} "
                 f"gen={int(dark_mask(strip_g).sum())}")
    # asset-space tick numerals (native res, left strip + bottom strip)
    ga = np.asarray(Image.open(gen_path).convert("RGB")).astype(int)
    gm = ga.max(2) < 160
    left = int(gm[40:930, 20:210].sum())
    bottom = int(gm[890:985, 210:1100].sum())
    lines.append(f"asset-space tick ink: left(z)={left} bottom(x/y)={bottom}")
    txt = "\n".join(lines) + "\n"
    with open(LOG, "a") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    import sys
    tag = sys.argv[1] if len(sys.argv) > 1 else "1"
    p = plot_bl()
    compare(p, tag)
    print("done", p)
