#!/usr/bin/env python3
"""Adjudicate A13 (attempt 13) findings PIL-first: BR descent-path ink volume,
BL bottom-edge tick clipping, X/Y label presence (frame space 960x540)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{V}/recreated_pptx/qa/slide_025"
S = 2001 / 960.0

imgs = {
    "ORIG":   np.asarray(Image.open(f"{V}/unique_slides/slide_025.jpg").convert("RGB")).astype(int),
    "REND13": np.asarray(Image.open(f"{QA}/render_13.png").convert("RGB")).astype(int),
    "REND12": np.asarray(Image.open(f"{QA}/render_12.png").convert("RGB")).astype(int),
}


def zone(a, x0, y0, x1, y1):
    return a[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]


def darkink(z):
    return z.sum(axis=2) < 300


print("=== 1. BR descent path: dark-ink volume x615..886 y344..538 ===")
for tag, a in imgs.items():
    z = zone(a, 615, 344, 886, 538)
    d = darkink(z)
    print(f"  {tag}: total dark {int(d.sum()):6d}  ({100*d.mean():.2f}% of region)")

print("=== 2. BR path start corridor x620..700 y350..420 (upper-left of BR panel) ===")
for tag, a in imgs.items():
    z = zone(a, 620, 350, 700, 420)
    d = darkink(z)
    print(f"  {tag}: dark {int(d.sum()):6d}")

print("=== 3. BL bottom band row profiles: dark ink vs red border (y495..535, x83..383) ===")
for tag, a in imgs.items():
    z = zone(a, 83, 495, 383, 535)
    d = darkink(z)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    red = (r > 110) & (r - g > 55) & (r - b > 55)
    prof_d = d.sum(axis=1)
    prof_r = red.sum(axis=1)
    print(f"  -- {tag}: (row y, dark, red)")
    for i in range(0, z.shape[0], 2):
        if prof_d[i] > 3 or prof_r[i] > 3:
            print(f"     y{495 + i / S:6.1f}  dark {int(prof_d[i]):4d}  red {int(prof_r[i]):4d}")

print("=== 4. X/Y label glyphs in BL corners (orig vs renders) ===")
# candidate zones: left edge below pane (Y), right edge below pane (X)
for tag, a in imgs.items():
    yz = zone(a, 83, 430, 130, 530)
    xz = zone(a, 330, 430, 383, 530)
    dy, dx = darkink(yz), darkink(xz)
    print(f"  {tag}: left-corner dark {int(dy.sum()):5d}  right-corner dark {int(dx.sum()):5d}")

print("=== 5. BL tick-label x-positions in bottom band y505..530 (digit ink columns) ===")
for tag, a in imgs.items():
    z = zone(a, 83, 505, 383, 530)
    d = darkink(z)
    cols = np.nonzero(d.sum(axis=0) > 2)[0]
    if len(cols):
        runs, st = [], cols[0]
        for i in range(1, len(cols)):
            if cols[i] != cols[i - 1] + 1:
                runs.append((st, cols[i - 1])); st = cols[i]
        runs.append((st, cols[-1]))
        print(f"  {tag}: col clusters " + ", ".join(
            f"{83 + a_ / S:.0f}..{83 + b_ / S:.0f}" for a_, b_ in runs))
    else:
        print(f"  {tag}: none")
