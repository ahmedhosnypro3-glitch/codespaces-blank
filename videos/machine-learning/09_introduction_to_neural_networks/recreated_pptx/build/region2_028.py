"""Accurate region/colour classification for slide_028 original (content x 56..906, y 42..540)."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("../../unique_slides/slide_028.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 56, 907, 42, 540
SL = o[Y0:Y1, X0:X1]
h, w, _ = SL.shape
print("content region %dx%d (frame x %d..%d y %d..%d)" % (w, h, X0, X1 - 1, Y0, Y1 - 1))

# quantize to 8-level buckets, count
q = (SL // 32) * 32
flat = q.reshape(-1, 3)
cnt = Counter(map(tuple, flat))
print("\n=== top 25 colour buckets (fraction of content region) ===")
tot = w * h
for c, n in cnt.most_common(25):
    print("  %-16s %7d  %.4f" % (str(c), n, n / tot))

# vertical-strip colour profile: for each x-strip of 8px, dominant non-white/non-gray colour
print("\n=== dominant colour per 8px column strip (y 60..470) ===")
for x in range(0, w, 24):
    strip = SL[60:470, x:x+24].reshape(-1, 3)
    cc = Counter(map(tuple, (strip // 32) * 32))
    c, n = cc.most_common(1)[0]
    print("  x %4d..%4d (frame %d..%d): dom %-16s %.3f" % (x, x+24, x+X0, x+24+X0, str(c), n/strip.shape[0]))
