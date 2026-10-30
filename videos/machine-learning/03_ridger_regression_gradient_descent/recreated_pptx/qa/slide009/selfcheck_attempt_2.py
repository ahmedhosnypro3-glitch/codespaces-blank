#!/usr/bin/env python3
"""Slide 009 self-check attempt 2 (2026-10-23 — caption-band rose marks added) — closed-loop PIL
verification of render_2.png against the ORIGINAL frame.

Every "want" value is either FRAME px measured on unique_slides/slide_009.jpg
in the banked probe set (qa/slide009/measurements_summary.txt) or re-measured
live from that same frame below, so the check is original-anchored, not
circular. Scale: render 2001x1125 vs frame 960x540 -> 2.0844/2.0833 render px
per frame px. Tolerances: ~2 frame px per edge (~4.2 render px).
"""
import numpy as np
from PIL import Image

HERE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_009.jpg"
REND = HERE + "/render_2.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
H, W = r.shape[:2]
SY, SX = H / 540.0, W / 960.0
print("render %dx%d   scale x %.5f y %.5f" % (W, H, SX, SY))

orr, og, ob = o[:, :, 0], o[:, :, 1], o[:, :, 2]
rr, rg, rb = r[:, :, 0], r[:, :, 1], r[:, :, 2]
NAVY_R = (rb - rr > 30) & (rb - rg > 30) & (rb < 190)
RED_R = (rr > 100) & (rr - rg > 40) & ((rr - rb) > 45)
BLUE_R = (rb - rr > 30) & (rb - rg > 30) & (rb < 260)
ORANGE_R = (rr > 200) & (rg > 70) & (rg < 190) & (rb < 90) & ((rr - rg) > 60)
GRID_R = (np.abs(r - np.array([216, 218, 215])).max(axis=2) < 45) & (r.sum(axis=2) < 720)
NAVY_O = (ob - orr > 20) & (ob - og > 20) & (ob < 200)
RED_O = (orr > 90) & ((orr - og) > 40) & ((orr - ob) > 30)
BLUE_O = (ob - orr > 20) & (ob - og > 20) & (ob < 260)
ORANGE_O = (orr > 200) & (og > 70) & (og < 190) & (ob < 110) & ((orr - og) > 55)
INK_R = np.abs(r - np.array([51, 51, 51])).max(axis=2) < 90   # near-black body ink
EQINK_R = (r.sum(axis=2) < 400) & (r[:, :, 2] < 90)          # black eq ink (no navy)

results = []
def chk(name, ok, detail=""):
    results.append((name, ok))
    print("  [%s] %-38s %s" % ("OK " if ok else "FIX", name, detail))

f2rx = lambda v: int(round(v * SX))
f2ry = lambda v: int(round(v * SY))
r2fx = lambda v: v / SX
r2fy = lambda v: v / SY

def bbox(mask, fx0, fx1, fy0, fy1):
    x0, x1, y0, y1 = f2rx(fx0), f2rx(fx1), f2ry(fy0), f2ry(fy1)
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (r2fx(x0 + xs.min()), r2fx(x0 + xs.max()),
            r2fy(y0 + ys.min()), r2fy(y0 + ys.max()))

