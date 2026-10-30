#!/usr/bin/env python3
"""Side-by-side green-ink ASCII comparison: original frame vs current build render.

Isolates saturated green (predicted-y colour) and prints the ink mask for the
NO REG row-group numerals so the glyph shapes can be compared directly.
1 frame px == 1 pt (960x540 frame).
"""
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_019.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide019/render_8.png"


def green_mask(path, box):
    im = Image.open(path).convert("RGB")
    x0, y0, x1, y1 = box
    crop = im.crop(box)
    px = crop.load()
    w, h = crop.size
    rows = []
    for y in range(h):
        line = []
        for x in range(w):
            r, g, b = px[x, y]
            # saturated green: G clearly dominant and reasonably bright
            if g > 90 and g - r > 45 and g - b > 45:
                line.append("#")
            else:
                line.append(".")
        rows.append("".join(line))
    return rows


def print_rows(label, rows, x0, y0):
    print(f"--- {label} (box origin x={x0} y={y0}) ---")
    for i, line in enumerate(rows):
        print(f"{y0+i:4d} {line}")
    print()


def bbox(rows):
    ys = [i for i, r in enumerate(rows) if "#" in r]
    if not ys:
        return None
    xs_min = min(r.index("#") for r in rows if "#" in r)
    xs_max = max(r.rindex("#") for r in rows if "#" in r)
    return xs_min, ys[0], xs_max, ys[-1]


for tag, box in [("NO REG row2", (300, 378, 345, 405)),
                 ("NO REG row3", (300, 487, 345, 514)),
                 ("NO REG row1", (300, 270, 345, 297))]:
    print(f"==================== {tag} ====================")
    o = green_mask(ORIG, box)
    r = green_mask(REND, box)
    print_rows("ORIGINAL", o, box[0], box[1])
    print_rows("RENDER_8", r, box[0], box[1])
    print("orig green bbox (abs):", bbox(o))
    print("rend green bbox (abs):", bbox(r))
    print()
