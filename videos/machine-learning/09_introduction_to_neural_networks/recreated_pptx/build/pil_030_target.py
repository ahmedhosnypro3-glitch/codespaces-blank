# target column + output annotations measurement for original slide_030
import numpy as np
from PIL import Image
from scipy import ndimage

a = np.asarray(Image.open("unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]

dark = (a.sum(axis=2) < 320)
blue = (a[:, :, 2] > 110) & ((a[:, :, 2] - a[:, :, 0]) > 35) & ((a[:, :, 2] - a[:, :, 1]) > 35)
red = (a[:, :, 0] > 140) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110) & ((a[:, :, 0] - a[:, :, 1]) > 50)
green = (a[:, :, 1] > 100) & ((a[:, :, 1] - a[:, :, 0]) > 30) & ((a[:, :, 1] - a[:, :, 2]) > 30)

def comps(m, minpx=12):
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) >= minpx:
            out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
    return sorted(out, key=lambda t: (t[2], t[0]))

for nm, m in [("dark", dark), ("blue", blue), ("red", red), ("green", green)]:
    print(f"== {nm} comps x>=630 and y<250 ==")
    for c in comps(m):
        if c[0] >= 630 and c[2] < 250:
            print("   %s x%3d-%3d y%3d-%3d (%dpx)  in: x%.2f-%.2f y%.2f-%.2f"
                  % (nm, c[0], c[1], c[2], c[3], c[4], c[0]/960*13.33, c[1]/960*13.33, c[2]/540*7.5, c[3]/540*7.5))

print("== dark/blue/red in x 190-410 (input side) ==")
for nm, m in [("dark", dark), ("blue", blue), ("red", red)]:
    for c in comps(m):
        if 180 <= c[0] < 410 and c[2] < 250:
            print("   %s x%3d-%3d y%3d-%3d (%dpx)  in: x%.2f-%.2f y%.2f-%.2f"
                  % (nm, c[0], c[1], c[2], c[3], c[4], c[0]/960*13.33, c[1]/960*13.33, c[2]/540*7.5, c[3]/540*7.5))
