"""PIL ground-truth measurements for slide_028 original frame vs render."""
import sys
from PIL import Image
import numpy as np

ORIG = Image.open("../../unique_slides/slide_028.jpg").convert("RGB")
REN = Image.open("slide_028_rendered-1.png").convert("RGB")
W, H = ORIG.size  # 960x540
print("orig size", ORIG.size, "render size", REN.size, "scale", REN.size[0]/W)

o = np.asarray(ORIG).astype(int)
r = np.asarray(REN).astype(int)

# --- background color: corners / most common color
from collections import Counter
c = Counter(map(tuple, o[0:6, 0:6].reshape(-1, 3)))
print("top-left corner colors:", c.most_common(4))
c2 = Counter(map(tuple, o[0:20, 0:960:7].reshape(-1, 3)))
print("top row colors:", c2.most_common(4))

# most common color in whole frame (sampled)
sample = o[::4, ::4].reshape(-1, 3)
cc = Counter(map(tuple, sample))
print("most common frame colors:", cc.most_common(6))

# --- row / col ink profiles (ink = far from bg)
bg = np.array(cc.most_common(1)[0][0])
d = np.abs(o - bg).max(axis=2)
ink = d > 28
print("\nbg =", bg, "ink frac", round(ink.mean(), 4))

rows = ink.sum(axis=1)
cols = ink.sum(axis=0)
# print band structure: contiguous row bands with ink
def bands(v, thr=3):
    out = []
    st = None
    for i, x in enumerate(v):
        if x > thr and st is None:
            st = i
        elif x <= thr and st is not None:
            out.append((st, i - 1))
            st = None
    if st is not None:
        out.append((st, len(v) - 1))
    return out

rb = bands(rows)
print("\nROW bands (orig), y px (x0.5 for 960w):")
for a, b in rb:
    if b - a >= 2:
        print("  y %4d..%4d  rows %4d  inkpx %5d" % (a, b, b - a + 1, rows[a:b+1].max()))
