#!/usr/bin/env python3
"""Targeted PIL adjudication round 2 for slide 014 (color + fill extents)."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
ORIG = BASE + "unique_slides/slide_014.jpg"
REND = BASE + "recreated_pptx/qa/slide014/render_9.png"
SC = 2001 / 960.0

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)

def oc(box):
    return o[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

def rcb(box):
    return r[int(round(box[1]*SC)):int(round(box[3]*SC)), int(round(box[0]*SC)):int(round(box[2]*SC))]

def classify(a):
    """per-pixel ink color class census; returns counts dict + per-class bbox-free."""
    nw = a.sum(axis=2) > 700          # white-ish background
    ink = ~nw
    R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
    blue = ink & (B > R + 40) & (B > G + 40) & (B > 110)
    red = ink & (R > G + 40) & (R > B + 40) & (R > 110)
    green = ink & (G > R + 30) & (G > B + 30) & (G > 90)
    dark = ink & (R < 120) & (G < 120) & (B < 120)
    return dict(ink=int(ink.sum()), blue=int(blue.sum()), red=int(red.sum()),
                green=int(green.sum()), dark=int(dark.sum()))

print("== targeted color checks (orig-px windows) ==")
checks = [
    ("J(W) band2 (att-9#8/att-8#5)", (195, 303, 250, 341)),
    ("lambda+R(W) band2 tail", (600, 303, 900, 341)),
    ("Yhat=Y band1 (att-8#4)", (120, 243, 260, 285)),
    ("||W|| band1", (260, 243, 330, 285)),
    ("Ridge Reg band1", (700, 243, 900, 285)),
    ("Loss label define (att-8#6)", (150, 347, 260, 392)),
    ("squared distance define", (300, 347, 460, 392)),
    ("Loss Term box (att-8#7-ish)", (100, 399, 470, 448)),
    ("Reg Term box (att-9#9)", (540, 399, 880, 448)),
    ("final box (att-9#8/att-8#7)", (90, 469, 880, 528)),
]
for name, box in checks:
    co = classify(oc(box)); cr = classify(rcb(box))
    print(f"  {name}:")
    print(f"    ORIG {co}")
    print(f"    REND {cr}")

print()
print("== fill colors sampled at band centers ==")
for name, cx, cy in [("band1", 480, 264), ("band2", 480, 322), ("define", 380, 370),
                     ("termL", 250, 423), ("termR", 700, 423), ("final", 480, 498)]:
    so = o[cy, cx]; sr = r[int(cy*SC), int(cx*SC)]
    print(f"  {name}: ORIG rgb {tuple(so)}  REND rgb {tuple(sr)}")

print()
print("== fill extents with matched sampled color (tol 18) ==")
def fill_extent(img, box, center, tol=18):
    x0, y0, x1, y1 = box
    crop = img[y0:y1, x0:x1]
    ref = img[center[1], center[0]]
    d = np.abs(crop - ref).max(axis=2)
    m = d <= tol
    rows = np.where(m.mean(axis=1) > 0.5)[0]
    cols = np.where(m.mean(axis=0) > 0.5)[0]
    return (int(x0+cols[0]), int(y0+rows[0]), int(x0+cols[-1]), int(y0+rows[-1])) if len(rows) and len(cols) else None

for name, box, center in [
    ("band1", (40, 220, 920, 300), (480, 264)),
    ("band2", (40, 290, 920, 360), (480, 322)),
    ("define", (70, 330, 680, 410), (380, 370)),
    ("termL", (80, 390, 480, 455), (250, 423)),
    ("termR", (520, 390, 890, 455), (700, 423)),
    ("final", (80, 460, 890, 545), (480, 498)),
]:
    eo = fill_extent(o, box, center)
    er = fill_extent(r, box, (int(center[0]*SC), int(center[1]*SC)))
    if er:
        er = tuple(round(v/SC, 1) for v in er)
    print(f"  {name}: ORIG {eo}  REND(orig-px) {er}")

print()
print("== title extent (y60..100) ==")
def text_extent(img, box):
    x0, y0, x1, y1 = box
    g = np.array(Image.fromarray(img[y0:y1, x0:x1].astype('uint8')).convert("L"))
    ink = g < 140
    cols = np.where(ink.any(axis=0))[0]
    rows = np.where(ink.any(axis=1))[0]
    return (int(x0+cols[0]), int(y0+rows[0]), int(x0+cols[-1]), int(y0+rows[-1])) if len(cols) else None
print("  ORIG:", text_extent(o, (60, 55, 900, 105)))
print("  REND:", text_extent(r, (int(60*SC), int(55*SC), int(900*SC), int(105*SC))), "in orig-px:",
      (lambda t: None if not t else tuple(round(v/SC) for v in t))(text_extent(r, (int(60*SC), int(55*SC), int(900*SC), int(105*SC)))))

print()
print("== underline check: dark rule under target glyphs ==")
def underline_rows(img, box):
    x0, y0, x1, y1 = box
    g = np.array(Image.fromarray(img[y0:y1, x0:x1].astype('uint8')).convert("L"))
    ink = g < 140
    rowfrac = ink.mean(axis=1)
    return [round(float(v), 2) for v in rowfrac]
# define-band 'Loss' word around x150..200; underline would be a row with high fill just below baseline
print("  ORIG define x150..205 row-fill:", underline_rows(o, (150, 347, 205, 392)))
print("  REND define x150..205 row-fill:", underline_rows(r, (int(150*SC), int(347*SC), int(205*SC), int(392*SC))))
