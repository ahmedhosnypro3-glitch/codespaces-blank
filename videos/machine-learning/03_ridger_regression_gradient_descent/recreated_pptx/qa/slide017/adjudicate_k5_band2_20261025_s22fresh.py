#!/usr/bin/env python3
"""Adjudication of the K=5 band2 crop-leg findings (slide 017, S22 fresh carrier).

Judge transcript crop_5_band2_judge.txt: FAIL, 1 MAJOR + 3 MINOR.
  MAJOR-1 row-label case (IMG1 X1/X2 vs IMG2 x1/x2)      -> measured here
  MINOR-2 superfluous W underline                        -> band-2 signature of the
        banked norm-underline item (render 145 vs orig 33 blue px, band 1)
  MINOR-3 norm-line color red (IMG1) vs blue (IMG2)      -> measured here
  MINOR-4 arrow fill hollow (IMG1) vs solid (IMG2)       -> certified pixels
        (render_5 vs render_4 diff confined to the left-paren columns;
        arrows untouched) — barred per band1 adjudication MINOR-4 precedent

Band 2 = slide frame y 255..395 (W box 2: y 265..389). Slide space 960x540;
render_5 scale S = height/540.
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
ri = np.asarray(Image.open(os.path.join(HERE, "render_5.png")).convert("RGB")).astype(int)
oi = np.asarray(Image.open(os.path.join(ROOT, "unique_slides", "slide_017.jpg")).convert("RGB")).astype(int)
S = ri.shape[0] / 540.0


def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gray = (abs(r - 233) < 22) & (abs(g - 233) < 22) & (abs(b - 231) < 24)
    white = a.sum(axis=2) > 735
    bg = gray | white
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10) & ~bg
    blue = (b > 90) & ((b - r) > 40) & ((g - r) < 30) & ~bg
    dark = (a.sum(axis=2) < 330) & ~bg
    return dict(red=red, blue=blue, dark=dark)


mo, mr = masks(oi), masks(ri)
ANY = lambda m: m["dark"] | m["blue"] | m["red"]


def sl(mask, ren, y0, y1, x0, x1):
    if ren:
        return mask[int(y0 * S):int(y1 * S) + 1, int(x0 * S):int(x1 * S) + 1]
    return mask[y0:y1 + 1, x0:x1 + 1]


def row_clusters(mask, ren, y0, y1, x0, x1, gap=2, min_ink=1):
    sub = sl(mask, ren, y0, y1, x0, x1)
    counts = sub.sum(axis=1)
    scale = S if ren else 1.0
    out = []
    for i, c in enumerate(counts):
        if c < min_ink:
            continue
        y = y0 + i / scale
        if out and y - out[-1][1] <= gap / scale:
            out[-1][1] = y
            out[-1][2] += int(c)
        else:
            out.append([y, y, int(c)])
    return [(round(a, 1), round(b, 1), c, round(b - a + 1 / scale, 1)) for a, b, c in out]


def bbox_of(mask, ren, y0, y1, x0, x1):
    sub = sl(mask, ren, y0, y1, x0, x1)
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    sc = S if ren else 1.0
    return (round(x0 + xs.min() / sc, 1), round(x0 + xs.max() / sc, 1),
            round(y0 + ys.min() / sc, 1), round(y0 + ys.max() / sc, 1), int(len(xs)))


print("== A. MAJOR-1: band-2 Train-table text rows, label column x84..140 ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    for a, b, c, h in row_clusters(ANY(m), ren, 255, 395, 84, 140):
        bb = bbox_of(ANY(m), ren, int(a), int(b) + 1, 84, 140)
        print(f"  {nm} rows y{a}..{b} h={h} ink={c} bbox_x=({bb[0]},{bb[1]})")

print("\n== A2. digit-height reference: value columns x150..350, same rows ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    for a, b, c, h in row_clusters(m["dark"], ren, 255, 395, 150, 350, min_ink=4):
        print(f"  {nm} dark rows y{a}..{b} h={h} ink={c}")

print("\n== A3. header row of table 2: blue/red cells y255..300 x84..350 ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    for key in ("blue", "red"):
        for a, b, c, h in row_clusters(m[key], ren, 255, 305, 84, 350, min_ink=3):
            bb = bbox_of(m[key], ren, int(a), int(b) + 1, 84, 350)
            print(f"  {nm} {key} rows y{a}..{b} h={h} ink={c} x=({bb[0]},{bb[1]})")

print("\n== B. MINOR-3: norm-line color, W-box 2 (slide y 347..385, x 505..624) ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    nb = int(sl(m["blue"], ren, 347, 385, 505, 624).sum())
    nr = int(sl(m["red"], ren, 347, 385, 505, 624).sum())
    print(f"  {nm}: blue px={nb} red px={nr}")

print("\n== C. MINOR-2: W underline, W-box 2 (blue rows under W glyph) ==")
for nm, m, ren in (("orig", mo, False), ("rend", mr, True)):
    for a, b, c, h in row_clusters(m["blue"], ren, 290, 325, 500, 570, min_ink=2):
        print(f"  {nm} blue rows y{a}..{b} h={h} ink={c}")
