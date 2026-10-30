#!/usr/bin/env python3
"""S4b PIL adjudication of crop_12 findings, frame space (960x540).
render_12.png (2001x1125, 150dpi) vs unique_slides/slide_025.jpg.
Q1: does render_12's TR match the CURRENT k11 asset (dotted grid, floor
contours, thin redrect, spike) or the k10 state?
Q2: TR tick-ink layout at left edge (invert check by tick-row positions).
Q3: TL floor contour rings present in render_12? orig?
Q4: BL which edge carries the Z ticks; leader-line/red-X ink census.
Q5: BR black trajectory ink census (present vs tiny-dash claim).
"""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
R = BASE + "/recreated_pptx/qa/slide_025/render_12.png"
O = BASE + "/unique_slides/slide_025.jpg"

ri = Image.open(R).convert("RGB"); oi = Image.open(O).convert("RGB")
ra = np.asarray(ri).astype(int); oa = np.asarray(oi).astype(int)
RS = ra.shape[1] / 960.0

def cf(a, x0, y0, x1, y1, s):
    return a[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]

def redm(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (r > 110) & (r - g > 55) & (r - b > 55)

def darkm(c, t=400):
    return c.sum(axis=2) < t

def graym(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (np.abs(r-g) < 18) & (np.abs(g-b) < 18) & (c.sum(axis=2) < 640) & (c.sum(axis=2) > 330)

# TR box (frame px): x616..879 y115..317
print("=== Q1a TR redrect weight: red px per row on the TOP frame edge y114..122 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 616, 113, 879, 123, s)
    rm = redm(c)
    rows = rm.sum(axis=1)
    print(f"  {nm}: rows {[(round(113+v/s,1), int(rows[v]/s)) for v in np.nonzero(rows > 30*s)[0]]}")

print("=== Q1b TR floor-contour ink (gray, z=0 floor zone x640..870 y270..312) ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 640, 270, 870, 312, s)
    gm = graym(c)
    print(f"  {nm}: gray ink n={int(gm.sum()/s/s)}")

print("=== Q1c TR gridline texture: longest uninterrupted dark run along a row band x660..860 y150..250 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 660, 150, 860, 250, s)
    gm = graym(c) | darkm(c, 560)
    longest = 0
    for row in range(gm.shape[0]):
        run = best = 0
        for v in gm[row]:
            run = run + 1 if v else 0
            best = max(best, run)
        longest = max(longest, best)
    print(f"  {nm}: longest horiz ink run = {longest/s:.1f} frame px")

print("=== Q2 TR left-edge tick rows: dark ink row-profile x618..640, y125..315 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 618, 125, 640, 315, s)
    dm = darkm(c, 480)
    rowsum = dm.sum(axis=1)
    rows = np.nonzero(rowsum > 2.5*s)[0]
    groups = []
    if len(rows):
        st = rows[0]; pv = rows[0]
        for v in rows[1:]:
            if v - pv > int(3*s):
                groups.append((st, pv)); st = v
            pv = v
        groups.append((st, pv))
    print(f"  {nm}: tick-row bands y " + str([(round(125+g0/s,1), round(125+g1/s,1)) for g0, g1 in groups]))

print("=== Q3 TL floor rings: colored (non-gray non-white) ink on floor zone x100..250 y240..285 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 100, 240, 250, 285, s)
    r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
    sat = (np.max(c, axis=2) - np.min(c, axis=2)) > 40
    print(f"  {nm}: saturated ink n={int(sat.sum()/s/s)}")

print("=== Q4 BL Z-axis side: dark tick ink cols x86..106 (left) vs x352..372 (right), y300..520 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    cl = darkm(cf(a, 86, 300, 106, 520, s), 460).sum()
    cr = darkm(cf(a, 352, 300, 372, 520, s), 460).sum()
    print(f"  {nm}: left-band ink n={int(cl/s/s)}  right-band ink n={int(cr/s/s)}")

print("=== Q4b BL red X markers: red ink n in plot interior x120..350 y310..510 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 120, 310, 350, 510, s)
    rm = redm(c)
    print(f"  {nm}: red ink n={int(rm.sum()/s/s)}")

print("=== Q5 BR black trajectory ink: dark n in interior x630..870 y360..520 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 630, 360, 870, 520, s)
    dm = darkm(c, 330)
    print(f"  {nm}: near-black ink n={int(dm.sum()/s/s)}")

print("=== Q6 asset-vs-render TR: downscale loose plot_025_tr.png to TR box, mean|diff| ===")
try:
    pa = np.asarray(Image.open(BASE + "/recreated_pptx/build/assets/plot_025_tr.png").convert("RGB").resize(
        (int(263*RS), int(202*RS)))).astype(int)
    rb = cf(ra, 616, 115, 879, 317, RS)
    print(f"  mean|diff| render_TR vs loose k11 asset = {np.abs(pa-rb).mean():.1f} (0-10 same, >40 different)")
except Exception as e:
    print("  skip:", e)
