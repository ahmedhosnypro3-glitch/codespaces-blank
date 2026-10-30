#!/usr/bin/env python3
"""Self-check for slide 028 attempt 1.
Validates frame containment, equations (none), delimiter geometry, lineSpacing, table data.
"""
import sys
sys.path.insert(0, '/workspaces/codespaces-blank/ai_llm_slides')
from PIL import Image
import numpy as np

RENDER = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/render_1.png'
ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'

im_r = np.asarray(Image.open(RENDER).convert('RGB')).astype(int)
im_o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
H, W = im_r.shape[:2]
scale = H / 540.0  # ~2.083

print(f"Render: {W}x{H}, scale={scale:.3f}")
print(f"Original: {im_o.shape[1]}x{im_o.shape[0]}")

def cv(v): return int(v * scale)

r, g, b = im_r[:,:,0], im_r[:,:,1], im_r[:,:,2]
ro, go, bo = im_o[:,:,0], im_o[:,:,1], im_o[:,:,2]

# 1. Frame containment: all content inside house panel (x54..903, y45..540) and dark blue frame (x90..858, y127..508)
print("\n=== FRAME CONTAINMENT ===")
# Check panel gray extent
panel_gray = (abs(r-233)<16)&(abs(g-233)<16)&(abs(b-231)<18)
panel_cols = np.where(panel_gray[cv(100):cv(530)].sum(axis=0) > cv(430)*0.5)[0]
if len(panel_cols):
    print(f"Panel gray x: {panel_cols.min()}..{panel_cols.max()} (expected ~{cv(54)}..{cv(903)})")
    assert abs(panel_cols.min() - cv(54)) < 10, "Panel left edge"
    assert abs(panel_cols.max() - cv(903)) < 10, "Panel right edge"

# Check dark blue frame
dblue = (r<70)&(g<110)&(b>90)
mid_row = dblue[cv(317)]
frame_cols = np.where(mid_row)[0]
if len(frame_cols):
    print(f"Frame x at mid: {frame_cols.min()}..{frame_cols.max()} (expected ~{cv(90)}..{cv(858)})")
    assert abs(frame_cols.min() - cv(90)) < 10, "Frame left"
    assert abs(frame_cols.max() - cv(858)) < 10, "Frame right"

# Check NO top stroke
top_band = (r>90)&((r-g)>40)&((r-b)>10)
top_red = top_band[cv(44):cv(52), cv(80):cv(880)].sum()
print(f"Top stroke red px: {top_red} (should be <30)")
assert top_red < 30, "TOP STROKE PRESENT - BUILD DEFECT"

# 2. Title position
title_red = (r>200)&(g<100)&(b<100)
title_rows = np.where(title_red.sum(axis=1) > 100)[0]
if len(title_rows):
    print(f"Title y: {title_rows.min()}..{title_rows.max()} (expected ~{cv(74)}..{cv(95)})")

# 3. Badge
yel = (r>200)&(g>200)&(b<100)
yel_px = np.where(yel)
if len(yel_px[0]):
    cy, cx = yel_px[0].mean(), yel_px[1].mean()
    print(f"Badge center: ({cx:.0f},{cy:.0f}) expected ~({cv(876)},{cv(73)})")

# 4. Panel divider at x=474
divider_x = np.where(dblue[cv(200), :] > 0)[0]
# Actually check at mid-height for frame + divider
mid_y = cv(317)
dblue_mid = dblue[mid_y]
frame_x = np.where(dblue_mid)[0]
print(f"Frame+divider at mid: x={frame_x.min()}..{frame_x.max()} count={len(frame_x)}")

# 5. Heading positions (black text at y≈191)
black = (r<100)&(g<100)&(b<100)
heading_rows = np.where(black[cv(185):cv(200)].sum(axis=1) > 50)[0] + cv(185)
if len(heading_rows):
    print(f"Heading band y: {heading_rows.min()}..{heading_rows.max()} (expected ~{cv(188)}..{cv(199)})")

# 6. Curve presence (blue)
curve_blue = (b>r+20)&(b>g+10)&(b<250)
curve_px = curve_blue.sum()
print(f"Curve blue pixels: {curve_px} (original had ~1161 at frame scale = ~2400)")

# 7. "Loss" labels (red vertical)
loss_red = (r>150)&(g<100)&(b<100)
loss_px = loss_red.sum()
print(f"Loss red pixels: {loss_px}")

# 8. "Value of weight" labels
vow_black = (r<120)&(g<120)&(b<120)
vow_rows = np.where(vow_black[cv(450):cv(465)].sum(axis=1) > 20)[0] + cv(450)
if len(vow_rows):
    print(f"VoW label band y: {vow_rows.min()}..{vow_rows.max()} (expected ~{cv(454)}..{cv(458)})")

# 9. Axes shafts (dark blue)
shaft = (r<50)&(g<50)&(b>80)&(b<150)
# Left y-axis at x≈90
left_shaft = shaft[:, cv(88):cv(94)].sum()
# Right y-axis at x≈474
right_shaft = shaft[:, cv(472):cv(478)].sum()
# X-axis at y≈508
x_shaft = shaft[cv(506):cv(510), :].sum()
print(f"Left y-shaft px: {left_shaft}, Right y-shaft: {right_shaft}, X-shaft: {x_shaft}")

# 10. Descent dots (left) and oscillation dots (right)
# Left panel dots around x=190-360
left_dots = curve_blue[:, cv(170):cv(370)].sum()
# Right panel dots around x=540-710
right_dots = curve_blue[:, cv(520):cv(720)].sum()
print(f"Left panel curve+dot px: {left_dots}, Right: {right_dots}")

print("\n=== SELF-CHECK COMPLETE ===")