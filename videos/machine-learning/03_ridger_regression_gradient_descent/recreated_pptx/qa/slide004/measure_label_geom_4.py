#!/usr/bin/env python3
"""Banked measurement for MAJOR finding #1 of judge_attempt_4.

Question: in the two top "Let" boxes, do the red/blue label captions sit as
vertical flanks to the RIGHT of the Y / Y-hat matrices (judge's claim), or as
horizontal sentences stacked above/below them (recreation's claim)?

Method: region-locked colour masks + 1-D ink profiles. No visual reading.
"""
from PIL import Image

VID = "."
ORIG = f"{VID}/unique_slides/slide_004.jpg"
RENDER = f"{VID}/recreated_pptx/qa/slide004/render_4.png"

o = Image.open(ORIG).convert("RGB")
r = Image.open(RENDER).convert("RGB").resize((960, 540), Image.LANCZOS)
opx, rpx = o.load(), r.load()

# Box interiors, border ring excluded
BOX1 = (82, 103, 392, 220)
BOX2 = (582, 103, 871, 220)

RED = lambda p: p[0] > 170 and p[1] < 100 and p[2] < 100 and p[0] - max(p[1], p[2]) > 90
BLUE = lambda p: p[2] > 140 and p[0] < 110 and p[1] < 110 and p[2] - max(p[0], p[1]) > 60
DARK = lambda p: p[0] < 200 and p[1] < 200 and p[2] < 200


def pix_rows(px, pred, box):
    x0, y0, x1, y1 = box
    rows = {}
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                rows.setdefault(y, []).append(x)
    return rows


def band(px, pred, box, tag):
    rows = pix_rows(px, pred, box)
    if not rows:
        print(f"{tag}: NONE")
        return None
    ys, xs = [], []
    for y, v in rows.items():
        ys.append(y)
        xs.extend(v)
    bb = (min(xs), min(ys), max(xs), max(ys))
    w, h = bb[2] - bb[0] + 1, bb[3] - bb[1] + 1
    nrows = len(rows)
    print(f"{tag}: x{bb[0]}..{bb[2]} y{bb[1]}..{bb[3]}  w={w} h={h} rows={nrows} "
          f"avg_px/row={len(xs)/nrows:.0f} w/h={w/h:.1f}")
    return bb


print("### ORIGINAL, Box1 'Let Y' interior x82..392 y103..220")
band(opx, RED, BOX1, "ORIG red caption   ")
band(opx, BLUE, BOX1, "ORIG blue caption  ")
print()
print("### ORIGINAL, Box2 'Let Yhat' interior x582..892 y103..220")
band(opx, RED, BOX2, "ORIG red caption   ")
band(opx, BLUE, BOX2, "ORIG blue caption  ")
print()

print("### ORIGINAL Box1 dark-ink column profile (n>=15):")
x0, y0, x1, y1 = BOX1
colpr = []
for x in range(x0, x1):
    c = sum(1 for y in range(y0, y1) if DARK(opx[x, y]))
    colpr.append((x, c))
for x, c in colpr:
    if c >= 15:
        print(f"  x={x}: n={c}")
print()
print("### ORIGINAL Box2 dark-ink column profile (n>=15):")
x0, y0, x1, y1 = BOX2
for x in range(x0, x1):
    c = sum(1 for y in range(y0, y1) if DARK(opx[x, y]))
    if c >= 15:
        print(f"  x={x}: n={c}")
print()

print("### RENDER_4, Box1 region")
band(rpx, RED, BOX1, "REND red caption   ")
band(rpx, BLUE, BOX1, "REND blue caption  ")
print()
print("### RENDER_4, Box2 region")
band(rpx, RED, BOX2, "REND red caption   ")
band(rpx, BLUE, BOX2, "REND blue caption  ")
print()

print("### RENDER_4 Box1 dark-ink column profile (n>=15):")
x0, y0, x1, y1 = BOX1
for x in range(x0, x1):
    c = sum(1 for y in range(y0, y1) if DARK(rpx[x, y]))
    if c >= 15:
        print(f"  x={x}: n={c}")
print()
print("### RENDER_4 Box2 dark-ink column profile (n>=15):")
x0, y0, x1, y1 = BOX2
for x in range(x0, x1):
    c = sum(1 for y in range(y0, y1) if DARK(rpx[x, y]))
    if c >= 15:
        print(f"  x={x}: n={c}")
