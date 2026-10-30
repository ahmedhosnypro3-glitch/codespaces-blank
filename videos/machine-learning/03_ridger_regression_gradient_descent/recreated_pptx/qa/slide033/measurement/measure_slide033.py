#!/usr/bin/env python3
"""Detailed PIL measurement of slide_033.jpg for precise recreation."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]  # 540, 960
print(f"Frame: {W}x{H}")

r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
gray = (np.abs(r - 233) < 16) & (np.abs(g - 233) < 16) & (np.abs(b - 231) < 18)
print(f"Gray panel extent - cols: {np.where(gray.any(axis=0))[0][[0,-1]]}, rows: {np.where(gray.any(axis=1))[0][[0,-1]]}")

# Find red strokes
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
print(f"Red stroke rows: {np.where(red.any(axis=1))[0][[0,-1]]}")
print(f"Red stroke cols: {np.where(red.any(axis=0))[0][[0,-1]]}")

# Badge - yellow disc
yel = (r > 200) & (g > 200) & (b < 190)
ys, xs = np.where(yel)
if len(ys):
    print(f"Yellow badge - cx: {(xs.min()+xs.max())/2:.0f}, cy: {(ys.min()+ys.max())/2:.0f}, d: {xs.max()-xs.min()+1}")

# Purple ring
pur = (b > 150) & (r > 70) & (r < 180) & (g < 130)
ps, pxs = np.where(pur)
if len(ps):
    print(f"Purple ring - cx: {(pxs.min()+pxs.max())/2:.0f}, cy: {(ps.min()+ps.max())/2:.0f}")

# Title area - red text (FF0000 area)
title_red = (r > 200) & (g < 60) & (b < 60)
tr, tc = np.where(title_red)
if len(tr):
    print(f"Title red - rows: {tr.min()}-{tr.max()}, cols: {tc.min()}-{tc.max()}")

# Subtitle blue text
title_blue = (b > 200) & (r < 60) & (g < 60)
tb_r, tb_c = np.where(title_blue)
if len(tb_r):
    print(f"Subtitle blue - rows: {tb_r.min()}-{tb_r.max()}, cols: {tb_c.min()}-{tb_c.max()}")

# Scan for table gridlines (alternating row bands)
# Look for horizontal lines
for row in range(300, 500, 10):
    line_colors = set()
    for c in range(100, 900):
        line_colors.add((r[row,c], g[row,c], b[row,c]))
    if len(line_colors) < 10:
        print(f"Row {row}: uniform-ish, colors={list(line_colors)[:5]}")

# Find table grid lines - look for rows with many color changes
print("\n--- Table row detection (color transitions) ---")
for row in range(320, 530):
    changes = 0
    for c in range(100, 860):
        if abs(int(r[row,c]) - int(r[row,c+1])) > 20 or abs(int(g[row,c]) - int(g[row,c+1])) > 20 or abs(int(b[row,c]) - int(b[row,c+1])) > 20:
            changes += 1
    if changes > 20:
        print(f"Row {row}: {changes} transitions")

# Detect vertical grid lines
print("\n--- Vertical grid lines ---")
for col in range(100, 900, 5):
    changes = 0
    for row in range(320, 530):
        if abs(int(r[row,col]) - int(r[row+1,col])) > 20 or abs(int(g[row,col]) - int(g[row+1,col])) > 20 or abs(int(b[row,col]) - int(b[row+1,col])) > 20:
            changes += 1
    if changes > 5:
        print(f"Col {col}: {changes} vertical transitions")

# Function plot area - green curve
print("\n--- Function plot (green curve) ---")
green = (g > 120) & (r < 100) & (b < 100)
gr, gc = np.where(green)
if len(gr):
    print(f"Green curve - rows: {gr.min()}-{gr.max()}, cols: {gc.min()}-{gc.max()}")

# Red initial point
red_pt = (r > 200) & (g < 100) & (b < 100)
rp_r, rp_c = np.where(red_pt)
if len(rp_r):
    print(f"Red point - rows: {rp_r.min()}-{rp_r.max()}, cols: {rp_c.min()}-{rp_c.max()}")

# Orange arrow
orange = (r > 180) & (g > 100) & (g < 160) & (b < 80)
or_r, or_c = np.where(orange)
if len(or_r):
    print(f"Orange arrow - rows: {or_r.min()}-{or_r.max()}, cols: {or_c.min()}-{or_c.max()}")

# Purple callout
purple = (r > 80) & (r < 150) & (g < 80) & (b > 120)
pr_r, pr_c = np.where(purple)
if len(pr_r):
    print(f"Purple callout - rows: {pr_r.min()}-{pr_r.max()}, cols: {pr_c.min()}-{pr_c.max()}")

# Axes - black lines
black = (r < 60) & (g < 60) & (b < 60)
bl_r, bl_c = np.where(black)
if len(bl_r):
    print(f"Black (axes/text) - rows: {bl_r.min()}-{bl_r.max()}, cols: {bl_c.min()}-{bl_c.max()}")

# Gridlines light gray D9D9D9
grid = (np.abs(r - 217) < 20) & (np.abs(g - 217) < 20) & (np.abs(b - 217) < 20)
gd_r, gd_c = np.where(grid)
if len(gd_r):
    print(f"Gridlines - rows: {gd_r.min()}-{gd_r.max()}, cols: {gd_c.min()}-{gd_c.max()}")

# Parameter box area
print("\n--- Parameter box (left-middle) ---")
# Look for yellow accent in left area
yel_left = yel[:, :300]
yl, xl = np.where(yel_left)
if len(yl):
    print(f"Yellow in left - rows: {yl.min()}-{yl.max()}, cols: {xl.min()}-{xl.max()}")

# Formula area (center)
print("\n--- Formula area (center) ---")
# Black text in center region
center_black = black[:, 300:700]
cb_r, cb_c = np.where(center_black)
if len(cb_r):
    print(f"Center black - rows: {cb_r.min()}-{cb_r.max()}, cols: {cb_c.min()+300}-{cb_c.max()+300}")

# Print ASCII map of table area
print("\n--- Table area ASCII (rows 320-530, cols 100-860) ---")
for row in range(320, 530, 20):
    line = ""
    for col in range(100, 860, 30):
        line += f"({r[row,col]:3d},{g[row,col]:3d},{b[row,col]:3d}) "
    print(f"Row {row}: {line[:120]}...")

print("\n--- Detailed table row bands (sample cols 150-200) ---")
for row in range(320, 530):
    colors = [(r[row,c], g[row,c], b[row,c]) for c in range(150, 200)]
    uniq = len(set(colors))
    if uniq < 5:
        dom = max(set(colors), key=colors.count)
        print(f"Row {row}: {uniq} colors, dominant {dom}")