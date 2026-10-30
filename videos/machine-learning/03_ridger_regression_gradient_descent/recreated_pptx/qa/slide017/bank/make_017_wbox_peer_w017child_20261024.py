#!/usr/bin/env python3
"""Generate slide 017's three W-box interiors as 600-dpi transparent PNGs.

Slide 017 ("Adding Ridge Regularizer to the model λ=3") inherits slide 013's
certified math-image MECHANISM (matplotlib mathtext, STIX serif, exact px/600
placement) — the images carry 017's own measured content, never 013's.

Every number below is PIL-measured from unique_slides/slide_017.jpg (960x540,
1px=1pt); see recreated_pptx/qa/slide017/MEASUREMENTS.md.

Measured differences vs 013 (the parent):
  - NO pale-yellow ||W||^2 ellipse: 017 prints the norm line as plain BLUE ink
    on the white cell (PIL: 0 pale-yellow px in any box interior; 013 has 2176).
  - The norm line is BLUE (frame median (23,12,132)); 013's was olive.
  - The bracket pair hugs the value stack: left paren ~x560, right ~x607.
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
OUTDIR = os.path.join(HERE, "..", "assets")
os.makedirs(OUTDIR, exist_ok=True)
W_PX, H_PX = 115, 123
ORIGIN_X = 507
RED = "#C00000"
BLACK = "#000000"
BLUE = "#0000A7"  # 013's measured blue ink

# per band: y0 = image origin y (frame px); every other value is absolute frame px
BANDS = [
    dict(
        y0=127,
        w_cx=530.0, w_base=179.0,                 # W glyph centre + baseline
        eq=(544, 556, 168, 174),                  # "=" two black bars (x0,x1,ytop,ybot)
        lparen=(562, 559.5, 136, 215),            # (tip, body, ytop, ybot)
        rparen=(607, 610.0, 136, 215),
        digits=[("0.1", 156, 583.0), ("1.95", 180, 583.0), ("0.03", 206, 583.0)],
        norm_y=241.0, norm="3.8",
    ),
    dict(
        y0=265,
        w_cx=535.5, w_base=317.0,
        eq=(550, 562, 305, 311),
        lparen=(560, 557.5, 274, 350),
        rparen=610,  # placeholder, set below
        digits=[("1.2", 293, 588.0), ("0.72", 319, 588.0), ("0.77", 344, 588.0)],
        norm_y=380.5, norm="2.45",
    ),
    dict(
        y0=403,
        w_cx=530.0, w_base=455.0,
        eq=(544, 556, 442, 449),
        lparen=(561, 558.5, 412, 487),
        rparen=(617, 620.0, 412, 487),
        digits=[("1.77", 431, 588.0), ("0.32", 456, 588.0), ("0.99", 482, 588.0)],
        norm_y=518.5, norm="4.2",
    ),
]
# band 2's right paren measured separately (bow reversed: tip left, body right)
BANDS[1]["rparen"] = (607.0, 610.0, 274, 350)

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

    name = "wbox017_band%d.png" % i
    fig.savefig(os.path.join(OUTDIR, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(ORIGIN_X, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(OUTDIR, "wbox017_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
