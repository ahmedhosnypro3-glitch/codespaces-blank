#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image

def bands(path, label):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]
    print("%s %dx%d" % (label, w, h))
    # very dark = video letterbox / black bars
    dark = (a.sum(axis=2) < 90)
    rows = dark.sum(axis=1); cols = dark.sum(axis=0)
    print("  dark rows >50%%:", np.nonzero(rows > 0.5*w)[0].tolist()[:20])
    print("  dark cols >50%%:", np.nonzero(cols > 0.5*h)[0].tolist()[:20])
    # near-white vs page-gray: coarse quantization row/col
    for r in range(0, h, max(1, h//18)):
        row = a[r]
        vals = [tuple(map(int,row[c])) for c in range(0, w, max(1,w//8))]
        print("   y=%3d %s" % (r, vals))
    print()

for spec in [
    ("unique_slides/slide_001.jpg", "ORIG001"),
    ("qa/slide001/geom/render_001-1.png", "REND001"),
]:
    bands(*spec)
