#!/usr/bin/env python3
"""Final measurement: original plot interiors (axis lines), label ink boxes,
axis-title positions, tan asymptotes, sigmoid legend + note.

Panel border boxes measured earlier (blue-purple ink):
  TL 104..410 x 59..237 | TR 499..790 x 59..237
  BL 105..410 x 297..476 | BR 499..790 x 297..476
"""
import os
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
V = os.path.join(ROOT, "videos/machine-learning/09_introduction_to_neural_networks")
im = Image.open(os.path.join(V, "unique_slides/slide_019.jpg")).convert("RGB")
W, H = im.size
px = im.load()
print(f"image {W}x{H}")


def is_gray_axis(c):
    r, g, b = c
    return abs(r - 140) < 34 and abs(g - 140) < 34 and abs(b - 140) < 34


def is_gray_axis2(c):  # #404040-ish dark gray
    r, g, b = c
    return abs(r - 64) < 30 and abs(g - 64) < 30 and abs(b - 64) < 30


def is_text(c):
    r, g, b = c
    if r < 130 and g < 130 and b < 130:
        # exclude blue-purple panel border ink
        if b - r > 40 and b - g > 40:
            return False
        return True
    return False


def longest_h(x0, y0, x1, y1, pred):
    best = (0, None, None)  # (run, y, xstart)
    for y in range(y0, y1 + 1):
        run = 0; start = None
        for x in range(x0, x1 + 1):
            if pred(px[x, y]):
                if run == 0:
                    start = x
                run += 1
                if run > best[0]:
                    best = (run, y, start)
            else:
                run = 0
    return best


def longest_v(x0, y0, x1, y1, pred):
    best = (0, None, None)
    for x in range(x0, x1 + 1):
        run = 0; start = None
        for y in range(y0, y1 + 1):
            if pred(px[x, y]):
                if run == 0:
                    start = y
                run += 1
                if run > best[0]:
                    best = (run, x, start)
            else:
                run = 0
    return best


PANELS = {
    "sigmoid": (104, 59, 410, 237),
    "tanh":    (499, 59, 790, 237),
    "tan":     (105, 297, 410, 476),
    "arctan":  (499, 297, 790, 476),
}

for key, (bx0, by0, bx1, by1) in PANELS.items():
    ix0, iy0, ix1, iy1 = bx0 + 4, by0 + 4, bx1 - 4, by1 - 4
    print(f"\n=== {key} panel ({bx0},{by0})-({bx1},{by1}) ===")
    for pname, pred in (("gray140", is_gray_axis), ("darkgray64", is_gray_axis2)):
        h = longest_h(ix0, iy0, ix1, iy1, pred)
        v = longest_v(ix0, iy0, ix1, iy1, pred)
        print(f"  {pname}: longest H run={h[0]} at y={h[1]} x_start={h[2]} | "
              f"longest V run={v[0]} at x={v[1]} y_start={v[2]}")
    # text ink bbox (ticks, axis titles, legend, in-panel title)
    pts = [(x, y) for y in range(iy0, iy1 + 1) for x in range(ix0, ix1 + 1)
           if is_text(px[x, y])]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f"  text ink bbox: x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)}  n={len(pts)}")
        # row bands of text ink
        rows = {}
        for x, y in pts:
            rows.setdefault(y, []).append(x)
        band = []
        for y in sorted(rows):
            if band and y - band[-1] <= 2:
                band.append(y)
            else:
                if band:
                    xs2 = [x for t in band for x in rows[t]]
                    print(f"    text band y {band[0]}..{band[-1]}: x {min(xs2)}..{max(xs2)} n={len(xs2)}")
                band = [y]
        if band:
            xs2 = [x for t in band for x in rows[t]]
            print(f"    text band y {band[0]}..{band[-1]}: x {min(xs2)}..{max(xs2)} n={len(xs2)}")
    else:
        print("  text ink: none")

# tan asymptotes: columns in BL panel with rose/pink/red ink
print("\n=== TAN panel rose/red column profile (x 105..410, y 300..470) ===")
for x in range(105, 411):
    n = 0
    for y in range(300, 471):
        r, g, b = px[x, y]
        if r - g > 28 and r - b > 20 and r > 120:
            n += 1
    if n > 15:
        ys = [y for y in range(300, 471)
              if (lambda c: c[0] - c[1] > 28 and c[0] - c[2] > 20 and c[0] > 120)(px[x, y])]
        print(f"  x={x}: n={n} y {min(ys)}..{max(ys)}")

# BR in-panel title precise
print("\n=== BR title region: ink darker than 150 (excl blue-purple grid/rose) ===")
pts = []
for y in range(297, 340):
    for x in range(499, 700):
        r, g, b = px[x, y]
        if r < 150 and g < 150 and b < 150 and not (b - r > 40 and b - g > 40):
            pts.append((x, y))
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  bbox x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)} n={len(pts)}")
    rows = {}
    for x, y in pts:
        rows.setdefault(y, []).append(x)
    for y in sorted(rows):
        print(f"   y={y}: x {min(rows[y])}..{max(rows[y])} n={len(rows[y])}")
else:
    print("  none")
