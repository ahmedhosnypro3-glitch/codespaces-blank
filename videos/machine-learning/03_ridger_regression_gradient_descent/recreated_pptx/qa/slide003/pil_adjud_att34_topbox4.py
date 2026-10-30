#!/usr/bin/env python3
"""Probe 4: y-label glyph boxes + colors, orig vs render_34; also sample the
delimiter stroke colors."""
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/render_34.png"
S = 2001 / 960.0
im = Image.open(ORIG).convert("RGB")
im2 = Image.open(REND).convert("RGB")

def glyphs(img, x0, x1, y0, y1, scale=1.0, thr=170):
    """ink column ranges + per-glyph y extent + mean color of dark ink"""
    px = img.load()
    cols = []
    for x in range(x0, x1):
        ink = sum(1 for y in range(y0, y1) if sum(px[x, y]) / 3 < thr)
        cols.append(ink > 0)
    runs = []
    s = None
    for i, c in enumerate(cols):
        if c and s is None: s = i
        if not c and s is not None:
            runs.append((s, i - 1)); s = None
    if s is not None: runs.append((s, len(cols) - 1))
    out = []
    for a, b in runs:
        ys = [y for y in range(y0, y1) for x in range(x0 + a, x0 + b + 1) if sum(px[x, y]) / 3 < thr]
        rs = [px[x, y] for y in range(y0, y1) for x in range(x0 + a, x0 + b + 1) if sum(px[x, y]) / 3 < thr]
        n = len(rs)
        avg = tuple(round(sum(c[i] for c in rs) / n) for i in range(3)) if n else None
        redish = sum(1 for r, g, b in rs if r > 120 and g < 90 and b < 90)
        out.append(dict(x=(round((x0 + a) / scale, 1), round((x0 + b) / scale, 1)),
                        y=(round(min(ys) / scale), round(max(ys) / scale)), n=n,
                        avg=avg, redpx=redish))
    return out

print("ORIG y-label zones (thr 170):")
for tag, x0, x1 in [("yellow y1", 300, 345), ("cyan y2", 370, 412), ("pink yn", 505, 556)]:
    for g in glyphs(im, x0, x1, 270, 300):
        print(f"  {tag}: x={g['x']} y={g['y']} n={g['n']} avgRGB={g['avg']} redpx={g['redpx']}")

print()
print("RENDER y-label zones (scaled, thr 170):")
for tag, x0, x1 in [("yellow y1", 298, 340), ("cyan y2", 372, 416), ("pink yn", 505, 558)]:
    for g in glyphs(im2, int(x0 * S), int(x1 * S), int(268 * S), int(300 * S), S):
        print(f"  {tag}: x={g['x']} y={g['y']} n={g['n']} avgRGB={g['avg']} redpx={g['redpx']}")

print()
print("ORIG delimiter stroke colors (sample the core column at mid-height):")
px = im.load()
for name, xc, y in [("yellowL", 296.5, 210), ("yellowR", 331.5, 210), ("cyanR", 409, 210),
                    ("midcolR", 475, 210), ("pinkL", 517.5, 210), ("pinkR", 552.5, 210)]:
    xi = int(xc)
    vals = [(x, px[x, y]) for x in range(xi - 2, xi + 3)]
    best = min(vals, key=lambda t: sum(t[1]))
    print(f"  {name}: darkest at x={best[0]} rgb={best[1]}")

print()
print("ORIG 'N Training Samples' red reference color (y185, x85..250):")
rs = [px[x, y] for y in range(185, 195) for x in range(85, 250) if px[x, y][0] > 120 and px[x, y][1] < 90 and px[x, y][2] < 90]
print(f"  n={len(rs)} avgRGB={tuple(round(sum(c[i] for c in rs)/len(rs)) for i in range(3))}" if rs else "  none")
