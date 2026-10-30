#!/usr/bin/env python3
"""Worker-6 clean re-measurement of slide 028 (all numbers in frame px 960x540, 1px=1pt).
Prior worker's measure_original*.py are LEADS; this re-derives each item independently.
Outputs a geometry model for build/slide_028.js."""
import numpy as np
from PIL import Image

IMG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
IM = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, 0], IM[:, 2] if False else IM[:, 1], IM[:, 2]
# fix channel naming
R, G, B = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# ---- masks ----
# curve/dot blue ~ (46,117,182); tolerant
blue = (B - R > 28) & (B > 110) & (B > G)
# dark-blue frame 1F4E79 ~ (31,78,121): darker blue, low green
dblue = (B - R > 30) & (B > 70) & (B < 210) & (G < 120) & (R < 90)
# content red (title + axes) ~ FF0000 but JPEG-darkened; exclude house strokes (x<62 or x>898 or y>536)
red = (R > 110) & (R - G > 45) & (R - B > 45)
red_content = red & (R - G > 45)
# pure dark text (black)
dark = (R < 120) & (G < 120) & (B < 120)

def bbox(mask, x0=0, x1=W, y0=0, y1=H):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(sub.sum()))

print("frame size", W, H)

# ---------- 1. FRAME BORDER (1F4E79) ----------
# the frame border vertical strokes are near-continuous tall columns
colsum = dblue.sum(axis=0)
rowsum = dblue.sum(axis=0) # placeholder
xs_cand = np.where(colsum > 40)[0]
ys_cand = np.where(dblue.sum(axis=1) > 40)[0]
if len(xs_cand) and len(ys_cand):
    print("FRAME dblue extent x", xs_cand.min(), xs_cand.max(), "y", ys_cand.min(), ys_cand.max())
# precise edges: left/right tall columns, top/bottom long rows
leftcols = np.where(colsum > 150)[0]
print("  frame tall-left cols:", leftcols[:5], "tall-right cols:", (np.where(colsum>150)[0][-5:] if len(np.where(colsum>150)[0]) else None))
# find the two dominant vertical lines (left & right frame edge)
strong_cols = np.where(colsum > 200)[0]
if len(strong_cols):
    # cluster
    print("  strong vertical cols (frame L/R edges & inner features):", strong_cols.min(), strong_cols.max())

# ---------- 2. TITLE (red content, top band y60..110, exclude badge x>855) ----------
tb = bbox(red_content, 0, 855, 60, 110)
print("TITLE red ink bbox (x0,y0,x1,y1,n):", tb)

# ---------- 3. HEADINGS (black y182..200) ----------
hb = bbox(dark, 0, W, 182, 201)
print("HEADINGS dark band y182-200 bbox:", hb)
# split left/right at gutter ~ 490
lh = bbox(dark, 200, 490, 182, 201)
rh = bbox(dark, 490, 760, 182, 201)
print("  LEFT heading:", lh, "  RIGHT heading:", rh)

# ---------- 4. PANEL SPLIT ----------
# gutter is around x ~ 485..545 (no blue there); find it
panelblue_cols = np.where(blue[:, :].sum(axis=0) > 2)[0]
# find a gap in blue columns between ~420..560
gaps = []
run = None
for x in range(430, 560):
    if blue[:, x].sum() < 1:
        if run is None: run = [x, x]
        else: run[1] = x
    else:
        if run is not None and run[1]-run[0] > 2:
            gaps.append(tuple(run))
        run = None
if run is not None and run[1]-run[0] > 2:
    gaps.append(tuple(run))
print("blue column gaps between x430-560 (panel gutter):", gaps)

# ---------- 5. CURVE TRACE per panel (naked-band + dots) ----------
def trace_panel(xlo, xhi, label):
    print(f"\n== CURVE TRACE {label}: x {xlo}..{xhi} ==")
    pts = []
    for x in range(xlo, xhi + 1):
        col = np.where(blue[:, x])[0]
        if len(col) == 0:
            continue
        # split into runs
        runs = []
        s = col[0]; p = col[0]
        for y in col[1:]:
            if y - p <= 1:
                p = y
            else:
                runs.append((s, p)); s = y; p = y
        runs.append((s, p))
        # report runs (y0,y1,h)
        for (a, c) in runs:
            h = c - a + 1
            yc = (a + c) / 2
            pts.append((x, yc, h))
    return pts

