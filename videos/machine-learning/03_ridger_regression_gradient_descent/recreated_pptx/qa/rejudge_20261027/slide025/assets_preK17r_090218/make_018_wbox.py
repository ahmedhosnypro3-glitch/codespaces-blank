#!/usr/bin/env python3
"""Generate slide 018's three W-box interiors as 600-dpi transparent PNGs.

Dependency chain (deck edge 18 > 17): slide 018's composition is the certified
017 component rendered with 018's own values — the W boxes sit in the SAME slot
(origin x507, y127/265/403, 115x123 px), so this generator reuses 017's closed
-loop typography (DIGIT_FS 20.0, W_FS 19.5, NORM_FS 19.0 — ink height matches
017's frame to ~1px and the frames are the same capture) and only changes the
VALUES, measured from unique_slides/slide_018.jpg (qa/slide018/measure_018.txt):

  * values (0.13 1.87 0.09 | 0.54 0.73 0.81) and band 3 (0.82 0.33 1.1)
  * ||W||^2 = 3.5 | 1.48 | 1.92  (blue; band 2/3 norm lines are longer than
    band 1's because 1.48/1.92 carry a leading digit band 1's "3.5" lacks —
    the sequential-advance typesetting absorbs that automatically)
  * no pale-yellow ellipse (as in 017) — PIL on 018's frame: 0 pale-yellow px

matplotlib mathtext (STIX) at 600 dpi is the deck's certified professional-2D
math mechanism; the component places each PNG at exact px/600 inches.
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

# per band: y0 = interior origin y; item coordinates are ABSOLUTE frame px,
# measured on 018's frame (same slot as the certified 017 boxes).
BANDS = [
    dict(y0=127,
         w=dict(cx=530.0, base=172.4, under=(521.0, 538.5, 178.0)),
         eq=dict(x0=543.0, x1=555.5, y1=168.6, y2=173.6),
         parens=dict(ltip=560.2, lbody=557.5, rtip=603.8, rbody=606.5, yt=137.0, yb=211.5),
         digits=[("0.13", 582.5, 156.0), ("1.87", 582.5, 180.5), ("0.09", 582.5, 206.0)],
         norm=dict(bar1=520.25, text="3.5", base=239.0, vx=581.5, vw=24.5)),
    dict(y0=265,
         w=dict(cx=535.5, base=310.5, under=(528.5, 543.5, 315.5)),
         eq=dict(x0=549.0, x1=560.5, y1=306.5, y2=311.7),
         parens=dict(ltip=563.7, lbody=561.0, rtip=608.3, rbody=611.0, yt=274.0, yb=350.0),
         digits=[("0.54", 588.5, 293.0), ("0.73", 588.5, 318.5), ("0.81", 588.5, 344.0)],
         norm=dict(bar1=520.25, text="1.48", base=376.3, vx=584.0, vw=33.5)),
    dict(y0=403,
         w=dict(cx=530.5, base=449.0, under=(522.0, 539.0, 455.0)),
         eq=dict(x0=544.0, x1=555.5, y1=444.5, y2=449.5),
         parens=dict(ltip=560.2, lbody=557.5, rtip=603.8, rbody=606.5, yt=412.0, yb=487.0),
         digits=[("0.82", 583.0, 431.0), ("0.33", 583.0, 456.0), ("1.1", 583.0, 482.0)],
         norm=dict(bar1=520.25, text="1.92", base=513.3, vx=584.0, vw=32.5)),
]

DIGIT_FS = 20.0      # closed loop on 017: STIX digit ink 13.5px == frame 13-14px
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

    # ── ||W||^2 = value (blue) ───────────────────────────────────────────────
    # 018 PIL (measure_018.txt + fix round 1): the original skeleton
    # (‖ W ‖² =) is TALL-AND-NARROW — bars 24px tall spanning x520..577 in ALL
    # bands, value starting at x581.5/584 — while mathtext at NORM_FS renders
    # the skeleton 11px wider and 4px shorter. So the skeleton is drawn with
    # explicit primitives at the measured landmarks, each text element
    # self-calibrated to its measured frame width; the value keeps the
    # certified mathtext mechanism.
    N = b["norm"]
    base = N["base"]
    fig.canvas.draw()
    inv = ax.transData.inverted()

    def width_of(t):
        fig.canvas.draw()
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        return abs(x1 - x0)

    def fitted_text(x, y, s, target_w, color, ha="left", va="baseline", fs0=NORM_FS):
        t = ax.text(x, y, s, fontsize=fs0, color=color, ha=ha, va=va, zorder=3)
        w0 = width_of(t)
        t.remove()
        t = ax.text(x, y, s, fontsize=fs0 * target_w / w0, color=color,
                    ha=ha, va=va, zorder=3)
        return t

    # first ‖ : bars at x 520.25 / 524.25, y base−17..base+4
    for bx in (N["bar1"], N["bar1"] + 4.0):
        ax.plot([bx, bx], [base - 17, base + 4], color=BLUE, lw=1.2, zorder=3)
    # W italic, centered x537.5, target width 17.5
    fitted_text(537.5, base, r"$W$", 17.5, BLUE, ha="center")
    # second ‖ : bars at 550.25 / 554.25, y base−20..base+4, + superscript ²
    for bx in (N["bar1"] + 30.0, N["bar1"] + 34.0):
        ax.plot([bx, bx], [base - 20, base + 4], color=BLUE, lw=1.2, zorder=3)
    fitted_text(556.0, base - 8, r"$^{2}$", 5.5, BLUE)
    # "=" : two horizontal bars x566.25..576.5 at base−9.5 / base−3
    for yy in (base - 9.5, base - 3.0):
        ax.plot([N["bar1"] + 46.0, N["bar1"] + 56.25], [yy, yy],
                color=BLUE, lw=2.0, zorder=3)
    # value: mathtext at measured x / width (band1 581.5/24.5, band2|3 584/33.5)
    fitted_text(N["vx"], base, "$%s$" % N["text"], N["vw"], BLUE)

    name = "wbox018_band%d.png" % i
    fig.savefig(os.path.join(HERE, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(ORIGIN_X, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(HERE, "wbox018_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
