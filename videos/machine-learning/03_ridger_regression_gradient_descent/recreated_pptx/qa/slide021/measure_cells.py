#!/usr/bin/env python3
"""measure_cells.py — strict-digit per-cell maps + glyph cluster counts.

Digits are near-black (core ~(33,34,32)); grid hairlines are gray
(core 109..144). A strict dark mask (r,g,b<95) isolates the digits.
Per cell: tight ink bbox, per-row-glyph x-clusters (count = glyph count),
and a 1px ASCII map so each digit can be decoded by eye.
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
dark = (a[..., 0] < 95) & (a[..., 1] < 95) & (a[..., 2] < 95)

TABLES = {
    "top": (98, 166, 234, 302, 174, 191, 209, 226),
    "mid": (90, 158, 226, 294, 342, 360, 377, 395),
    "bot": (422, 490, 558, 625, 458, 475, 493, 511),
}

def clusters(xs, gap=3):
    if not len(xs):
        return []
    out = []
    s = p = xs[0]
    for x in xs[1:]:
        if x - p > gap:
            out.append((s, p))
            s = x
        p = x
    out.append((s, p))
    return out

for tname, (c0, c1, c2, c3, r0, r1, r2, r3) in TABLES.items():
    cols = [c0, c1, c2, c3]
    rows = [r0, r1, r2, r3]
    print(f"===== {tname} TABLE =====")
    for ri in range(3):
        for ci in range(3):
            x0, x1 = cols[ci] + 1, cols[ci + 1] - 1   # exclude gridline cols
            y0, y1 = rows[ri] + 1, rows[ri + 1] - 1   # exclude gridline rows
            m = dark[y0:y1 + 1, x0:x1 + 1]
            if not m.any():
                print(f" r{ri+1}c{ci+1}: EMPTY")
                continue
            ys, xs = np.where(m)
            xa, xb = xs.min(), xs.max()
            ya, yb = ys.min(), ys.max()
            cl = clusters(sorted(set(xs.tolist())))
            glyphs = [f"{s+x0}..{e+x0}" for (s, e) in cl]
            print(f" r{ri+1}c{ci+1}: ink x{x0+xa}..{x0+xb} y{y0+ya}..{y0+yb} "
                  f"cap_h={yb-ya+1} adv={xb-xa+1} | glyph clusters ({len(cl)}): {glyphs}")
            for y in range(y0 + ya, y0 + yb + 1):
                print(f"    {y}: " + "".join("#" if dark[y, x] else "." for x in range(x0 + xa, x0 + xb + 1)))
    print()
