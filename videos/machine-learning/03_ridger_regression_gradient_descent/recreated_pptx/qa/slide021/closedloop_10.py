#!/usr/bin/env python3
"""Closed-loop verification of slide 021 render_5.png against the ORIGINAL frame.

render_5 is the FIRST build carrying the multi-colour equation composites
(eq_021_* "color":"multi" sidecars), so this check verifies for every equation:
  * the TOTAL ink box (all colours merged) against the original's ink box
  * the RED X^T X band and the BLUE "+ lambda I" band against the original's
    own colour bands (the attempt-3 FAIL's claim 5, plus a PIL-checkable form)
plus the non-equation elements carried over from closedloop_4 (tables, chain text,
arrows) and the attempt-3 claim re-checks (det0 in P1, nothing above the title,
lambda=3 in P2, arrows blue).

TOL: 6px positions, 10px widths (pipeline closed-loop standard).
"""
import numpy as np
from PIL import Image

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg")
R = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/render_10.png")
OUT = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
       "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/render_10_closedloop.txt")

SC = 2000 / 960.0
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(R).convert("RGB")).astype(int)

lo, lr = o.mean(axis=2), r.mean(axis=2)
blue_o = (o[:, :, 2] - o[:, :, 0]) > 25
blue_r = (r[:, :, 2] - r[:, :, 0]) > 45
gray_o = (abs(o[:, :, 0] - 233) < 14) & (abs(o[:, :, 1] - 233) < 14) & (abs(o[:, :, 2] - 231) < 16)
gray_r = (abs(r[:, :, 0] - 233) < 16) & (abs(r[:, :, 1] - 233) < 16) & (abs(r[:, :, 2] - 231) < 18)
red_o = (o[:, :, 0] > 110) & (o[:, :, 0] - o[:, :, 1] > 55) & (o[:, :, 0] - o[:, :, 2] > 55)
red_r = (r[:, :, 0] > 110) & (r[:, :, 0] - r[:, :, 1] > 55) & (r[:, :, 0] - r[:, :, 2] > 55)
grn_o = (o[:, :, 1] > 90) & (o[:, :, 1] - o[:, :, 0] > 30) & (o[:, :, 1] - o[:, :, 2] > 30)
grn_r = (r[:, :, 1] > 90) & (r[:, :, 1] - r[:, :, 0] > 30) & (r[:, :, 1] - r[:, :, 2] > 30)
# equation ink = any saturated colour or near-black, excluding the gray panel + white
ink_o = ~(lo > 238) & ~blue_o & ~gray_o
ink_r = ~(lr > 240) & ~blue_r & ~gray_r
# hard-black equation ink (the |, =, digits, parens) — near-black, not red/blue/green
blk_o = ink_o & ~red_o & ~blue_o & ~grn_o
blk_r = ink_r & ~red_r & ~blue_r & ~grn_r


