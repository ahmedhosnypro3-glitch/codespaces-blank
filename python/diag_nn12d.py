#!/usr/bin/env python3
"""Element-level geometry for slide_012 diagram + strips."""
import numpy as np
from PIL import Image
from scipy import ndimage

P = "videos/machine-learning/10_nn_training_and_example/unique_slides/slide_012.jpg"
o = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W = 540, 960
IN = 13.33 / W


def comps(mask, name, min_n=250):
    lbl, k = ndimage.label(mask)
    print(f"{name}: {k} comps")
    for i in range(1, k + 1):
        ys, xs = np.where(lbl == i)
        if len(ys) >= min_n:
            print(f"  n={len(ys):>5} rows {ys.min():>3}-{ys.max():>3} cols {xs.min():>3}-{xs.max():>3}  "
                  f"in=({(xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f}) "
                  f"cx={((xs.min()+xs.max())/2)*IN:.2f} cy={((ys.min()+ys.max())/2)*IN:.2f}")


# sample the actual fill colors from the known circle centroids
pts = {"greenA": (150, 335), "greenB": (200, 335), "greenC": (265, 335),
       "orangeA": (200, 470), "orangeB": (200, 560), "orangeC": (200, 655),
       "redErr": (270, 560), "blueT": (200, 900)}
for k, (y, x) in pts.items():
    print(f"sample {k} @({x},{y}) = {tuple(o[y, x])}")

print()
# detect green circles: saturated green anywhere
gsat = o[:, :, 1] - np.maximum(o[:, :, 0], o[:, :, 2]) > 30
gsat &= o[:, :, 1] > 90
comps(gsat, "green-saturated", min_n=300)

# orange
om = (o[:, :, 0] - o[:, :, 2] > 60) & (o[:, :, 1] > 100) & (o[:, :, 0] > 200)
comps(om, "orange", min_n=200)

# red fill (Error box)
rm = (o[:, :, 0] - o[:, :, 1] > 70) & (o[:, :, 0] - o[:, :, 2] > 70) & (o[:, :, 0] > 200)
comps(rm, "redfill", min_n=2500)

# light blue rects (t_j)
bm = (o[:, :, 2] - o[:, :, 0] > 30) & (o[:, :, 2] > 190) & (o[:, :, 1] > 150)
comps(bm, "blue", min_n=600)

# pale green strip (one or two bars)
pg = (o[:, :, 1] - o[:, :, 0] > 5) & (o[:, :, 1] > 230) & (o[:, :, 2] < 235) & (o[:, :, 1] - o[:, :, 2] > 5)
comps(pg, "palegreen", min_n=500)

# white box on the gray/white content area
wm = (o[:, :, 0] > 250) & (o[:, :, 1] > 250) & (o[:, :, 2] > 250)
comps(wm, "white-box", min_n=2000)
