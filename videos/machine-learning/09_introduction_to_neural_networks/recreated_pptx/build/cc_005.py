from PIL import Image
import numpy as np
from scipy import ndimage
import sys

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 244) & (G > 244) & (B > 244)
masks = {
    "RED": (R - G > 60) & (R - B > 60) & (R > 120),
    "BLUE": (B - R > 60) & (B - G > 50) & (B > 90),
    "DARK": (~white) & (R < 130) & (G < 130) & (B < 130),
}

for name, m in masks.items():
    # close small gaps so a bracket glyph is one component
    filled = ndimage.binary_closing(m, structure=np.ones((3, 3)))
    lab, n = ndimage.label(filled)
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs):
        if sl is None:
            continue
        ys, xs = sl
        cnt = int((filled[sl]).sum())
        if cnt < 6:
            continue
        comps.append((ys.start, ys.stop, xs.start, xs.stop, cnt))
    comps.sort(key=lambda c: (c[0], c[2]))
    print(f"\n===== {name}: {len(comps)} components (y0,y1,x0,x1,px) =====")
    for c in comps:
        print(f"  y[{c[0]:3d}..{c[1]:3d}] x[{c[2]:3d}..{c[3]:3d}] w={c[3]-c[2]+1:3d} h={c[1]-c[0]+1:3d} px={c[4]}")
