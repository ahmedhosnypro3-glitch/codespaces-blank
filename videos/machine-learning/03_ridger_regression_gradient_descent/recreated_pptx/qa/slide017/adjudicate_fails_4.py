#!/usr/bin/env python3
"""Adjudication part 4: ASCII map of the title tail + direct border colour samples."""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
ri = np.asarray(Image.open(os.path.join(HERE, "render_2.png")).convert("RGB")).astype(int)
oi = np.asarray(Image.open(os.path.join(ROOT, "unique_slides", "slide_017.jpg")).convert("RGB")).astype(int)
S = ri.shape[0] / 540.0

def cls(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    if r + g + b > 735: return "."          # white
    if abs(r - 233) < 22 and abs(g - 233) < 22 and abs(b - 231) < 24: return ","  # panel gray
    if r > 90 and (r - g) > 40 and (r - b) > 10: return "R"
    if b > 90 and (b - r) > 40 and (g - r) < 30: return "B"
    if g > 200 and b < 245 and (g - r) > 15: return "M"   # mint
    if r > 225 and g > 225 and b < 200: return "Y"        # yellow
    if r + g + b < 330: return "#"        # dark
    return "o"                             # other

print("== ASCII map: title tail x735..905, y56..100 (1 char = 2 frame px) ==")
for nm, img, ren in (("ORIG", oi, False), ("REND", ri, True)):
    print(f"-- {nm} --")
    for y in range(56, 101, 2):
        row = []
        for x in range(735, 906, 2):
            if ren:
                px = img[int(y * S), int(x * S)]
            else:
                px = img[y, x]
            row.append(cls(px))
        print(f"  y{y:3d} " + "".join(row))

print("\n== direct border-line colour samples (median of non-white/panel px on the line) ==")
def sample(img, y, x0, x1, ren):
    if ren:
        seg = img[int(y * S) - 1:int(y * S) + 3, int(x0 * S):int(x1 * S)]
    else:
        seg = img[max(0, y - 1):y + 3, x0:x1]
    px = seg.reshape(-1, 3)
    keep = px[~((px.sum(axis=1) > 735) |
                ((np.abs(px[:, 0] - 233) < 22) & (np.abs(px[:, 1] - 233) < 22) & (np.abs(px[:, 2] - 231) < 24)))]
    if not len(keep): return None, 0
    return np.median(keep, axis=0).astype(int).tolist(), len(keep)
print(" TEST table B1: top(y128) / h-line(y160) / h-line(y190) / h-line(y221) / bottom(y251)")
for y in (128, 160, 190, 221, 251):
    for nm, img, ren in (("orig", oi, False), ("rend", ri, True)):
        med, n = sample(img, y, 680, 860, ren)
        print(f"   y{y} {nm}: median {med} n={n}")
print(" TRAIN table B1: top(y126) / h(y157) / bottom(y249)")
for y in (126, 157, 249):
    for nm, img, ren in (("orig", oi, False), ("rend", ri, True)):
        med, n = sample(img, y, 100, 455, ren)
        print(f"   y{y} {nm}: median {med} n={n}")