def box(mask, y0, y1, x0, x1, is_render):
    s = SC if is_render else 1.0
    sub = mask[int(y0 * s):int(y1 * s) + 1, int(x0 * s):int(x1 * s) + 1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    if is_render:
        return (round(x0 + xs.min() / s, 1), round(y0 + ys.min() / s, 1),
                round(x0 + xs.max() / s, 1), round(y0 + ys.max() / s, 1), int(sub.sum()))
    # xs indexes columns (-> x), ys indexes rows (-> y): tuple is (x_min, y_min, x_max, y_max)
    return (int(x0 + xs.min()), int(y0 + ys.min()),
            int(x0 + xs.max()), int(y0 + ys.max()), int(sub.sum()))


# (label, orig mask, render mask, search window, target box frame px)
ITEMS = [
    # equations: TOTAL ink box
    ("det0 ink",    ink_o,  ink_r,  183, 216, 336, 440, (341, 187, 435, 212)),
    ("d5685 ink",   ink_o,  ink_r,  350, 383, 333, 470, (338, 354, 464, 379)),
    ("regmat ink",  ink_o,  ink_r,  296, 330,  84, 212, (89, 300, 206, 326)),
    ("invexpr ink", ink_o,  ink_r,  462, 496, 150, 295, (155, 466, 289, 492)),
    ("xtx ink",     ink_o,  ink_r,  129, 161,  92, 147, (97, 133, 141, 157)),
    ("lambda3 ink", ink_o,  ink_r,  300, 325, 240, 295, (245, 304, 289, 321)),
    # colour bands inside the equations
    ("det0 red X",  red_o,  red_r,  183, 216, 336, 400, (345, 192, 390, 210)),
    ("d5685 red X", red_o,  red_r,  350, 383, 333, 400, (342, 359, 387, 377)),
    ("regmat red X", red_o, red_r,  296, 330,  92, 150, (98, 305, 143, 324)),
    ("regmat blue", blue_o, blue_r, 300, 326, 165, 205, (171, 301, 198, 326)),
    ("invexpr red",  red_o, red_r,  462, 496, 158, 215, (164, 471, 208, 490)),
    ("invexpr blue", blue_o, blue_r, 466, 492, 232, 270, (237, 470, 263, 492)),
    # dark glyphs (bars, +, =, digits, parens) must be present and near-black
    ("det0 bars",   blk_o,  blk_r,  188, 214, 338, 345, (341, 190, 343, 212)),
    ("det0 =0",     blk_o,  blk_r,  190, 214, 400, 440, (404, 197, 435, 208)),
    ("regmat (",     blk_o,  blk_r,  300, 328,  86, 100, (89, 301, 95, 326)),
    # carried-over elements
    ("P1 table",    ink_o,  ink_r,  168, 232,  80, 320, (97, 173, 303, 227)),
    ("P2 table",    ink_o,  ink_r,  335, 400,  80, 300, (89, 340, 295, 395)),
    ("P3 table",    ink_o,  ink_r,  450, 520, 410, 640, (421, 457, 626, 511)),
    ("singular txt", ink_o, ink_r,  185, 215, 480, 640, (492, 192, 626, 212)),
    ("no inverse",  red_o,  red_r,  185, 215, 695, 800, (704, 193, 794, 207)),
    ("nonsingular", ink_o,  ink_r,  352, 382, 494, 700, (495, 358, 693, 378)),
    ("inverse exist", red_o, red_r, 350, 390, 750, 890, (761, 359, 876, 373)),
    ("P1 arrow1",   blue_o, blue_r, 190, 212, 455, 482, (460, 196, 476, 207)),
    ("P1 arrow2",   blue_o, blue_r, 190, 212, 650, 685, (660, 196, 677, 207)),
    ("P2 arrow1",   blue_o, blue_r, 355, 380, 480, 510, (489, 363, 505, 373)),
    ("P2 arrow2",   blue_o, blue_r, 355, 380, 720, 750, (728, 363, 744, 374)),
    ("P3 arrow",    blue_o, blue_r, 468, 492, 355, 390, (364, 475, 380, 485)),
]

L = []
say = lambda s="": L.append(s)
say("=== RENDER_5 CLOSED-LOOP vs ORIGINAL (frame px; render 150dpi, SC=%.4f) ===" % SC)
say("TOL: 6px positions, 10px widths (pipeline closed-loop standard).")
say("Equations measured as TOTAL ink + per-colour bands (render_5 = first multi-colour build).")
say()
say(f"{'element':16s} {'ORIG x0..x1 y0..y1 (w,h)':36s} {'RENDER':36s} dx  dy  dw   verdict")
fails = []
for lab, mo, mr, y0, y1, x0, x1, tgt in ITEMS:
    ob = box(mo, y0, y1, x0, x1, False)
    rb = box(mr, y0, y1, x0, x1, True)
    if ob is None or rb is None:
        say(f"{lab:16s} MISSING orig={'None' if ob is None else ob} render={'None' if rb is None else rb}")
        fails.append(lab)
        continue
    dx = rb[0] - ob[0]; dy = rb[1] - ob[1]; dw = (rb[2] - rb[0]) - (ob[2] - ob[0])
    ok = abs(dx) <= 6 and abs(dy) <= 6 and abs(dw) <= 10
    if not ok:
        fails.append(lab)
    say(f"{lab:16s} x{ob[0]:>4}..{ob[2]:<4} y{ob[1]:>3}..{ob[3]:<3} ({ob[2]-ob[0]:>3},{ob[3]-ob[1]:>2}) "
        f"x{rb[0]:>5.0f}..{rb[2]:<5.0f} y{rb[1]:>3.0f}..{rb[3]:<3.0f} ({rb[2]-rb[0]:>4.0f},{rb[3]-rb[1]:>2.0f}) "
        f"{dx:>4.0f} {dy:>4.0f} {dw:>4.0f}  {'OK' if ok else '<<< CHECK'}")

say()
say("--- target boxes (original's measured ink/colour boxes) ---")
for lab, mo, mr, y0, y1, x0, x1, tgt in ITEMS:
    rb = box(mr, y0, y1, x0, x1, True)
    if rb is None:
        continue
    tx0, ty0, tx1, ty1 = tgt
    ex = max(abs(rb[0] - tx0), abs(rb[2] - tx1))
    ey = max(abs(rb[1] - ty0), abs(rb[3] - ty1))
    ew = abs((rb[2] - rb[0]) - (tx1 - tx0))
    v = "OK" if (ex <= 8 and ey <= 8 and ew <= 12) else "CHECK"
    if v == "CHECK":
        fails.append(lab + "/tgt")
    say(f"  {lab:16s} target x{tx0}..{tx1} y{ty0}..{ty1} (w{tx1-tx0}) | render "
        f"dx{ex:4.1f} dy{ey:4.1f} dw{ew:4.1f}  {v}")

say()
say("--- containment: every element inside its block's blue strokes ---")
for name, (by0, by1, bx0, bx1) in {
    "P1": (129, 257, 76, 886), "P2": (288, 418, 76, 889), "P3": (437, 530, 76, 889),
}.items():
    y0, y1 = int(by0 * SC), int((by1 + 1) * SC)
    band = ink_r[y0:y1, :]
    left = int(band[:, :int(bx0 * SC)].sum())
    right = int(band[:, int((bx1 + 1) * SC):].sum())
    say(f"  {name}: ink LEFT of block = {left}, RIGHT of block = {right} (0 = contained)")

say()
say("--- attempt-3 claim re-checks ---")
b = box(red_r, 180, 222, 330, 445, True)
say(f"  det0 red ink in P1: {b}  (claim 'det0 displaced above title' must be FALSE)")
sub = red_r[int(40 * SC):int(77 * SC), :]
ys, xs = np.where(sub)
others = []
if len(ys):
    colcov = sub.sum(axis=0)
    others = [round(i / SC, 1) for i in range(len(colcov))
              if colcov[i] > 0 and not (57 <= i / SC <= 60 or 898 <= i / SC <= 902)]
say(f"  red ink in y46..76 outside house L/R strokes: {others if others else 'NONE'}"
    f" -> {'STILL DISPLACED' if others else 'CLEAN'}")
sub = red_r[int(125 * SC):int(257 * SC), int(330 * SC):int(450 * SC)]
say(f"  red ink in P1 x330..450 n={int(sub.sum())} (det0 present; 5685 must NOT be here)")
b2 = box(red_r, 345, 390, 330, 470, True)
say(f"  d5685 red ink in P2: {b2} (must be present -> claim 1 FALSE)")
b3 = box(grn_r, 295, 332, 240, 300, True)
say(f"  lambda=3 green ink: {b3} (must be y304..321 -> claim 3 FALSE)")
b4 = box(blue_r, 190, 212, 455, 482, True)
say(f"  P1 arrow1 blue ink: {b4} (claim 6: arrows must be blue)")
b5 = box(red_r, 462, 496, 150, 295, True)
say(f"  invexpr red ink (X^T X + ^-1) in P3: {b5} (claim 4: ^-1 belongs to P3)")
b6 = box(blue_r, 296, 330, 165, 212, True)
say(f"  regmat blue (lam I) in P2: {b6} (claim 2: P1 header must NOT carry lambda)")
b7 = box(blue_r, 125, 258, 60, 215, True)
say(f"  P1 blue ink above/at header band: {b7} (claim 2: P1 header X^T X is RED, no lambda)")

say()
say("VERDICT: " + ("ALL MEASURED ELEMENTS MATCH" if not fails else f"elements to check: {fails}"))
txt = "\n".join(L) + "\n"
open(OUT, "w").write(txt)
print(txt)
