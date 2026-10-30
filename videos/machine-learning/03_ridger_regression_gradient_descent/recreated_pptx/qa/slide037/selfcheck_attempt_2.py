#!/usr/bin/env python3
"""Self-check for slide 037 attempt 2."""
import numpy as np
from PIL import Image

render = Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037/render_2.png").convert("RGB")
original = Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_037.jpg").convert("RGB")

r_arr = np.asarray(render).astype(int)
o_arr = np.asarray(original).astype(int)

H_r, W_r = r_arr.shape[:2]
H_o, W_o = o_arr.shape[:2]
scale = H_r / H_o

print(f"Render: {W_r}x{H_r}, Original: {W_o}x{H_o}, Scale: {scale:.3f}")

rr, rg, rb = r_arr[:, :, 0], r_arr[:, :, 1], r_arr[:, :, 2]

# ===== 1. TITLE COLOR CHECK =====
title_x = int(479.5 * scale)
title_y = int(74 * scale)
print(f"\n=== TITLE CHECK ===")
print(f"Title center ({title_x},{title_y}): RGB=({rr[title_y,title_x]}, {rg[title_y,title_x]}, {rb[title_y,title_x]})")
# Should be dark red ~(192, 0, 0)
if rr[title_y,title_x] > 150 and rg[title_y,title_x] < 50 and rb[title_y,title_x] < 50:
    print("  PASS: Title is dark red")
else:
    print("  FAIL: Title color wrong")

# ===== 2. EQUATIONS EXIST =====
print("\n=== EQUATIONS EXIST ===")
# Error equation region: original rows 264-287
eq1_top = int(264 * scale)
eq1_bot = int(287 * scale)
eq1_left = int(82 * scale)
eq1_right = int(868 * scale)
region = r_arr[eq1_top:eq1_bot, eq1_left:eq1_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240))
print(f"Error equation region: {'HAS INK' if ink.any() else 'EMPTY'} ({ink.sum()} px)")

# First update equation region: original rows 404-449
eq2_top = int(404 * scale)
eq2_bot = int(449 * scale)
eq2_left = int(84 * scale)
eq2_right = int(715 * scale)
region = r_arr[eq2_top:eq2_bot, eq2_left:eq2_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220))
print(f"First update equation region: {'HAS INK' if ink.any() else 'EMPTY'} ({ink.sum()} px)")

# Second update equation region: original rows 473-513
eq3_top = int(473 * scale)
eq3_bot = int(513 * scale)
eq3_left = int(85 * scale)
eq3_right = int(405 * scale)
region = r_arr[eq3_top:eq3_bot, eq3_left:eq3_right]
ink = ~((region[:,:,0] > 240) & (region[:,:,1] > 240) & (region[:,:,2] > 240)) & \
      ~((region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220))
print(f"Second update equation region: {'HAS INK' if ink.any() else 'EMPTY'} ({ink.sum()} px)")

# ===== 3. GREEN HIGHLIGHTS =====
print("\n=== GREEN HIGHLIGHTS ===")
# Highlight 1 area: around first eq left part
h1_top = int(417 * scale)
h1_bot = int(430 * scale)
h1_left = int(724 * scale)
h1_right = int(752 * scale)
region = r_arr[h1_top:h1_bot, h1_left:h1_right]
green = (region[:,:,0] < 100) & (region[:,:,1] > 200) & (region[:,:,2] < 100)  # dark green border
green_fill = (region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220)  # light green fill
print(f"Highlight 1: border px={green.sum()}, fill px={green_fill.sum()}")

# Highlight 2 area
h2_top = int(480 * scale)
h2_bot = int(493 * scale)
h2_left = int(432 * scale)
h2_right = int(460 * scale)
region = r_arr[h2_top:h2_bot, h2_left:h2_right]
green = (region[:,:,0] < 100) & (region[:,:,1] > 200) & (region[:,:,2] < 100)
green_fill = (region[:,:,0] > 220) & (region[:,:,1] > 235) & (region[:,:,2] > 220)
print(f"Highlight 2: border px={green.sum()}, fill px={green_fill.sum()}")

# ===== 4. ARROW =====
print("\n=== ARROW ===")
arr_top = int(430 * scale)
arr_bot = int(470 * scale)
arr_left = int(740 * scale)
arr_right = int(780 * scale)
region = r_arr[arr_top:arr_bot, arr_left:arr_right]
green = (region[:,:,0] < 100) & (region[:,:,1] > 100) & (region[:,:,2] < 100)
print(f"Arrow region: green px={green.sum()}")

# ===== 5. PANEL COLORS =====
print("\n=== PANEL COLORS ===")
# Pale yellow panel center
py_x = int(480 * scale)
py_y = int(150 * scale)
print(f"Pale yellow ({py_x},{py_y}): RGB=({rr[py_y,py_x]}, {rg[py_y,py_x]}, {rb[py_y,py_x]})")

# Tan panel 1
t1_x = int(480 * scale)
t1_y = int(300 * scale)
print(f"Tan panel 1 ({t1_x},{t1_y}): RGB=({rr[t1_y,t1_x]}, {rg[t1_y,t1_x]}, {rb[t1_y,t1_x]})")

# Tan panel 2
t2_x = int(480 * scale)
t2_y = int(450 * scale)
print(f"Tan panel 2 ({t2_x},{t2_y}): RGB=({rr[t2_y,t2_x]}, {rg[t2_y,t2_x]}, {rb[t2_y,t2_x]})")

# ===== 6. FRAME CONTAINMENT (rough) =====
print("\n=== FRAME CONTAINMENT (rough) ===")
# Check text doesn't hit house frame strokes
# Left stroke at x=58.5 -> render ~122
# Right stroke at x=901 -> render ~1876
# Bottom stroke at y=538.5 -> render ~1122

# Sample near left stroke
left_stroke_x = int(58.5 * scale)
mid_y = int(270 * scale)
print(f"Near left stroke ({left_stroke_x},{mid_y}): RGB=({rr[mid_y,left_stroke_x]}, {rg[mid_y,left_stroke_x]}, {rb[mid_y,left_stroke_x]})")

# Sample near right stroke
right_stroke_x = int(901 * scale)
print(f"Near right stroke ({right_stroke_x},{mid_y}): RGB=({rr[mid_y,right_stroke_x]}, {rg[mid_y,right_stroke_x]}, {rb[mid_y,right_stroke_x]})")

# Sample near bottom stroke
bot_stroke_y = int(538.5 * scale)
mid_x = int(480 * scale)
print(f"Near bottom stroke ({mid_x},{bot_stroke_y}): RGB=({rr[bot_stroke_y,mid_x]}, {rg[bot_stroke_y,mid_x]}, {rb[bot_stroke_y,mid_x]})")

print("\n=== SELF-CHECK COMPLETE ===")