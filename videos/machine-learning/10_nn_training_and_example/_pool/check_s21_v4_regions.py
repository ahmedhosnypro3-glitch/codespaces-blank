#!/usr/bin/env python3
"""Closed-loop check that slide_021 v4's equation regions contain TYPESET math,
not literal mathtext source.

Method: for each equation region of the 150dpi render, count vertical ink bands
and the longest horizontal ink run. Literal source text is a single flat line
of glyphs (1-2 bands, no wide run); typeset math with subscripts and a Sigma
limit has >=2 bands and a tall glyph column structure.

Also reports ink colour census per region: typeset math here carries the
original's colour coding (blue O_i, green O_j(1-O_j), red sum term).
"""
import sys
import numpy as np
from PIL import Image

render = sys.argv[1]
im = Image.open(render).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
SX = W / 13.33   # inches -> px
SY = H / 7.5

REGIONS = {
    # name: (x_in, y_in, w_in, h_in) — exact placements from slide_021_v4.js
    "strip_eq1": (3.559, 3.963, 3.48167, 0.6),
    "bottom_eq2": (4.681, 5.442, 1.23833, 0.28833),
    "bottom_eq3": (3.372, 5.913, 3.85667, 0.59667),
}

for name, (x, y, w, h) in REGIONS.items():
    px0, py0 = int(x * SX), int(y * SY)
    px1, py1 = int((x + w) * SX), int((y + h) * SY)
    reg = a[max(py0, 0):py1, max(px0, 0):px1]
    ink = (reg < 200).any(axis=2)
    if not ink.any():
        print(f"{name}: EMPTY region")
        continue
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    rowdens = ink.any(axis=1).view(np.int8)
    bands = int(np.sum(np.diff(np.concatenate(([0], rowdens, [0]))) == 1))
    longest = 0
    for i in range(ink.shape[0]):
        r = ink[i]
        if not r.any():
            continue
        d = np.diff(np.concatenate(([0], r.view(np.int8), [0])))
        st = np.where(d == 1)[0]
        en = np.where(d == -1)[0]
        if len(st):
            longest = max(longest, int((en - st).max()))
    # colour census of dark-ish ink
    dark = ink & (reg.sum(axis=2) < 600)
    cols_present = set()
    for c in [(0, 0, 200), (0, 120, 0), (200, 0, 0)]:
        m = (np.abs(reg - np.array(c)).sum(axis=2) < 150) & ink
        if m.sum() > 12:
            cols_present.add(c)
    print(f"{name}: ink {cols[-1]-cols[0]+1}x{rows[-1]-rows[0]+1} "
          f"bands={bands} longest_run={longest}px colors={sorted(cols_present)}")
    print(f"    top_row={rows[0]} bottom_row={rows[-1]} "
          f"left_col={cols[0]} right_col={cols[-1]}")
