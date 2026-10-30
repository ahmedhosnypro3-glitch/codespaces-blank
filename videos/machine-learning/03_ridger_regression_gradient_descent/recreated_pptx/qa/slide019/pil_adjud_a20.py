#!/usr/bin/env python3
"""PIL verify of attempt-20 fixes, frame space (960x540).
render_20.png (2001x1125, 150dpi) vs unique_slides/slide_019.jpg.
Targets: arrow reposition, label color/center, value-col rules v0+colW/v0+2colW
(no label|value vline), maroon gridlines, norm-text blue, red L1 y170 x383..640,
outlier digit colors (row2 blue, row3 red).
"""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_20.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"

ri = Image.open(R).convert("RGB")
oi = Image.open(O).convert("RGB")
ra = np.asarray(ri).astype(int)
oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0

def crop_frame(a, x0, y0, x1, y1, scale):
    return a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]

def blue_mask(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (b > 120) & (b - r > 50) & (b - g > 40)

def dark_mask(c):
    return c.sum(axis=2) < 260

def red_mask(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (r > 110) & (r - g > 55) & (r - b > 55)

def bbox(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (xs.min(), ys.min(), xs.max(), ys.max(), len(xs))

COLS = [124, 384, 644]
GYS = [205, 310, 420]

print("=== 1. ARROW blue ink vs table border (label window x cx+70..cx+125) ===")
for cx in COLS:
    for gy in GYS:
        for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
            c = crop_frame(a, cx + 70, gy + 28, cx + 125, gy + 68, s)
            bb = bbox(blue_mask(c))
            if bb:
                print(f"  col{cx} gy{gy} {nm}: blue ink x {cx+70+bb[0]/s:.1f}..{cx+70+bb[2]/s:.1f}"
                      f" y {gy+28+bb[1]/s:.1f}..{gy+28+bb[3]/s:.1f} n={bb[4]}")
            else:
                print(f"  col{cx} gy{gy} {nm}: NO blue ink")

print("=== 2. TABLE LEFT BORDER x (long vertical dark run) ===")
for cx in COLS:
    for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
        c = crop_frame(a, cx + 75, 210, cx + 130, 295, s)
        dm = dark_mask(c)
        colsum = dm.sum(axis=0)
        cands = np.nonzero(colsum > (80 * s) * 0.5)[0]
        if len(cands):
            print(f"  col{cx} {nm}: vertical candidates x "
                  f"{[round(cx+75+v/s,1) for v in cands[:8]]}")
        else:
            print(f"  col{cx} {nm}: none")

print("=== 3. x1/x2/y LABELS: color census + ink extent (window x cx+90..cx+150, y gy+28..gy+55) ===")
for cx in COLS:
    for gy in GYS[:1]:
        for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
            c = crop_frame(a, cx + 90, gy + 28, cx + 150, gy + 55, s)
            ink = c.sum(axis=2) < 420
            r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
            blu = ink & (b_ - r_ > 40)
            red = ink & (r_ - b_ > 40) & (r_ - g_ > 40)
            blk = ink & ~blu & ~red
            bb = bbox(ink)
            ext = (f"x {cx+90+bb[0]/s:.1f}..{cx+90+bb[2]/s:.1f} y {gy+28+bb[1]/s:.1f}..{gy+28+bb[3]/s:.1f}"
                   if bb else "none")
            print(f"  col{cx} {nm}: blue={int(blu.sum()/s/s)} red={int(red.sum()/s/s)} black={int(blk.sum()/s/s)} ink {ext}")

print("=== 4. VALUE-COL INTERIOR RULES (vertical runs in body band y gy+18..gy+80, x cx+135..cx+265) ===")
for cx in COLS[:1]:
    for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
        c = crop_frame(a, cx + 135, 223, cx + 265, 285, s)
        nonbg = (np.abs(c - c[2, 2]).sum(axis=2) > 90)
        colsum = nonbg.sum(axis=0)
        nz = np.nonzero(colsum > (55 * s) * 0.55)[0]
        print(f"  col{cx} {nm}: long-vertical x "
              f"{[round(cx+135+v/s,1) for v in nz]}")

print("=== 5. VALUE COL COLORS row1/row2/row3 (value col1 zone x cx+140..cx+180) ===")
for cx in COLS[:1]:
    for lbl, y0, y1 in (("row1", 203, 222), ("row2", 314, 333), ("row3", 424, 443)):
        for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
            c = crop_frame(a, cx + 140, y0, cx + 180, y1, s)
            ink = c.sum(axis=2) < 420
            r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
            blu = ink & (b_ - r_ > 40)
            red = ink & (r_ - b_ > 40) & (r_ - g_ > 40)
            blk = ink & ~blu & ~red
            print(f"  col{cx} {lbl} {nm}: blue={int(blu.sum()/s/s)} red={int(red.sum()/s/s)} black={int(blk.sum()/s/s)}")

print("=== 6. OUTLIER DIGITS x78..120 ===")
for lbl, y0, y1 in (("row1", 203, 222), ("row2", 314, 333), ("row3", 424, 443)):
    for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
        c = crop_frame(a, 78, y0, 120, y1, s)
        ink = c.sum(axis=2) < 420
        r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
        blu = ink & (b_ - r_ > 40)
        red = ink & (r_ - b_ > 40) & (r_ - g_ > 40)
        blk = ink & ~blu & ~red
        print(f"  {lbl} {nm}: blue={int(blu.sum()/s/s)} red={int(red.sum()/s/s)} black={int(blk.sum()/s/s)}")

print("=== 7. NORM TEXT color (x126..215 y258..285) ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = crop_frame(a, 126, 258, 215, 285, s)
    ink = c.sum(axis=2) < 460
    r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
    blu = ink & (b_ - r_ > 40)
    red = ink & (r_ - b_ > 40) & (r_ - g_ > 40)
    blk = ink & ~blu & ~red
    print(f"  {nm}: blue={int(blu.sum()/s/s)} red={int(red.sum()/s/s)} black={int(blk.sum()/s/s)}")

print("=== 8. GRIDLINE COLOR CENSUS (table body x135..370 y210..480) ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = crop_frame(a, 135, 210, 370, 480, s)
    r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
    maroon = (r_ - g_ > 35) & (r_ - b_ > 35) & (r_ > 100)
    neutral = (np.abs(r_ - g_) < 25) & (np.abs(g_ - b_) < 25) & (c.sum(axis=2) < 330)
    print(f"  {nm}: maroon-ish={int(maroon.sum()/s/s)} neutral-dark={int(neutral.sum()/s/s)}")

print("=== 9. RED L1 SEGMENT y168..173: x-extent per column zone ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = crop_frame(a, 60, 166, 904, 176, s)
    rm = red_mask(c)
    for lbl, x0, x1 in (("NOREG", 124, 384), ("RIDGE3", 384, 644), ("RIDGE10", 644, 900)):
        z = rm[:, int(x0 * s):int(x1 * s)]
        nz = np.nonzero(z.sum(axis=0) > 0)[0]
        if len(nz):
            print(f"  {nm} {lbl}: red cols x {x0+nz.min()/s:.1f}..{x0+nz.max()/s:.1f} n={int(z.sum()/s)}")
        else:
            print(f"  {nm} {lbl}: none")
