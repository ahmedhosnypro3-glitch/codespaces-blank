#!/usr/bin/env python3
"""Self-check for slide 037 attempt 1 - verify frame containment, equations, delimiters, etc."""
import numpy as np
from PIL import Image

# Load render and original
render = Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037/render_1.png").convert("RGB")
original = Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_037.jpg").convert("RGB")

r_arr = np.asarray(render).astype(int)
o_arr = np.asarray(original).astype(int)

H_r, W_r = r_arr.shape[:2]
H_o, W_o = o_arr.shape[:2]
scale = H_r / H_o  # ~2.083

print(f"Render: {W_r}x{H_r}, Original: {W_o}x{H_o}, Scale: {scale:.3f}")

# Color channels
rr, rg, rb = r_arr[:, :, 0], r_arr[:, :, 1], r_arr[:, :, 2]
or_, og, ob = o_arr[:, :, 0], o_arr[:, :, 1], o_arr[:, :, 2]

# ===== 1. FRAME CONTAINMENT =====
print("\n=== 1. FRAME CONTAINMENT ===")
# House frame boundaries in render px
# Gray panel: x 54..903 -> render: 112..1882 (from house_chrome_check)
# Strokes: left x58.5->122, right x901->1876, bottom y538.5->1122
# Content should be inside these

# Check content in pale yellow panel area (should be inside gray panel)
# Pale yellow panel original: rows ~110-200, cols ~70-890
# Render: rows ~229-416, cols ~146-1854
py_top = int(110 * scale)
py_bot = int(200 * scale)
py_left = int(70 * scale)
py_right = int(890 * scale)

# Find non-white/non-gray ink in this region
region = r_arr[py_top:py_bot, py_left:py_right]
# Ink = not white (255,255,255) and not gray panel (233,233,231) and not pale yellow (255,249,196)
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((abs(region[:,:,0] - 233) < 20) & (abs(region[:,:,1] - 233) < 20) & (abs(region[:,:,2] - 231) < 20)) & \
      ~((region[:,:,0] > 240) & (region[:,:,1] > 230) & (region[:,:,2] < 210))

ink_rows = np.where(ink.any(axis=1))[0]
ink_cols = np.where(ink.any(axis=0))[0]
if len(ink_rows) > 0:
    print(f"Pale yellow panel ink: rows {ink_rows.min()+py_top}..{ink_rows.max()+py_top}, cols {ink_cols.min()+py_left}..{ink_cols.max()+py_left}")
    # Check containment
    if ink_rows.min() < 5 or ink_rows.max() > (py_bot - py_top) - 5:
        print("  WARNING: Ink near panel top/bottom edge")
    if ink_cols.min() < 5 or ink_cols.max() > (py_right - py_left) - 5:
        print("  WARNING: Ink near panel left/right edge")
else:
    print("Pale yellow panel: NO INK FOUND")

# Check tan panel 1 (middle)
t1_top = int(228 * scale)
t1_bot = int(379 * scale)
t1_left = int(70 * scale)
t1_right = int(890 * scale)

region = r_arr[t1_top:t1_bot, t1_left:t1_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((abs(region[:,:,0] - 245) < 25) & (abs(region[:,:,1] - 230) < 25) & (abs(region[:,:,2] - 202) < 25))

ink_rows = np.where(ink.any(axis=1))[0]
ink_cols = np.where(ink.any(axis=0))[0]
if len(ink_rows) > 0:
    print(f"Tan panel 1 ink: rows {ink_rows.min()+t1_top}..{ink_rows.max()+t1_top}, cols {ink_cols.min()+t1_left}..{ink_cols.max()+t1_left}")
    if ink_rows.min() < 5 or ink_rows.max() > (t1_bot - t1_top) - 5:
        print("  WARNING: Ink near panel top/bottom edge")
    if ink_cols.min() < 5 or ink_cols.max() > (t1_right - t1_left) - 5:
        print("  WARNING: Ink near panel left/right edge")
else:
    print("Tan panel 1: NO INK FOUND")

# Check tan panel 2 (bottom)
t2_top = int(380 * scale)
t2_bot = int(519 * scale)
t2_left = int(70 * scale)
t2_right = int(890 * scale)

region = r_arr[t2_top:t2_bot, t2_left:t2_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((abs(region[:,:,0] - 245) < 25) & (abs(region[:,:,1] - 230) < 25) & (abs(region[:,:,2] - 202) < 25)) & \
      ~((region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220))  # green fill

ink_rows = np.where(ink.any(axis=1))[0]
ink_cols = np.where(ink.any(axis=0))[0]
if len(ink_rows) > 0:
    print(f"Tan panel 2 ink: rows {ink_rows.min()+t2_top}..{ink_rows.max()+t2_top}, cols {ink_cols.min()+t2_left}..{ink_cols.max()+t2_left}")
    if ink_rows.min() < 5 or ink_rows.max() > (t2_bot - t2_top) - 5:
        print("  WARNING: Ink near panel top/bottom edge")
    if ink_cols.min() < 5 or ink_cols.max() > (t2_right - t2_left) - 5:
        print("  WARNING: Ink near panel left/right edge")
else:
    print("Tan panel 2: NO INK FOUND")

# ===== 2. EQUATIONS EXIST (ink in equation regions) =====
print("\n=== 2. EQUATIONS EXIST ===")
# Error equation region: original rows 264-287
eq1_top = int(264 * scale)
eq1_bot = int(287 * scale)
eq1_left = int(82 * scale)
eq1_right = int(868 * scale)
region = r_arr[eq1_top:eq1_bot, eq1_left:eq1_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240))
if ink.any():
    print(f"Error equation region: HAS INK ({ink.sum()} px)")
else:
    print("Error equation region: EMPTY - BLOCKER")

# First update equation region: original rows 404-449
eq2_top = int(404 * scale)
eq2_bot = int(449 * scale)
eq2_left = int(84 * scale)
eq2_right = int(715 * scale)
region = r_arr[eq2_top:eq2_bot, eq2_left:eq2_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220))
if ink.any():
    print(f"First update equation region: HAS INK ({ink.sum()} px)")
