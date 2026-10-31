#!/usr/bin/env python3
"""Slide 34 network box: find all node fills with loose color masks."""
import numpy as np
from PIL import Image
from scipy import ndimage

base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
a = np.asarray(Image.open(f"{base}/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
PX = 13.33 / 960.0
box = (53, 200, 360, 870)  # y0,y1,x0,x1

def dump(mask, name, minpx=25):
    m = np.zeros_like(mask)
    m[box[0]:box[1], box[2]:box[3]] = mask[box[0]:box[1], box[2]:box[3]]
    lab, cnt = ndimage.label(m)
    out = []
    for i in range(1, cnt + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < minpx:
            continue
        cx, cy = (xs.min()+xs.max())/2, (ys.min()+ys.max())/2
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(ys)))
    print(f"-- {name}: {len(out)}")
    for c in sorted(out, key=lambda t: t[0]):
        cx, cy = (c[0]+c[2])/2, (c[1]+c[3])/2
        print(f"   x={c[0]}-{c[2]} y={c[1]}-{c[3]} (w={c[2]-c[0]+1} h={c[3]-c[1]+1}) "
              f"c_px=({cx:.0f},{cy:.0f}) c_in=({cx*PX:.2f},{cy*PX:.2f}) n={c[4]}")

notwhite = (r < 235) | (g < 235) | (b < 235)
dump(notwhite, "NON-WHITE blobs", 40)
dump((r > 200) & (g > 150) & (b < 215) & ((r - b) > 30), "yellowish", 25)
dump((r > 180) & (g < 190) & ((r - b) > 70), "orange-ish", 20)

# sample colors at candidate node centers
print("\n-- pixel samples --")
for (x, y) in [(542, 78), (544, 118), (542, 158), (650, 90), (650, 130), (400, 115),
               (772, 120), (600, 100), (620, 170), (520, 170)]:
    print(f"   ({x},{y}) = {tuple(a[y, x])}")
