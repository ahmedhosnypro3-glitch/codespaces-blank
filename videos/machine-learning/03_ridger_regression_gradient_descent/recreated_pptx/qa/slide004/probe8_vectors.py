#!/usr/bin/env python3
"""ATTEMPT-8 MEASUREMENT — vector internals, where-line glyphs, LO subscript calibration.

Sections:
  A. box1 / box2 vector regions (red ink): paren stroke columns, ink bboxes,
     entry row bands, "N x 1" label bbox, stroke/entry/label colors.
  B. lead-in bands "Let Y =" (box1) / "Let Yh =" (box2): glyph bboxes + ink density.
  C. where-line L1/L2/L3: main-glyph heights vs subscript glyph heights
     (chooses the subscript fontSize for the build).
  D. LO subscript calibration from the certified slide003 render_33.png:
     matrix-entry main-glyph height vs its subscript digit height
     (build used same-size 11pt runs with subscript:true).
"""
from PIL import Image
import numpy as np

BASE = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")

orig = Image.open(f"{BASE}/unique_slides/slide_004.jpg").convert("RGB")
A = np.asarray(orig).astype(int)
render33 = Image.open(f"{BASE}/recreated_pptx/qa/slide003/render_33.png").convert("RGB")
R33 = np.asarray(render33).astype(int)


def red_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 130) & (r - g > 45) & (r - b > 45)


def dark_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r + g + b) < 420


