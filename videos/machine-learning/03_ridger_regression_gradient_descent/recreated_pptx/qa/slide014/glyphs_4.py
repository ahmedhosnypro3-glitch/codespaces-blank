#!/usr/bin/env python3
"""Segment a text region into glyph columns and print each glyph separately (brightness art)."""
from PIL import Image
import numpy as np
import sys

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
im = Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)

x0, x1, y0, y1 = (int(v) for v in sys.argv[1:5])
hue = sys.argv[5] if len(sys.argv) > 5 else "any"

def sel(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    s = r + g + b
    if s < 330:
        if r > g + 40 and r > b + 40: return "R"
        if b > r + 40: return "B"
        if g > r + 25 and g > b + 25: return "G"
        return "K"
    if r > g + 45 and r > b + 45 and s < 620: return "r"
    if b > r + 35 and b > g + 20 and s < 720: return "b"
    if g > r + 20 and g > b + 20 and s < 720: return "g"
    return "."

ALLOWED = {"any": None, "R": {"R", "r"}, "G": {"G", "g"}, "B": {"B", "b"},
           "K": {"K"}, "red": {"R", "r"}, "green": {"G", "g"}, "blue": {"B", "b"}}
allow = ALLOWED[hue]

def ink(x, y):
    c = sel(a[y, x])
    if allow is None:
        return c != "."
    return c in allow

cols = []
for x in range(x0, x1):
    n = sum(1 for y in range(y0, y1) if ink(x, y))
    cols.append(n)

groups = []
cur = None
for i, n in enumerate(cols):
    x = x0 + i
    if n:
        if cur is None:
            cur = [x, x]
        else:
            cur[1] = x
    else:
        if cur is not None and x - cur[1] > 2:
            groups.append(tuple(cur)); cur = None
if cur is not None:
    groups.append(tuple(cur))

for gi, (gs, ge) in enumerate(groups):
    ys = [y for y in range(y0, y1) if any(ink(x, y) for x in range(gs, ge + 1))]
    print(f"\n--- glyph {gi}: x{gs}..{ge} y{min(ys)}..{max(ys)} w={ge-gs+1}")
    for y in range(min(ys), max(ys) + 1):
        row = ""
        for x in range(gs, ge + 1):
            row += "#" if ink(x, y) else "."
        print("   " + row)
