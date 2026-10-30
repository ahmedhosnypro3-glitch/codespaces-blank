#!/usr/bin/env python3
"""Measure slide_025 bottom charts + node colors."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]

dark = a.mean(axis=2) < 120
red = (r > 140) & (r - g > 45) & (r - b > 45)
blue = (b > 140) & (b - r > 45) & (b - g > 35)
green = (g > 110) & (g - r > 35) & (g - b > 35)


def runs(mask, minlen=2):
    idx = np.where(mask.any(axis=1))[0]
    out, s, p = [], None, None
    for i in idx:
        if s is None:
            s = p = i
        elif i - p > 1:
            if p - s + 1 >= minlen:
                out.append((int(s), int(p)))
            s = p = i
        else:
            p = i
    if s is not None and p - s + 1 >= minlen:
        out.append((int(s), int(p)))
    return out


print("=== BOTTOM LEFT chart region x40..360, y300..540 ===")
for nm, m in [("dark", dark), ("red", red), ("blue", blue)]:
    mm = np.zeros_like(m)
    mm[300:540, 40:360] = m[300:540, 40:360]
    for (s, e) in runs(mm):
        cc = np.where(mm[s:e + 1].any(axis=0))[0]
        print(f"  {nm}: rows {s}-{e} cols {cc[0]}-{cc[-1]}  in y {s/72:.2f}-{e/72:.2f} x {cc[0]/72:.2f}-{cc[-1]/72:.2f}")

print("\n=== BOTTOM RIGHT chart region x360..960, y300..540 ===")
for nm, m in [("dark", dark), ("red", red), ("blue", blue), ("green", green)]:
    mm = np.zeros_like(m)
    mm[300:540, 360:960] = m[300:540, 360:960]
    for (s, e) in runs(mm):
        cc = np.where(mm[s:e + 1].any(axis=0))[0]
        print(f"  {nm}: rows {s}-{e} cols {cc[0]}-{cc[-1]}  in y {s/72:.2f}-{e/72:.2f} x {cc[0]/72:.2f}-{cc[-1]/72:.2f}")

print("\n=== node color samples ===")
pts = [(485, 141), (519, 141), (598, 141), (638, 141), (690, 152), (713, 141),
       (754, 141), (576, 151), (622, 152), (320, 182), (322, 199), (322, 216),
       (505, 285), (625, 285), (850, 200), (780, 152), (900, 200), (900, 100)]
for (x, y) in pts:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

print("\n=== chart border pixels (left chart) ===")
for y in [345, 346, 347, 400, 515, 516, 517]:
    print(f"  y={y}: x=54 {tuple(a[y,54])} x=56 {tuple(a[y,56])} x=200 {tuple(a[y,200])} x=344 {tuple(a[y,344])}")
print("=== right chart border ===")
for y in [360, 361, 362, 450, 515, 516]:
    print(f"  y={y}: x=363 {tuple(a[y,363])} x=400 {tuple(a[y,400])} x=888 {tuple(a[y,888])}")
