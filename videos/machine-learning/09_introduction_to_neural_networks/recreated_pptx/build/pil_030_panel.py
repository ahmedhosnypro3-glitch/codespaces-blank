# find white panel + target column + input bracket in original
import numpy as np
from PIL import Image
from scipy import ndimage

a = np.asarray(Image.open("unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (r > 233) & (g > 233) & (b > 233)
lab, n = ndimage.label(white)
sizes = ndimage.sum(white, lab, range(1, n + 1))
print("white comps >800 px:")
for i in range(1, n + 1):
    if sizes[i - 1] > 800:
        ys, xs = np.where(lab == i)
        print(f"  x {xs.min():4d}-{xs.max():4d} y {ys.min():4d}-{ys.max():4d} px {int(sizes[i-1])}"
              f"  fn x{xs.min()/W:.3f}-{xs.max()/W:.3f} y{ys.min()/H:.3f}-{ys.max()/H:.3f}")

# row scan for red across full width: find panel border rows
red = (r > 140) & (g < 100) & (b < 100) & ((r - g) > 55)
for y in [60, 100, 150, 200, 245, 250, 400, 500]:
    xs = np.where(red[y])[0]
    if len(xs):
        # group runs
        groups = []
        s = xs[0]; p = xs[0]
        for x in xs[1:]:
            if x - p > 3:
                groups.append((s, p)); s = x
            p = x
        groups.append((s, p))
        print(f"y={y} red runs:", groups[:12])
for x in [74, 180, 186, 846, 880]:
    ys = np.where(red[:, x])[0]
    if len(ys):
        groups = []; s = ys[0]; p = ys[0]
        for y in ys[1:]:
            if y - p > 3:
                groups.append((s, p)); s = y
            p = y
        groups.append((s, p))
        print(f"x={x} red runs:", groups[:8])

# dark text bbox bands
dark = (r + g + b) < 300
rowsum = dark.sum(axis=1)
bands = []
inb = False
for y in range(H):
    if rowsum[y] > 12 and not inb:
        s = y; inb = True
    elif rowsum[y] <= 12 and inb:
        bands.append((s, y - 1)); inb = False
if inb: bands.append((s, H - 1))
print("dark text bands (y):", [(b0, b1) for b0, b1 in bands if b1 - b0 >= 3])
