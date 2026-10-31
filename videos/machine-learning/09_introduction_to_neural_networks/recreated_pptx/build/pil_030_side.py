# measure input side, weight labels, target column, pink box in original
import numpy as np
from PIL import Image
from scipy import ndimage

a = np.asarray(Image.open("unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]

dark = (a.sum(axis=2) < 300)
green = (a[:, :, 1] > 105) & ((a[:, :, 1] - a[:, :, 0]) > 38) & ((a[:, :, 1] - a[:, :, 2]) > 38)
blue = (a[:, :, 2] > 120) & ((a[:, :, 2] - a[:, :, 0]) > 45) & ((a[:, :, 2] - a[:, :, 1]) > 45)
red = (a[:, :, 0] > 140) & (a[:, :, 1] < 100) & (a[:, :, 2] < 100) & ((a[:, :, 0] - a[:, :, 1]) > 55)
pinkf = (np.abs(a[:, :, 0] - 248) < 25) & (np.abs(a[:, :, 1] - 203) < 25) & (np.abs(a[:, :, 2] - 173) < 30)

def comps(m, minpx=25):
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) >= minpx:
            out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
    return sorted(out, key=lambda t: t[0])

print("== dark text comps left of panel (x<190) ==")
for c in comps(dark)[:40]:
    if c[0] < 200 and 40 < c[1] and c[2] < 260:
        print("   dark x%3d-%3d y%3d-%3d (%dpx)" % c)

print("== green comps (weight labels) in panel ==")
for c in comps(green):
    print("   green x%3d-%3d y%3d-%3d (%dpx)" % c)

print("== blue comps in panel (O labels) ==")
for c in comps(blue):
    if c[2] < 260:
        print("   blue x%3d-%3d y%3d-%3d (%dpx)" % c)

print("== pink fill comps ==")
for c in comps(pinkf):
    print("   pink x%3d-%3d y%3d-%3d (%dpx)" % c)

print("== target column region x>820 ==")
for c in comps(dark):
    if c[0] > 780 and c[2] < 260:
        print("   dark x%3d-%3d y%3d-%3d (%dpx)" % c)
print("== red comps in panel (red weight labels) ==")
for c in comps(red):
    if c[2] < 260:
        print("   red x%3d-%3d y%3d-%3d (%dpx)" % c)
