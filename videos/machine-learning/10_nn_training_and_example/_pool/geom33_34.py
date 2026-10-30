#!/usr/bin/env python3
"""Precise geometry: gray fills, red rules, colored node blobs, for slide 33/34."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

n = sys.argv[1]
base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
a = np.asarray(Image.open(f"{base}/unique_slides/slide_0{n}.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def report(mask, name, min_px=60, dilate=1):
    if dilate:
        mask = ndimage.binary_dilation(mask, iterations=dilate)
    lab, cnt = ndimage.label(mask)
    out = []
    for i in range(1, cnt + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(ys)))
    print(f"-- {name}: {len(out)} components")
    for c in sorted(out, key=lambda t: (t[1] // 40, t[0])):
        print(f"   x={c[0]}-{c[2]}(w{c[2]-c[0]+1}) y={c[1]}-{c[3]}(h{c[3]-c[1]+1}) px={c[4]}")

gray = (abs(r - 231) < 12) & (abs(g - 233) < 12) & (abs(b - 230) < 12)
report(gray, "LIGHT-GRAY FILL", 400)
red = (r > 110) & (r < 235) & (g < 145) & (b < 160) & ((r - g) > 35) & ((r - b) > 20)
report(red, "RED", 60, 0)
for nm, m in [
    ("YELLOW", (r > 200) & (g > 170) & (b < 180) & ((r - b) > 45)),
    ("BLUE", (b > 120) & ((b - r) > 35) & ((b - g) > 15)),
    ("GREEN", (g > 110) & ((g - r) > 20) & ((g - b) > 20)),
    ("ORANGE", (r > 200) & (g > 110) & (g < 190) & (b < 130) & ((r - b) > 60)),
]:
    report(m, nm, 80)
dark = (r < 120) & (g < 120) & (b < 120)
report(dark, "DARK TEXT", 40, 0)