def bands(mask_1d, min_gap=2, min_run=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for v in idx[1:]:
        if v - p > min_gap:
            if p - s + 1 >= min_run:
                out.append((s, p))
            s = v
        p = v
    if p - s + 1 >= min_run:
        out.append((s, p))
    return out


def med_rgb(a, mask):
    px = a[mask]
    if len(px) == 0:
        return None
    return tuple(int(v) for v in np.median(px, axis=0))


def section_vector(name, x0, x1, y0, y1):
    reg = A[y0:y1, x0:x1]
    m = red_mask(reg)
    cols = np.where(m.any(axis=0))[0]
    rows = np.where(m.any(axis=1))[0]
    print(f"\n== {name} region x{x0}..{x1} y{y0}..{y1}")
    if len(cols) == 0:
        print("   NO RED INK")
        return
    colb = bands(m.any(axis=0), min_gap=3)
    rowb = bands(m.any(axis=1), min_gap=3)
    print(f"   red col bands (abs x): {[(x0 + s, x0 + e) for s, e in colb]}")
    print(f"   red row bands (abs y): {[(y0 + s, y0 + e) for s, e in rowb]}")
    # stroke columns = outermost col bands; entries = interior col bands
    stroke_cols = np.zeros_like(m)
    stroke_cols[:, colb[0][0]:colb[0][1] + 1] = m[:, colb[0][0]:colb[0][1] + 1]
    stroke_cols[:, colb[-1][0]:colb[-1][1] + 1] = m[:, colb[-1][0]:colb[-1][1] + 1]
    print(f"   L stroke col rows (abs): {[(y0 + s, y0 + e) for s, e in bands(stroke_cols.any(axis=1), min_gap=4)]}")
    print(f"   stroke color median: {med_rgb(reg, stroke_cols)}")
    # entries: red ink excluding the two stroke bands
    inner = np.zeros_like(m)
    inner[:, colb[0][1] + 1:colb[-1][0]] = True
    ent = m & inner
    entrows = bands(ent.any(axis=1), min_gap=3)
    print(f"   entry row bands (abs y): {[(y0 + s, y0 + e) for s, e in entrows]}")
    for s, e in entrows:
        seg = ent[s:e + 1]
        cb = bands(seg.any(axis=0), min_gap=2)
        print(f"      row y{y0+s}..{y0+e}: col bands abs x {[(x0+c, x0+d) for c, d in cb]} color {med_rgb(reg[s:e+1], seg)}")
    # label: red ink below the strokes
    lab = m.copy()
    lab[:max(e for _, e in entrows[:1]) + 2] = False
    lab[:, :colb[0][0]] = False
    lab[:, colb[-1][1] + 1:] = True  # label may extend right of R stroke
    labrows = bands(lab.any(axis=1), min_gap=3)
    for s, e in labrows:
        if s < (entrows[0][0] if entrows else 0):
            continue
        seg = lab[s:e + 1]
        cb = bands(seg.any(axis=0), min_gap=2)
        print(f"   label band y{y0+s}..{y0+e}: cols abs {[(x0+c, x0+d) for c, d in cb]} color {med_rgb(reg[s:e+1], seg)}")


def section_lead(name, x0, x1, y0, y1):
    reg = A[y0:y1, x0:x1]
    d = dark_mask(reg)
    rows = bands(d.any(axis=1), min_gap=3)
    cols = bands(d.any(axis=0), min_gap=3)
    print(f"\n== {name} x{x0}..{x1} y{y0}..{y1}")
    print(f"   dark row bands abs: {[(y0+s, y0+e) for s, e in rows]}")
    print(f"   dark col bands abs: {[(x0+s, x0+e) for s, e in cols]}")
    print(f"   ink px: {int(d.sum())} density over glyph bbox: ", end="")
    if d.any():
        rs, cs = np.where(d)
        print(f"{d.sum() / ((rs.max()-rs.min()+1) * (cs.max()-cs.min()+1)):.3f}")
    # red underline bar hunt (thin wide red run)
    m = red_mask(reg)
    for s, e in bands(m.any(axis=1), min_gap=1):
        seg = m[s:e + 1]
        w = seg.any(axis=0).sum()
        if w >= 8 and (e - s) <= 4:
            print(f"   RED BAR rows y{y0+s}..{y0+e} width {w}")


def section_whereline(name, x0, x1, y0, y1):
    reg = A[y0:y1, x0:x1]
    d = dark_mask(reg) | red_mask(reg)
    rowb = bands(d.any(axis=1), min_gap=3)
    print(f"\n== {name} x{x0}..{x1} y{y0}..{y1} row bands: {[(y0+s, y0+e) for s, e in rowb]}")
    for s, e in rowb:
        seg = d[s:e + 1]
        cb = bands(seg.any(axis=0), min_gap=2)
        desc = []
        for c, cc in cb:
            sub = seg[:, c:cc + 1]
            rr = np.where(sub.any(axis=1))[0]
            col = med_rgb(reg[s:e + 1, c:cc + 1], sub)
            desc.append(f"x{x0+c}..{x0+cc} h{rr.max()-rr.min()+1} {col}")
        print(f"   band y{y0+s}..{y0+e}:")
        for t in desc:
            print(f"      {t}")


def section_lo33(name, x0, x1, y0, y1):
    reg = R33[y0:y1, x0:x1]
    d = dark_mask(reg)
    rowb = bands(d.any(axis=1), min_gap=2)
    print(f"\n== {name} (render_33, 2001x1125, SX=2001/960={2001/960:.4f}) x{x0}..{x1} y{y0}..{y1}")
    for s, e in rowb:
        seg = d[s:e + 1]
        cb = bands(seg.any(axis=0), min_gap=2)
        for c, cc in cb:
            sub = seg[:, c:cc + 1]
            rr = np.where(sub.any(axis=1))[0]
            print(f"   y{y0+s}..{y0+e} x{x0+c}..{x0+cc} h{rr.max()-rr.min()+1}")


print("### A. VECTORS")
section_vector("BOX1 vector (Y)", 150, 225, 105, 215)
section_vector("BOX2 vector (Yhat)", 495, 570, 105, 218)

print("\n### B. LEAD-INS")
section_lead("BOX1 lead-in 'Let Y ='", 82, 156, 136, 170)
section_lead("BOX2 lead-in 'Let Yh ='", 428, 500, 140, 175)

print("\n### C. WHERE LINES (main vs subscript heights)")
section_whereline("L1", 500, 780, 283, 306)
section_whereline("L2", 570, 780, 313, 336)
section_whereline("L3", 560, 780, 343, 366)
section_whereline("L1 outcome", 770, 880, 283, 306)
section_whereline("L2 outcome", 770, 880, 313, 336)
section_whereline("L3 outcome", 770, 880, 343, 366)

print("\n### D. LO SUBSCRIPT CALIBRATION (slide003 certified render)")
# slide003 build: matrix entries 11pt 'x' + 11pt subscript digit, at x194..388 y362..484 frame
# frame->render scale 2001/960
SX = 2001 / 960
SY = 1125 / 540
fx0, fx1 = int(196 * SX), int(232 * SX)
fy0, fy1 = int(366 * SY), int(484 * SY)
section_lo33("s003 matrix entries", fx0, fx1, fy0, fy1)
