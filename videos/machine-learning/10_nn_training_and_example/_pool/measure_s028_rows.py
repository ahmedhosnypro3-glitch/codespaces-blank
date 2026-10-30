#!/usr/bin/env python3
"""Row-by-row x-gap segmentation for slide_028 lower half (fixed)."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_028.jpg").convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
INK = (np.abs(a - a[5, 5]).sum(axis=2) > 40)
INK[:, :46] = False
INK[:, 916:] = False
INK[:46, :] = False
INK[534:, :] = False
BLUE_LOOSE = (b > r + 25) & (b > 70)
RED_LOOSE = (r > g + 30) & (r > b + 30) & (r > 90)


def groups_from_cols(colink, x0, gap):
    runs = []
    i = 0
    n = len(colink)
    while i < n:
        if colink[i]:
            j = i
            while j + 1 < n and colink[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    out = []
    for (s, e) in runs:
        if out and s - out[-1][1] - 1 <= gap:
            out[-1] = (out[-1][0], e)
        else:
            out.append((s, e))
    return [(x0 + s, x0 + e) for (s, e) in out]


def profile(mask, y0, y1, x0, x1, gap=14, label=""):
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    gs = groups_from_cols(sub.any(axis=0), x0, gap)
    print(f"-- {label} rows {y0}-{y1}: " + " | ".join(f"x[{a}-{b}]({b-a+1})" for a, b in gs))


def rowbands(mask, y0, y1, x0, x1, minpx=6, gap=3):
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    counts = sub.sum(axis=1)
    bands = []
    st = None
    for i, c in enumerate(counts):
        if c >= minpx and st is None:
            st = i
        elif c < minpx and st is not None:
            bands.append((st, i - 1))
            st = None
    if st is not None:
        bands.append((st, len(counts) - 1))
    merged = []
    for (s, e) in bands:
        if merged and s - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return [(y0 + s, y0 + e) for (s, e) in merged]


print("=== HEADER ROW (y193-218) ===")
profile(INK, 193, 218, 42, 919, gap=16, label="INK")
profile(BLUE_LOOSE, 193, 218, 42, 919, gap=16, label="BLUE")
profile(RED_LOOSE, 193, 218, 42, 919, gap=16, label="RED")

print("\n=== ROW BANDS ===")
for (y0, y1) in rowbands(INK, 185, 536, 42, 919, minpx=6, gap=3):
    if y1 - y0 < 3:
        continue
    profile(INK, y0, y1, 42, 919, gap=16, label=f"rows {y0}-{y1}")
