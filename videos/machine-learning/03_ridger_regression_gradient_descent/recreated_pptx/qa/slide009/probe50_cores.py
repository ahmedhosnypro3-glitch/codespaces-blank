#!/usr/bin/env python3
"""Probe 50: core colour (max saturation pixel) of every genuine red mark."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

MARKS = [
    ("LEFT small disc", 184, 190, 151, 160),
    ("LEFT composite", 199, 245, 198, 255),
    ("LEFT big disc core", 226, 244, 234, 250),
    ("LEFT dim mark", 243, 250, 285, 294),
    ("RIGHT small disc", 600, 606, 140, 154),
    ("RIGHT composite", 624, 651, 210, 266),
    ("RIGHT mark", 676, 683, 316, 325),
    ("LEFT y-axis shaft core", 124, 129, 200, 240),
    ("LEFT x-axis core", 200, 240, 432, 437),
    ("LEFT caption 'Overfit' core", 109, 160, 488, 504),
]
for nm, x0, x1, y0, y1 in MARKS:
    sub = a[y0:y1 + 1, x0:x1 + 1]
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    sat = rr - np.maximum(gg, bb)
    m = sat > 40
    if not m.any():
        print(f"{nm:28s}: no red px")
        continue
    px = sub[m]
    order = np.argsort(-(px[:, 0] - np.maximum(px[:, 1], px[:, 2])))
    top = px[order[:6]]
    print(f"{nm:28s}: most-saturated px = "
          + ", ".join(f"({int(t[0])},{int(t[1])},{int(t[2])})" for t in top)
          + f"   n={int(m.sum())}")

print("\n=== LEFT big disc: is it a UNIFORM fill? 3x3 block means ===")
for y in range(232, 254, 3):
    row = []
    for x in range(223, 248, 5):
        blk = a[y:y + 3, x:x + 5].reshape(-1, 3)
        row.append(f"{blk[:,0].mean():3.0f}/{blk[:,1].mean():3.0f}/{blk[:,2].mean():3.0f}")
    print(f"  y{y:3d} " + "  ".join(row))

print("\n=== background panel colour for reference ===")
print("  panel gray sample:", a[60, 300].tolist(), a[530, 300].tolist())
print("  chart interior:", a[200, 380].tolist(), a[420, 380].tolist())
print("  orange core:", a[333, 261].tolist(), a[333, 295].tolist())
