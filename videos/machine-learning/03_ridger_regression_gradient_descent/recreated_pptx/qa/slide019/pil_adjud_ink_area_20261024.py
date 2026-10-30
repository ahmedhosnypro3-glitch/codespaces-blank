#!/usr/bin/env python3
"""DECISIVE ADJUDICATION: which NO REG rows 2/3 y-values does the original show?

Method — relative ink-area calibration with in-frame controls:
  * For every y-value cell, measure dark-ink pixel count inside the cell's
    y-line band (adaptive local threshold).
  * Controls: cells whose values ALL lanes agree on (NO REG g1 = 60/80/100;
    Ridge λ=3 and λ=10 rows = the JSON values) calibrate "ink per glyph".
  * The disputed cells are then classified by ink count against the two
    candidate strings rendered at the SAME pipeline (font/size) so the
    calibration is apples-to-apples.

Both images measured; original (frame px) and render (px * 72/150).
"""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
REND = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_8.png"

Ao = np.asarray(Image.open(ORIG).convert("L")).astype(float)
Ar = np.asarray(Image.open(REND).convert("L")).astype(float)
S = Ar.shape[0] / 540.0

# column + test-box geometry (frame px) matching the build
COLS = {
    "NOREG": (124, 380, 206),
    "R3":    (384, 640, 466),
    "R10":   (644, 900, 726),
}
XTW = 58.0   # test box width (build: (x1-x0-82)/3)

def cell_boxes(colname):
    x0, x1, xt = COLS[colname]
    return [(xt + i * XTW + 2, xt + (i + 1) * XTW - 2) for i in range(3)]

YLINE = {1: (253, 269), 2: (360, 378), 3: (469, 487)}

def ink_in(img, x0, x1, y0, y1, frac=0.5):
    """Dark-ink count with adaptive threshold = bg - frac*(bg-min)."""
    reg = img[int(y0):int(y1), int(x0):int(x1)]
    if reg.size == 0:
        return 0, None
    bg = np.percentile(reg, 85)
    mn = reg.min()
    thr = bg - frac * (bg - mn)
    m = reg < thr
    return int(m.sum()), thr

print("scale render->frame = 1/%.4f" % S)

# ---- Reference calibration: how much ink does each candidate string produce? ----
# Render the candidate strings with the actual pipeline (pptxgenjs render_8 == hyp B).
# Instead of re-rendering, calibrate from the render's OWN known cells.
print("\n=== RENDER ink (hyp B build, known strings) — calibration ===")
for cn in COLS:
    for gi in range(1, 4):
        yy = YLINE[gi]
        row = []
        for bi, (a, b) in enumerate(cell_boxes(cn)):
            n, thr = ink_in(Ar, a * S, b * S, yy[0] * S, yy[1] * S)
            row.append(n)
        print(f"  {cn} g{gi}: {row}")

print("\n=== ORIGINAL ink (same cells) ===")
res = {}
for cn in COLS:
    for gi in range(1, 4):
        yy = YLINE[gi]
        row = []
        for bi, (a, b) in enumerate(cell_boxes(cn)):
            n, thr = ink_in(Ao, a, b, yy[0], yy[1])
            row.append(n)
        res[(cn, gi)] = row
        print(f"  {cn} g{gi}: {row}")

# ---- Normalize: original is 1px=1pt antialiasing, render is 2.083x. Compare SHAPES
#      by rescaling the render's ink to frame-px area, and also compute the
#      per-cell ratio original/render_scaled as a relative fingerprint.
print("\n=== per-cell ink ratio (original / (render/scale^2)) ===")
for k, v in res.items():
    cn, gi = k
    rrow = []
    for bi, (a, b) in enumerate(cell_boxes(cn)):
        n, _ = ink_in(Ar, a * S, b * S, YLINE[gi][0] * S, YLINE[gi][1] * S)
        nr = n / (S * S)
        rrow.append(v[bi] / nr if nr else float("nan"))
    print(f"  {k}: orig/rescaled-render = {['%.2f' % x for x in rrow]}")

print("\n=== GLYPH COUNT per cell (connected clusters, adaptive) ===")
def glyphs(img, x0, x1, y0, y1, scale=1.0, frac=0.5, gap=1):
    reg = img[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    bg = np.percentile(reg, 85); mn = reg.min()
    thr = bg - frac * (bg - mn)
    m = reg < thr
    cols = m.sum(axis=0)
    out, cur = [], None
    for i, v in enumerate(cols):
        if v > 0:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        else:
            if cur is not None:
                out.append(cur); cur = None
    if cur is not None:
        out.append(cur)
    # merge clusters closer than `gap`
    merged = []
    for c in out:
        if merged and c[0] - merged[-1][1] - 1 <= gap:
            merged[-1][1] = c[1]
        else:
            merged.append(list(c))
    ws = [c[1] - c[0] + 1 for c in merged]
    return len(merged), ws

for cn in COLS:
    for gi in range(1, 4):
        o, rr = [], []
        for bi, (a, b) in enumerate(cell_boxes(cn)):
            n1, w1 = glyphs(Ao, a, b, *YLINE[gi])
            n2, w2 = glyphs(Ar, a * S, b * S, *YLINE[gi])
            o.append((n1, w1)); rr.append((n2, w2))
        print(f"  {cn} g{gi}: orig(glyphs)={[x[0] for x in o]} render={[x[0] for x in rr]}")
