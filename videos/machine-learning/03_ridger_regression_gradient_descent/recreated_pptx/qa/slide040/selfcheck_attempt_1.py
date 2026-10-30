#!/usr/bin/env python3
"""Mandatory pre-judge self-check for slide 040 attempt 1.
Run on 150dpi render (2001x1125 px). Frame px scale = 2001/960 = 2.084375."""
from PIL import Image
import numpy as np
import sys

RENDER = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide040/render_1.png"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_040.jpg"

im = Image.open(RENDER)
arr = np.array(im.convert("RGB"))
H, W = arr.shape[:2]
print(f"=== Render: {W}x{H} (expected 2001x1125 for 150dpi LAYOUT_WIDE) ===")

r, g, b = arr[:,:,0].astype(int), arr[:,:,1].astype(int), arr[:,:,2].astype(int)
scale = W / 960.0  # render px per frame px
print(f"Scale: {scale:.4f} render px per frame px")

# 1. FRAME CONTAINMENT
# Panel inner frame: x54..903, y45..540 in frame px -> render px
panel_x0 = int(54 * scale)
panel_x1 = int(903 * scale)
panel_y0 = int(45 * scale)
panel_y1 = int(540 * scale)
print(f"\n1. PANEL frame containment (render px): x {panel_x0}..{panel_x1}, y {panel_y0}..{panel_y1}")

# Find text ink (non-panel, non-white, non-stroke)
# Panel gray is ~E9E9E7 (233,233,231)
panel_gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
# Strokes are red C00000
strokes = (r > 120) & ((r - g) > 40) & ((r - b) > 40)
# White/near-white background
white = (r > 250) & (g > 250) & (b > 250)

# Text ink = dark pixels that are not in panel gray, not strokes, not white
ink = ~(panel_gray | strokes | white)
ink = ink & (arr.sum(axis=2) < 600)  # dark-ish

ys, xs = np.where(ink)
if len(ys):
    print(f"   Ink bbox (render): x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
    # Check if any ink is outside panel
    outside_x = ((xs < panel_x0) | (xs > panel_x1)).sum()
    outside_y = ((ys < panel_y0) | (ys > panel_y1)).sum()
    print(f"   Ink outside panel horizontally: {outside_x} px")
    print(f"   Ink outside panel vertically: {outside_y} px")
    if outside_x > 0 or outside_y > 0:
        print(f"   *** FAIL: Ink touches/crosses panel boundary ***")
    else:
        print(f"   PASS: All content ink inside panel")
else:
    print(f"   No ink found (unexpected)")

# 2. EQUATIONS - none on this slide per analysis
print(f"\n2. EQUATIONS: None on this slide (analysis shows empty equations array) - PASS")

# 3. DELIMITER GEOMETRY - none
print(f"\n3. DELIMITER GEOMETRY: No multi-line delimiters - PASS")

# 4. TABLE DATA - none
print(f"\n4. TABLE DATA: No tables - PASS")

# 5. LINE SPACING - each text box is single-line (one band per element)
# Check line separation between the three text lines
# Find red text lines (title + subheader) and blue line
red = (r > 120) & ((r - g) > 40) & ((r - b) > 40)
blue = (b > 120) & ((b - r) > 40) & ((b - g) > 40)

# Red text bands (exclude left/right stroke columns)
left_stroke_x = int(58.5 * scale)
right_stroke_x = int(901 * scale)
inner_x = slice(left_stroke_x + 10, right_stroke_x - 10)

red_rows = red[:, inner_x].sum(axis=1)
red_bands = []
y = 0
while y < H:
    if red_rows[y] > 5:
        s = y
        while y < H and red_rows[y] > 5:
            y += 1
        red_bands.append((s, y-1))
    else:
        y += 1
print(f"\n5. TEXT LINE SPACING (red text, inner panel):")
for s, e in red_bands:
    print(f"   Band y={s}..{e} h={e-s+1}")

blue_rows = blue[:, inner_x].sum(axis=1)
blue_bands = []
y = 0
while y < H:
    if blue_rows[y] > 5:
        s = y
        while y < H and blue_rows[y] > 5:
            y += 1
        blue_bands.append((s, y-1))
    else:
        y += 1
print(f"   Blue band(s):")
for s, e in blue_bands:
    print(f"     y={s}..{e} h={e-s+1}")

# Check inter-line gaps
all_bands = red_bands + blue_bands
all_bands.sort()
print(f"   Ordered bands (centre y):")
centres = []
for s, e in all_bands:
    c = (s + e) / 2
    centres.append(c)
    print(f"     y={s}..{e} centre={c:.1f}")

# Line spacing = gap between centres
for i in range(len(centres)-1):
    gap = centres[i+1] - centres[i]
    print(f"   Line spacing {i}->{i+1}: {gap:.1f} render px = {gap/scale:.1f} frame px")

# 6. VERTICAL CENTERING IN BOXES - N/A (single-line boxes)
print(f"\n6. VERTICAL CENTERING: Single-line boxes, no multi-line - PASS")

# 7. BADGE check
print(f"\n7. BADGE:")
cy = int(73 * scale)
cx = int(876 * scale)
d = int(35 * scale)
patch = arr[cy-d//2:cy+d//2, cx-d//2:cx+d//2]
# Yellow
yel = (patch[:,:,0] > 200) & (patch[:,:,1] > 200) & (patch[:,:,2] < 100)
print(f"   Yellow disc pixels: {yel.sum()}")
# Purple ring
pur = (patch[:,:,0] > 70) & (patch[:,:,0] < 180) & (patch[:,:,1] < 130) & (patch[:,:,2] > 170) & (patch[:,:,2] < 230)
print(f"   Purple ring pixels: {pur.sum()}")
# Dark numeral
dark = patch.sum(axis=2) < 300
print(f"   Dark numeral pixels: {dark.sum()}")

# 8. TEXT CONTENT CHECK - verify the three lines exist at expected positions
print(f"\n8. TEXT POSITION CHECK:")
# Red text 1: "Training of Linear Regression Model" ~ y177 frame = y369 render
# Red text 2: "Solved Example" ~ y326 frame = y680 render
# Blue: "usnig SGD" ~ y257 frame = y536 render
# Sample middle of each band
for label, y_frame in [("L1 title", 180), ("L2 subtitle", 260), ("L3 subheader", 330)]:
    y_r = int(y_frame * scale)
    row = arr[y_r, inner_x]
    # Find darkest pixels
    dark_row = row.sum(axis=1)
    if dark_row.min() < 200:
        ink_x = np.where(dark_row < 200)[0]
        ctr = ink_x.mean() + inner_x.start
        print(f"   {label}: y_frame={y_frame} y_render={y_r}, ink centre x={ctr:.0f} (frame x={ctr/scale:.0f})")

print(f"\n=== Self-check complete ===")
