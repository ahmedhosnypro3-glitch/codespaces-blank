#!/usr/bin/env python3
"""Second-pass forensics: background, table glyph/-fill profiles, bottom-left diagram."""
import numpy as np
from PIL import Image

IMG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/unique_slides/slide_011.jpg")
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = a.shape


def hexs(px):
    return "#%02X%02X%02X" % tuple(px)


print("=== background samples ===")
for (x, y) in [(30, 30), (60, 60), (500, 100), (500, 300), (900, 200), (450, 480),
                (60, 500), (200, 100), (350, 60), (700, 100), (840, 400)]:
    print(f"  ({x},{y}) = {tuple(a[y,x])} {hexs(a[y,x])}")

print()
print("=== O/P column vertical profile at x=266 and x=282 (cyan/green fills) ===")
for x in (262, 266, 274, 282, 288):
    ys = []
    for y in range(140, 306):
        r, g, b = a[y, x]
        if (g - r > 20 and b - r > 20) or (g - r > 35 and g - b > 20):
            ys.append(y)
    # group
    groups = []
    for y in ys:
        if groups and y == groups[-1][1] + 1:
            groups[-1][1] = y
        else:
            groups.append([y, y])
    print(f"  x={x}: {groups}")

print()
print("=== table glyph (dark) x-runs per row band ===")
for label, y0, y1 in [("hdr", 142, 172), ("r1", 174, 206), ("r2", 206, 240),
                      ("r3", 240, 274), ("r4", 274, 304)]:
    band = a[y0:y1, 98:312]
    mx = band.max(axis=2); mn = band.min(axis=2)
    dark = (mx < 140) & ((mx - mn) < 40)
    cols = np.nonzero(dark.any(axis=0))[0] + 98
    groups = []
    for x in cols:
        if groups and x == groups[-1][1] + 1:
            groups[-1][1] = x
        else:
            groups.append([x, x])
    print(f"  {label}: dark col groups {groups}")

print()
print("=== title band dark/red extent ===")
band = a[60:100, 0:960]
R, G, B = band[:, :, 0], band[:, :, 1], band[:, :, 2]
red = (R > 110) & (R - G > 45) & (R - B > 45)
ys, xs = np.nonzero(red)
print(f"  title red bbox: x {xs.min()}..{xs.max()} y {60+ys.min()}..{60+ys.max()}")

print()
print("=== bottom-left diagram: red pixel map (x140-500,y395-485) ===")
def classify(px):
    r, g, b = px
    mxv, mnv = max(px), min(px)
    s = mxv - mnv
    if r > 110 and r - g > 45 and r - b > 45: return "R"
    if b - r > 45 and b > 100: return "B"
    if g - r > 25 and b - r > 25: return "C"
    if g - r > 40 and g - b > 25: return "G"
    if r > 180 and b > 180 and g < r - 20: return "P"   # pink/magenta
    if s < 18:
        if mxv < 90: return "#"
        if mxv < 190: return "+"
        return "."
    return "?"
for y in range(396, 486, 2):
    row = []
    for x in range(140, 500):
        counts = {}
        for dy in range(2):
            c = classify(a[y + dy, x])
            counts[c] = counts.get(c, 0) + 1
        row.append(max(counts, key=counts.get))
    print(f"{y:4d} " + "".join(row))

print()
print("=== diagram magenta/pink bbox ===")
reg = a[395:485, 140:500]
R, G, B = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
pink = (R > 190) & (B > 190) & (G < R - 15)
ys, xs = np.nonzero(pink)
if len(xs):
    print(f"  pink bbox: x {140+xs.min()}..{140+xs.max()} y {395+ys.min()}..{395+ys.max()} n={len(xs)}")
blue = (B - R > 45) & (B > 100)
ys, xs = np.nonzero(blue)
print(f"  blue bbox: x {140+xs.min()}..{140+xs.max()} y {395+ys.min()}..{395+ys.max()}")
