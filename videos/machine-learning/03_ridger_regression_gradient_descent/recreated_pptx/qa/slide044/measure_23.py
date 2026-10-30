#!/usr/bin/env python3
"""Rule-line colours + long vertical dark strokes in the right column."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
ink = LUM < 185

print("=== rule line core colours ===")
for y in (140, 197, 205, 206, 461, 462):
    xs = np.where(ink[y, 280:850])[0] + 280
    if len(xs):
        core = IM[y, xs]
        # darkest 20%
        lum = 0.299 * core[:, 0] + 0.587 * core[:, 1] + 0.114 * core[:, 2]
        d = core[lum.argsort()[:max(1, len(core) // 20)]].mean(axis=0).astype(int)
        print(f"  y{y}: x{xs.min()}..{xs.max()} n={len(xs)} darkest-core #{d[0]:02X}{d[1]:02X}{d[2]:02X}  "
              f"median #{int(np.median(core[:,0])):02X}{int(np.median(core[:,1])):02X}{int(np.median(core[:,2])):02X}")

print("\n=== long vertical dark strokes in x265..860, y140..530 (>=20px) ===")
for x in range(265, 861):
    ys = np.where(ink[140:531, x])[0]
    if len(ys) < 20:
        continue
    runs = []
    s = ys[0]; p = ys[0]
    for i in ys[1:]:
        if i - p <= 3: p = i
        else:
            if p - s >= 20: runs.append((140 + s, 140 + p))
            s = i; p = i
    if p - s >= 20: runs.append((140 + s, 140 + p))
    for a, b in runs:
        if b - a >= 20:
            print(f"  x{x}: y{a}..{b} len {b - a + 1}")
