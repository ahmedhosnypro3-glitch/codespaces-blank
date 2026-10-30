#!/usr/bin/env python3
"""More targeted PIL measurement of slide_033.jpg."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# Badge - look at top-right area specifically (876, 73) d~35
print("=== BADGE (top-right, expected cx~876, cy~73, d~35) ===")
# Crop top-right region
tr = im[30:110, 830:930]
tr_r, tr_g, tr_b = tr[:,:,0], tr[:,:,1], tr[:,:,2]
yel = (tr_r > 200) & (tr_g > 200) & (tr_b < 190)
ys, xs = np.where(yel)
if len(ys):
    print(f"  Yellow: cx={xs.mean()+830:.0f}, cy={ys.mean()+30:.0f}, w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1}")
pur = (tr_b > 150) & (tr_r > 70) & (tr_r < 180) & (tr_g < 130)
ps, pxs = np.where(pur)
if len(ps):
    print(f"  Purple: cx={pxs.mean()+830:.0f}, cy={ps.mean()+30:.0f}")

# Title area - top-left
print("\n=== TITLE AREA (top-left) ===")
# Red title "Non-Convex Function"
title_region = im[30:100, 50:500]
tr_r, tr_g, tr_b = title_region[:,:,0], title_region[:,:,1], title_region[:,:,2]
red = (tr_r > 200) & (tr_g < 80) & (tr_b < 80)
rr, rc = np.where(red)
if len(rr):
    print(f"  Red title: rows {rr.min()+30}-{rr.max()+30}, cols {rc.min()+50}-{rc.max()+50}")

# Blue subtitle
blue = (tr_b > 200) & (tr_r < 80) & (tr_g < 80)
br, bc = np.where(blue)
if len(br):
    print(f"  Blue subtitle: rows {br.min()+30}-{br.max()+30}, cols {bc.min()+50}-{bc.max()+50}")

# Parameter box - left middle (x 3%-18% = ~29-173, y 33%-50% = ~178-270)
print("\n=== PARAMETER BOX (left-middle) ===")
pb = im[170:280, 30:180]
pb_r, pb_g, pb_b = pb[:,:,0], pb[:,:,1], pb[:,:,2]
# Yellow accent
yel = (pb_r > 200) & (pb_g > 200) & (pb_b < 190)
ys, xs = np.where(yel)
if len(ys):
    print(f"  Yellow accent: rows {ys.min()+170}-{ys.max()+170}, cols {xs.min()+30}-{xs.max()+30}")
# Black text
black = (pb_r < 80) & (pb_g < 80) & (pb_b < 80)
bl_r, bl_c = np.where(black)
if len(bl_r):
    print(f"  Black text: rows {bl_r.min()+170}-{bl_r.max()+170}, cols {bl_c.min()+30}-{bl_c.max()+30}")

# Red block arrow from parameter box to table
print("\n=== RED ARROW (left-middle to bottom) ===")
# Arrow should be around x 180-300, y 200-350
arrow_region = im[200:360, 180:320]
ar_r, ar_g, ar_b = arrow_region[:,:,0], arrow_region[:,:,1], arrow_region[:,:,2]
red_arrow = (ar_r > 200) & (ar_g < 100) & (ar_b < 100)
ar_rr, ar_rc = np.where(red_arrow)
if len(ar_rr):
    print(f"  Red arrow: rows {ar_rr.min()+200}-{ar_rr.max()+200}, cols {ar_rc.min()+180}-{ar_rc.max()+180}")

# Formula area - center (x 38%-66% = ~365-634, y 32%-52% = ~173-281)
print("\n=== FORMULA AREA (center) ===")
formula = im[160:290, 350:650]
fr, fg, fb = formula[:,:,0], formula[:,:,1], formula[:,:,2]
# Black text
black = (fr < 80) & (fg < 80) & (fb < 80)
fbr, fbc = np.where(black)
if len(fbr):
    print(f"  Black text: rows {fbr.min()+160}-{fbr.max()+160}, cols {fbc.min()+350}-{fbc.max()+350}")
# Red text in annotation
red = (fr > 200) & (fg < 80) & (fb < 80)
frr, frc = np.where(red)
if len(frr):
    print(f"  Red text: rows {frr.min()+160}-{frr.max()+160}, cols {frc.min()+350}-{frc.max()+350}")

# Function plot - right (x 64%-97% = ~615-931, y 24%-60% = ~130-324)
print("\n=== FUNCTION PLOT (right) ===")
plot = im[120:330, 600:940]
pr, pg, pb = plot[:,:,0], plot[:,:,1], plot[:,:,2]
# Green curve
green = (pg > 120) & (pr < 100) & (pb < 100)
gr, gc = np.where(green)
if len(gr):
    print(f"  Green curve: rows {gr.min()+120}-{gr.max()+120}, cols {gc.min()+600}-{gc.max()+600}")
# Red initial point
red_pt = (pr > 200) & (pg < 100) & (pb < 100)
rpr, rpc = np.where(red_pt)
if len(rpr):
    print(f"  Red point: rows {rpr.min()+120}-{rpr.max()+120}, cols {rpc.min()+600}-{rpc.max()+600}")
# Orange arrow
orange = (pr > 180) & (pg > 100) & (pg < 160) & (pb < 80)
or_r, or_c = np.where(orange)
if len(or_r):
    print(f"  Orange arrow: rows {or_r.min()+120}-{or_r.max()+120}, cols {or_c.min()+600}-{or_c.max()+600}")
# Purple callout
purple = (pr > 80) & (pr < 150) & (pg < 80) & (pb > 120)
pur_r, pur_c = np.where(purple)
if len(pur_r):
    print(f"  Purple callout: rows {pur_r.min()+120}-{pur_r.max()+120}, cols {pur_c.min()+600}-{pur_c.max()+600}")

# Axes - black lines in plot area
black = (pr < 60) & (pg < 60) & (pb < 60)
bpr, bpc = np.where(black)
if len(bpr):
    print(f"  Black (axes/labels): rows {bpr.min()+120}-{bpr.max()+120}, cols {bpc.min()+600}-{bpc.max()+600}")

# Gridlines
grid = (np.abs(pr - 217) < 20) & (np.abs(pg - 217) < 20) & (np.abs(pb - 217) < 20)
gd_r, gd_c = np.where(grid)
if len(gd_r):
    print(f"  Gridlines: rows {gd_r.min()+120}-{gd_r.max()+120}, cols {gd_c.min()+600}-{gd_c.max()+600}")

# Table area - bottom (x 2%-98% = ~19-941, y 62%-95% = ~335-513)
print("\n=== TABLE AREA (bottom) ===")
table = im[330:520, 20:940]
tr, tg, tb = table[:,:,0], table[:,:,1], table[:,:,2]

# Find horizontal grid lines (rows with many transitions)
print("  Horizontal grid lines (high transition rows):")
for row in range(190):  # 0-189 in table coords = 330-519 absolute
    changes = 0
    for c in range(200, 900):
        if c+1 < 920:
            dr = abs(int(tr[row,c]) - int(tr[row,c+1]))
            dg = abs(int(tg[row,c]) - int(tg[row,c+1]))
            db = abs(int(tb[row,c]) - int(tb[row,c+1]))
            if dr > 25 or dg > 25 or db > 25:
                changes += 1
    if changes > 50:
        print(f"    Row {row+330}: {changes} transitions")

# Find vertical grid lines
print("  Vertical grid lines (high transition cols):")
for col in range(100, 920, 5):
    changes = 0
    for row in range(190):
        if row+1 < 190:
            dr = abs(int(tr[row,col]) - int(tr[row+1,col]))
            dg = abs(int(tg[row,col]) - int(tg[row+1,col]))
            db = abs(int(tb[row,col]) - int(tb[row+1,col]))
            if dr > 25 or dg > 25 or db > 25:
                changes += 1
    if changes > 20:
        print(f"    Col {col+20}: {changes} transitions")

# Row band colors - look at specific columns in label area (first ~80px)
print("\n  Row band colors (label column, x=30-100):")
for row in range(330, 520):
    colors = [(r[row,c], g[row,c], b[row,c]) for c in range(30, 100)]
    uniq = len(set(colors))
    if uniq < 5:
        dom = max(set(colors), key=colors.count)
        print(f"    Row {row}: {dom}")

# Sample some cells to understand table structure
print("\n  Table cell sampling (data area x=120-900):")
# Look at a few rows for data
for row in [340, 360, 380, 400, 420, 440, 460, 480, 500]:
    # Sample at regular intervals
    for col in range(150, 860, 60):
        print(f"    ({row},{col}): ({r[row,col]},{g[row,col]},{b[row,col]})")
    print()

# Check for yellow highlighted columns
print("\n  Yellow highlight detection in table:")
yel_table = (tr > 200) & (tg > 200) & (tb < 100)
yt, yc = np.where(yel_table)
if len(yt):
    print(f"  Yellow in table: rows {yt.min()+330}-{yt.max()+330}, cols {yc.min()+20}-{yc.max()+20}")

# Red bold cells in table
print("\n  Red bold cells in table:")
red_table = (tr > 200) & (tg < 80) & (tb < 80)
rt, rc = np.where(red_table)
if len(rt):
    print(f"  Red in table: rows {rt.min()+330}-{rt.max()+330}, cols {rc.min()+20}-{rc.max()+20}")