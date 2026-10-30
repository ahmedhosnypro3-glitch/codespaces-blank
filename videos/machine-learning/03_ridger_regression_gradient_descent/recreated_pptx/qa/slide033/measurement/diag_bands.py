#!/usr/bin/env python3
"""Definitive region analysis: colour bands, interiors, text extents."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)


def band_scan(name, x0, x1, y0, y1, samp_x=None):
    """Dominant colour per row (sampled over a text-light strip)."""
    print(f"=== {name} row bands (x {x0}-{x1}, sampling every 3px) ===")
    if samp_x is None:
        samp_x = list(range(x0 + 6, x1, 7))
    prev = None; start = None; rows_out = []
    for y in range(y0, y1):
        cnt = Counter(tuple(o[y, xx]) for xx in samp_x)
        dom, n = cnt.most_common(1)[0]
        # treat near-identical as same
        if dom != prev:
            if prev is not None and y - start >= 3:
                rows_out.append((start, y - 1, prev))
            prev = dom; start = y
    if prev is not None:
        rows_out.append((start, y1 - 1, prev))
    for s, e, c in rows_out:
        print(f"  y {s:>3}-{e:>3} (h={e-s+1:>3}): {c}")
    print()


band_scan("TABLE bands", 90, 860, 318, 522)

print("=== COLUMN structure: scan a text-free row inside each band ===")
for ry in [345, 390, 460, 490]:
    print(f" row {ry}:")
    prev = None; start = None
    for x in range(88, 870):
        c = tuple(o[ry, x])
        if c != prev:
            if prev is not None and x - start >= 4:
                print(f"    x {start}-{x-1}: {prev}")
            prev = c; start = x
    print(f"    x {start}-869: {prev}")

print()
print("=== CENTER sage-green box interior (x 244-599, y 252-301) ===")
sub = o[254:300, 246:597].reshape(-1, 3)
print("  histogram:", Counter(map(tuple, sub)).most_common(12))

print("\n=== white-ish pixels inside that box (likely glyphs) ===")
m = (o[:, :, 0] > 235) & (o[:, :, 1] > 235) & (o[:, :, 2] > 235)
sel = m[254:300, 246:597]
ys, xs = np.where(sel)
if len(ys):
    print(f"  {len(ys)} white px, rows {254+ys.min()}-{254+ys.max()}, cols {246+xs.min()}-{246+xs.max()}")
    h, e = np.histogram(ys + 254, bins=20, range=(254, 300))
    print("  row hist:", [(int(e[i]), int(c)) for i, c in enumerate(h) if c])

print("\n=== PLOT region structure ===")
sub = o[60:320, 600:860].reshape(-1, 3)
print("  histogram:", Counter(map(tuple, sub)).most_common(14))

print("\n=== TEXT colour census by region ===")
def census(name, x0, y0, x1, y1):
    sub = o[y0:y1, x0:x1].reshape(-1, 3)
    # ink = anything far from the two backgrounds (white and panel gray)
    r_, g_, b_ = sub[:, 0], sub[:, 1], sub[:, 2]
    mx = np.maximum(np.maximum(r_, g_), b_); mn = np.minimum(np.minimum(r_, g_), b_)
    ink = (mx - mn) > 45
    if ink.sum() == 0:
        print(f"  {name}: no saturated ink")
        return
    c = Counter(map(tuple, sub[ink]))
    print(f"  {name}: {ink.sum()} saturated px; top:", c.most_common(8))

census("title", 190, 58, 450, 90)
census("subtitle L1", 100, 92, 520, 118)
census("subtitle L2", 190, 118, 840, 145)
census("param box", 75, 245, 180, 312)
census("center box", 246, 254, 597, 300)
census("center-right", 600, 175, 700, 240)
census("plot", 600, 60, 860, 320)
census("table rows", 90, 320, 868, 520)
