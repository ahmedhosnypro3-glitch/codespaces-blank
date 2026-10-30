#!/usr/bin/env python3
"""Probe 51: raw pixel profiles through key features (final geometry/colour)."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)


def hcut(y, x0, x1, label):
    print(f"\n--- HORIZONTAL CUT y={y}  x{x0}..{x1}  ({label}) ---")
    for x in range(x0, x1 + 1):
        p = a[y, x]
        print(f"   x={x:3d} ({p[0]:3d},{p[1]:3d},{p[2]:3d})")


def vcut(x, y0, y1, label):
    print(f"\n--- VERTICAL CUT x={x}  y{y0}..{y1}  ({label}) ---")
    for y in range(y0, y1 + 1):
        p = a[y, x]
        print(f"   y={y:3d} ({p[0]:3d},{p[1]:3d},{p[2]:3d})")


hcut(300, 92, 100, "LEFT navy border left edge")
hcut(300, 462, 470, "LEFT navy border right edge")
hcut(150, 122, 132, "LEFT y-axis + arrowhead")
vcut(126, 145, 160, "LEFT y-axis shaft top")
vcut(126, 300, 310, "LEFT y-axis shaft mid")
vcut(434, 425, 445, "LEFT x-axis + arrowhead (cut along x)")
vcut(235, 232, 250, "LEFT big disc centre")
print("\n--- LEFT big disc: raw centre 10x10 x228..238 y236..246 ---")
for y in range(236, 247):
    print("   " + " ".join(f"{a[y,x,0]:3d},{a[y,x,1]:3d},{a[y,x,2]:3d}" for x in range(228, 239)))
print("\n--- LEFT small disc raw x184..190 y153..160 ---")
for y in range(153, 161):
    print(f"   y={y} " + " ".join(f"{a[y,x,0]:3d},{a[y,x,1]:3d},{a[y,x,2]:3d}" for x in range(184, 191)))
print("\n--- RIGHT small disc raw x600..607 y145..155 ---")
for y in range(145, 156):
    print(f"   y={y} " + " ".join(f"{a[y,x,0]:3d},{a[y,x,1]:3d},{a[y,x,2]:3d}" for x in range(600, 608)))
print("\n--- RIGHT y-axis raw x538..543 y300 ---")
for x in range(537, 545):
    print(f"   x={x} {tuple(a[300,x])}")
print("\n--- blue line raw: LEFT x=250 y294..300 ---")
for y in range(293, 301):
    print(f"   y={y} {tuple(a[y,250])}")
print("\n--- grid line raw: LEFT row y120 x300..306 / row y121 ---")
for x in range(299, 308):
    print(f"   x={x} y120={tuple(a[120,x])} y121={tuple(a[121,x])} y119={tuple(a[119,x])}")
print("\n--- annotation box border raw: LEFT x214..220 y161 ---")
for x in range(214, 221):
    print(f"   x={x} {tuple(a[161,x])}")
print("--- annotation box fill raw: LEFT y160 x230..240 ---")
for x in range(230, 241):
    print(f"   x={x} {tuple(a[160,x])}")
