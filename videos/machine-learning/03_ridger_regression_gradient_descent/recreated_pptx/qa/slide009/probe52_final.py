#!/usr/bin/env python3
"""Probe 52: final localization — right panel borders, eq boxes/ink, small discs."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== RIGHT panel borders (cuts at y=300) ===")
for x in range(482, 492):
    print(f"   x={x} {tuple(a[300, x])}")
print("   ...")
for x in range(864, 874):
    print(f"   x={x} {tuple(a[300, x])}")
print("=== panel top/bottom rows LEFT (cut x=300) / RIGHT (cut x=700) ===")
for y in range(105, 113):
    print(f"   LEFT  y={y} {tuple(a[y, 300])}")
print()
for y in range(470, 478):
    print(f"   LEFT  y={y} {tuple(a[y, 300])}")
print()
for y in range(105, 113):
    print(f"   RIGHT y={y} {tuple(a[y, 700])}")
print()
for y in range(470, 478):
    print(f"   RIGHT y={y} {tuple(a[y, 700])}")

print("\n=== equation boxes: navy-border detection (b-r>25, b>110, dark) ===")
NAVY = (r < 150) & (b > 90) & ((b - r) > 55)
for nm, x0, x1 in (("LEFT", 200, 340), ("RIGHT", 615, 755)):
    m = np.zeros_like(NAVY)
    m[140:185, x0:x1] = NAVY[140:185, x0:x1]
    ys, xs = np.where(m)
    # column histogram to find the two vertical borders
    ch = m.sum(axis=0)
    cols = [int(x) for x in range(x0, x1) if ch[x] > 20]
    print(f"  {nm} border cols (>20px): {cols}")
    rh = m.sum(axis=1)
    rows = [int(y) for y in range(140, 185) if rh[y] > 20]
    print(f"  {nm} border rows (>20px): {rows}")

print("\n=== equation ink (achromatic dark) inside each box ===")
DARK = (r < 140) & (g < 140) & (b < 140) & (abs(r - g) < 60) & (abs(g - b) < 60)
for nm, x0, x1, y0, y1 in (("LEFT", 218, 316, 148, 174), ("RIGHT", 633, 734, 147, 175)):
    m = DARK[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm} ink x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
    # pale fill sample (median of non-ink pixels)
    sub = a[y0 + 4:y1 - 3, x0 + 6:x1 - 5].reshape(-1, 3)
    med = np.median(sub, axis=0)
    print(f"  {nm} interior median RGB = {med}")

print("\n=== small red discs: tight bbox of truest-red core ===")
TRED = (r > 90) & (g < 75) & (b < 75) & ((r - g) > 60) & ((r - b) > 60)
for nm, x0, x1, y0, y1 in (("L-disc1", 182, 194, 149, 163), ("L-disc2", 241, 252, 283, 296),
                           ("R-disc1", 598, 611, 143, 157), ("R-disc2", 673, 685, 313, 326)):
    m = TRED[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    if len(ys):
        cx = (xs.min() + xs.max()) / 2 + x0
        cy = (ys.min() + ys.max()) / 2 + y0
        print(f"  {nm}: core bbox x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} "
              f"centre ({cx:.1f},{cy:.1f}) n={len(ys)}")
        # full extent with looser red
        LOOSE = (r > 60) & ((r - g) > 30) & ((r - b) > 20)
        m2 = LOOSE[y0:y1 + 1, x0:x1 + 1]
        ys2, xs2 = np.where(m2)
        print(f"      loose bbox x {xs2.min()+x0}..{xs2.max()+x0} y {ys2.min()+y0}..{ys2.max()+y0} "
              f"centre ({(xs2.min()+xs2.max())/2+x0:.1f},{(ys2.min()+ys2.max())/2+y0:.1f})")

print("\n=== big red disc LEFT: loose extent ===")
LOOSE = (r > 60) & ((r - g) > 30) & ((r - b) > 20)
m = LOOSE[222:262, 214:254]
ys, xs = np.where(m)
print(f"  bbox x {xs.min()+214}..{xs.max()+214} y {ys.min()+222}..{ys.max()+222} n={len(ys)}")
print(f"  centre ({(xs.min()+xs.max())/2+214:.1f}, {(ys.min()+ys.max())/2+222:.1f})")

print("\n=== thin red diagonal extents (loose) ===")
for nm, x0, x1, y0, y1 in (("L diag", 195, 250, 195, 258), ("R diag", 618, 656, 208, 270)):
    m = LOOSE[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm}: bbox x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
        # per-row centroid
        for yy in range(ys.min() + y0, ys.max() + y0, 6):
            row = np.where(LOOSE[yy, x0:x1 + 1])[0]
            if len(row):
                print(f"      y={yy} x {row.min()+x0}..{row.max()+x0} centroid {row.mean()+x0:.1f}")
