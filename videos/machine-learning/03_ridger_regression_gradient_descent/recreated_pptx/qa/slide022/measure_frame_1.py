#!/usr/bin/env python3
"""Measure original frame slide_022.jpg (960x540, 1px=1pt) for the build.

Goals (geometry from measurement, never intuition):
  1. Full-frame ink census — every non-background cluster, so nothing is missed.
  2. Title lines L1 '[3] Inverse of High Dimension', L2 '(non-singular) Matrix':
     ink bbox (x0..x1, y0..y1), ink center, darkest-core color, band height =>
     font-size + advance-fit estimate.
  3. Underline check: any solid red bar under L2 (sibling 020 has one)?
  4. Badge cluster position (house chrome sanity on THIS frame).
  5. Cursor cluster (video artifact, to be OMITTED — record it).
"""
import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_022.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# background sample: center of the panel, away from any ink
bg = im[150:200, 400:560].reshape(-1, 3).mean(axis=0)
print(f"background sample (panel interior) mean RGB = {bg.round(1)}")

# --- 1. ink census: everything that differs strongly from the panel gray ------
graydist = np.abs(im - np.array([233, 233, 231])).sum(axis=2)
ink = graydist > 60
ys, xs = np.where(ink)
print(f"ink px total = {ink.sum()}")
# row profile -> find bands
rows = np.where(ink.sum(axis=1) > 3)[0]
bands = []
if len(rows):
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y - p > 4:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
print("ink row bands (y0..y1, x-extent, npx):")
for (y0, y1) in bands:
    sel = ink[y0:y1 + 1]
    xs_ = np.where(sel.any(axis=0))[0]
    # split x runs into clusters (gap > 40 px = separate element)
    runs = []
    if len(xs_):
        st = xs_[0]; pv = xs_[0]
        for x in xs_[1:]:
            if x - pv > 40:
                runs.append((st, pv)); st = x
            pv = x
        runs.append((st, pv))
    for (x0, x1) in runs:
        sub = ink[y0:y1 + 1, x0:x1 + 1]
        print(f"  y {y0}..{y1}  x {x0}..{x1}  ({x1-x0+1}x{y1-y0+1})  npx={sub.sum()}")

# --- 2. title lines: red ink mask (C00000 family, JPEG-darkened ok) ----------
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
# but exclude the chrome strokes (x<70, x>895) and bottom rows > 530 from the
# TITLE measurement; keep badge yellow separate.
title_zone = np.zeros_like(red)
title_zone[60:500, 70:895] = True
tred = red & title_zone
ys2, xs2 = np.where(tred)
print(f"\nred ink px in title zone = {tred.sum()}")
if tred.sum():
    tbands = []
    rows2 = np.where(tred.sum(axis=1) > 2)[0]
    if len(rows2):
        s = rows2[0]; p = rows2[0]
        for y in rows2[1:]:
            if y - p > 6:
                tbands.append((s, p)); s = y
            p = y
        tbands.append((s, p))
    for i, (y0, y1) in enumerate(tbands):
        sel = tred[y0:y1 + 1]
        xs_ = np.where(sel.any(axis=0))[0]
        # per-line glyph row profile for cap-height estimate
        prof = sel.sum(axis=1)
        print(f"  title band {i}: y {y0}..{y1} (h={y1-y0+1}), x {xs_.min()}..{xs_.max()} (w={xs_.max()-xs_.min()+1}), "
              f"row-ink max={prof.max()}, ink center=({(xs_.min()+xs_.max())/2:.1f},{(y0+y1)/2:.1f})")
        # dense glyph rows (rows with real ink, not AA halo)
        dense = np.where(prof > 2)[0]
        print(f"    dense glyph rows: y {y0+dense.min()}..{y0+dense.max()}")
    # darkest core color
    core = im[tred]
    if len(core):
        dk = core[core.sum(axis=1).argmin()]
        print(f"  darkest red-core RGB = {tuple(dk)}")
        # median of strong cores
        strong = core[(core[:, 0] > 120)]
        if len(strong):
            print(f"  median strong-red RGB = {tuple(np.median(strong, axis=0).astype(int))}")

# --- 3. underline check: solid wide red rows between the two bands / below L2 -
print("\nunderline check (rows with red-run width > 200px in title zone):")
for y in range(60, 500):
    row = tred[y]
    if row.sum() > 200:
        xs_ = np.where(row)[0]
        # longest contiguous run
        runs = np.split(xs_, np.where(np.diff(xs_) > 3)[0] + 1)
        longest = max(runs, key=len)
        print(f"  row {y}: red px {row.sum()}, longest run x {longest.min()}..{longest.max()} (len {len(longest)})")

# --- 4. badge on THIS frame (yellow disc) -------------------------------------
yel = (r > 200) & (g > 200) & (b < 190)
ys3, xs3 = np.where(yel)
if len(ys3):
    print(f"\nbadge yellow disc: x {xs3.min()}..{xs3.max()}, y {ys3.min()}..{ys3.max()} "
          f"=> center ({(xs3.min()+xs3.max())/2:.1f},{(ys3.min()+ys3.max())/2:.1f}) d~{xs3.max()-xs3.min()+1}")

# --- 5. cursor cluster (white pointer w/ black outline) -----------------------
# dark px (near-black) not part of red text, excluding badge ring/numeral zone
dark = (r < 90) & (g < 90) & (b < 90)
badge_zone = np.zeros_like(dark)
badge_zone[max(ys3.min()-8,0):ys3.max()+8, max(xs3.min()-8,0):xs3.max()+8] = True if len(xs3) else False
dz = dark & ~badge_zone
ys4, xs4 = np.where(dz)
if len(ys4):
    # cluster by rows
    rows4 = np.where(dz.sum(axis=1) > 1)[0]
    if len(rows4):
        print("\nnear-black ink bands (cursor outline / numeral / other):")
        s = rows4[0]; p = rows4[0]
        for y in rows4[1:]:
            if y - p > 6:
                blk = dz[s:p + 1]
                xb = np.where(blk.any(axis=0))[0]
                print(f"  y {s}..{p}, x {xb.min()}..{xb.max()}, npx={blk.sum()}")
                s = y
            p = y
        blk = dz[s:p + 1]
        xb = np.where(blk.any(axis=0))[0]
        print(f"  y {s}..{p}, x {xb.min()}..{xb.max()}, npx={blk.sum()}")

# white px inside the slide that are NOT panel gray and NOT badge (cursor fill)
white = (r > 245) & (g > 245) & (b > 245)
wz = white & ~badge_zone
ys5, xs5 = np.where(wz)
print(f"\nbright-white px outside badge: {wz.sum()}")
if wz.sum():
    rows5 = np.where(wz.sum(axis=1) > 1)[0]
    if len(rows5):
        s = rows5[0]; p = rows5[0]
        for y in rows5[1:]:
            if y - p > 6:
                blk = wz[s:p + 1]
                xb = np.where(blk.any(axis=0))[0]
                print(f"  white band y {s}..{p}, x {xb.min()}..{xb.max()}, npx={blk.sum()}")
                s = y
            p = y
        blk = wz[s:p + 1]
        xb = np.where(blk.any(axis=0))[0]
        print(f"  white band y {s}..{p}, x {xb.min()}..{xb.max()}, npx={blk.sum()}")
