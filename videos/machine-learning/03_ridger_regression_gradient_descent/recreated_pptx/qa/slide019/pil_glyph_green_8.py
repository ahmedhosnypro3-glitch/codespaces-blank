#!/usr/bin/env python3
"""Read the ORIGINAL's green numerals glyph-by-glyph (slide 019).

The coarse colour map shows the original carries green numerals inside the
table body at row bands y279..289 / y387..397 / y496..506, which is NOT where
the build paints its green 'y=' values (build: gy+44).  These numerals are
isolated in colour, so a 1-char-per-pixel ink map of the green mask alone is
directly readable.  This script prints, per row group, every green ink run
(>=3 px columns, phantom-trap law) and its ASCII glyph map.

It also prints the same map for the RENDER (resampled to 960x540) so the two
sets of green numerals can be compared position by position.
"""
from PIL import Image
import numpy as np

Q = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
     "recreated_pptx/qa/slide019")
ORIG = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "unique_slides/slide_019.jpg")

O = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
R = np.asarray(Image.open(f"{Q}/render_8.png").convert("RGB")
               .resize((960, 540), Image.LANCZOS)).astype(np.int16)


def green_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > r + 15) & (g > b + 15) & (g > 60) & (g < 235)


def runs(vals):
    out, s = [], None
    for i, v in enumerate(vals):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(vals) - 1))
    return out


def report(label, arr, band, x_lo=60, x_hi=900, y_lo=160, y_hi=540):
    gm = green_mask(arr)
    sub = gm[y_lo:y_hi, x_lo:x_hi]
    cols = sub.sum(axis=0)
    keep = np.nonzero(cols >= 3)[0]
    cruns = [(a + x_lo, b + x_lo) for a, b in runs(keep)]
    cruns = [c for c in cruns if c[1] - c[0] >= 2]
    print(f"### {label} :: {band}")
    for a, b in cruns:
        seg = gm[:, a:b + 1]
        rws = np.nonzero(seg.sum(axis=1) >= 3)[0]
        rr = runs(list(rws))
        for r0, r1 in rr:
            if r1 - r0 < 2:
                continue
            print(f"  green run x{a}..{b}  rows {r0}..{r1}")
            for y in range(r0, r1 + 1):
                row = "".join("#" if gm[y, x] else "." for x in range(a, b + 1))
                print(f"    {y:4d} {row}")
            print()
    print()


for name, gy in (("row1", 205), ("row2", 310), ("row3", 420)):
    report("ORIGINAL", O, name, y_lo=gy + 55, y_hi=gy + 115)
    report("RENDER", R, name, y_lo=gy + 55, y_hi=gy + 115)
