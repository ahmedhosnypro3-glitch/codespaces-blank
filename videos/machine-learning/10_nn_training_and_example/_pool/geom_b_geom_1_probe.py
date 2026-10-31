#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image

def stats(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]
    flat = a.reshape(-1, 3)
    cols, counts = np.unique(flat, axis=0, return_counts=True)
    order = np.argsort(-counts)[:5]
    print("  size=%dx%d mean=%.1f" % (w, h, a.mean()))
    for i in order:
        c = cols[i]
        print("    modal %6.2f%% rgb=(%d,%d,%d)" % (100.0*counts[i]/len(flat), c[0], c[1], c[2]))
    # red frame detection
    r, g, b = a[...,0], a[...,1], a[...,2]
    red = (r > 140) & (g < 90) & (b < 90)
    ys, xs = np.nonzero(red)
    if xs.size:
        print("    RED bbox x=%d..%d y=%d..%d n=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), xs.size))
        # column histogram of red
        colcount = red.sum(axis=0)
        top = np.argsort(-colcount)[:6]
        print("    red columns:", [(int(t), int(colcount[t])) for t in sorted(top)])
    else:
        print("    RED none")
    # yellow badge
    yel = (r > 200) & (g > 190) & (b < 200)
    ys2, xs2 = np.nonzero(yel)
    if xs2.size:
        print("    YELLOW bbox x=%d..%d y=%d..%d n=%d" % (xs2.min(), xs2.max(), ys2.min(), ys2.max(), ys2.size))
    else:
        print("    YELLOW none")
    # dark ink pixels (text/lines)
    dark = (r < 120) & (g < 120) & (b < 120)
    ys3, xs3 = np.nonzero(dark)
    if xs3.size:
        print("    DARK bbox x=%d..%d y=%d..%d n=%d" % (xs3.min(), xs3.max(), ys3.min(), ys3.max(), xs3.size))
    else:
        print("    DARK none")

for p in sys.argv[1:]:
    print(p)
    stats(p)
