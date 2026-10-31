#!/usr/bin/env python3
"""Slide 014 v3 measurements: eq bands+colors, cream inset box, inset internals, legend."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
S = 13.333 / W
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def i(v):
    return round(v * S, 3)


print("=== equation region row bands (x 78..600, sum<450) ===")
sub = a[320:485, 78:600]
dark = sub.sum(axis=2) < 450
rows = dark.sum(axis=1)
bands = []
inb = False
for k, v in enumerate(rows):
    if v > 2 and not inb:
        st = k; inb = True
    elif v <= 2 and inb:
        bands.append((st + 320, k + 320)); inb = False
if inb:
    bands.append((st + 320, 485))
for y0, y1 in bands:
    seg = dark[y0 - 320:y1 - 320]
    xs = np.where(seg.any(axis=0))[0] + 78
    print(f"  y[{y0}..{y1}] h={y1-y0}px ({i(y0)}..{i(y1)}in) x[{xs.min()}..{xs.max()}]"
          f" ({i(xs.min())}..{i(xs.max())}in)")

print("\n=== per-line colored segment x-extents (red labels / green w / blue) ===")
gold = {"red": (r > 110) & (r > g + 50) & (r > b + 30),
        "green": (g > r + 25) & (g > b + 25),
        "blue": (b > 110) & (b > r + 40) & (b > g + 30)}
for (nm, y0, y1) in [("L1", 324, 350), ("L2", 376, 404), ("L3", 408, 432), ("L4", 445, 470)]:
    print(f"  {nm} y[{y0}..{y1}]:")
    for cn, m in gold.items():
        seg = m[y0:y1, 78:600]
        ys, xs = np.where(seg)
        if len(xs) > 20:
            print(f"     {cn}: x[{xs.min()+78}..{xs.max()+78}] ({i(xs.min()+78)}..{i(xs.max()+78)}in)"
                  f" y[{ys.min()+y0}..{ys.max()+y0}] n={len(xs)}")

print("\n=== cream inset box (r>245,g>240,150<b<240) ===")
cream = (r > 240) & (g > 235) & (b > 150) & (b < 240)
lab, n = ndimage.label(cream)
sizes = ndimage.sum(cream, lab, range(1, n + 1))
for k in np.argsort(sizes)[::-1][:4]:
    ys, xs = np.where(lab == k + 1)
    m = a[ys, xs].mean(axis=0).astype(int)
    print(f"  x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={int(sizes[k])} "
          f"in=({i(xs.min())}..{i(xs.max())} x {i(ys.min())}..{i(ys.max())}) mean=#{m[0]:02X}{m[1]:02X}{m[2]:02X}")

print("\n=== inset internals (region x 560..880, y 310..470) dark blobs ===")
reg = a[310:470, 560:880]
dd = reg.sum(axis=2) < 400
lab2, n2 = ndimage.label(dd)
sizes2 = ndimage.sum(dd, lab2, range(1, n2 + 1))
for k in np.argsort(sizes2)[::-1][:16]:
    if sizes2[k] < 30:
        break
    ys, xs = np.where(lab2 == k + 1)
    print(f"  x[{xs.min()+560}..{xs.max()+560}] y[{ys.min()+310}..{ys.max()+310}] px={int(sizes2[k])} "
          f"in=({i(xs.min()+560)},{i(ys.min()+310)})")

print("\n=== legend box + text colors (region x 335..415, y 108..150) ===")
lr, lg, lb = a[108:150, 335:415, 0], a[108:150, 335:415, 1], a[108:150, 335:415, 2]
lm = (lr + lg + lb) < 420
ys, xs = np.where(lm)
print(f"  dark ink x[{xs.min()+335}..{xs.max()+335}] y[{ys.min()+108}..{ys.max()+108}] n={len(xs)}")
m1 = (lr > 110) & (lr > lg + 50)
if m1.sum():
    ys1, xs1 = np.where(m1)
    print(f"  red ink: x[{xs1.min()+335}..{xs1.max()+335}] y[{ys1.min()+108}..{ys1.max()+108}] n={int(m1.sum())}")
    print(f"  red rows: {sorted(set((ys1+108).tolist()))[:40]}")
print("  ink rows:", [int(y + 108) for y in np.where(lm.sum(axis=1) > 1)[0]])

print("\n=== step box border color (main) + node outline ===")
for (x, y, nm) in [(415, 210, "stepbox left border"), (470, 210, "stepbox right border"),
                   (283, 126, "node1 top outline"), (712, 381, "inset sigma top outline"),
                   (285, 152, "node1 fill center"), (355, 205, "node3 fill center"),
                   (712, 396, "inset sigma fill")]:
    print(f"  {nm} ({x},{y}) = {tuple(a[y, x])}")
