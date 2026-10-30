#!/usr/bin/env python3
"""Numeric colour probes for slide_011 table + NN diagram."""
import numpy as np
from PIL import Image

IMG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/unique_slides/slide_011.jpg")
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = a.shape


def hexs(px):
    return "#%02X%02X%02X" % tuple(px)


print("=== TABLE O/P column samples (x 245..305, rows) ===")
for label, y in [("hdr", 160), ("r1", 195), ("r2", 230), ("r3", 262), ("r4", 292)]:
    print(f" {label} y={y}:")
    for x in range(242, 312, 8):
        print(f"   x={x}: {tuple(a[y,x])} {hexs(a[y,x])}")

print()
print("=== saturated-pixel clusters in table region x96-315,y138-307 ===")
reg = a[138:307, 96:315]
mx = reg.max(axis=2); mn = reg.min(axis=2)
sat = mx - mn
ys, xs = np.nonzero(sat > 25)
from collections import Counter
cnt = Counter()
for y, x in zip(ys, xs):
    cnt[hexs(reg[y, x])] += 1
for c, n in cnt.most_common(12):
    print(f"   {c}: {n}")

print()
print("=== NN diagram region x140-500 y395-490: saturated clusters ===")
reg2 = a[395:490, 140:500]
mx = reg2.max(axis=2); mn = reg2.min(axis=2)
sat2 = mx - mn
ys, xs = np.nonzero(sat2 > 25)
cnt2 = Counter()
for y, x in zip(ys, xs):
    cnt2[hexs(reg2[y, x])] += 1
for c, n in cnt2.most_common(15):
    print(f"   {c}: {n}")

print()
print("=== NN diagram: bbox per colour class ===")
R, G, B = reg2[:, :, 0], reg2[:, :, 1], reg2[:, :, 2]
def bbox(mask, name):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        print(f"  {name}: none"); return
    print(f"  {name}: x {140+xs.min()}..{140+xs.max()} y {395+ys.min()}..{395+ys.max()} n={len(xs)}")

bbox((R > 110) & (R - G > 45) & (R - B > 45), "red")
bbox((B - R > 45) & (B > 100), "blue")
bbox((G - R > 25) & (B - R > 25), "cyan")
bbox((G - R > 40) & (G - B > 25), "green")
bbox((mx < 110) & (sat2 < 25), "dark")

print()
print("=== NN diagram fine map x150-500 y400-490 (sx=2,sy=3) ===")
def classify(px):
    r, g, b = px
    mxv, mnv = max(px), min(px)
    s = mxv - mnv
    if r > 110 and r - g > 45 and r - b > 45: return "R"
    if b - r > 45 and b > 100: return "B"
    if g - r > 25 and b - r > 25: return "C"
    if g - r > 40 and g - b > 25: return "G"
    if s < 18:
        if mxv < 90: return "#"
        if mxv < 190: return "+"
        return "."
    return "?"
for y in range(400, 492, 3):
    row = []
    for x in range(150, 500, 2):
        counts = {}
        for dy in range(3):
            for dx in range(2):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W:
                    c = classify(a[yy, xx]); counts[c] = counts.get(c, 0) + 1
        row.append(max(counts, key=counts.get) if counts else " ")
    print(f"{y:4d} " + "".join(row))
