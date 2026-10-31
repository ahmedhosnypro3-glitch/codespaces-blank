#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image

def scan(path, label):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]
    print("%s %dx%d" % (label, w, h))
    r, g, b = a[...,0], a[...,1], a[...,2]
    red = (r > 140) & (g < 100) & (b < 100)
    # row profile
    rowsum = red.sum(axis=1); colsum = red.sum(axis=0)
    print("  rows with most red:", [(int(i), int(rowsum[i])) for i in np.argsort(-rowsum)[:8]])
    print("  cols with most red:", [(int(i), int(colsum[i])) for i in np.argsort(-colsum)[:8]])
    for name, idx in (("row", rowsum), ("col", colsum)):
        nz = np.nonzero(idx > 0.3 * (a.shape[1] if name == "row" else a.shape[0]))[0]
        print("  %s lines>30%%: %s" % (name, nz.tolist()[:12]))
    # yellow
    yel = (r > 200) & (g > 190) & (b < 210) & (b > 140)
    ys, xs = np.nonzero(yel)
    if xs.size:
        print("  YELLOW(%s) x=%d..%d y=%d..%d n=%d" % (label, xs.min(), xs.max(), ys.min(), ys.max(), xs.size))

for spec in [
    ("unique_slides/slide_001.jpg", "ORIG001"),
    ("qa/slide001/geom/render_001-1.png", "REND001"),
]:
    scan(*spec)
