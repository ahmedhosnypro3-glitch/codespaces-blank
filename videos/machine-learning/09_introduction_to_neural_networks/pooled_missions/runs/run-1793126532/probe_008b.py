#!/usr/bin/env python3
"""Detailed probe of slide_008.jpg: axis pixels, hatch regions, label positions."""
from PIL import Image
import numpy as np

im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"{W}x{H}")

def hx(p):
    return "#%02X%02X%02X" % (p[0], p[1], p[2])

def region(x0, y0, x1, y1, label):
    r = a[y0:y1, x0:x1].reshape(-1, 3)
    print(f"\n== {label}  [{x0},{y0}]-[{x1},{y1}] ==")
    # palette census
    q = (r // 24 * 24)
    uniq, cnt = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-cnt)[:6]
    for i in order:
        print(f"   {hx(uniq[i])}  {cnt[i]*100.0/len(r):5.1f}%")

# Axes: origin approx [315,420], vertical to [315,145], horizontal to [780,420]
print("\n--- AXIS SAMPLES ---")
for (x, y) in [(315, 400), (315, 300), (315, 200), (315, 155), (315, 145),
               (350, 420), (500, 420), (700, 420), (770, 420), (780, 418)]:
    print(f"  ({x:4d},{y:4d}) {hx(a[y,x])}")

# decision lines at their measured points
print("\n--- LINE SAMPLES ---")
for (x, y, lbl) in [(300, 231, "red d1 mid"), (450, 340, "red d1 mid2"),
                    (450, 418, "blue mid"), (600, 282, "blue mid2"),
                    (400, 366, "green mid"), (600, 358, "green mid2")]:
    print(f"  {lbl:12s} ({x:4d},{y:4d}) {hx(a[y,x])}")

# hatch regions
region(200, 150, 280, 230, "upper-left zone (C1? / green hatch?)")
region(700, 400, 780, 490, "lower-right zone (C2 blue hatch?)")
region(200, 430, 300, 500, "lower-left zone (C3 red hatch?)")
region(180, 200, 200, 260, "far-left edge strip")

# label boxes / callouts
region(550, 175, 600, 210, "C1 yellow box area")
region(640, 320, 700, 360, "C2 yellow box area")
region(270, 430, 320, 470, "C3 yellow box area")
region(85, 135, 165, 185, "Undefined box")
region(760, 360, 900, 420, "New Class box")

# plot border - find red rectangle edges by scanning columns/rows near expected
print("\n--- PLOT BORDER SCAN ---")
redmask = (a[:,:,0] > 140) & (a[:,:,1] < 90) & (a[:,:,2] < 90)
for x in [160, 170, 175, 180, 190, 780, 790, 800, 810]:
    col = np.where(redmask[:, x])[0]
    if len(col):
        print(f"  x={x:4d}: red ys {col.min()}..{col.max()} n={len(col)}")
    else:
        print(f"  x={x:4d}: no red")
for y in [110, 115, 120, 125, 130, 500, 510, 515, 520]:
    row = np.where(redmask[y, :])[0]
    if len(row):
        print(f"  y={y:4d}: red xs {row.min()}..{row.max()} n={len(row)}")
    else:
        print(f"  y={y:4d}: no red")