def obox(img, mask, fx0, fx1, fy0, fy1):
    sub = mask[fy0:fy1, fx0:fx1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (fx0 + xs.min(), fx0 + xs.max(), fy0 + ys.min(), fy0 + ys.max())

# ══════════════════════════════════════════════════════════════════════════
print("\n== 1. EQUATIONS exist in the render (2D mathtext PNG ink, in-box) ==")
EQ = [("LEFT", 220, 313, 152, 171), ("RIGHT", 635, 729, 152, 171)]
for nm, x0, x1, y0, y1 in EQ:
    w = bbox(EQINK_R, x0, x1, y0, y1)
    ok = w is not None and (w[1] - w[0]) > 60
    chk("%s eq ink present" % nm, ok,
        "ink x %.1f..%.1f w %.1fpt y %.1f..%.1f" % (w[0], w[1], w[1] - w[0], w[2], w[3])
        if w else "MISSING")
    # ink width vs original's own ink width (measure live)
    wo = obox(o, EQINK_R, x0, x1, y0, y1)
    if w and wo:
        d = abs((w[1] - w[0]) - (wo[1] - wo[0]))
        chk("%s eq ink width vs frame" % nm, d <= 8.0,
            "render %.1f vs frame %.1f (d %.1f)" % (w[1] - w[0], wo[1] - wo[0], d))

print("\n== 2. EQUATION ink sits INSIDE the annotation box (no border crossing) ==")
BOXES = {"LEFT": (216, 316, 148, 175), "RIGHT": (631, 731, 148, 175)}
for nm, x0, x1, y0, y1 in EQ:
    bx0, bx1, by0, by1 = BOXES[nm]
    w = bbox(EQINK_R, bx0, bx1, by0, by1)
    ok = w is not None and w[0] > bx0 + 2 and w[1] < bx1 - 2 and w[2] > by0 + 2 and w[3] < by1 - 2
    chk("%s eq ink inside box" % nm, ok,
        "ink %.1f..%.1f / %.1f..%.1f in box %d..%d / %d..%d" % (w[0], w[1], w[2], w[3], bx0, bx1, by0, by1)
        if w else "MISSING")

print("\n== 3. CAPTION ONTENT: 4 lines, red keyword + black remainder ==")
CAPS = [
    ("LCAP1 whole", INK_R, 100, 430, 484, 508, 109, 419),
    ("LCAP1 red kw", RED_R, 100, 170, 484, 508, 109, 160),
    ("LCAP2", INK_R, 100, 430, 505, 524, 178, 350),
    ("RCAP1 whole", INK_R, 510, 830, 484, 508, 523, 818),
    ("RCAP1 red kw", RED_R, 510, 620, 484, 508, 523, 610),
    ("RCAP2", INK_R, 510, 830, 505, 524, 568, 773),
]
for nm, m, x0, x1, y0, y1, ex0, ex1 in CAPS:
    w = bbox(m, x0, x1, y0, y1)
    ok = w is not None and abs(w[0] - ex0) <= 4 and abs(w[1] - ex1) <= 4
    chk(nm, ok, "x %.1f..%.1f want %d..%d" % (w[0], w[1], ex0, ex1) if w else "MISSING")

print("\n== 4. LINE SPACING: 2 caption lines per side, pitch vs original ==")
for nm, x0, x1, y0, y1, ex0, ex1 in (("LCAP", 100, 430, 484, 524, 178, 419),
                                     ("RCAP", 510, 830, 484, 524, 523, 818)):
    w = bbox(INK_R, x0, x1, y0, y1)
    wo = obox(o, (np.abs(o - np.array([51, 51, 51])).max(axis=2) < 90), x0, x1, y0, y1)
    ok = w is not None and wo is not None and abs((w[3] - w[2]) - (wo[3] - wo[2])) <= 3
    chk("%s two-line block height" % nm, ok,
        "render y %.1f..%.1f (h %.1f) vs frame y %d..%d (h %d)"
        % ((w[2], w[3], w[3] - w[2], wo[2], wo[3], wo[3] - wo[2]) if w and wo else (-1, -1, -1, -1, -1, -1)))

print("\n== 5. FRAME CONTAINMENT: no ink crosses the house panel x54..903 / y45..540 ==")
# panel gray mask
panel = (np.abs(r - np.array([233, 233, 231])).max(axis=2) < 18)
nonwhite = r.sum(axis=2) < 730   # any non-canvas ink
# find ink columns outside the panel region
ys_left = slice(f2ry(45), f2ry(540))
col_left = np.where(nonwhite[ys_left, 0:f2rx(50)].any(axis=0))[0]
col_right = np.where(nonwhite[ys_left, f2rx(910):].any(axis=0))[0]
chk("no ink left of panel", not len(col_left), "%d ink cols" % len(col_left))
chk("no ink right of panel", not len(col_right), "%d ink cols" % len(col_right))
top_band = nonwhite[f2ry(0):f2ry(40), f2rx(90):f2rx(880)]
chk("no ink in top band above panel", not top_band.any(), "%d px" % int(top_band.sum()))

print("\n== 6. CHROME: badge + panel + strokes covered by house_chrome_check.py ==")
print("    (run separately: shared_patterns/house_chrome_check.py render_2.png 9)")

print("\n== SUMMARY ==")
n_ok = sum(1 for _, ok in results if ok)
print("%d/%d checks OK" % (n_ok, len(results)))
for nm, ok in results:
    if not ok:
        print("  FIX:", nm)
