#!/usr/bin/env python3
import numpy as np
from PIL import Image
from scipy import ndimage

CANVAS = (53, 42, 907, 517)

def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32)

def local_bg(a, size):
    return np.stack([ndimage.uniform_filter(a[...,c], size=size) for c in range(3)], axis=-1)

for tag, path in [("REND001","qa/slide001/geom/render_001-1.png"), ("ORIG001","unique_slides/slide_001.jpg")]:
    a = load(path)
    print("===", tag, a.shape)
    for size in (31, 61, 91):
        bg = local_bg(a, size)
        d = np.abs(a - bg).sum(axis=2)
        for th in (60, 80, 100):
            ink = d >= th
            if tag.startswith("REND"):
                x0,y0,x1,y1 = 0,0,a.shape[1],a.shape[0]
            else:
                x0,y0,x1,y1 = CANVAS
            sub = ink[y0:y1, x0:x1]
            ys,xs = np.nonzero(sub)
            print("  size=%d th=%d ink=%d (%.2f%%) bbox x %d..%d y %d..%d" % (
                size, th, sub.sum(), 100*sub.mean(),
                xs.min() if xs.size else -1, xs.max() if xs.size else -1,
                ys.min() if ys.size else -1, ys.max() if xs.size else -1))
