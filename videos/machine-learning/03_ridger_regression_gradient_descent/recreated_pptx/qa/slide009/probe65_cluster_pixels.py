#!/usr/bin/env python3
"""probe65 - exact pixels of the annotation cluster near each outlier.

LEFT  x160..205 y135..170     RIGHT x578..612 y132..162
Also: LEFT label ink bbox with the big disc excluded (y<=228).
"""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)


def cls(p):
    r, g, b = p
    if r > 200 and 90 < g < 190 and b < 90:          # orange point
        return "O"
    if r - max(g, b) > 90:                          # strong red
        return "R"
    if r - max(g, b) > 40:
        return "r"
    if r > 200 and g > 150 and b > 150 and r - b > 18:   # rose / pink
        return "p"
    if r < 170 and g < 170 and b < 170:
        return "#"
    return "."


def dump(tag, x0, y0, x1, y1):
    print(f"===== {tag}  x{x0}..{x1} y{y0}..{y1} =====")
    print("      " + "".join(str((x // 10) % 10) for x in range(x0, x1 + 1)))
    print("      " + "".join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        row = "".join(cls(a[y, x]) for x in range(x0, x1 + 1))
        print(f"  {y:3d} {row}")
    print("  -- non-background pixels (rgb) --")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = cls(a[y, x])
            if c in "Rr":
                print(f"     ({x},{y}) {c} rgb={tuple(a[y, x])}")


dump("LEFT cluster", 160, 135, 205, 170)
dump("RIGHT cluster", 578, 132, 612, 162)

# LEFT label ink bbox, disc excluded
sub = a[188:229, 192:240]
m = np.array([[1 if (p[0] > 150 and p[0] - p[1] > 25 and p[0] - p[2] > 15) else 0
               for p in row] for row in sub])
ys, xs = np.nonzero(m)
print(f"LEFT label ink (no disc): n={len(xs)} bbox x{192+xs.min()}..{192+xs.max()} "
      f"y{188+ys.min()}..{188+ys.max()} centroid=({192+xs.mean():.1f},{188+ys.mean():.1f})")
# strongest red cores inside the label band
cores = [(tuple(a[188 + yy, 192 + xx]),
          (192 + xx, 188 + yy))
         for yy, xx in zip(ys, xs) if a[188 + yy, 192 + xx][0] - a[188 + yy, 192 + xx][1] > 60]
cores.sort(key=lambda t: t[0][0] - max(t[0][1], t[0][2]), reverse=True)
print("  strongest label pixels:", cores[:6])
