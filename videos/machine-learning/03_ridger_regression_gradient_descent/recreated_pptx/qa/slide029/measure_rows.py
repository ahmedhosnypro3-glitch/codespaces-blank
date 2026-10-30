#!/usr/bin/env python3
"""Precise re-measurement of slide_029.jpg title block with a sensitive ink mask,
per-line row profiles (ascender/x-height/baseline/descender structure), to derive
font metrics. Complements measure_original.py (strict red mask = ink core)."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_029.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# sensitive ink mask: any pixel far from the local panel bg (231,233,230) in the
# red-dominant direction; catches antialiased glyph edges the strict mask drops.
bg_r, bg_g, bg_b = 231, 233, 230
dist = np.sqrt((r - bg_r) ** 2 + (g - bg_g) ** 2 + (b - bg_b) ** 2)
ink = dist > 40
# restrict to panel interior (exclude chrome strokes + badge)
ink[:, :75] = False
ink[:, 885:] = False
ink[530:, :] = False
ink[:45, :] = False

rows = ink.sum(axis=1)
bands, in_b = [], False
for y in range(H):
    if rows[y] > 0 and not in_b:
        s = y; in_b = True
    elif rows[y] == 0 and in_b:
        bands.append((s, y - 1)); in_b = False
if in_b:
    bands.append((s, H - 1))
bands = [bd for bd in bands if ink[bd[0]:bd[1] + 1].sum() > 50]
print("SENSITIVE-MASK line bands:")
for (y0, y1) in bands:
    seg = ink[y0:y1 + 1]
    xs_l = np.where(seg.any(axis=0))[0]
    print(f"  y {y0}-{y1} h={y1 - y0 + 1}, x {xs_l.min()}-{xs_l.max()} w={xs_l.max() - xs_l.min() + 1}, "
          f"cx={(xs_l.min() + xs_l.max()) / 2:.1f}, ink={seg.sum()}")

print("\nPer-line row profiles (rows with ink>2), to see ascender/x-height/descender structure:")
for (y0, y1) in bands:
    print(f"  --- band y{0}..".format(y0))
    prof = ink[y0:y1 + 1].sum(axis=1)
    # print compact: y:count  (mark x-height core >50% of max)
    mx = prof.max()
    line = []
    for i, c in enumerate(prof):
        mark = "#" if c > mx * 0.55 else ("+" if c > mx * 0.2 else ".")
        line.append(f"{y0 + i}:{c}{mark}")
    for i in range(0, len(line), 8):
        print("    " + "  ".join(line[i:i + 8]))
