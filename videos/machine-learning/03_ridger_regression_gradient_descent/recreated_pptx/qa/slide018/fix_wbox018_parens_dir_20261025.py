#!/usr/bin/env python3
"""Fix slide 018's W-box parentheses: BOTH sides were MIRRORED in all bands.

Copy-then-modify of build/assets/make_018_wbox.py (banked, never edited).
Paren anatomy per the S22 audit: a "(" has its two ENDPOINTS on the INNER side
(facing the vector digits) and its BELLY pulled toward the OUTER side; a ")" is
mirrored. The certified generator named its values ltip/lbody and built
verts=[(tip,yt),(body,yt+18),(body,yb-18),(tip,yb)] — endpoints at tip and
belly at body. With ltip=557.5 (outer) / lbody=560.2 (inner) the LEFT parens
bow inward (mirrored), and with rtip=606.5 (outer) / rbody=603.8 (inner) the
RIGHT parens bow outward at the wrong end as well (mirrored). The fix restates
the SAME measured values as l_inner/l_outer/r_inner/r_outer with roles swapped:
endpoints at inner, belly control at outer. No measured x moves.

All other elements (W, =, digits, norm skeleton) are carried over unchanged.
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

# per band: y0 = interior origin y; item coordinates are ABSOLUTE frame px,
# measured on 018's frame (same slot as the certified 017 boxes).
BANDS = [
    dict(y0=127,
         w=dict(cx=530.0, base=172.4, under=(521.0, 538.5, 178.0)),
         eq=dict(x0=543.0, x1=555.5, y1=168.6, y2=173.6),
         parens=dict(l_inner=560.2, l_outer=557.5, r_inner=603.8, r_outer=606.5, yt=137.0, yb=211.5),
         digits=[("0.13", 582.5, 156.0), ("1.87", 582.5, 180.5), ("0.09", 582.5, 206.0)],
         norm=dict(bar1=520.25, text="3.5", base=239.0, vx=581.5, vw=24.5)),
    dict(y0=265,
         w=dict(cx=535.5, base=310.5, under=(528.5, 543.5, 315.5)),
         eq=dict(x0=549.0, x1=560.5, y1=306.5, y2=311.7),
         parens=dict(l_inner=563.7, l_outer=561.0, r_inner=608.3, r_outer=611.0, yt=274.0, yb=350.0),
         digits=[("0.54", 588.5, 293.0), ("0.73", 588.5, 318.5), ("0.81", 588.5, 344.0)],
         norm=dict(bar1=520.25, text="1.48", base=376.3, vx=584.0, vw=33.5)),
    dict(y0=403,
         w=dict(cx=530.5, base=449.0, under=(522.0, 539.0, 455.0)),
         eq=dict(x0=544.0, x1=555.5, y1=444.5, y2=449.5),
         parens=dict(l_inner=560.2, l_outer=557.5, r_inner=603.8, r_outer=606.5, yt=412.0, yb=487.0),
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

    # ── parentheses as cubic Beziers: endpoints INNER, belly control OUTER ──
    P = b["parens"]
    for inner, outer in ((P["l_inner"], P["l_outer"]), (P["r_inner"], P["r_outer"])):
        verts = [(inner, P["yt"]), (outer, P["yt"] + 18), (outer, P["yb"] - 18), (inner, P["yb"])]
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
    fig.savefig(os.path.join(OUTDIR, name), dpi=600, transparent=True)
    plt.close(fig)
    sidecar.append(dict(image=name, origin=(ORIGIN_X, y0), size_px=(W_PX, H_PX)))

with open(os.path.join(OUTDIR, "wbox018_sidecar.json"), "w") as f:
    json.dump(sidecar, f, indent=2)
print(json.dumps(sidecar, indent=2))
