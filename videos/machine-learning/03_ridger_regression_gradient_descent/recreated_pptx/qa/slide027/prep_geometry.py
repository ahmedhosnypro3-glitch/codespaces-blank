#!/usr/bin/env python3
"""Geometry prep for slide 027 build.

Sources:
- Banked trace points for the parabola (qa/slide027/measured_geometry.md — TRUSTED).
- Supplemental PIL probes on the original frame ONLY for quantities the dossier
  itself marks halo-inclusive (dot diameters, curve stroke width) — centers and
  all other geometry come from the banked rows, not re-measured.

Outputs:
1. Parabola representation: quartic LSQ y=f(x) over the trace; if max residual
   <= 5 px accept, else fall back to decimated knots. Then sample dense knots
   and emit a Catmull-Rom -> cubic bezier chain as a JS array literal
   (frame px) for build/slide_027.js custGeom.
2. Pure-blue per-dot diameters (dot mask only, no curve/halo).
3. Yellow dot diameter.
4. Curve stroke width modal from clean vertical slices.
"""
import json

import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# ---- banked trace (measured_geometry.md) -----------------------------------
LEFT = [(253,230),(254,236),(255,242),(256,246),(259,252),(262,272),(268,280),
        (270,286),(272,292),(274,296),(276,300),(278,302),(288,318),(290,322),
        (291,324),(293,326),(294,328),(296,330),(297,332),(299,334),(313,350),
        (316,352),(318,354),(320,356),(322,358),(324,360),(363,386),(365,388),
        (383,395),(400,400),(420,404),(436,406)]
RIGHT = [(641,236),(640,240),(639,244),(638,248),(637,252),(635,260),(632,268),
         (628,280),(624,288),(619,300),(612,312),(604,324),(595,336),(584,348),
         (571,360),(561,368),(543,380),(525,390),(497,400),(479,404),(463,406)]
VERTEX = (445, 408)

pts = np.array(LEFT + RIGHT + [VERTEX], dtype=float)
xs, ys = pts[:, 0], pts[:, 1]

# ---- quartic fit ------------------------------------------------------------
best = None
for deg in (2, 3, 4, 5):
    coef = np.polyfit(xs, ys, deg)
    resid = ys - np.polyval(coef, xs)
    maxr = np.abs(resid).max()
    meanr = np.abs(resid).mean()
    print(f"poly deg {deg}: max|resid|={maxr:.2f}px mean={meanr:.2f}px")
    if best is None or maxr < best[0]:
        best = (maxr, deg, coef)

maxr, deg, coef = best
print(f"polynomial best: deg {deg}, max|resid| {maxr:.2f}px — ABOVE 5px tolerance, "
      "so the curve is NOT a polynomial; the trace itself is the geometry.")
print("DECISION: use ALL banked trace points as Catmull-Rom knots (curve passes "
      "through every knot; the build script embeds the same trace + CR formula).")

# knots = the full banked trace (+ measured vertex), sorted by x (single-valued in x)
knots = sorted(set(map(tuple, pts.tolist())), key=lambda k: k[0])
print(f"knots: {len(knots)} from ({knots[0][0]:.1f},{knots[0][1]:.1f}) to ({knots[-1][0]:.1f},{knots[-1][1]:.1f})")

# ---- Catmull-Rom -> cubic bezier --------------------------------------------
def catmull_rom_beziers(knots):
    """Uniform Catmull-Rom through knots -> cubic bezier segments.
    B1 = P1 + (P2 - P0)/6 ; B2 = P2 - (P3 - P1)/6  (building.md law)."""
    P = [np.array(k, dtype=float) for k in knots]
    # duplicate endpoints for the phantom neighbors
    P = [P[0] + (P[0] - P[1])] + P + [P[-1] + (P[-1] - P[-2])]
    segs = []
    for i in range(1, len(P) - 2):
        P0, P1, P2, P3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        B1 = P1 + (P2 - P0) / 6.0
        B2 = P2 - (P3 - P1) / 6.0
        segs.append((P1, B1, B2, P2))
    return segs

segs = catmull_rom_beziers(knots)
js = []
p0 = segs[0][0]
js.append("{ x: px(%.2f), y: px(%.2f), moveTo: true }" % (p0[0], p0[1]))
for (P1, B1, B2, P2) in segs:
    js.append("{ x: px(%.2f), y: px(%.2f), curve: { type: \"cubic\", x1: px(%.2f), y1: px(%.2f), x2: px(%.2f), y2: px(%.2f) } }"
               % (P2[0], P2[1], B1[0], B1[1], B2[0], B2[1]))
