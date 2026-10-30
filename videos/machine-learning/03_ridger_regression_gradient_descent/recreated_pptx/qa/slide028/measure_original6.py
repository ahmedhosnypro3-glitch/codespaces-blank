#!/usr/bin/env python3
"""Pass 6: erosion-based dot detection + ASCII ink maps of both panels."""
import numpy as np
from PIL import Image
from scipy import ndimage

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
blue = (b - r > 45) & (b > 110)

print("== EROSION DOT DETECTION (2x erosion of blue mask) ==")
er = ndimage.binary_erosion(blue, structure=np.ones((3, 3)), iterations=2)
lbl, n = ndimage.label(er)
for i in range(1, n + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) < 8:
        continue
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    if w_ < 4 or h_ < 4:
        continue
    print(f"  core n={len(ys)} x {x0}-{x1} y {y0}-{y1} w={w_} h={h_} "
          f"cx={(x0+x1)/2:.1f} cy={(y0+y1)/2:.1f}")

# 1x erosion too (small dots)
print("\n== EROSION x1 ==")
er1 = ndimage.binary_erosion(blue, structure=np.ones((3, 3)), iterations=1)
lbl1, n1 = ndimage.label(er1)
for i in range(1, n1 + 1):
    ys, xs = np.where(lbl1 == i)
    if len(ys) < 25:
        continue
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    fill = len(ys) / (w_ * h_)
    tag = "BLOB" if 0.55 <= w_ / h_ <= 1.8 and fill > 0.45 and w_ <= 26 else ""
    print(f"  n={len(ys)} x {x0}-{x1} y {y0}-{y1} w={w_} h={h_} fill={fill:.2f} {tag} "
          f"cx={(x0+x1)/2:.1f} cy={(y0+y1)/2:.1f}")


def ascii_map(x0, x1, y0, y1, step, label):
    print(f"\n== ASCII BLUE-INK MAP {label} (x {x0}-{x1}, y {y0}-{y1}, {step}px/char) ==")
    print("    " + "".join(str((x0 + i * step) // 100 % 10) for i in range(0, (x1 - x0) // step)))
    print("    " + "".join(str((x0 + i * step) // 10 % 10) for i in range(0, (x1 - x0) // step)))
    for yy in range(y0, y1, step):
        row = ""
        for xx in range(x0, x1, step):
            cell = blue[yy:yy + step, xx:xx + step]
            f = cell.mean()
            row += "#" if f > 0.55 else ("+" if f > 0.3 else ("." if f > 0.05 else " "))
        print(f"{yy:3d} {row}")


ascii_map(150, 400, 228, 448, 2, "LEFT panel")
ascii_map(500, 745, 226, 448, 2, "RIGHT panel")
