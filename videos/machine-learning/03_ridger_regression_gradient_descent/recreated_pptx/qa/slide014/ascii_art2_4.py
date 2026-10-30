#!/usr/bin/env python3
"""Read the remaining frame text regions as ASCII art (ridge, objective, midband1) + vector box border scan."""
from PIL import Image
import numpy as np
from collections import Counter

def classify(px):
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

im = Image.open("unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def art(x0, x1, y0, y1, label, step):
    print(f"\n=== {label} x{x0}..{x1} y{y0}..{y1} step{step} ===")
    for y in range(y0, y1 + 1):
        print(f"{y:4d} " + "".join(classify(a[y, x]) for x in range(x0, x1 + 1, step)))

art(100, 640, 254, 280, "RIDGE band text (left part)", 3)
art(100, 400, 362, 384, "MIDBAND1 text (left part)", 2)
art(300, 480, 362, 384, "MIDBAND1 text (blue word region)", 2)

print("\n=== RAW RGB samples ===")
for (x0, x1, y0, y1, tag) in [(218, 264, 258, 271, "ridge RED span x218..264"),
                              (356, 383, 258, 271, "ridge BLUE span x356..383"),
                              (667, 700, 258, 271, "ridge GREEN span x667..700"),
                              (535, 548, 315, 330, "objective GREEN span x535..548"),
                              (282, 300, 315, 330, "objective BLUE x282..300"),
                              (352, 390, 315, 330, "objective RED x352..390"),
                              (163, 204, 366, 380, "mb1 RED x163..204"),
                              (328, 466, 366, 380, "mb1 BLUE x328..466")]:
    sub = a[y0:y1+1, x0:x1+1].reshape(-1, 3)
    cc = Counter(map(tuple, sub))
    print(f"{tag}: top colors {cc.most_common(4)}")

print("\n=== VECTOR BOX borders (maroon scan) ===")
for y in range(98, 242):
    row = a[y]
    m = [x for x in range(55, 905) if classify(row[x]) in ("R", "r") and row[x][0] > 90]
    if len(m) > 100:
        print(f"y={y}: red-ish x{min(m)}..{max(m)} n={len(m)}")
# vertical maroon columns
cols = {}
for y in range(98, 240):
    row = a[y]
    for x in range(55, 905):
        r, g, b = row[x]
        if r > 90 and r < 200 and g < 80 and b < 90:
            cols[x] = cols.get(x, 0) + 1
print("maroon-ish vertical columns:", {x: c for x, c in sorted(cols.items()) if c > 60})
print("\n=== box row fills ===")
for y in (110, 130, 150, 170, 200, 225):
    row = a[y]
    print(f"y={y}: " + " ".join(f"x{x}={tuple(int(v) for v in row[x])}" for x in (62, 75, 82, 85, 300, 430, 436, 450, 455, 460, 700, 805, 812, 850, 895)))
