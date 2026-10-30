#!/usr/bin/env python3
"""Focused plot-region measurement of slide_033.jpg."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Plot region x 615-930, y 120-330
print("=== PLOT REGION ANALYSIS (x 615-930, y 120-330) ===")

# 1. Full green curve extent with a broader green mask
green = (g > 100) & (g - r > 25) & (g - b > 25)
gr, gc = np.where(green[120:330, 615:930])
print(f"Green curve (broad mask): rows {gr.min()+120}-{gr.max()+120}, cols {gc.min()+615}-{gc.max()+615}")

# 2. Green marker (square) - look for saturated green square
strong_green = (g > 140) & (r < 120) & (b < 120) & (g - r > 40)
sgr, sgc = np.where(strong_green[120:330, 615:930])
if len(sgr):
    print(f"Strong green: rows {sgr.min()+120}-{sgr.max()+120}, cols {sgc.min()+615}-{sgc.max()+615}")

# 3. Red point (initial) - broad red
red_pt = (r > 150) & (r - g > 40) & (r - b > 40)
rpr, rpc = np.where(red_pt[120:330, 615:930])
if len(rpr):
    print(f"Red point: rows {rpr.min()+120}-{rpr.max()+120}, cols {rpc.min()+615}-{rpc.max()+615}")

# 4. Orange arrow
orange = (r > 150) & (g > 70) & (g < 170) & (b < 120) & (r - b > 40) & (r - g > 20)
oar, oac = np.where(orange[120:330, 615:930])
if len(oar):
    print(f"Orange arrow: rows {oar.min()+120}-{oar.max()+120}, cols {oac.min()+615}-{oac.max()+615}")

# 5. Purple callout (rounded rect)
purple = (r > 70) & (b > 140) & (b - r > 40) & (g < 120)
pur, puc = np.where(purple[120:330, 615:930])
if len(pur):
    print(f"Purple callout: rows {pur.min()+120}-{pur.max()+120}, cols {puc.min()+615}-{puc.max()+615}")

# 6. Axes - black lines: scan for long horizontal/vertical black runs
black = (r < 80) & (g < 80) & (b < 80)
print("\n--- AXES ---")
# Long horizontal black runs (x-axis)
for row in range(120, 330):
    run = black[row, 615:930].sum()
    if run > 80:
        cols = np.where(black[row, 615:930])[0]
        print(f"  horizontal black at row {row}: len~{run}px, cols {cols.min()+615}-{cols.max()+615}")

# Long vertical black runs (y-axis)
for col in range(615, 930, 5):
    run = black[120:330, col].sum()
    if run > 80:
        rows_ = np.where(black[120:330, col])[0]
        print(f"  vertical black at col {col}: len~{run}px, rows {rows_.min()+120}-{rows_.max()+120}")

# 7. Gridlines - light gray lines
print("\n--- GRIDLINES ---")
gray_grid = (np.abs(r - 217) < 30) & (np.abs(g - 217) < 30) & (np.abs(b - 217) < 30) & (np.abs(r-g)<10) & (np.abs(g-b)<10)
# horizontal gridlines
for row in range(120, 330):
    run = gray_grid[row, 615:930].sum()
    if run > 100:
        cols = np.where(gray_grid[row, 615:930])[0]
        print(f"  horizontal grid at row {row}: len~{run}px, cols {cols.min()+615}-{cols.max()+615}")
for col in range(615, 930, 5):
    run = gray_grid[120:330, col].sum()
    if run > 100:
        rows_ = np.where(gray_grid[120:330, col])[0]
        print(f"  vertical grid at col {col}: len~{run}px, rows {rows_.min()+120}-{rows_.max()+120}")

# 8. Axis tick labels - black text OUTSIDE plot region (left/below axes)
print("\n--- TICK LABELS (text near axes) ---")
# Below x-axis: rows 295-320, cols 610-930
for row in range(290, 325):
    cols_txt = np.where(black[row, 610:930])[0]
    if len(cols_txt) > 2:
        print(f"  row {row}: black text cols {cols_txt.min()+610}-{cols_txt.max()+610} ({len(cols_txt)}px)")
# Left of y-axis: cols 570-615, rows 130-320
for row in range(130, 320):
    cols_txt = np.where(black[row, 565:615])[0]
    if len(cols_txt) > 2:
        print(f"  row {row}: black label cols {cols_txt.min()+565}-{cols_txt.max()+565} ({len(cols_txt)}px)")

# 9. Sub-region sampling to find ax labels
print("\n--- X-axis label 'x' (below-right of axis) ---")
region = im[298:322, 880:932]
reg_r, reg_g, reg_b = region[:,:,0], region[:,:,1], region[:,:,2]
blk = (reg_r < 80) & (reg_g < 80) & (reg_b < 80)
ir, ic = np.where(blk)
if len(ir):
    print(f"  'x' label: rows {ir.min()+298}-{ir.max()+298}, cols {ic.min()+880}-{ic.max()+880}")

print("\n--- Y-axis label 'y' (above-left of axis) ---")
region = im[115:135, 570:615]
reg_r, reg_g, reg_b = region[:,:,0], region[:,:,1], region[:,:,2]
blk = (reg_r < 80) & (reg_g < 80) & (reg_b < 80)
ir, ic = np.where(blk)
if len(ir):
    print(f"  'y' label: rows {ir.min()+115}-{ir.max()+115}, cols {ic.min()+570}-{ic.max()+570}")

# 10. Table area: measure precise table grid with lower threshold & skip label col
print("\n=== TABLE GRID (precise) ===")
# Table x 20-940, y 330-520. Find strong gridlines.
# Horizontal gridlines: rows with >30% long runs of dark-ish line
for row in range(330, 521):
    darkish = np.abs(r[row, 20:940] - g[row, 20:940]) < 12
    # find rows that look like uniform line color (not cell fills)
    # check for short horizontal runs of uniform nonfill color
    pass

# Better: look at the exact transition structure using column 200-800
# Detect cell fill bands by row
prev = None
start = None
for row in range(330, 521):
    # sample color from col 200 (data area) at row+/- 2 avg
    c = (int(r[row, 300]), int(g[row, 300]), int(b[row, 300]))
    if c != prev:
        if prev is not None and start is not None:
            if row - start > 2:
                print(f"  row {start}-{row-1}: fill {prev}")
        prev = c
        start = row
if start is not None:
    print(f"  row {start}-520: fill {prev}")

# Check column boundaries via scanning a data row (e.g. row 350 = first data row)
print("\n--- Column boundaries from data row 350 ---")
for col in range(20, 940):
    c1 = (int(r[350, col]), int(g[350, col]), int(b[350, col]))
    c2 = (int(r[350, col+1]), int(g[350, col+1]), int(b[350, col+1])) if col+1 < 940 else c1
    if abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2]) > 30:
        print(f"  col {col}: {c1} -> {c2}")
