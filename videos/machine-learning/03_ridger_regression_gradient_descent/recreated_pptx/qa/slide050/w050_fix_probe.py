#!/usr/bin/env python3
"""Three measurements for the 050 fix cycle:
1. orig pink box bbox + per-side border colors
2. step text core color (rows 61..72, x364..425 only)
3. augmented header row (y164..176) + class row (y231..244) cluster centres
"""
import numpy as np
from PIL import Image

NS = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")).astype(int)

# 1. pink box bbox in x725..845 y45..185
sub = o[45:185, 725:845]
m = (sub[:,:,0] > 235) & (sub[:,:,1] > 205) & (sub[:,:,1] < 250) & (sub[:,:,2] > 205) & (sub[:,:,2] < 250) & ((sub[:,:,0] - sub[:,:,1]) > 8)
ys, xs = np.where(m)
print("pink-fill bbox: x%d..%d y%d..%d n=%d" % (725+xs.min(), 725+xs.max(), 45+ys.min(), 45+ys.max(), m.sum()))
print("per-row pink count (bottom rows):")
for yy in range(138, 152):
    print("  y%d n=%d" % (yy, int(m[yy-45].sum())))
midy = slice(80, 120)
print("border samples:")
print("  top y58 x750..820:", o[58, 750:820].mean(axis=0).round(0), " y59:", o[59, 750:820].mean(axis=0).round(0))
print("  bottom y142 x750..820:", o[142, 750:820].mean(axis=0).round(0), " y143:", o[143, 750:820].mean(axis=0).round(0))
print("  left x737 y90..130:", o[90:130, 737].mean(axis=0).round(0), " x738:", o[90:130, 738].mean(axis=0).round(0))
print("  right x829 y90..130:", o[90:130, 829].mean(axis=0).round(0), " x830:", o[90:130, 830].mean(axis=0).round(0))
print("  corner darkness: min lum in border ring:", )
ring = np.concatenate([o[57:60, 740:825].reshape(-1,3), o[141:145, 740:825].reshape(-1,3),
                       o[60:140, 736:740].reshape(-1,3), o[60:140, 827:832].reshape(-1,3)])
print("  ring mean %s median %s min-lum px %s" % (ring.mean(axis=0).round(0), np.median(ring, axis=0), ring[ring.mean(axis=1).argmin()]))

# 2. step core color
win = o[61:73, 364:425]
lum = win.mean(axis=2)
for th in (100, 120, 140):
    c = win[lum < th]
    print("step core lum<%d: n=%d mean %s median %s" % (th, len(c), c.mean(axis=0).round(1), np.median(c, axis=0)))

# 3. header + class row clusters
def clusters(cols, gap=4):
    if len(cols) == 0: return []
    out, s, p = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - p > gap: out.append((s, p)); s = c
        p = c
    out.append((s, p)); return out
for lo, hi, tag in [(163, 177, "header"), (230, 245, "class")]:
    band = o[lo:hi, 66:250].mean(axis=2) < 190
    cols = np.where(band.any(axis=0))[0]
    cl = clusters(cols)
    cs = [round(66+(a+b)/2, 1) for a, b in cl]
    print("%s clusters:" % tag, [(66+a, 66+b) for a, b in cl])
    print("%s centres: %s" % (tag, cs))
