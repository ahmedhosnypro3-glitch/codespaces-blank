#!/usr/bin/env python3
"""PIL adjudication of slide 014 att-7/att-9 judge claims: render_9 vs original."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
ORIG = BASE + "unique_slides/slide_014.jpg"
REND = BASE + "recreated_pptx/qa/slide014/render_9.png"
SC = 2001 / 960.0

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
ro, rr = o.shape[0], r.shape[0]

def ocrop(box):
    return o[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

def rcrop(box):
    x0, x1 = int(round(box[0] * SC)), int(round(box[2] * SC))
    y0, y1 = int(round(box[1] * SC)), int(round(box[3] * SC))
    return r[y0:y1, x0:x1]

def is_white(a):
    return a.sum(axis=2) > 690

def is_pastel(a):
    """non-white, low-saturation fill (bands/boxes)."""
    s = a.sum(axis=2)
    mx = a.max(axis=2); mn = a.min(axis=2)
    return (s <= 690) & ((mx - mn) < 60)

def is_navy(a):
    return (a[:, :, 2] > a[:, :, 0] + 40) & (a[:, :, 2] > 60) & (a[:, :, 2] < 200) & (a[:, :, 0] < 120)

def is_maroon(a):
    return (a[:, :, 0] > a[:, :, 1] + 50) & (a[:, :, 0] > a[:, :, 2] + 50) & (a[:, :, 0] < 200)

def ink_classes(a):
    """count ink px by color class."""
    tot = a.shape[0] * a.shape[1]
    nonwhite = ~is_white(a)
    navy = is_navy(a) & nonwhite
    maroon = is_maroon(a) & nonwhite
    ink = nonwhite
    return dict(total=tot, ink=int(ink.sum()), navy=int(navy.sum()),
                maroon=int(maroon.sum()))

print("=" * 70)
print("A. VECTOR REGIONS (att-9 #1/#2 BLOCKER — expected CONFIRMED on render_9)")
for name, box in [("left y-vec", (150, 118, 232, 213)), ("right yhat-vec", (505, 118, 590, 213))]:
    ce = ink_classes(ocrop(box)); cr = ink_classes(rcrop(box))
    dens_o = ce["ink"] / ce["total"] * 100
    dens_r = cr["ink"] / cr["total"] * 100
    print(f"  {name}: ORIG ink {ce['ink']}/{ce['total']} ({dens_o:.2f}%)  "
          f"REND ink {cr['ink']}/{cr['total']} ({dens_r:.2f}%)  maroon o/r {ce['maroon']}/{cr['maroon']}")

print("=" * 70)
print("B. BAND GEOMETRY (att-9 #6/#7) — pastel-fill row/col extents")
def band_extent(img_crop, axis, fill_frac=0.35):
    """along axis: return [start,end] of the pastel-fill run."""
    p = is_pastel(img_crop)
    if axis == "row":
        prof = p.mean(axis=1)
    else:
        prof = p.mean(axis=0)
    idx = np.where(prof > fill_frac)[0]
    return (int(idx[0]), int(idx[-1])) if len(idx) else None

# build-declared bands (orig-frame px): name, x0,x1,y0,y1
bands = [
    ("band1 yellow", 60, 898, 243, 285),
    ("band2 yellow", 60, 898, 303, 341),
    ("define peach", 90, 665, 347, 392),
    ("term L peach2", 89, 471, 399, 448),
    ("term R paleyel", 533, 880, 399, 448),
    ("final cyan", 87, 880, 469, 528),
]
for name, x0, x1, y0, y1 in bands:
    # search window a bit larger than declared
    wx0, wy0, wx1, wy1 = x0 - 14, y0 - 14, x1 + 14, y1 + 14
    co, cr_ = ocrop((wx0, wy0, wx1, wy1)), rcrop((wx0, wy0, wx1, wy1))
    rowext_o = band_extent(co, "row"); rowext_r = band_extent(cr_, "row")
    colext_o = band_extent(co, "col"); colext_r = band_extent(cr_, "col")
    print(f"  {name}:")
    if rowext_o:
        print(f"    ORIG y {wy0+rowext_o[0]}..{wy0+rowext_o[1]}  x {wx0+colext_o[0]}..{wx0+colext_o[1]}")
    else:
        print("    ORIG none")
    if rowext_r and colext_r:
        y0r = (wy0 + rowext_r[0]) / SC; y1r = (wy0 + rowext_r[1]) / SC
        x0r = (wx0 + colext_r[0]) / SC; x1r = (wx0 + colext_r[1]) / SC
        print(f"    REND y {y0r:.1f}..{y1r:.1f}  x {x0r:.1f}..{x1r:.1f} (orig-px space)")
    else:
        print("    REND none")

print("=" * 70)
print("C. BAND TOP/BOTTOM RULES (att-9 #5 — build draws top+bottom rules)")
for name, x0, x1, y0, y1, kind in [
    ("band1", 60, 898, 243, 285, "navy"),
    ("band2", 60, 898, 303, 341, "navy"),
    ("define", 90, 665, 347, 392, "maroon"),
    ("final", 87, 880, 469, 528, "navy"),
]:
    for label, rows in [("top", (y0 - 2, y0 + 4)), ("bottom", (y1 - 4, y1 + 2))]:
        co = ocrop((x0 + 5, rows[0], x1 - 5, rows[1]))
        cr_ = rcrop((x0 + 5, rows[0], x1 - 5, rows[1]))
        if kind == "navy":
            mo, mr = is_navy(co).sum(), is_navy(cr_).sum()
        else:
            mo, mr = is_maroon(co).sum(), is_maroon(cr_).sum()
        print(f"  {name} {label}-rule {kind}: ORIG {mo}px  REND {mr}px")

print("=" * 70)
print("D. FONT SHAPE (att-9 #4 — serif vs sans); measure stroke widths in band1 text")
def stroke_profile(img_crop, label):
    a = np.array(Image.fromarray(img_crop.astype('uint8')).convert("L"))
    ink = a < 140
    if ink.sum() == 0:
        print(f"  {label}: no ink")
        return
    # horizontal run lengths of ink -> stem width estimate
    runs = []
    for row in ink:
        c = 0
        for v in row:
            if v:
                c += 1
            elif c:
                runs.append(c); c = 0
        if c: runs.append(c)
    runs = np.array(runs)
    print(f"  {label}: ink {ink.sum()}px, runs n={len(runs)}, median stem {int(np.median(runs))}, p90 {int(np.percentile(runs,90))}, max {runs.max()}")

stroke_profile(ocrop((100, 250, 300, 280)), "ORIG band1 text")
stroke_profile(rcrop((100, 250, 300, 280)), "REND band1 text")
stroke_profile(ocrop((150, 355, 400, 390)), "ORIG define text")
stroke_profile(rcrop((150, 355, 400, 390)), "REND define text")

print("=" * 70)
print("E. TITLE EXTENT (att-9 #11)")
def title_extent(img_crop, sc=1.0):
    a = np.array(Image.fromarray(img_crop.astype('uint8')).convert("L"))
    ink = a < 140
    cols = np.where(ink.any(axis=0))[0]
    return (int(cols[0] / sc), int(cols[-1] / sc), int(ink.sum())) if len(cols) else None
print("  ORIG title ink x-extent (origpx):", title_extent(ocrop((100, 62, 900, 100))))
print("  REND title ink x-extent (origpx):", title_extent(rcrop((100, 62, 900, 100)), SC))

print("=" * 70)
print("F. COLOR CENSUS in band2 (att-9 #8 / att-8 #5 J(W) blue-vs-black)")
for label, crop in [("ORIG", ocrop((100, 305, 850, 340))), ("REND", rcrop((100, 305, 850, 340)))]:
    nw = ~is_white(crop)
    navy = (is_navy(crop) & nw).sum()
    maroon = (is_maroon(crop) & nw).sum()
    dark = ((crop.sum(axis=2) < 260) & nw).sum()
    green = ((crop[:, :, 1] > crop[:, :, 0] + 25) & (crop[:, :, 1] > crop[:, :, 2] + 25) & nw).sum()
    print(f"  {label}: ink {nw.sum()}  dark(black) {dark}  navy/blue {navy}  red {maroon}  green {green}")

print("=" * 70)
print("G. 'Ŷ=Y' color in band1 (att-8 #4): red+underline expected in ORIG")
for label, crop in [("ORIG", ocrop((100, 250, 500, 280))), ("REND", rcrop((100, 250, 500, 280)))]:
    nw = ~is_white(crop)
    maroon = (is_maroon(crop) & nw).sum()
    dark = ((crop.sum(axis=2) < 260) & nw).sum()
    navy = (is_navy(crop) & nw).sum()
    green = ((crop[:, :, 1] > crop[:, :, 0] + 25) & (crop[:, :, 1] > crop[:, :, 2] + 25) & nw).sum()
    print(f"  {label}: ink {nw.sum()}  black {dark}  red {maroon}  blue {navy}  green {green}")
