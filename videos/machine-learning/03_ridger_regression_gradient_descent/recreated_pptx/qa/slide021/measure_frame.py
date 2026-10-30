#!/usr/bin/env python3
"""measure_frame.py — pass-1 broad census of unique_slides/slide_021.jpg (960x540).

Goal: locate the three blue-outlined light-gray panels, the title band, and the
content blocks inside each panel. Prints bboxes + color cores. Banked in
qa/slide021/ per the deck law (geometry from measurement, never intuition).
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("size", W, H)

r, g, b = a[..., 0], a[..., 1], a[..., 2]

# --- blue ink mask (panel outlines; blue = B >> R and B >> G) ---
blue = (b > 120) & (b - r > 60) & (b - g > 60)
# --- red ink mask (title, labels; R >> G,B) ---
red = (r > 100) & (r - g > 60) & (r - b > 60)
# --- green ink mask (lambda=3 label; G >> R,B) ---
green = (g > 100) & (g - r > 50) & (g - b > 50)
# --- dark ink mask (text/table lines: all channels low) ---
dark = (r < 90) & (g < 90) & (b < 90)
# --- yellow mask (badge, diagonal highlights) ---
yellow = (r > 180) & (g > 180) & (b < 140)

for name, m in [("blue", blue), ("red", red), ("green", green), ("dark", dark), ("yellow", yellow)]:
    n = int(m.sum())
    print(f"\n== {name}: {n} px")
    if n == 0:
        continue
    # row/col projections, find clusters
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    print(f"   row extent {rows.min()}..{rows.max()}  col extent {cols.min()}..{cols.max()}")
    # row bands (gaps > 3 split)
    bands = []
    start = rows[0]; prev = rows[0]
    for y in rows[1:]:
        if y - prev > 4:
            bands.append((start, prev)); start = y
        prev = y
    bands.append((start, prev))
    print("   row bands:", bands)

# --- gray panel fills: census distinct light-gray fills inside panels ---
# sample a horizontal line through the middle of each candidate panel band
print("\n== fill sampling along column x=480 (center) per row (step 6):")
for y in range(40, 540, 6):
    px = a[y, 480]
    print(f"  y={y}: ({px[0]},{px[1]},{px[2]})")
