#!/usr/bin/env python3
"""Generate slide 017's three W-box interiors as 600-dpi transparent PNGs.

Region per band = the W box's interior in frame px (960x540, 1px = 1pt):
  origin (507, 128/266/404), size 115 x 123 px  (parent 013's certified W-box
  origin/size; re-measured on 017's frame: border centreline x507..622,
  y127..251 / 265..389 / 403..527).

Contents (all measured from unique_slides/slide_017.jpg; numbers banked in
qa/slide017/measure_017.txt):
  * red italic serif "W" with a red underline bar
  * black "=" (two bars)
  * thin black parentheses spanning the three stacked values
  * the three vector values, black serif (0.1/1.95/0.03 | 1.2/0.72/0.77 |
    1.77/0.32/0.99) at the frame's measured baselines
  * the blue ||W||^2 = <value> line (3.8 | 2.45 | 4.2) with a blue underline
    under the W, typeset as measured glyph-group positions
  Unlike slide 013 there is NO pale-yellow ellipse on 017 (PIL: 0 pale-yellow px
  inside the three boxes).

matplotlib mathtext (STIX = Times-like) is the deck's certified mechanism for
math; images are placed at exact px/600 inches, never rescaled. The 013 parent
supplied the mechanism only — every coordinate/value here is 017's own.
Closed-loop: font sizes were tuned so each digit line's ink height lands within
1px of the frame (see qa/slide017/wbox17_compare.txt).
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
W_PX, H_PX = 115, 123
ORIGIN_X = 507
RED = "#C00000"
BLACK = "#000000"
BLUE = "#0000A7"

# per band: y0 = interior origin y; every item coordinate is ABSOLUTE frame px
BANDS = [
    dict(y0=128,
         w=dict(cx=530.0, base=172.4, under=(521.0, 538.5, 178.0)),
         eq=dict(x0=543.0, x1=555.5, y1=168.6, y2=173.6),
         parens=dict(ltip=560.2, lbody=557.5, rtip=603.8, rbody=606.5, yt=137.0, yb=211.5),
         digits=[("0.1", 582.5, 156.0), ("1.95", 582.5, 180.5), ("0.03", 582.5, 206.0)],
         norm=dict(bar1=524.0, w=530.0, bar2=551.0, eq=567.0, val=582.0,
                   base=239.0, text="3.8", wunder=(530.0, 546.0))),
    dict(y0=266,
         w=dict(cx=535.5, base=310.5, under=(528.5, 543.5, 315.5)),
         eq=dict(x0=549.0, x1=560.5, y1=306.5, y2=311.7),
         parens=dict(ltip=563.7, lbody=561.0, rtip=608.3, rbody=611.0, yt=274.0, yb=350.0),
         digits=[("1.2", 588.5, 293.0), ("0.72", 588.5, 318.5), ("0.77", 588.5, 344.0)],
         norm=dict(bar1=521.5, w=531.0, bar2=551.0, eq=568.0, val=583.0,
                   base=376.3, text="2.45", wunder=(531.0, 547.0))),
    dict(y0=404,
         w=dict(cx=530.5, base=449.0, under=(522.0, 539.0, 455.0)),
         eq=dict(x0=544.0, x1=555.5, y1=444.5, y2=449.5),
         parens=dict(ltip=560.2, lbody=557.5, rtip=603.8, rbody=606.5, yt=412.0, yb=487.0),
         digits=[("1.77", 583.0, 431.0), ("0.32", 583.0, 456.0), ("0.99", 583.0, 482.0)],
         norm=dict(bar1=521.5, w=530.0, bar2=551.0, eq=567.0, val=582.0,
                   base=513.3, text="4.2", wunder=(530.0, 546.0))),
]

DIGIT_FS = 20.0      # closed loop: STIX digit ink 13.5px == frame 13-14px
W_FS = 19.5
NORM_FS = 19.0

sidecar = []
for i, b in enumerate(BANDS, start=1):
    y0 = b["y0"]
    fig = plt.figure(figsize=(W_PX / 72.0, H_PX / 72.0), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(ORIGIN_X, ORIGIN_X + W_PX)
    ax.set_ylim(y0 + H_PX, y0)          # inverted y: frame coordinates
    ax.axis("off")
    fig.patch.set_alpha(0)

    # ── "W" red italic + red underline ──────────────────────────────────────
    W = b["w"]
    ax.text(W["cx"], W["base"], r"$W$", fontsize=W_FS, color=RED,
            ha="center", va="baseline", zorder=3)
    ax.plot([W["under"][0], W["under"][1]], [W["under"][2], W["under"][2]],
            color=RED, lw=1.6, zorder=3)

    # ── "=" two black bars ──────────────────────────────────────────────────
    E = b["eq"]
    for yy in (E["y1"], E["y2"]):
        ax.plot([E["x0"], E["x1"]], [yy, yy], color=BLACK, lw=1.5, zorder=3)

    # ── parentheses as cubic Beziers ────────────────────────────────────────
    P = b["parens"]
    for tip, body in ((P["ltip"], P["lbody"]), (P["rtip"], P["rbody"])):
        verts = [(tip, P["yt"]), (body, P["yt"] + 18), (body, P["yb"] - 18), (tip, P["yb"])]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        ax.add_patch(PathPatch(Path(verts, codes), facecolor="none",
                               edgecolor=BLACK, lw=0.9, zorder=3))

    # ── stacked vector values ───────────────────────────────────────────────
    for txt, cx, base in b["digits"]:
        ax.text(cx, base, txt, fontsize=DIGIT_FS, color=BLACK,
                ha="center", va="baseline", zorder=3)

    # ── ||W||^2 = value (blue) ──────────────────────────────────────────────
    # Typeset sequentially (natural mathtext kerning) starting at the frame's
    # measured left ink edge; each group is advanced by its RENDERED width so
    # the tight frame spacing (no gaps) is reproduced without hand-guessed x's.
    N = b["norm"]
    fig.canvas.draw()
    inv = ax.transData.inverted()

    def width_of(t):
        fig.canvas.draw()
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        return abs(x1 - x0)

    x = N["bar1"]
    t = ax.text(x, N["base"], r"$\|$", fontsize=NORM_FS, color=BLUE,
                ha="left", va="baseline", zorder=3)
    x += width_of(t)
    t = ax.text(x, N["base"], r"$W$", fontsize=NORM_FS, color=BLUE,
                ha="left", va="baseline", zorder=3)
    w0 = x
    x += width_of(t)
    ax.plot([w0 + 0.4, x - 0.4], [N["base"] + 2.2, N["base"] + 2.2],
            color=BLUE, lw=1.3, zorder=3)
    t = ax.text(x + 0.3, N["base"], r"$\|^2$", fontsize=NORM_FS, color=BLUE,
                ha="left", va="baseline", zorder=3)
    x += 0.3 + width_of(t)
    t = ax.text(x + 5.0, N["base"], r"$=$", fontsize=NORM_FS, color=BLUE,
                ha="left", va="baseline", zorder=3)
    x += 5.0 + width_of(t)
    ax.text(x + 4.5, N["base"], "$%s$" % N["text"], fontsize=NORM_FS, color=BLUE,
            ha="left", va="baseline", zorder=3)

    name = "wbox017_band%d.png" % i
    fig.savefig(os.path.join(HERE, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(ORIGIN_X, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(HERE, "wbox017_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