# Print compact per-column runs for both panels
for (xlo, xhi, lab) in [(150, 470, "LEFT"), (500, 745, "RIGHT")]:
    print(f"\n== {lab} PANEL blue runs per column (x: ymid/h for each run) ==")
    for x in range(xlo, xhi + 1, 3):
        col = np.where(blue[:, x])[0]
        if not len(col):
            continue
        runs = []; s = col[0]; p = col[0]
        for y in col[1:]:
            if y - p <= 1: p = y
            else: runs.append((s, p)); s = y; p = y
        runs.append((s, p))
        sstr = " ".join(f"[{round((a+c)/2,1)}:{c-a+1}]" for a, c in runs)
        print(f"  x={x}: {sstr}")

# ---------- 6. RED AXES per panel ----------
print("\n== RED AXES ==")
for (xlo, xhi, lab) in [(150, 470, "LEFT"), (500, 745, "RIGHT")]:
    redp = np.zeros_like(red); redp[:, xlo:xhi] = red[:, xlo:xhi]
    # vertical arrow: find column with tall red run (the shaft)
    colcnt = redp.sum(axis=0)
    shaftcols = np.where(colcnt > 80)[0]
    shaft_x = int(np.median(shaftcols)) if len(shaftcols) else None
    # vertical extent of the vertical stroke (rows near shaft_x)
    print(f"  {lab}: vertical red shaft cols:", shaftcols[:6], "..", shaftcols[-6:] if len(shaftcols) else None, "median", shaft_x)
    if shaft_x is not None:
        colpx = np.where(redp[:, shaft_x])[0]
        print(f"    shaft col {shaft_x} red rows: {colpx.min()}..{colpx.max()} (apex~{colpx.min()})")
        # arrowhead width near apex
        apex = colpx.min()
        for yy in range(apex, apex + 16):
            row = np.where(redp[yy, xlo:xhi])[0]
            xs = row + xlo if len(row) else []
            print(f"      apex y={yy}: x {int(xs.min())}..{int(xs.max())} n={len(row)}" if len(xs) else f"      apex y={yy}: -")
    # horizontal arrow: find row with long red run
    rowcnt = redp.sum(axis=1)
    shaftrows = np.where(rowcnt > 60)[0]
    print(f"  {lab}: horizontal red rows(>60px):", list(shaftrows))
    if len(shaftrows):
        shaft_y = int(np.median(shaftrows))
        rowpx = np.where(redp[shaft_y, xlo:xhi])[0] + xlo
        print(f"    shaft row ~{shaft_y}: red cols {rowpx.min()}..{rowpx.max()}")
        # the arrow tip = rightmost; arrowhead shape near tip
        tip = int(rowpx.max())
        for xx in range(tip - 14, tip + 2):
            colpx2 = np.where(redp[:, xx])[0]
            print(f"      tip x={xx}: y {colpx2.min()}..{colpx2.max()} n={len(colpx2)}" if len(colpx2) else f"      tip x={xx}: -")

# ---------- 7. AXIS LABELS ----------
print("\n== AXIS LABELS (dark text) ==")
# 'Loss' vertical labels: left ~ y220-232, right ~ y216-229
l_loss = bbox(dark, 110, 150, 215, 235)
r_loss = bbox(dark, 465, 505, 210, 232)
print("  left Loss:", l_loss, "  right Loss:", r_loss)
# 'Value of weight' bottom ~ y446-460
l_vow = bbox(dark, 250, 465, 444, 463)
r_vow = bbox(dark, 700, 810, 444, 463)
print("  left ValueOfWeight:", l_vow, "  right ValueOfWeight:", r_vow)

# ---------- 8. VALLEY ARROW (dark, left panel near valley x240..300 y410..445) ----------
print("\n== VALLEY ARROW region (left panel center-bottom) ==")
va = dark[405:445, 235:305]
ys, xs = np.where(va)
if len(xs):
    print("  dark ink bbox x", 235+xs.min(), "..", 235+xs.max(), "y", 405+ys.min(), "..", 405+ys.max(), "n", len(xs))
    # per-row detail
    for yy in range(405, 445):
        row = np.where(dark[yy, 235:310])[0] + 235
        if len(row):
            print(f"    y={yy}: x {row.min()}..{row.max()} n={len(row)}")

# ---------- 9. CURVE COLOR + AXIS COLOR sampling ----------
print("\n== COLOR SAMPLES ==")
# sample a curve point (right arm naked, left panel ~ x340 y330) and a dot
for (x, y, what) in [(344, 320, "left curve sample"), (600, 410, "right curve/valley sample"),
                     (592, 396, "right big dot core"), (166, 238, "left small dot core"),
                     (159, 350, "left y-axis shaft"), (400, 442, "left x-axis shaft"),
                     (91, 300, "frame left edge"), (480, 260, "canvas/panel mid")]:
    print(f"  {what} @({x},{y}): {tuple(IM[y, x])}")
