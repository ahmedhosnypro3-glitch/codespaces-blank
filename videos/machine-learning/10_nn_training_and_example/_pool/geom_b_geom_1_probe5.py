#!/usr/bin/env python3
import numpy as np
from PIL import Image

def edges(path, label):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]
    lum = a.mean(axis=2)
    # a "page" pixel: light but not the near-white margin and not near-black
    page = (lum > 120) & (lum < 246)
    rows = np.nonzero(page.sum(axis=1) > 0.6 * w)[0]
    cols = np.nonzero(page.sum(axis=0) > 0.5 * h)[0]
    r0, r1 = (int(rows.min()), int(rows.max())) if rows.size else (None, None)
    c0, c1 = (int(cols.min()), int(cols.max())) if cols.size else (None, None)
    print("%s page rows %s..%s cols %s..%s  (%dx%d)" % (label, r0, r1, c0, c1, c1-c0+1, r1-r0+1))
    # red frame: loose reddish mask
    r, g, b = a[...,0], a[...,1], a[...,2]
    red = (r > 120) & (r - g > 40) & (r - b > 40)
    rr = red.sum(axis=1); rc = red.sum(axis=0)
    fr = np.nonzero(rr > 0.35 * w)[0]; fc = np.nonzero(rc > 0.35 * h)[0]
    print("   redframe rows %s cols %s" % (fr.tolist()[:6], fc.tolist()[:6]))
    # fine: at a red row, find x extent of the red line
    if fr.size:
        y = int(fr[len(fr)//2])
        xs = np.nonzero(red[y])[0]
        print("   at red row y=%d x=%d..%d" % (y, xs.min(), xs.max()))
    if fc.size:
        x = int(fc[len(fc)//2])
        ys = np.nonzero(red[:, x])[0]
        print("   at red col x=%d y=%d..%d" % (x, ys.min(), ys.max()))

for s in ["001","004","005","006","007"]:
    edges("unique_slides/slide_%s.jpg" % s, "ORIG%s" % s)
