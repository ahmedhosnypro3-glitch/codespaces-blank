#!/usr/bin/env python3
"""Generate slide 013's three W-box interiors as 600-dpi transparent PNGs.

Region per band = the W box's interior in frame px (960x540 frame, 1px = 1pt):
  origin (507, 128/266/404), size 115 x 123 px.
Everything is placed in frame-px coordinates measured from
unique_slides/slide_013.jpg (see qa/slide013/measure_013_final*.txt):
  "W" bold-italic serif red + underline; black "=" bars; two thin black
  parentheses (cubic Beziers, 1pt); the stacked vector values (serif, 22pt);
  the pale-yellow ||W||^2 ellipse + olive italic text with a real superscript.

matplotlib mathtext (STIX = Times-like) is the deck's certified mechanism for
math; placeholders are exact px/600 inches, never rescaled.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, PathPatch
from matplotlib.path import Path
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "stix"
rcParams["font.family"] = "Liberation Serif"

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = HERE
W_PX, H_PX = 115, 123
RED = "#C00000"
BLACK = "#000000"
OLIVE = "#808000"
ELL = "#FBFF85"

# per band: y0 = image origin y; measured items in absolute frame px
BANDS = [
    dict(y0=128, w_base=177.0, w_cx=535.0, eq=(549, 561, 168, 173),       # "=" bar rows
         lparen=(567, 564.5, 135, 214), rparen=(583, 586.0, 135, 212),   # tip, body, ytop, ybot
         digits=[("0", 156, 575.5), ("2", 181, 575.5), ("0", 206, 575.5)],
         ell=(564.5, 231.0, 105, 36), etext="4"),
    dict(y0=266, w_base=313.0, w_cx=534.5, eq=(549, 561, 306, 311),
         lparen=(567, 564.5, 272, 352), rparen=(610, 612.0, 272, 349),
         digits=[("2.7", 293, 588.5), ("0.67", 319, 588.5), ("0.64", 344, 588.5)],
         ell=(567.0, 369.0, 104, 36), etext="8.11"),
    dict(y0=404, w_base=452.0, w_cx=535.0, eq=(549, 561, 444, 449),
         lparen=(567, 564.5, 410, 488), rparen=(610, 612.0, 410, 487),
         digits=[("4", 431, 588.5), ("0.29", 457, 588.5), ("0.78", 482, 588.5)],
         ell=(569.5, 507.0, 103, 36), etext="16.7"),
]

sidecar = []
for i, b in enumerate(BANDS, start=1):
    y0 = b["y0"]
    fig = plt.figure(figsize=(W_PX / 72.0, H_PX / 72.0), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(507, 507 + W_PX)
    ax.set_ylim(y0 + H_PX, y0)          # inverted y: frame coordinates
    ax.axis("off")
    fig.patch.set_alpha(0)

    # ellipse (pale yellow) + text
    ex, ey, ew, eh = b["ell"]
    ax.add_patch(Ellipse((ex, ey), ew, eh, facecolor=ELL, edgecolor="none", zorder=1))
    ax.text(ex, ey, r"$\|W\|^2 = %s$" % b["etext"], fontsize=20, color=OLIVE,
            ha="center", va="center", zorder=2)

    # "W" italic math glyph red (STIX, measured 17x15) on its measured baseline,
    # with the frame's red underline bar at y177.5..179 (x527..544).
    wx = b["w_cx"]
    ax.text(wx, b["w_base"], r"$W$", fontsize=21, color=RED,
            ha="center", va="baseline", zorder=3)
    ax.plot([wx - 8.5, wx + 8.5], [b["w_base"] + 1.6, b["w_base"] + 1.6],
            color=RED, lw=1.6, zorder=3)

    # "=" two black bars
    x0, x1, ytop, ybot = b["eq"]
    for yy in (ytop, ybot):
        ax.plot([x0, x1], [yy + 0.5, yy + 0.5], color=BLACK, lw=1.4, zorder=3)

    # parentheses as cubic Beziers
    for tip, body, yt, yb in (b["lparen"], b["rparen"]):
        verts = [(tip, yt), (body, yt + 18), (body, yb - 18), (tip, yb)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                               edgecolor=BLACK, lw=0.9, zorder=3))

    # vector values (serif, 22pt, baseline at the measured ink bottom)
    for txt, base, cx in b["digits"]:
        ax.text(cx, base, txt, fontsize=22, color=BLACK, ha="center",
                va="baseline", zorder=3)

    name = "wbox_band%d.png" % i
    fig.savefig(os.path.join(OUTDIR, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(507, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(OUTDIR, "wbox_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
