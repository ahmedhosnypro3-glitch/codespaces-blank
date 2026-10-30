#!/usr/bin/env python3
"""Precise per-row band census: for each frame row, report the color classes and
their x-extents in the original AND the render. Answers: how many bands, where
does each start/end vertically, and is each band full-width or half-width.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0

# distinct measured fills (original space), from the runs observed
CLASSES = {
    "yellow": None,
    "peach": None,
    "pink": None,
    "blue": None,
    "gray": None,
    "white": None,
}

# Build class prototypes by sampling known-empty spots
proto_yellow = (250, 253, 219)
proto_peach = (248, 223, 193)
proto_pink = (255, 225, 229)
proto_blue = (236, 254, 252)
proto_gray = (233, 233, 232)
proto_white = (255, 255, 255)


def classify(c):
    out = []
    for name, p in (("yellow", proto_yellow), ("peach", proto_peach),
                    ("pink", proto_pink), ("blue", proto_blue),
                    ("gray", proto_gray), ("white", proto_white)):
        d = abs(int(c[0])-p[0]) + abs(int(c[1])-p[1]) + abs(int(c[2])-p[2])
        if d <= 40:
            out.append((d, name))
    if not out:
        return None
    return min(out)[1]


def row_runs(im, y, scale, label):
    row = im[int((y + 0.5) * scale)]
    prev = None
    runs = []
    for i, c in enumerate(row):
        k = classify(c)
        if k != prev:
            runs.append([i, i, k])
            prev = k
        else:
            runs[-1][1] = i
    # merge runs shorter than 4 render-px
    merged = []
    for a, b, k in runs:
        if merged and (b - a) < 4 * scale:
            merged[-1][1] = b
            # blend: if the merged run had a class, keep it; else take k
            if merged[-1][2] is None and k is not None:
                merged[-1][2] = k
        else:
            merged.append([a, b, k])
    big = [(a, b, k) for a, b, k in merged if (b - a) >= 6 * scale]
    s = []
    for a, b, k in big:
        s.append(f"{k or '?'}[{a/scale:.0f}-{b/scale:.0f}]")
    print(f"{label:>9} y={y:3d}: " + "  ".join(s))


print("ROW-BY-ROW band classes (frame px). '?' = ink/other (text, strokes, tables)")
print("=" * 100)
print("ORIGINAL:")
for y in range(240, 535, 5):
    row_runs(o, y, 1.0, "ORIG")
print()
print("RENDER:")
for y in range(240, 535, 5):
    row_runs(r, y, SC, "REND")
