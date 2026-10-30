#!/usr/bin/env python3
"""Measure slide_001.jpg (960x540, 1px=1pt) geometry for the build.
Masks per color class; ink bboxes per connected text region (row/col projections).
Output banked as qa/slide001/selfcheck_measure_original.txt evidence.
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]


def bbox_of(mask, label):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{label}: NO INK")
        return None
    bb = (xs.min(), ys.min(), xs.max(), ys.max())
    print(f"{label}: bbox x {bb[0]}..{bb[2]} y {bb[1]}..{bb[3]}  (w={bb[2]-bb[0]+1}, h={bb[3]-bb[1]+1}) px")
    return bb


def row_bands(mask, label, min_gap=3, min_h=4):
    """Split a mask's rows into contiguous ink bands (text lines)."""
    rows = np.where(mask.any(axis=1))[0]
    if not len(rows):
        print(f"{label}: no rows")
        return []
    bands = []
    start = prev = rows[0]
    for y in rows[1:]:
        if y - prev > min_gap:
            if prev - start >= min_h - 1:
                bands.append((start, prev))
            start = y
        prev = y
    if prev - start >= min_h - 1:
        bands.append((start, prev))
    print(f"{label}: {len(bands)} row bands: {bands}")
    return bands


def band_bbox(mask, y0, y1, label):
    sub = mask[y0:y1 + 1]
    xs = np.where(sub.any(axis=0))[0]
    if not len(xs):
        print(f"{label}: empty")
        return None
    print(f"{label}: y {y0}..{y1}, x {xs.min()}..{xs.max()} (w={xs.max()-xs.min()+1})")
    return (xs.min(), y0, xs.max(), y1)


print("=== slide_001.jpg measurement (960x540) ===")
print(f"canvas corners: TL{tuple(IM[5,5])} TR{tuple(IM[5,954])} BL{tuple(IM[534,5])} BR{tuple(IM[534,954])}")
print(f"panel samples: (300,500)={tuple(IM[300,500])} (100,100)={tuple(IM[100,100])}")

# color masks
red = (r > 120) & (r - g > 55) & (r - b > 55)          # title text C00000-family
blue = (b - r > 60) & (b - g > 40) & (b > 100)          # blue body text
dark = (r < 90) & (g < 90) & (b < 90)                   # black-ish ink
teal = (g > 90) & (b > 90) & (r < 80) & (abs(g - b) < 45)  # logo teal panel
yellow = (r > 200) & (g > 200) & (b < 190)

print("\n--- RED (title) ---")
bbox_of(red, "red-ink total")
row_bands(red, "red bands")

print("\n--- BLUE text ---")
bbox_of(blue, "blue-ink total")
blue_bands = row_bands(blue, "blue bands")
for i, (y0, y1) in enumerate(blue_bands):
    band_bbox(blue, y0, y1, f"blue band {i}")

print("\n--- DARK (black ink: Instructors header + logo EN text + badge numeral) ---")
# exclude the badge region (x>855,y<95) and logo region from 'dark' for the header measurement
dark_noBadge = dark.copy()
dark_noBadge[:100, 850:] = False
bbox_of(dark_noBadge, "dark-ink total (badge excluded)")
dark_bands = row_bands(dark_noBadge, "dark bands (badge excl)")
for i, (y0, y1) in enumerate(dark_bands):
    band_bbox(dark_noBadge, y0, y1, f"dark band {i}")

print("\n--- TEAL (logo panel) ---")
bbox_of(teal, "teal total")

print("\n--- YELLOW (badge) ---")
bbox_of(yellow, "yellow total")

# Gray panel extent via the chrome values (sanity, panel fill E9E9E7 ~ (231,233,230))
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
cols = np.where(gray[100:520].sum(axis=0) > 300)[0]
rows = np.where(gray[:, 100:800].sum(axis=1) > 500)[0]
print(f"\npanel gray: x {cols.min()}..{cols.max()}, y {rows.min()}..{rows.max()}")
