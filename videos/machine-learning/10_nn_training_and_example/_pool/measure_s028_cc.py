#!/usr/bin/env python3
"""Connected-component analysis of slide_028 diagram + column regions."""
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_028.jpg").convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]

# background is light gray ~ (230,230,230). anything clearly different = ink
bgdist = np.abs(a - a[5, 5]).sum(axis=2)
ink = bgdist > 45
# suppress the outer frame (x<42 or x>920 or y<43 or y>536)
frame = np.zeros_like(ink)
frame[44:536, 42:919] = True
ink = ink & frame

lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
print(f"components={n}")
objs = ndimage.find_objects(lab)
items = []
for i, sl in enumerate(objs, start=1):
    ys, xs = sl
    h = ys.stop - ys.start
    w = xs.stop - xs.start
    area = int((lab[sl] == i).sum())
    if area < 6 or h < 5 or w < 5:
        continue
    fill = area / float(h * w)
    reg = a[sl]
    mr, mg, mb = reg.reshape(-1, 3).mean(axis=0)
    kind = "?"
    if mr > 180 and mg < 140 and mb < 110:
        kind = "ORANGE"
    elif mb > 110 and mb - mr > 45:
        kind = "BLUE"
    elif mr > 140 and mr - mg > 55 and mr - mb > 55:
        kind = "RED"
    elif mr < 140 and mg < 140 and mb < 140:
        kind = "DARK"
    else:
        kind = "GRAY"
    items.append((ys.start, ys.stop, xs.start, xs.stop, area, fill, kind, (mr, mg, mb)))

print("\n=== LARGE / CIRCLE-LIKE (area>=60, fill>=0.35) ===")
for (y0, y1, x0, x1, area, fill, kind, rgb) in sorted(items, key=lambda t: (t[0], t[2])):
    if area >= 60 and fill >= 0.30 and 8 <= (y1 - y0) <= 60 and 8 <= (x1 - x0) <= 60:
        print(f"  y[{y0}-{y1-1}] x[{x0}-{x1-1}] {y1-y0}x{x1-x0} area={area} fill={fill:.2f} {kind} rgb={tuple(int(v) for v in rgb)}")

print("\n=== ALL components with area>=40, sorted by y ===")
for (y0, y1, x0, x1, area, fill, kind, rgb) in sorted(items, key=lambda t: (t[0], t[2])):
    if area >= 40:
        print(f"  y[{y0}-{y1-1}] x[{x0}-{x1-1}] {y1-y0}x{x1-x0} area={area} fill={fill:.2f} {kind} rgb={tuple(int(v) for v in rgb)}")
