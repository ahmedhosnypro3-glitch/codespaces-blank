#!/usr/bin/env python3
"""Probe 46: TRUE-red census (orange points excluded), blue line thickness,
orange point diameters, composite arrow shapes."""
import numpy as np
from PIL import Image
from scipy import ndimage

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# TRUE red: C00000 family — saturated red with negligible green AND blue.
TRED = (r > 90) & (g < 75) & (b < 75) & ((r - g) > 60) & ((r - b) > 60)
ORANGE = (r > 180) & (g > 70) & (g < 175) & (b < 90) & ((r - g) > 60)
BLUE = (b > 90) & ((b - r) > 40) & ((b - g) > 30) & (r < 90)

print("=== TRUE-RED COMPONENTS (whole frame, n>=12) ===")
lab, n = ndimage.label(TRED, structure=np.ones((3, 3)))
sizes = ndimage.sum(TRED, lab, range(1, n + 1))
objs = ndimage.find_objects(lab)
kept = 0
for i, (sl, sz) in enumerate(zip(objs, sizes), 1):
    if sz < 12:
        continue
    y0, y1 = sl[0].start, sl[0].stop - 1
    x0, x1 = sl[1].start, sl[1].stop - 1
    kept += 1
    print(f"  comp{i}: x {x0}..{x1} (w={x1-x0+1}) y {y0}..{y1} (h={y1-y0+1}) n={int(sz)} "
          f"fill={(x1-x0+1)*(y1-y0+1)} dens={sz/((x1-x0+1)*(y1-y0+1)):.2f}")

print("\n=== ORANGE COMPONENTS in panels (n>=12) ===")
lo, oe = ndimage.label(ORANGE, structure=np.ones((3, 3)))
osz = ndimage.sum(ORANGE, lo, range(1, oe + 1))
oob = ndimage.find_objects(lo)
pts = []
for i, (sl, sz) in enumerate(zip(oob, osz), 1):
    if sz < 12:
        continue
    y0, y1 = sl[0].start, sl[0].stop - 1
    x0, x1 = sl[1].start, sl[1].stop - 1
    if not (94 < x0 < 900 and 107 < y0 < 475):
        continue
    cy = (sl[0].start + sl[0].stop) / 2
    cx = (sl[1].start + sl[1].stop) / 2
    pts.append((cx, cy, x1 - x0 + 1, y1 - y0 + 1, int(sz)))
    print(f"  comp{i}: cx={cx:6.1f} cy={cy:6.1f} w={x1-x0+1} h={y1-y0+1} n={int(sz)} dens={sz/((x1-x0+1)*(y1-y0+1)):.2f}")
print(f"  ORANGE POINT COUNT: {len(pts)}")

print("\n=== BLUE LINE thickness (perpendicular estimate) ===")
for nm, c0, c1 in (("LEFT", 141, 433), ("RIGHT", 555, 849)):
    widths = []
    for x in range(c0 + 20, c1, 20):
        col = np.where(BLUE[:, x])[0]
        if len(col):
            grp, s, p = [], col[0], col[0]
            for v in col[1:]:
                if v <= p + 1:
                    p = v
                    continue
                grp.append((s, p)); s = p = v
            grp.append((s, p))
            grp.sort(key=lambda t: t[1] - t[0], reverse=True)
            widths.append((x, grp[0][0], grp[0][1], grp[0][1] - grp[0][0] + 1))
    ws = [w[3] for w in widths]
    print(f"  {nm}: n={len(ws)} median per-col span={int(np.median(ws))} "
          f"min={min(ws)} max={max(ws)} samples={widths[:4]}")

print("\n=== composite arrow detail (LEFT x195..250 y195..260) ASCII ===")
sub = TRED[195:260, 195:250]
for j in range(sub.shape[0]):
    print("   " + "".join("#" if sub[j, k] else "." for k in range(sub.shape[1])))

print("\n=== LEFT diamond comp8 (x180..195 y145..165) ASCII ===")
sub = TRED[145:166, 180:196]
for j in range(sub.shape[0]):
    print("   " + "".join("#" if sub[j, k] else "." for k in range(sub.shape[1])))

print("\n=== RIGHT extra comp16 (x635..655 y245..270) ASCII ===")
sub = TRED[245:271, 635:656]
for j in range(sub.shape[0]):
    print("   " + "".join("#" if sub[j, k] else "." for k in range(sub.shape[1])))

print("\n=== RIGHT diamond comp7 (x595..610 y140..158) ASCII ===")
sub = TRED[140:159, 595:611]
for j in range(sub.shape[0]):
    print("   " + "".join("#" if sub[j, k] else "." for k in range(sub.shape[1])))
