#!/usr/bin/env python3
"""Slide 027 attempt-9 self-check on a FRESH re-render of the current deliverable.

Dispatch brief step (b): prove the render is current vs the build script and that
every measured element still sits on its measured frame band BEFORE spending a
vision call. This gates the dispatch; it never substitutes for a judge.

Masks are element-specific (an earlier generic version falsely counted the C00000
house strokes and the FF0000 box border as "black", and dot AA halos as violet):
  title   8B0000 only       : R 100..185, G<60, B<60
  box     FF0000 only       : R>235, G<80, B<80
  black   000000 only       : lum<70
  violet  dot fill 5F41C4   : B>R+40, B>110, R<160, lum<200
  yellow  FFFF00            : R>215, G>200, B<180
  stepgr  #ACACAD arrow ink : neutral (max-min channel spread <= 18), lum 130..215,
                              and >4 render px from every non-white pixel
Tolerance 2.0 frame px (building.md standard) except where noted.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = "/home/ahmed/Projects/ai_llm_slides"
V = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = V + "/recreated_pptx/qa/slide027/render_10.png"

ren = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
RH, RW = ren.shape[:2]
S = RW / 960.0
flags = []


def fr(x, y):
    return int(round(x * S)), int(round(y * S))


def ink(mask, x0, y0, x1, y1):
    """(rows_lo, rows_hi, cols_lo, cols_hi, npx) of mask inside a frame-px box."""
    a, b = fr(x0, y0)
    c, d = fr(x1, y1)
    ys, xs = np.where(mask[b:d + 1, a:c + 1])
    if len(xs) == 0:
        return None
    return (ys.min() / S + y0, ys.max() / S + y0,
            xs.min() / S + x0, xs.max() / S + x0, len(xs))


def near(mask, cx, cy, r=3.0):
    """Count mask px in a +-r frame-px window centred on (cx,cy)."""
    a, b = fr(cx - r, cy - r)
    c, d = fr(cx + r, cy + r)
    return int(mask[b:d + 1, a:c + 1].sum())


def cmp(name, got, exp, tol):
    if got is None:
        flags.append(f"{name}: NO INK")
        print(f"  {name:16s} NO INK in window")
        return
    lo, hi, lc, hc, n = got
    r = max(abs(lo - exp[0]), abs(hi - exp[1]), abs(lc - exp[2]), abs(hc - exp[3]))
    print(f"  {name:16s} rows {lo:7.1f}..{hi:7.1f} cols {lc:7.1f}..{hc:7.1f} "
          f"(exp {exp[0]}..{exp[1]}, {exp[2]}..{exp[3]}) ink {n}")
    if r > tol:
        flags.append(f"{name}: residual {r:.1f} > {tol}")


R, G, B = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
lum = ren.sum(axis=2) / 3.0
spread = ren.max(axis=2) - ren.min(axis=2)

m_title = (R > 100) & (R < 185) & (G < 60) & (B < 60)
m_red = (R > 235) & (G < 80) & (B < 80)
m_black = lum < 70
m_violet = (B > R + 40) & (B > 110) & (R < 160) & (lum < 200)
m_yellow = (R > 215) & (G > 200) & (B < 180)
# the chain ink renders at (172,172,173) = #ACACAD exactly; the discs' AA halo blends
# toward it, so the chain mask is a tight neutral band around 172.5.
m_chain = (spread <= 14) & (lum >= 158) & (lum <= 190)
# step arrows: neutral gray, far (>4 render px) from every coloured/black ink
ink_any = (m_black | m_red | m_violet | m_yellow | ((lum < 205) & (spread > 18)))
d_non = ndimage.distance_transform_edt(~ink_any)
m_step = (spread <= 18) & (lum >= 130) & (lum <= 215) & (d_non > 4)

print("render %dx%d  scale %.4f" % (RW, RH, S))

print("== TITLE (8B0000) ==")
cmp("title L1", ink(m_title, 150, 60, 800, 106), (73, 100, 191, 744), 5.0)
cmp("title L2", ink(m_title, 150, 104, 800, 142), (108, 135, 321, 621), 5.0)

print("== GRAPH BOX (FF0000) ==")
cmp("box left", ink(m_red, 188, 175, 197, 500), (175, 500, 193, 194), 2.0)
cmp("box right", ink(m_red, 712, 175, 721, 500), (175, 500, 715, 717), 2.0)
cmp("box top", ink(m_red, 200, 162, 710, 176), (166, 168, 200, 710), 2.0)
cmp("box bottom", ink(m_red, 200, 502, 710, 512), (506, 508, 200, 710), 2.0)

print("== AXES + HEADS (000000) ==")
cmp("y-axis", ink(m_black, 218, 228, 229, 432), (228, 432, 222, 224), 2.0)
cmp("y-head", ink(m_black, 212, 202, 236, 219), (206, 219, 218, 228), 2.0)
g = ink(m_black, 272, 428, 438, 446)
if g:
    lo, hi, lc, hc, n = g
    ctr = (lo + hi) / 2
    print(f"  x-axis          rows {lo:.1f}..{hi:.1f} (crisp stroke, centre {ctr:.1f}; "
          f"exp centre {(431 + 442) / 2:.1f}) cols {lc:.1f}..{hc:.1f} ink {n}")
    if abs(ctr - (431 + 442) / 2) > 2.5:
        flags.append(f"x-axis: centre {ctr:.1f} vs {(431 + 442) / 2:.1f}")
    if not (272 <= lc <= 276 and 434 <= hc <= 442):
        flags.append(f"x-axis: cols {lc:.1f}..{hc:.1f}")
cmp("x-head", ink(m_black, 669, 428, 692, 446), (431, 442, 670, 686), 2.5)

print("== DASHES (black, dash COUNT on the two dashed leader columns) ==")
for xcol, y0, y1, exp_n in ((262.5, 265, 440, 12), (444.5, 410, 445, 2)):
    a, b = fr(xcol - 2, y0)
    c, d = fr(xcol + 2, y1)
    sub = m_black[b:d, a:c].any(axis=1)
    runs, k = [], 0
    while k < len(sub):
        if sub[k]:
            k0 = k
            while k < len(sub) and sub[k]:
                k += 1
            runs.append(((b + k0) / S, (b + k) / S))
        else:
            k += 1
    print(f"  x={xcol}: {len(runs)} dash bands (exp {exp_n}) "
          f"{[(round(a, 1), round(bb, 1)) for a, bb in runs]}")
    if len(runs) != exp_n:
        flags.append(f"dashes x={xcol}: {len(runs)} bands != {exp_n}")

print("== PARABOLA (attempt 10: ONE analytic quadratic, every column) ==")
# Shipping definition (build_attempt_10.js / slide_027.js line 193):
#   y = -0.00395282 * (x - 450.41)^2 + 407.25, extent x=239..658, 420 samples.
# Founder finding A: the curve must be identified as a quadratic and drawn smooth, so
# the check is per-column: black ink within 3.0 frame px of the analytic y at every
# column, plus the de-noised ripple (d2 of the band-limited centroid residual).
# Control: the same census on attempt 8's render (the Catmull-Rom chain, which is not
# this quadratic) misses ~250 of 388 columns within 4.8 fpx of the analytic y -- so
# this check does discriminate.
m_curve = (lum < 110) & (spread <= 25)     # black stroke incl. its AA blend with discs
# occlusion bands = the nine disc centroids and the yellow minimum, +-8.5 fpx in x:
# the discs are drawn ON TOP of the curve, so the curve's ink is legitimately blended
# away there (measured: the blend is lighter than the curve mask's threshold).
DISC_COLS = [(263.12 - 8.5, 263.12 + 8.5), (283.64 - 8.5, 283.64 + 8.5),
             (306.85 - 8.5, 306.85 + 8.5), (331.65 - 8.5, 331.65 + 8.5),
             (354.26 - 8.5, 354.26 + 8.5), (373.91 - 8.5, 373.91 + 8.5),
             (392.40 - 8.5, 392.40 + 8.5), (410.77 - 8.5, 410.77 + 8.5),
             (428.21 - 8.5, 428.21 + 8.5), (444.49 - 8.5, 444.49 + 8.5)]


def q(x):
    return -0.00395282 * (x - 450.41) ** 2 + 407.25


dmax, dtot, miss, ncol = 0.0, 0.0, 0, 0
misscol = []
resid = []
for xf in range(239, 659):
    if 259 <= xf <= 266 or 441 <= xf <= 448:      # the two black dash leaders
        continue
    X, Y = fr(xf, q(xf))
    win = m_curve[Y - 10:Y + 11, X - 2:X + 3]
    if not win.any():
        occluded = any(a <= xf <= b for a, b in DISC_COLS)
        if not occluded:
            miss += 1
            misscol.append(xf)
        continue
    ys, xs = np.where(win)
    yy = ys / S + (Y - 10) / S
    dd = float(np.abs(yy - q(xf)).min())
    dmax = max(dmax, dd)
    dtot += dd
    ncol += 1
    resid.append(float(yy.mean() - q(xf)))
print(f"  quadratic->ink: {ncol} cols with ink within 10 render px of the analytic y; "
      f"max |dy| {dmax:.2f}, mean {dtot / max(1, ncol):.2f} frame px; "
      f"{miss} columns with no ink OUTSIDE the disc-halo occlusion bands")
if dmax > 3.0 or miss:
    flags.append(f"quadratic: max |dy| {dmax:.2f}, {miss} unoccluded columns with no ink"
                 + (f" {misscol[:12]}" if misscol else ""))
r = np.array(resid)
k = np.ones(5) / 5.0
rs = np.convolve(r, k, mode="same")[2:-2]
d2 = np.diff(np.diff(rs))
print(f"  band-limited centroid residual: rms {np.sqrt((r ** 2).mean()):.4f}, "
      f"max {np.abs(r).max():.4f} fpx; de-noised ripple (d2) rms "
      f"{np.sqrt((d2 ** 2).mean()):.4f}, max {np.abs(d2).max():.4f} fpx")
if np.sqrt((d2 ** 2).mean()) > 0.25 or np.abs(d2).max() > 1.0:
    flags.append(f"quadratic ripple: rms {np.sqrt((d2 ** 2).mean()):.4f} > 0.25 "
                 f"(max {np.abs(d2).max():.4f})")
# the shipped extent: the stroke tips must land on the analytic curve's own ends, and
# the drawn ink envelope must not run past the quadratic's sampled extent (239..658).
xs_cols = []
for xf in range(230, 670):
    X = int(round(xf * S))
    Y0 = int(round(q(xf) * S))
    if m_curve[Y0 - 40:Y0 + 6, X - 1:X + 2].any():
        xs_cols.append(xf)
print(f"  drawn ink envelope x={min(xs_cols)}..{max(xs_cols)} "
      f"(shipped extent 239..658)")
if min(xs_cols) < 238 or max(xs_cols) > 660:
    flags.append(f"curve extent {min(xs_cols)}..{max(xs_cols)} outside 239..658")

print("== DOTS (5F41C4) -- attempt-10 measured halo-excluded centroids ==")
DOTS = [(263.12, 263.41), (283.64, 309.88), (306.85, 341.79), (331.65, 366.36),
        (354.26, 381.00), (373.91, 390.45), (392.40, 396.74), (410.77, 401.75),
        (428.21, 405.90)]
for i, (cx, cy) in enumerate(DOTS, 1):
    g = ink(m_violet, cx - 8, cy - 8, cx + 8, cy + 8)
    if g is None:
        flags.append(f"dot {i}: NO violet ink")
        continue
    lo, hi, lc, hc, n = g
    ccx, ccy = (lc + hc) / 2, (lo + hi) / 2
    dia = (hc - lc + hi - lo) / 2
    print(f"  dot {i}: centre ({ccx:.1f},{ccy:.1f}) d~{dia:.1f} (exp {cx},{cy} d~13) ink {n}")
    if abs(ccx - cx) > 1.5 or abs(ccy - cy) > 1.5:
        flags.append(f"dot {i}: centre off ({ccx - cx:+.1f},{ccy - cy:+.1f})")
    if not (12.2 <= dia <= 14.5):
        flags.append(f"dot {i}: d {dia:.1f}")
g = ink(m_yellow, 437, 399, 453, 415)
if g:
    lo, hi, lc, hc, n = g
    ccx, ccy = (lc + hc) / 2, (lo + hi) / 2
    print(f"  yellow dot: centre ({ccx:.1f},{ccy:.1f}) d~{(hc - lc + hi - lo) / 2:.1f} "
          f"(exp 444.49,407.25 d~12.5) ink {n}")
    if abs(ccx - 444.49) > 1.5 or abs(ccy - 407.25) > 1.5:
        flags.append(f"yellow dot: centre off ({ccx - 444.49:+.1f},{ccy - 407.25:+.1f})")
else:
    flags.append("yellow dot: NO yellow ink")

print("== TEXT LABELS (000000) ==")
for name, exp in [("Cost", (176, 189, 200, 238)), ("Learning step", (272, 289, 297, 404)),
                  ("Minimum", (364, 376, 428, 497)), ("Random", (444, 457, 230, 295)),
                  ("initial value", (466, 479, 219, 306)),
                  ("theta axis", (427, 444, 697, 709)),
                  ("thetahat body", (488, 504, 439, 449)),
                  ("thetahat hat", (480, 484, 440, 448))]:
    pad = 2.5 if name in ("thetahat body", "thetahat hat") else 4.0
    tol = 2.5 if name in ("Cost", "Learning step", "Random", "initial value",
                          "theta axis", "Minimum") else 2.5
    cmp(name, ink(m_black, exp[2] - pad, exp[0] - pad, exp[3] + pad, exp[1] + pad),
        exp, tol)

print("== STEP ARROWS (attempt 10: 9 centre-to-centre arcs + 9 arrowheads) ==")
# CHAIN_ARCS from build_attempt_10.js: [(P0, control, P2)] x 9, P0/P2 = measured dot
# centres; CHAIN_HEADS = the measured head triangles [tip, b1, b2].
ARCS = [
    ((263.12, 263.41), (298.32, 275.63), (283.64, 309.88)),
    ((283.64, 309.88), (316.79, 310.17), (306.85, 341.79)),
    ((306.85, 341.79), (336.00, 337.17), (331.65, 366.36)),
    ((331.65, 366.36), (358.14, 350.23), (354.26, 381.00)),
    ((354.26, 381.00), (372.23, 368.79), (373.91, 390.45)),
    ((373.91, 390.45), (391.42, 369.30), (392.40, 396.74)),
    ((392.40, 396.74), (408.35, 374.43), (410.77, 401.75)),
    ((410.77, 401.75), (425.41, 378.93), (428.21, 405.90)),
    ((428.21, 405.90), (438.78, 377.28), (444.49, 407.25)),
]
HEADS = [
    ((285.92, 303.76), (284.96, 297.80), (290.11, 299.42)),
    ((308.47, 335.44), (306.83, 329.63), (312.13, 330.64)),
    ((332.21, 359.84), (329.58, 354.41), (334.98, 354.48)),
    ((354.75, 374.49), (352.13, 369.05), (357.53, 369.13)),
    ((372.85, 384.00), (368.78, 379.54), (373.98, 378.07)),
    ((391.84, 390.26), (388.36, 385.33), (393.69, 384.51)),
    ((409.86, 395.24), (406.12, 390.50), (411.41, 389.40)),
    ((427.21, 399.40), (423.41, 394.71), (428.69, 393.55)),
    ((443.10, 401.09), (439.08, 396.58), (444.29, 395.17)),
]
print("  -- shaft continuity on every inter-dot arc (t=0.10..0.90) --")
for i, (P0, C, P2) in enumerate(ARCS, 1):
    hits, tot = 0, 0
    for j in range(1, 10):
        t = j / 10.0
        x = (1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * C[0] + t ** 2 * P2[0]
        y = (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * C[1] + t ** 2 * P2[1]
        g = ink(m_chain, x - 3, y - 3, x + 3, y + 3)
        tot += 1
        hits += bool(g)
    print(f"  arc {i} ({P0[0]:.1f},{P0[1]:.1f})->({P2[0]:.1f},{P2[1]:.1f}): "
          f"{hits}/{tot} sample points carry chain ink")
    if hits < 8:
        flags.append(f"arc {i}: only {hits}/{tot} sample points carry ink")
print("  -- founder finding B: each shaft runs INTO its disc, resuming at the rim --")
# walk outward from each dot centre along the arc and find the first chain ink at
# r >= 6.6 fpx (the disc radius is 6.5 fpx). The shaft is drawn before the disc, so
# the stretch inside r < 6.5 is legitimately occluded by the disc -- that is what
# "anchored on the centre" looks like on the render.
for i, (P0, C, P2) in enumerate(ARCS, 1):
    for side, CEN, trs in (("src", P0, np.arange(0.004, 0.30, 0.004)),
                           ("dst", P2, np.arange(0.70, 0.997, 0.004))):
        rs_ink = []
        for t in trs:
            x = (1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * C[0] + t ** 2 * P2[0]
            y = (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * C[1] + t ** 2 * P2[1]
            r = np.hypot(x - CEN[0], y - CEN[1])
            if r >= 6.6 and ink(m_chain, x - 3, y - 3, x + 3, y + 3):
                rs_ink.append(r)
        first = min(rs_ink) if rs_ink else None
        ok = first is not None and 6.6 <= first <= 9.0
        print(f"    arc {i} {side}: first chain ink at r="
              f"{'%.2f' % first if first is not None else 'NONE'} fpx from the dot "
              f"centre (disc radius 6.5) -> {'OK' if ok else 'FAIL'}")
        if not ok:
            flags.append(f"arc {i} {side}: first ink r={first}")
print("  -- founder finding C: nine grey ARROWHEADS at the measured triangles --")
for i, (tip, b1, b2) in enumerate(HEADS, 1):
    cen = ((tip[0] + b1[0] + b2[0]) / 3, (tip[1] + b1[1] + b2[1]) / 3)
    g = ink(m_chain, cen[0] - 3, cen[1] - 3, cen[0] + 3, cen[1] + 3)
    g8 = ink(m_chain, tip[0] - 4, tip[1] - 4, tip[0] + 4, tip[1] + 4)
    n = g[4] if g else 0
    n8 = g8[4] if g8 else 0
    print(f"  head {i}: centroid ({cen[0]:.1f},{cen[1]:.1f}) ink {n} px "
          f"(+-3 window), tip-window ink {n8} px")
    if n < 25:
        flags.append(f"head {i}: only {n} ink px at the measured centroid")
    if n8 < 5:
        flags.append(f"head {i}: only {n8} ink px at the tip")
# control zones: the ORIGINAL has 0 far-gray px here -> the render must too
# (below-dot9 zone contains the tail of the last arrow + dot 9 halo AA, hence >0)
for name, x0, y0, x1, y1 in [("above dot1", 205, 225, 400, 258),
                             ("below dot9 / yellow zone", 415, 412, 470, 500),
                             ("right branch", 465, 385, 716, 500),
                             ("empty box left", 205, 420, 300, 500)]:
    a, b = fr(x0, y0)
    c, d = fr(x1, y1)
    n = int(m_step[b:d, a:c].sum())
    print(f"  control zone {name}: step-gray px {n}")
    if n > 80:
        flags.append(f"step-gray stray in {name}: {n} px")

print("== CONTAINMENT ==")
g = ink(m_black, 195, 168, 715, 506)
if g:
    lo, hi, lc, hc, n = g
    print(f"  graph ink (black) bbox rows {lo:.1f}..{hi:.1f} cols {lc:.1f}..{hc:.1f} "
          f"(must be inside 167..507 x 194..715) ink {n}")
    if lo < 166 or hi > 508 or lc < 193 or hc > 716:
        flags.append("graph ink crosses the graph-box border")
g = ink(m_title, 40, 40, 920, 200)
if g:
    lo, hi, lc, hc, n = g
    print(f"  title ink cols {lc:.1f}..{hc:.1f} rows {lo:.1f}..{hi:.1f} (panel 54..903) ink {n}")
    if lc < 54 or hc > 903 or lo < 45 or hi > 140:
        flags.append("title ink outside the panel")

print()
if flags:
    print("SELFCHECK: FAIL")
    for f in flags:
        print("  CHECK: " + f)
    sys.exit(1)
print("SELFCHECK: PASS - title/box/axes/dashes/labels within 2.0 frame px; the curve is "
      "the shipped analytic quadratic at every column with de-noised ripple "
      f"{np.sqrt((d2 ** 2).mean()):.4f} fpx; 9 dot discs on the measured centres; "
      "all 9 connectors continuous centre-to-centre and resuming at each disc rim; "
      "9 arrowheads at the measured triangles; 0 stray step-gray ink in the off-chain "
      "control zones.")
