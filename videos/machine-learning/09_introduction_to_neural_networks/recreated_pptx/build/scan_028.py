"""Precise color scanning of slide_028 original."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("../../unique_slides/slide_028.jpg").convert("RGB")).astype(int)

print("=== scanline y=20,10 ===")
for x in range(0, 960, 40):
    print("  x=%3d  %s" % (x, tuple(o[20, x])))
print("=== scanline y=10 ===")
for x in range(0, 960, 40):
    print("  x=%3d  %s" % (x, tuple(o[10, x])))
print("=== scanline y=46 ===")
for x in range(0, 960, 40):
    print("  x=%3d  %s" % (x, tuple(o[46, x])))
print("=== scanline y=150 ===")
for x in range(0, 960, 40):
    print("  x=%3d  %s" % (x, tuple(o[150, x])))
print("=== scanline x=480 vertical ===")
for y in range(0, 540, 20):
    print("  y=%3d  %s" % (y, tuple(o[y, 480])))
print("=== scanline x=30 vertical ===")
for y in range(0, 540, 20):
    print("  y=%3d  %s" % (y, tuple(o[y, 30])))
print("=== scanline x=940 vertical ===")
for y in range(0, 540, 20):
    print("  y=%3d  %s" % (y, tuple(o[y, 940])))

# red frame detection: any pure-red-ish pixels
r, g, b = o[..., 0], o[..., 1], o[..., 2]
red = (r > 150) & (g < 90) & (b < 90)
ys, xs = np.nonzero(red)
print("\nred-ish pixels:", red.sum())
if red.sum():
    print("  bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    # which columns have the most red
    colc = red.sum(axis=0)
    topcols = np.argsort(colc)[::-1][:15]
    print("  top red cols:", sorted(topcols.tolist()), [int(colc[c]) for c in sorted(topcols.tolist())])
    rowc = red.sum(axis=1)
    toprows = np.argsort(rowc)[::-1][:10]
    print("  top red rows:", sorted(toprows.tolist()), [int(rowc[c]) for c in sorted(toprows.tolist())])
