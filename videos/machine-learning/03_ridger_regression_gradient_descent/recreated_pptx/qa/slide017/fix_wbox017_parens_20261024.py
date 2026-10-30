#!/usr/bin/env python3
"""Fix slide 017's W-box images: regenerate the three interiors with paren tips
and norm lines re-measured against unique_slides/slide_017.jpg.

Copy-then-modify of bank/make_017_wbox_peer_w017child_20261024.py (banked, never
edited). Measured corrections (qa/slide017/adjudicate_fails_*.py):
  - right paren tip: frame ink ends x~605 in ALL three bands (the prior script
    drew band 3's tip at 617 -> +14px defect); rtip=602.5 for every band
  - norm line: frame spans 520..606 (B1/B3) and 520..618 (B2); centre per band
  - left paren tip 557.5 / right body 606.0 as measured on the frame
Everything else (W, =, digits, baselines) is carried over unchanged.
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
OUTDIR = os.path.normpath(os.path.join(HERE, "..", "..", "build", "assets"))
os.makedirs(OUTDIR, exist_ok=True)
W_PX, H_PX = 115, 123
ORIGIN_X = 507
RED = "#C00000"
BLACK = "#000000"
BLUE = "#0000A7"

# per band: y0 = image origin y (frame px); every other value is absolute frame px
BANDS = [
    dict(
        y0=127,
        w_cx=530.0, w_base=179.0,
        eq=(544, 556, 168, 174),
        lparen=(557.5, 560.5, 136, 215),
        rparen=(602.5, 606.0, 136, 215),
        digits=[("0.1", 156, 583.0), ("1.95", 180, 583.0), ("0.03", 206, 583.0)],
        norm_centre=563.0, norm_y=241.0, norm="3.8",
    ),
    dict(
        y0=265,
        w_cx=535.5, w_base=317.0,
        eq=(550, 562, 305, 311),
        lparen=(557.5, 560.5, 274, 350),
        rparen=(602.5, 606.0, 274, 350),
        digits=[("1.2", 293, 588.0), ("0.72", 319, 588.0), ("0.77", 344, 588.0)],
        norm_centre=569.0, norm_y=380.5, norm="2.45",
    ),
    dict(
        y0=403,
        w_cx=530.0, w_base=455.0,
        eq=(544, 556, 442, 449),
        lparen=(557.5, 560.5, 412, 487),
        rparen=(602.5, 606.0, 412, 487),
        digits=[("1.77", 431, 588.0), ("0.32", 456, 588.0), ("0.99", 482, 588.0)],
        norm_centre=563.0, norm_y=518.5, norm="4.2",
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

    # ---- ||W||^2 norm line: BLUE ink, NO ellipse (017's measured form) ----
    ax.text(b["norm_centre"], b["norm_y"], r"$\|W\|^2 = %s$" % b["norm"],
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

    # ---- stacked vector values (serif 22pt, baseline at the measured ink bottom) ----
    for txt, base, cx in b["digits"]:
        ax.text(cx, base, txt, fontsize=22, color=BLACK, ha="center",
                va="baseline", zorder=3)

    name = "wbox017_band%d.png" % i
    fig.savefig(os.path.join(OUTDIR, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(ORIGIN_X, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(OUTDIR, "wbox017_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
