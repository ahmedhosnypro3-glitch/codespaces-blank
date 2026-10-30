#!/usr/bin/env python3
"""Generate slide 018's three W-box interiors as 600-dpi transparent PNGs.

Slide 018 ("Adding Ridge Regularizer to the model λ=10") inherits slide 017's
certified math-image MECHANISM (matplotlib mathtext, STIX serif, exact px/600
placement, BLUE ||W||^2 line, NO ellipse) — the images carry 018's own
PIL-measured content, never 017's.

Every number below is PIL-measured from unique_slides/slide_018.jpg (960x540,
1px=1pt); see recreated_pptx/qa/slide018/measure_018.txt. Differences vs 017
(measured):
  - values/norms: 018's own vector digits + norm values (3.5 / 1.48 / 1.92)
  - title lambda run is ALL BLUE in 018 (017 used blue λ + red "=3")
Mechanism/geometry inherited from the banked
qa/slide017/bank/make_017_wbox_peer_w017child_20261024.py.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "stix"
rcParams["font.family"] = "Liberation Serif"

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "..", "..", "..", "build", "assets")
os.makedirs(OUTDIR, exist_ok=True)
W_PX, H_PX = 115, 123
ORIGIN_X = 507
RED = "#C00000"
BLACK = "#000000"
BLUE = "#0000A7"  # measured norm-line blue ink (24,10,141)

# per band: y0 = image origin y (frame px); every other value is absolute frame px
BANDS = [
    dict(
        y0=127,
        w_cx=530.0, w_base=179.0,                 # W glyph centre + baseline
        eq=(544, 556, 168, 174),                  # "=" two black bars (x0,x1,ytop,ybot)
        lparen=(562, 559.5, 136, 215),            # (tip, body, ytop, ybot)
        rparen=(607, 610.0, 136, 215),
        digits=[("0.13", 156, 583.0), ("1.87", 180, 583.0), ("0.09", 206, 583.0)],
        norm_y=241.5, norm="3.5",
    ),
    dict(
        y0=265,
        w_cx=535.5, w_base=317.0,
        eq=(550, 562, 305, 311),
        lparen=(560, 557.5, 274, 350),
        rparen=(607, 610.0, 274, 350),  # band 2's right paren: bow same as band 1
        digits=[("0.54", 293, 583.0), ("0.73", 319, 583.0), ("0.81", 344, 583.0)],
        norm_y=379.5, norm="1.48",
    ),
    dict(
        y0=403,
        w_cx=530.0, w_base=455.0,
        eq=(544, 556, 442, 449),
        lparen=(561, 558.5, 412, 487),
        rparen=(617, 620.0, 412, 487),
        digits=[("0.82", 431, 583.0), ("0.33", 456, 583.0), ("1.1", 482, 583.0)],
        norm_y=517.5, norm="1.92",
    ),
]

sidecar = []
for i, b in enumerate(BANDS, start=1):
    y0 = b["y0"]
    fig = plt.figure(figsize=(W_PX / 72.0, H_PX / 72.0), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(ORIGIN_X, ORIGIN_X + W_PX)
    ax.set_ylim(y0 + H_PX, y0)  # inverted y: frame coordinates
    ax.axis("off")
    fig.patch.set_alpha(0)

    # ---- ||W||^2 norm line: BLUE ink, NO ellipse (018's measured form) ----
    ax.text((519 + 607) / 2.0, b["norm_y"], r"$\|W\|^2 = %s$" % b["norm"],
            fontsize=20, color=BLUE, ha="center", va="baseline", zorder=2)

    # ---- "W" italic math glyph, red, with the frame's red underline bar ----
    ax.text(b["w_cx"], b["w_base"], r"$W$", fontsize=21, color=RED,
            ha="center", va="baseline", zorder=3)
    ax.plot([b["w_cx"] - 9.0, b["w_cx"] + 9.0],
            [b["w_base"] + 1.6, b["w_base"] + 1.6], color=RED, lw=1.6, zorder=3)

    # ---- "=" two black bars ----
    x0, x1, ytop, ybot = b["eq"]
    for yy in (ytop, ybot):
        ax.plot([x0, x1], [yy + 0.5, yy + 0.5], color=BLACK, lw=1.4, zorder=3)

    # ---- parentheses as cubic Beziers (tip at the outer end, body bows in) ----
    for tip, body, yt, yb in (b["lparen"], b["rparen"]):
        verts = [(tip, yt), (body, yt + 20), (body, yb - 20), (tip, yb)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                               edgecolor=BLACK, lw=0.9, zorder=3))

    # ---- stacked vector values (serif 22pt, baseline at the measured ink bottom)
    for txt, base, cx in b["digits"]:
        ax.text(cx, base, txt, fontsize=22, color=BLACK, ha="center",
                va="baseline", zorder=3)

    name = "wbox018_band%d.png" % i
    fig.savefig(os.path.join(OUTDIR, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(ORIGIN_X, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(OUTDIR, "wbox018_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
