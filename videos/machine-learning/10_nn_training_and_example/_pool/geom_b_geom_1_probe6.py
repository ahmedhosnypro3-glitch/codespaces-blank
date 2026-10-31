#!/usr/bin/env python3
import numpy as np
from PIL import Image

def page_rect(path, label):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    lum = a.mean(axis=2)
    # subpixel: for the left edge use a clean row band, scan x
    def left_edge(y):
        row = lum[y]
        # find first x where lum drops below 246 (white margin -> gray page)
        idx = np.nonzero(row < 246)[0]
        return idx[0] if idx.size else None
    def right_edge(y):
        row = lum[y]
        idx = np.nonzero(row < 246)[0]
        return idx[-1] if idx.size else None
    def top_edge(x):
        col = lum[:, x]
        idx = np.nonzero(col < 246)[0]
        return idx[0] if idx.size else None
    def bot_edge(x):
        col = lum[:, x]
        idx = np.nonzero(col < 246)[0]
        return idx[-1] if idx.size else None
    le = [left_edge(y) for y in (300, 400, 200)]
    re = [right_edge(y) for y in (300, 400, 200)]
    te = [top_edge(x) for x in (300, 400, 600)]
    be = [bot_edge(x) for x in (300, 400, 600)]
    print("%s left=%s right=%s top=%s bot=%s" % (label, le, re, te, be))
    # red frame exact
    r,g,b = a[...,0],a[...,1],a[...,2]
    red = (r>120)&(r-g>40)&(r-b>40)
    rr = red.sum(axis=1); rc = red.sum(axis=0)
    print("   red rows>50%%w: %s" % np.nonzero(rr>0.5*w)[0].tolist())
    print("   red cols>50%%h: %s" % np.nonzero(rc>0.5*h)[0].tolist())

for s in ["001","004","005","006","007"]:
    page_rect("unique_slides/slide_%s.jpg" % s, "ORIG%s" % s)
