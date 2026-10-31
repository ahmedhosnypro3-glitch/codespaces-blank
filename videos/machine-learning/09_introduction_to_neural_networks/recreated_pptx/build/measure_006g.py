#!/usr/bin/env python3
"""Probe 3: fan-in line colors, exact RGB samples, word segmentation."""
from PIL import Image
import numpy as np
from scipy import ndimage
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)

print("=== exact RGB samples ===")
pts = [(105, 118), (90, 124), (410, 165), (437, 165), (435, 420), (77, 118),
       (72, 168), (73, 168), (137, 380), (326, 380), (145, 365), (230, 380),
       (320, 395), (681, 186), (681, 320), (681, 455), (743, 186), (744, 180),
       (640, 355), (424, 250), (895, 300), (500, 499), (740, 175), (682, 186)]
for x, y in pts:
    print(f"  ({x},{y}) = {tuple(a[y, x])}")

print("\n=== fan-zone color blobs (loose chroma) ===")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
reg = (slice(140, 480), slice(420, 660))
for name, m in (
    ("reddish", (R - G > 28) & (R - B > 28)),
    ("bluish", (B - G > 28) & (B - R > 28)),
    ("greenish", (G - R > 25) & (G - B > 25)),
):
    mm = np.zeros_like(m)
    mm[reg] = m[reg]
    lab, n = ndimage.label(mm, structure=np.ones((3, 3)))
    got = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 6:
            continue
        col = a[ys, xs].mean(axis=0).round().astype(int)
        got.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys), tuple(col)))
    got.sort(key=lambda t: t[1])
    print(f" {name}: {len(got)} blobs")
    for g in got[:35]:
        print(f"    x {g[0]}-{g[2]} y {g[1]}-{g[3]} n={g[4]} rgb{g[5]}")

print("\n=== word segmentation: callout text (y 364..396) ===")
ink = (a[364:397, 130:330].sum(axis=2) < 600)
colprof = ink.sum(axis=0)
runs = []
inrun = False
for i, v in enumerate(colprof):
    if v > 0 and not inrun:
        s = i; inrun = True
    elif v == 0 and inrun:
        runs.append((130 + s, 130 + i - 1)); inrun = False
if inrun:
    runs.append((130 + s, 329))
print("  column runs:", runs)

print("\n=== class-label text extents (right) ===")
for name, y0, y1 in (("label1 line A", 174, 190), ("label1 line B", 190, 200),
                     ("label2 line A", 305, 320), ("label3 line A", 441, 458)):
    ink2 = (a[y0:y1, 780:900].sum(axis=2) < 600)
    ys, xs = np.where(ink2)
    if len(xs):
        print(f"  {name}: x {780+xs.min()}-{780+xs.max()} y {y0+ys.min()}-{y0+ys.max()} n={len(xs)}")
    else:
        print(f"  {name}: none")

print("\n=== panel edges ===")
edge = (a[:, :, 2].astype(int) - a[:, :, 0].astype(int) > 12)
for x in range(410, 440):
    ys = np.where(edge[240:490, x])[0]
    if len(ys) > 100:
        print(f"  panel-left col x={x}: y {240+ys.min()}-{240+ys.max()} n={len(ys)}")
for y in (140, 141, 142, 143, 144, 145, 150):
    xs = np.where(edge[y, 450:900])[0]
    if len(xs) > 50:
        print(f"  panel-top row y={y}: x {450+xs.min()}-{450+xs.max()} n={len(xs)}")
