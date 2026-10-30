"""Structural color-region analysis of slide_028 original: bbox per color class."""
import numpy as np
from PIL import Image

o = np.asarray(Image.open("../../unique_slides/slide_028.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape

# restrict to actual slide content region (letterbox margins at x<62, x>901, y<42, y>517)
SL = o[42:518, 62:902]
h, w, _ = SL.shape
print("slide content region: %dx%d px (x 62..901, y 42..517)" % (w, h))

r, g, b = SL[..., 0], SL[..., 1], SL[..., 2]
bg = np.array([231, 233, 230])

def cls(name, mask):
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        print("%-14s none" % name)
        return
    # connected components via simple row-band + column-band histogram
    print("%-14s n=%6d  bbox x %3d..%3d  y %3d..%3d" %
          (name, len(ys), xs.min(), xs.max(), ys.min(), ys.max()))

grayish = np.abs(SL - bg).max(axis=2) < 14
print("gray bg fraction:", round(grayish.mean(), 3))

# color classes (saturation-based)
mx = SL.max(axis=2); mn = SL.min(axis=2)
sat = mx - mn
dark = (mx < 110) & (sat < 60)

print("\n--- SATURATED CLASSES ---")
cls("purple", (r > 110) & (b > 110) & (g < 110) & (sat > 50))
cls("blue", (b > 130) & (b - r > 40) & (b - g > 30) & (sat > 40))
cls("green", (g > 120) & (g - r > 30) & (sat > 35) & ~((g > 200) & (r > 180)))
cls("orange", (r > 190) & (g > 120) & (g < 200) & (b < 130) & (sat > 50))
cls("red", (r > 140) & (r - g > 60) & (r - b > 60) & (sat > 70))
cls("beige", (np.abs(r - 218) < 22) & (np.abs(g - 208) < 22) & (np.abs(b - 196) < 26))
cls("black", (mx < 60))
cls("near-black", (mx < 110) & (sat < 60))

print("\n--- BEIGE detail (row bands) ---")
beige = (np.abs(r - 218) < 22) & (np.abs(g - 208) < 22) & (np.abs(b - 196) < 26)
rows = beige.sum(axis=1)
for y in range(0, h, 10):
    pass
br = [(y, rows[y]) for y in range(h) if rows[y] > 40]
if br:
    st = br[0][0]; prev = st
    for y, _ in br[1:]:
        if y > prev + 3:
            print("  band y %d..%d (content coords y %d..%d)" % (st, prev, st + 42, prev + 42))
            st = y
        prev = y
    print("  band y %d..%d (content coords y %d..%d)" % (st, prev, st + 42, prev + 42))

print("\n--- BLACK detail (row bands) ---")
bl = (mx < 60).sum(axis=1)
bb = [(y, bl[y]) for y in range(h) if bl[y] > 30]
if bb:
    st = bb[0][0]; prev = st
    for y, _ in bb[1:]:
        if y > prev + 3:
            print("  band y %d..%d (content y %d..%d) maxpx=%d" % (st, prev, st + 42, prev + 42, bl[st:prev+1].max()))
            st = y
        prev = y
    print("  band y %d..%d (content y %d..%d) maxpx=%d" % (st, prev, st + 42, prev + 42, bl[st:prev+1].max()))

print("\n--- PURPLE detail (row bands) ---")
pu = ((r > 110) & (b > 110) & (g < 110) & (sat > 50)).sum(axis=1)
pb = [(y, pu[y]) for y in range(h) if pu[y] > 15]
if pb:
    st = pb[0][0]; prev = st
    for y, _ in pb[1:]:
        if y > prev + 3:
            print("  band y %d..%d (content y %d..%d) maxpx=%d" % (st, prev, st + 42, prev + 42, pu[st:prev+1].max()))
            st = y
        prev = y
    print("  band y %d..%d (content y %d..%d) maxpx=%d" % (st, prev, st + 42, prev + 42, pu[st:prev+1].max()))
