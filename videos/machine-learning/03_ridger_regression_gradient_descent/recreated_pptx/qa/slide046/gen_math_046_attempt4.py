#!/usr/bin/env python3
"""Slide 046 assets — attempt 4 (frame-true rebuild).

Ground truth: unique_slides/slide_046.jpg (960x540, 1 frame px == 1 pt).
All geometry below is FRAME PX measured by PIL on the original frame:
  - top matrix: 6 PARENTHESISED 2-value COLUMN VECTORS (not horizontal rows)
      x1(1,1) x2(2,1) x3(1,2) x4(5,4) x5(6,5) x6(6,6)
      header y64..73, values y80..88 / y97..104, parens y78..107,
      class row y114..124 (C1 red first three, C2 blue last three)
  - Z matrix: header Z1 Z1 Z1 y64..72; 3 parenthesised columns
      (0,0) (7,6) (3,2)   values y83..91 / y99..107
  - augmented vectors: 6 parenthesised 3-value columns
      (1,1,1) (1,2,1) (1,1,2) (1,5,4) (1,6,5) (1,6,6)
      values y184..192 / y199..207 / y214..222
  - final-weight box vector: 14 / -4 / 0 between tall parens x786 / x822,
      rows y67..83, y86..105, y118..133
  - scatter plot: red border x312..825 y173..482; data area x0=362.5, x8=784.5,
      y0=429.5, y7=214.5; red decision line x=546 (data 3.478) y193..447;
      markers per the frame; "+ve" red with a LEFT arrow at y~219.

Mechanism (deck equation law): matplotlib -> transparent PNG at 600 dpi ->
addImage at EXACT px/600 size (never rescaled).
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
DPI = 600


def _new_fig(w_px, h_px):
    fig = plt.figure(figsize=(w_px / 72.0, h_px / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_px)
    ax.set_ylim(h_px, 0)          # y grows downward like frame px
    ax.axis("off")
    return fig, ax


def _save(fig, name, transparent=True):
    path = os.path.join(ASSETS, name)
    fig.savefig(path, dpi=DPI, transparent=transparent, facecolor="white")
    plt.close(fig)
    im = Image.open(path)
    a = np.asarray(im)
    alpha = a[:, :, 3]
    ys, xs = np.nonzero(alpha > 8)
    ink = ((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
           if len(xs) else None)
    info = {"image": name, "w_px": im.size[0], "h_px": im.size[1],
            "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5),
            "ink_600px": ink, "ink_px72": tuple(round(v * 72.0 / DPI, 2) for v in ink) if ink else None}
    with open(os.path.join(ASSETS, name.replace(".png", ".json")), "w") as f:
        json.dump(info, f, indent=1)
    print(json.dumps(info))
    return info


def column(name, vals, w_px, h_px, digit_ys, digit_fs, paren_inset, color="000000"):
    """One parenthesised column vector: digits at explicit frame-relative y.

    Parens are drawn as thin quadratic Beziers (the frame's delimiters are
    STRETCHED math parens: ~1 px thick over a 29-46 px span, not a typewriter
    '(' glyph, whose advance would be ~9 px and overlap the digits).
    """
    fig, ax = _new_fig(w_px, h_px)
    cx = w_px / 2.0
    y0, y1 = paren_inset, h_px - paren_inset
    ym = (y0 + y1) / 2.0
    for is_left in (True, False):
        if is_left:
            xa, xb = 2.7, 0.9
        else:
            xa, xb = w_px - 2.7, w_px - 0.9
        p = Path([(xa, y0), (xb, ym), (xa, y1)],
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3])
        ax.add_patch(PathPatch(p, fill=False, color="#" + color, lw=0.9,
                               capstyle="round", clip_on=False))
    for v, y in zip(vals, digit_ys):
        ax.text(cx, y, v, fontsize=digit_fs, ha="center", va="center", color="#" + color)
    return _save(fig, name)


def plot(name):
    """Scatter plot reproduced from the frame's measured calibration."""
    W, H = 513, 309                      # plot frame x312..825, y173..482
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=DPI, facecolor="white")
    # figure-level red border (the frame's outer red box)
    fig.add_artist(Rectangle((0.002, 0.002), 0.996, 0.996, transform=fig.transFigure,
                             fill=False, edgecolor="#C00000", linewidth=0.9))
    left = (362.5 - 312) / W
    bottom = (482 - 429.5) / H
    ax = fig.add_axes([left, bottom, (784.5 - 362.5) / W, (429.5 - 214.5) / H])
    ax.set_xlim(0, 8); ax.set_ylim(0, 7)
    ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color("#CFD2CF"); s.set_linewidth(0.8)
    for y in range(0, 8):
        ax.axhline(y, color="#E2E4E1", lw=0.7, zorder=0)
    ax.set_xticks(range(0, 9)); ax.set_yticks(range(0, 8))
    ax.tick_params(axis="both", length=0, pad=1.5, labelsize=8, colors="#333333")
    ax.set_xticklabels([str(v) for v in range(0, 9)], fontsize=8)
    ax.set_yticklabels([str(v) for v in range(0, 8)], fontsize=8)
    # decision boundary (measured x=546 frame -> data 3.478), overshoots axes
    ax.plot([3.478, 3.478], [-0.57, 7.70], color="#C00000", lw=1.7, clip_on=False, zorder=4)
    # markers (frame-measured centres == these data coords)
    ax.scatter([1, 1, 2], [2, 1, 1], marker="s", s=68, color="#1F497D", zorder=5, linewidths=0)
    ax.scatter([5, 6, 6], [4, 5, 6], marker="D", s=30, color="#FF00FF", zorder=5, linewidths=0)
    ax.scatter([3, 7, 0], [2, 6, 0], marker="v", s=48, color="#CC0000", zorder=5, linewidths=0)
    # "+ve" + left-pointing arrow just above the y=7 gridline
    ax.text(2.24, 7.38, "+ve", color="#C00000", fontsize=12, ha="left", va="center",
            clip_on=False, zorder=6)
    ax.annotate("", xy=(2.72, 6.84), xytext=(3.46, 6.84),
                arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.2,
                                mutation_scale=11, shrinkA=0, shrinkB=0),
                annotation_clip=False, zorder=6)
    return _save(fig, name, transparent=False)


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    # ---- top matrix columns: 6 columns, 2 values, bbox y77..109 (h 32) ----
    top = [("1", "1"), ("2", "1"), ("1", "2"), ("5", "4"), ("6", "5"), ("6", "6")]
    for i, vals in enumerate(top, start=1):
        column("m046_topcol%d.png" % i, vals, 15, 32, [7, 23.5], 10.5, 1.5)
    # ---- Z matrix columns: 3 columns, 2 values, bbox y79..111 (h 32) ----
    z = [("0", "0"), ("7", "6"), ("3", "2")]
    for i, vals in enumerate(z, start=1):
        column("m046_zcol%d.png" % i, vals, 15, 32, [8, 24], 10.5, 1.5)
    # ---- augmented matrix columns: 6 columns, 3 values, bbox y178..228 (h 50) ----
    aug = [("1", "1", "1"), ("1", "2", "1"), ("1", "1", "2"),
           ("1", "5", "4"), ("1", "6", "5"), ("1", "6", "6")]
    for i, vals in enumerate(aug, start=1):
        column("m046_augcol%d.png" % i, vals, 15, 50, [9, 25, 41], 10.5, 2.0)
    # ---- initial W vector: parens + 4 / -2 / -2, bbox x331..371 y56..108 ----
    column("m046_vec_initial.png", ("4", "-2", "-2"), 41, 47, [12, 26, 40], 15, 2.0)
    # ---- final W vector: parens + 14 / -4 / 0, bbox x784..826 y57..142 ----
    column("m046_vec_final.png", ("14", "-4", "0"), 43, 70, [9, 29, 59], 22, 2.5)
    # ---- scatter plot ----
    plot("m046_plot.png")