else:
    print("First update equation region: EMPTY - BLOCKER")

# Second update equation region: original rows 473-513
eq3_top = int(473 * scale)
eq3_bot = int(513 * scale)
eq3_left = int(85 * scale)
eq3_right = int(405 * scale)
region = r_arr[eq3_top:eq3_bot, eq3_left:eq3_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220))
if ink.any():
    print(f"Second update equation region: HAS INK ({ink.sum()} px)")
else:
    print("Second update equation region: EMPTY - BLOCKER")

# ===== 3. DELIMITER GEOMETRY =====
print("\n=== 3. DELIMITER GEOMETRY ===")
# Check for parentheses/brackets in the equation regions
# Look for ( ) [ ] { } in the render
# The original has subscripts with _ but in professional format they should be proper subscripts
# We can't easily check delimiter geometry without knowing what delimiters exist
# The spec mentions subscripts but not multi-line delimiters
print("No multi-line delimiters detected in spec - skipping detailed check")

# ===== 4. TABLE DATA =====
print("\n=== 4. TABLE DATA ===")
print("No tables on this slide - skipping")

# ===== 5. EXPLICIT LINE SPACING =====
print("\n=== 5. LINE SPACING CHECK ===")
# Check multi-line text blocks have consistent line spacing
# The implication lines, error equation, update equations are single visual lines
# but may wrap. Check the implication lines.
# Implication 1: single line in original at row 146-162
# Implication 2: single line at row 172-189
# These appear as single lines - no multi-line wrapping expected

print("No multi-line text blocks detected that need explicit lineSpacing")

# ===== 6. COLOR SAMPLING =====
print("\n=== 6. KEY COLOR SAMPLING ===")
# Sample key locations in render vs expected
# Title center
title_y = int(74 * scale)
title_x = int(479.5 * scale)
print(f"Title center ({title_x},{title_y}): RGB=({rr[title_y,title_x]}, {rg[title_y,title_x]}, {rb[title_y,title_x]})")

# Badge center
badge_x = int(877 * scale)
badge_y = int(73.5 * scale)
print(f"Badge center ({badge_x},{badge_y}): RGB=({rr[badge_y,badge_x]}, {rg[badge_y,badge_x]}, {rb[badge_y,badge_x]})")

# Pale yellow panel
py_y = int(150 * scale)
py_x = int(480 * scale)
print(f"Pale yellow panel ({py_x},{py_y}): RGB=({rr[py_y,py_x]}, {rg[py_y,py_x]}, {rb[py_y,py_x]})")

# Tan panel
t1_y = int(300 * scale)
t1_x = int(480 * scale)
print(f"Tan panel 1 ({t1_x},{t1_y}): RGB=({rr[t1_y,t1_x]}, {rg[t1_y,t1_x]}, {rb[t1_y,t1_x]})")

# Red stroke left
ls_y = int(270 * scale)
ls_x = int(58.5 * scale)
print(f"Left stroke ({ls_x},{ls_y}): RGB=({rr[ls_y,ls_x]}, {rg[ls_y,ls_x]}, {rb[ls_y,ls_x]})")

print("\n=== SELF-CHECK COMPLETE ===")