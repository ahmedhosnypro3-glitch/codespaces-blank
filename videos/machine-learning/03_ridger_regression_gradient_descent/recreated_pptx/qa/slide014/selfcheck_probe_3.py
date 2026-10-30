#!/usr/bin/env python3
"""PIL measurement - tighter color detection for content bands."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

mask_yel = (r >= 250) & (g >= 240) & (b >= 180) & (b <= 210) & (r - b > 30)
ys = np.where(mask_yel)
if len(ys[0]) > 0:
    print(f"Light yellow: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

mask_pink = (r >= 250) & (g >= 225) & (g <= 245) & (b >= 228) & (b <= 248)
ys = np.where(mask_pink)
if len(ys[0]) > 0:
    print(f"Light pink: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

mask_lblue = (r >= 215) & (r <= 240) & (g >= 235) & (g <= 255) & (b >= 245) & (b <= 255)
ys = np.where(mask_lblue)
if len(ys[0]) > 0:
    print(f"Light blue: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

panel_mask = (np.abs(r[54:904, :] - 233) < 15) & (np.abs(g[54:904, :] - 233) < 15) & (np.abs(b[54:904, :] - 231) < 15)
ys = np.where(panel_mask)
if len(ys[0]) > 0:
    print(f"Panel gray: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")

# badge
br = im[55:90, 850:900]
rb, gb, bb = br[:, :, 0], br[:, :, 1], br[:, :, 2]
yel_mask = (rb > 220) & (gb > 220) & (bb < 120)
ys = np.where(yel_mask)
if len(ys[0]) > 0:
    print(f"Badge yellow center: ({ys[1].mean()+850:.1f}, {ys[0].mean()+55:.1f})")
pur_mask = (bb > 140) & (rb > 80) & (rb < 180) & (gb < 130)
ys = np.where(pur_mask)
if len(ys[0]) > 0:
    print(f"Badge purple center: ({ys[1].mean()+850:.1f}, {ys[0].mean()+55:.1f})")

print("\n--- Row transitions (ink density) ---")
prof = (np.abs(im - 255).max(axis=2) > 30).sum(axis=1)
prev = 0
for y in range(540):
    if abs(prof[y] - prev) > 150:
        print(f"  y={y}: {prev} -> {prof[y]}")
    prev = prof[y]

print("\n--- Upper middle (y=90-180) col profile ---")
sub = im[90:180, 60:900]
inkm = (np.abs(sub - 255).max(axis=2) > 30).sum(axis=0)
for x in range(0, 840, 40):
    if inkm[x] > 10:
        print(f"  x={x+60}: ink={inkm[x]}")

print("\n--- Lower middle (y=400-500) col profile ---")
sub = im[400:500, 60:900]
inkm = (np.abs(sub - 255).max(axis=2) > 30).sum(axis=0)
for x in range(0, 840, 40):
    if inkm[x] > 10:
        print(f"  x={x+60}: ink={inkm[x]}")

# blue text rows (title + accents)
blue = (b > 180) & (r < 120) & (g < 100)
ys = np.where(blue)
if len(ys[0]) > 0:
    print(f"\nBlue ink: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")
    rows_b = np.where(blue.sum(axis=1) > 2)[0]
    print(f"Blue ink rows: {rows_b.min()}-{rows_b.max()}")

# Black text ink in content bands (exclude panel gray FFFFFF)
blackish = (r < 120) & (g < 120) & (b < 120)
ys = np.where(blackish)
if len(ys[0]) > 0:
    print(f"Black ink: x {ys[1].min()}-{ys[1].max()}, y {ys[0].min()}-{ys[0].max()}")
