#!/usr/bin/env python3
"""Locate the box borders and matrix bars in the top band (y100..225) of both
the original slide 004 and render_4, using not-white pixel profiles.
"""
from PIL import Image

ORIG = "unique_slides/slide_004.jpg"
RENDER = "recreated_pptx/qa/slide004/render_4.png"
o = Image.open(ORIG).convert("RGB")
r = Image.open(RENDER).convert("RGB").resize((960, 540), Image.LANCZOS)
opx, rpx = o.load(), r.load()

NW = lambda p: not (p[0] > 235 and p[1] > 235 and p[2] > 235)


def col_profile(px, x0, x1, y0, y1, min_n=1):
    out = []
    for x in range(x0, x1):
        c = sum(1 for y in range(y0, y1) if NW(px[x, y]))
        if c >= min_n:
            out.append((x, c))
    return out


def tall_strokes(px, x0, x1, y0, y1, min_n):
    """x columns whose not-white run in [y0,y1) is >= min_n - i.e. tall bars."""
    res = []
    for x in range(x0, x1):
        c = sum(1 for y in range(y0, y1) if NW(px[x, y]))
        if c >= min_n:
            res.append((x, c))
    return res


def group(vals, gap=2):
    g, last = [], None
    for x, c in vals:
        if last is None or x - last > gap:
            g.append([])
        g[-1].append((x, c))
        last = x
    return g


Y0, Y1 = 95, 230
print("=" * 70)
print("ORIGINAL top band, not-white column profile (n>=60 of 135 rows)")
print("=" * 70)
for g in group(tall_strokes(opx, 70, 900, Y0, Y1, 60)):
    xs = [t[0] for t in g]
    print(f"  x{min(xs)}..{max(xs)}  heights {[t[1] for t in g]}")

print()
print("ORIGINAL not-white row profile (n>=180 of 960) in y95..230")
rows = [(y, sum(1 for x in range(960) if NW(opx[x, y]))) for y in range(Y0, Y1)]
for y, c in rows:
    if c >= 180:
        print(f"  y={y}: n={c}")

print()
print("=" * 70)
print("RENDER_4 top band, not-white column profile (n>=60 of 135 rows)")
print("=" * 70)
for g in group(tall_strokes(rpx, 70, 900, Y0, Y1, 60)):
    xs = [t[0] for t in g]
    print(f"  x{min(xs)}..{max(xs)}  heights {[t[1] for t in g]}")

print()
print("RENDER_4 not-white row profile (n>=180 of 960) in y95..230")
rows = [(y, sum(1 for x in range(960) if NW(rpx[x, y]))) for y in range(Y0, Y1)]
for y, c in rows:
    if c >= 180:
        print(f"  y={y}: n={c}")

print()
print("=" * 70)
print("ORIGINAL Box1 interior x82..392: tall not-white columns (n>=40)")
print("=" * 70)
for x, c in tall_strokes(opx, 82, 392, 103, 220, 40):
    print(f"  x={x}: n={c}")

print()
print("ORIGINAL Box2 interior x582..871: tall not-white columns (n>=40)")
for x, c in tall_strokes(opx, 582, 871, 103, 220, 40):
    print(f"  x={x}: n={c}")

print()
print("ORIGINAL Box1: not-white columns x140..250 (n>=5)  [matrix bar hunt]")
for x, c in tall_strokes(opx, 140, 250, 103, 220, 5):
    print(f"  x={x}: n={c}")