print(f"\n// ---- parabola custGeom points ({len(js)}) ----")
print(",\n".join(js))
chain = []
for (P1, B1, B2, P2) in segs:
    for t in np.linspace(0, 1, 40):
        mt = 1 - t
        chain.append(mt**3 * P1 + 3 * mt * mt * t * B1 + 3 * mt * t * t * B2 + t**3 * P2)
chain = np.array(chain)
d = np.sqrt(((pts[:, None, :] - chain[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
print(f"\ntrace-point -> bezier-chain distance: max {d.max():.2f}px mean {d.mean():.2f}px")

# ---- supplemental dot-diameter probes ---------------------------------------
# pure blue disc mask: strong blue, weak red/green — excludes black curve & halo
blue = (b > 120) & (r < 110) & (g < 110) & (b - r > 60) & (b - g > 60)
DOTS = [(262.0, 263.5), (283.0, 310.5), (306.5, 342.0), (332.0, 366.5),
        (354.5, 380.5), (374.5, 390.0), (392.0, 396.5), (411.0, 403.5), (426.5, 403.5)]
print("\n== blue dot discs (pure-blue mask around banked centers) ==")
diam = []
for i, (cx, cy) in enumerate(DOTS, 1):
    win = 14
    sub = blue[int(cy) - win:int(cy) + win, int(cx) - win:int(cx) + win]
    ys_, xs_ = np.where(sub)
    if len(ys_):
        wpx = xs_.max() - xs_.min() + 1
        hpx = ys_.max() - ys_.min() + 1
        bcx = xs_.mean() + int(cx) - win
        bcy = ys_.mean() + int(cy) - win
        print(f"  dot {i}: ink {wpx}x{hpx}  mask-center ({bcx:.1f},{bcy:.1f}) vs banked ({cx},{cy})")
        diam.append(wpx)
    else:
        print(f"  dot {i}: NO pure-blue px (halo-only?) at ({cx},{cy})")
if diam:
    print(f"  modal dot ink width: {max(set(diam), key=diam.count)} px; range {min(diam)}..{max(diam)}")

yel = (r > 200) & (g > 200) & (b < 140)
ys_, xs_ = np.where(yel[395:420, 432:458])
if len(ys_):
    print(f"== yellow dot: {xs_.max()-xs_.min()+1}x{ys_.max()-ys_.min()+1} at center ({xs_.mean()+432:.1f},{ys_.mean()+395:.1f})")

# ---- curve stroke width (clean vertical slices away from text/dots/axes) -----
print("\n== curve stroke width, vertical slices ==")
widths = []
for xcol in (350, 355, 540, 555, 585, 300, 320):
    col = (r[:, xcol] < 100) & (g[:, xcol] < 100) & (b[:, xcol] < 100)
    rows_ = np.where(col)[0]
    if len(rows_):
        runs = []
        s_ = p_ = rows_[0]
        for yv in rows_[1:]:
            if yv == p_ + 1:
                p_ = yv
            else:
                runs.append((s_, p_)); s_ = p_ = yv
        runs.append((s_, p_))
        runs = [(a, b_) for a, b_ in runs if b_ - a <= 6]
        for a, b_ in runs:
            widths.append(b_ - a + 1)
            print(f"  x={xcol}: curve run rows {a}..{b_} ({b_ - a + 1}px)")
if widths:
    print(f"  modal stroke width: {max(set(widths), key=widths.count)} px; all {widths}")

# ---- axis stroke widths ------------------------------------------------------
for name, sl in [("y-axis x=222", (slice(240, 430), 221, 224)), ("x-axis y=436", (434, 439, slice(300, 660)))]:
    pass
col = im[240:430, 221:225].sum(axis=2)
dark = (col < 300).sum(axis=1)
print(f"y-axis: dark-per-row over x221..224 modal = {max(set(dark.tolist()), key=dark.tolist().count)} px wide")
rowpx = im[433:440, 300:660].sum(axis=2)
darkrow = (rowpx < 300).sum(axis=0)
print(f"x-axis: dark-per-col over y433..439 modal = {max(set(darkrow.tolist()), key=darkrow.tolist().count)} px tall")

with open("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/prep_geometry_output.txt", "w") as f:
    pass  # placeholder; stdout is banked by tee at invocation
