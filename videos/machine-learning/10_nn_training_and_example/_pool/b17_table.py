#!/usr/bin/env python3
"""Row-band text inventory for slide 34's table region and top network box."""
import numpy as np
from PIL import Image
from scipy import ndimage

base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
a = np.asarray(Image.open(f"{base}/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 120) & ((r - g) > 45) & ((r - b) > 35)
green = (g > 100) & ((g - r) > 30) & ((g - b) > 30)
ink = (r < 200) & (g < 200) & (b < 200) & ~red & ~green

def bands(mask, y0, y1, x0, x1, gap=4):
    rows = mask[y0:y1, x0:x1].sum(axis=1)
    out, cur = [], None
    for i, c in enumerate(rows):
        if c > 3:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        else:
            if cur is not None and i - cur[1] > gap:
                out.append(cur); cur = None
    if cur:
        out.append(cur)
    return [(y0 + s, y0 + e) for s, e in out]

def clusters(mask, y0, y1, x0, x1, minpx=6):
    m = mask[y0:y1, x0:x1]
    lab, cnt = ndimage.label(m)
    res = []
    for i in range(1, cnt + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < minpx:
            continue
        res.append((int(xs.min() + x0), int(xs.max() + x0), len(ys)))
    return res

print("=== TABLE region: ink bands + red/green clusters per band ===")
for (y0, y1) in bands(ink, 205, 530, 50, 640):
    cl = clusters(ink, y0, y1 + 1, 50, 640)
    rc = clusters(red, y0, y1 + 1, 50, 640)
    gc = clusters(green, y0, y1 + 1, 50, 640)
    print(f" band y={y0}-{y1}")
    print(f"   ink: {[f'{a}-{b}' for a, b, _ in cl]}")
    if rc: print(f"   red: {[f'{a}-{b}' for a, b, _ in rc]}")
    if gc: print(f"   grn: {[f'{a}-{b}' for a, b, _ in gc]}")

print()
print("=== TOP-RIGHT network box (x=365..860, y=53..193): ink bands ===")
for (y0, y1) in bands(ink, 55, 192, 368, 858):
    cl = clusters(ink, y0, y1 + 1, 368, 858)
    rc = clusters(red, y0, y1 + 1, 368, 858)
    gc = clusters(green, y0, y1 + 1, 368, 858)
    bl = clusters((b > 130) & ((b - r) > 50) & ((b - g) > 30), y0, y1 + 1, 368, 858)
    print(f" band y={y0}-{y1}")
    print(f"   ink: {[f'{a}-{b}' for a, b, _ in cl]}")
    if rc: print(f"   red: {[f'{a}-{b}' for a, b, _ in rc]}")
    if gc: print(f"   grn: {[f'{a}-{b}' for a, b, _ in gc]}")
    if bl: print(f"   blu: {[f'{a}-{b}' for a, b, _ in bl]}")
