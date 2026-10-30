#!/usr/bin/env python3
"""Pass 9b — fix: true border cores (max-saturation single px) + per-line colour runs."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330


def core_blue(x0, x1, y0, y1):
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    sc = sub[:, 2] - np.maximum(sub[:, 0], sub[:, 1])
    k = sc > 20
    if not k.any():
        return None
    return tuple(int(sub[k][np.argmax(sc[k])][i]) for i in range(3))


def core_red(x0, x1, y0, y1):
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    sc = sub[:, 0] - np.maximum(sub[:, 1], sub[:, 2])
    k = sc > 20
    if not k.any():
        return None
    return tuple(int(sub[k][np.argmax(sc[k])][i]) for i in range(3))


print("=== true single-pixel border cores (max saturation) ===")
for name, (x0, x1, y0, y1) in {
    "BOX1 top":   (100, 390, 98, 102),
    "BOX2 top":   (440, 740, 98, 102),
    "Remember top": (790, 876, 101, 106),
    "Remember left(side)": (783, 788, 110, 148),
    "Objective top":  (82, 300, 242, 246),
    "Error top":      (82, 484, 306, 310),
    "PredWhere top":  (500, 880, 231, 235),
    "Define top":     (82, 650, 387, 392),
    "Formula top":    (82, 484, 461, 466),
}.items():
    rb, bb = core_red(x0, x1, y0, y1), core_blue(x0, x1, y0, y1)
    print(f"  {name:20s}: red_core={rb}  blue_core={bb}")


def colorruns(x0, x1, y0, y1, gap_merge=4):
    cr = red[y0:y1, x0:x1].sum(axis=0)
    cb = blue[y0:y1, x0:x1].sum(axis=0)
    ck = dark[y0:y1, x0:x1].sum(axis=0)
    segs, cur = [], None
    for i in range(x1 - x0):
        tot = cr[i] + cb[i] + ck[i]
        if tot == 0:
            if cur: segs.append(cur); cur = None
            continue
        lab = "R" if cr[i] >= cb[i] and cr[i] >= ck[i] else ("B" if cb[i] >= ck[i] else "K")
        if cur and cur[2] == lab and i - cur[1] - 1 <= gap_merge:
            cur = (cur[0], i, lab)
        else:
            if cur: segs.append(cur)
            cur = (i, i, lab)
    if cur: segs.append(cur)
    return [f"x{x0+a}-{x0+cc}:{lab}" for a, cc, lab in segs if cc - a >= 1]


print("\n=== PredWhere per-line colour runs ===")
for nm, (y0, y1) in {"L1": (248, 277), "L2": (281, 305), "L3": (309, 341), "L4": (343, 363)}.items():
    print(f"  {nm} y{y0}..{y1}:")
    print("    ", colorruns(498, 880, y0, y1))

print("\n=== Error line (y318..346) ===")
print("  ", colorruns(82, 486, 318, 346))
print("\n=== Define line (y404..430) ===")
print("  ", colorruns(82, 650, 404, 430))
print("\n=== Objective (y258..288) ===")
print("  ", colorruns(82, 302, 258, 288))
print("\n=== BOX2 PredLabels(blue) ===")
print("  ", colorruns(566, 742, 134, 152))
print("\n=== BOX2 FromModel(dark) ===")
print("  ", colorruns(566, 742, 156, 188))
print("\n=== Remember norm (y122..148) ===")
print("  ", colorruns(788, 874, 122, 148))
