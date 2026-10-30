#!/usr/bin/env python3
"""Extended forensics for slide_002.jpg (resumed worker, 2026-10-19).

Adds what measure_original.py/glyph_forensics.py did not bank:
  1. plus-sign zone ASCII art with a RELATIVE-ink mask (vs local panel fill),
     to pin the artifact's true bbox, stroke weight, color, and shape;
  2. badge window ASCII art (numeral + ring) vs house_chrome.js law;
  3. line-2 baseline / descender pin and per-line exact ink edges;
  4. full-slide relative-ink census (any content we have not accounted for);
  5. title core-color sample (brightest 2% = nominal draw color).
All coords in frame px (960x540, 1px = 1pt).
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_002.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# relative ink: distance from the local panel fill (E9E9E7 ~ (231,233,230))
PANEL = np.array([231, 233, 230])
dist = np.abs(IM - PANEL).max(axis=2)
ink = dist > 28  # relative mask, JPEG-safe on both sides

def art(x0, x1, y0, y1, step=1):
    print(f"--- window x{x0}..{x1} y{y0}..{y1} (relative ink) ---")
    for y in range(y0, y1 + 1, step):
        print(f"{y:3d} " + "".join("#" if ink[y, x] else "." for x in range(x0, x1 + 1)))

print("=" * 70)
print("1. PLUS-SIGN ZONE  x690..870  y30..100")
art(690, 870, 30, 100)
zs = ink[30:100, 690:870]
ys, xs = np.where(zs)
if len(ys):
    print(f"zone ink bbox: x {690+xs.min()}..{690+xs.max()}  y {30+ys.min()}..{30+ys.max()}  n={len(ys)}")
    pts = IM[30:100, 690:870][zs]
    print(f"zone ink mean rgb: {pts.mean(axis=0).round(0)}")
    # row/col profiles
    rp = zs.sum(axis=1)
    cp = zs.sum(axis=0)
    print("row profile:", {30 + i: int(v) for i, v in enumerate(rp) if v})
    print("col profile:", {690 + i: int(v) for i, v in enumerate(cp) if v})

print("=" * 70)
print("2. BADGE WINDOW  x850..905  y50..100")
art(850, 905, 50, 100)

print("=" * 70)
print("3. TITLE LINES — exact ink edges (core mask, strict red)")
tit = (r > 150) & (g < 110) & (b < 110)
for (y0, y1, name) in [(195, 240, "line1"), (270, 320, "line2")]:
    band = tit[y0:y1 + 1, :]
    ys, xs = np.where(band)
    rows = np.where(band.sum(axis=1) > 0)[0]
    print(f"{name}: ink rows {y0+rows.min()}..{y0+rows.max()}  x {xs.min()}..{xs.max()}")

# line-2 word gaps recheck (col profile inside band)
band2 = tit[274:315, :]
colsum = band2.sum(axis=0)
on = np.where(colsum > 0)[0]
gaps, in_g, gs = [], False, 0
for x in range(on.min(), on.max() + 1):
    if colsum[x] == 0 and not in_g:
        in_g, gs = True, x
    elif colsum[x] > 0 and in_g:
        in_g = False
        if x - gs >= 8:
            gaps.append((gs, x - 1))
print(f"line2 word gaps >=8px: {gaps}")

print("=" * 70)
print("4. FULL-SLIDE relative-ink census by region")
# exclude known chrome bands: strokes at x58,901 y46..539, bottom y537..539,
# badge box x855..900 y54..95, title x190..760 y195..320, plus zone x690..870 y30..100
mask = ink.copy()
mask[44:100, 0:960] = mask[44:100, 0:960] & False   # top band handled separately below
regions = {
    "top band y44..100 (excl badge x855..900)": (slice(44, 100), slice(0, 855)),
    "badge box x855..905 y50..100": (slice(50, 100), slice(855, 905)),
    "left of title x0..190 y100..530": (slice(100, 530), slice(0, 190)),
    "right of title x760..960 y100..530": (slice(100, 530), slice(760, 960)),
    "between title lines y235..270 x150..800": (slice(235, 270), slice(150, 800)),
    "below title y320..535 x54..903": (slice(320, 535), slice(54, 903)),
}
for name, (sy, sx) in regions.items():
    ys, xs = np.where(ink[sy, sx])
    if len(ys):
        print(f"{name}: n={len(ys)} bbox x {sx.start+xs.min()}..{sx.start+xs.max()} y {sy.start+ys.min()}..{sy.start+ys.max()}")
    else:
        print(f"{name}: clean")

print("=" * 70)
print("5. TITLE core color (top 2% brightest red ink)")
core = np.where(tit)
vals = IM[core]
order = np.argsort(vals[:, 0].astype(int))[-int(len(vals) * 0.02):]
print(f"core red mean rgb: {vals[order].mean(axis=0).round(0)}")

print("=" * 70)
print("6. STROKE bands sanity (house chrome vs frame)")
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
for nm, sl in {
    "left stroke rows 47..539 @ x58": (slice(47, 540), slice(55, 62)),
    "right stroke rows 47..539 @ x901": (slice(47, 540), slice(897, 905)),
    "bottom stroke rows 535..539": (slice(535, 540), slice(54, 904)),
    "top band y0..44 x80..880": (slice(0, 44), slice(80, 880)),
}.items():
    ys, xs = np.where(red[sl])
    print(f"{nm}: n={len(ys)}", f"y {sl.start+ys.min()}..{sl.start+ys.max()}" if len(ys) else "")
