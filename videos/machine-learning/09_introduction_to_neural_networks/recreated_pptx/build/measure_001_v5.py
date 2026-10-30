#!/usr/bin/env python3
"""slide_001 v5: definitive per-line, per-color ink measurement of ORIGINAL and RENDER."""
import os, sys
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = os.path.join(V, "unique_slides/slide_001.jpg")
OUT = os.path.join(V, "recreated_pptx/build/measure_001_v5.txt")

def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float64)

def analyze(a, ppi, label, box):
    H, W = a.shape[:2]
    L = 0.299*a[:,:,0] + 0.587*a[:,:,1] + 0.114*a[:,:,2]
    R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
    ink = L < 175
    x0, y0, x1, y1 = box
    m = np.zeros_like(ink); m[y0:y1+1, x0:x1+1] = ink[y0:y1+1, x0:x1+1]
    ink = m
    r = ink.sum(axis=1)
    bands = []; inb = False
    for y in range(H):
        if r[y] > 1 and not inb: st = y; inb = True
        elif r[y] <= 1 and inb: bands.append([st, y-1]); inb = False
    if inb: bands.append([st, H-1])
    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] <= 2: merged[-1][1] = b[1]
        else: merged.append(b)
    print("=" * 100)
    print("### %s  (px/in = %.2f)" % (label, ppi))
    print("  band y-range      x-range       w    h   inkpx  dominant-colour  dominant-ink bbox")
    for (by0, by1) in merged:
        sub = ink[by0:by1+1]
        if sub.sum() < 15: continue
        xs = np.nonzero(sub.sum(axis=0) > 0)[0]
        if len(xs) < 2: continue
        # dominant colour = most saturated common colour among ink pixels
        px = a[by0:by1+1][sub]
        q = (px // 24).astype(int)
        key = q[:,0]*10000 + q[:,1]*100 + q[:,2]
        vals, cnts = np.unique(key, return_counts=True)
        k = vals[np.argmax(cnts)]
        dom = np.array([((k//10000)*24+12), ((k//100)%100)*24+12, (k%100)*24+12])
        sel = (np.abs(px - dom).max(axis=1) < 40)
        if sel.sum() > 10:
            flat = np.zeros(px.shape[0], dtype=bool); flat[sel] = True
            mm = flat.reshape(sub.shape)
            yy, xx = np.nonzero(mm)
            dbox = "x %d-%d y %d-%d" % (xx.min(), xx.max(), by0+yy.min(), by0+yy.max())
        else:
            dbox = "-"
        print("  y %4d-%4d  x %4d-%4d  w=%4d h=%3d  %6d  #%02X%02X%02X  %s"
              % (by0, by1, xs.min(), xs.max(), xs.max()-xs.min()+1, by1-by0+1,
                 int(sub.sum()), int(dom[0]), int(dom[1]), int(dom[2]), dbox))
        print("        inches: y %.3f-%.3f  x %.3f-%.3f   (w %.3f in)"
              % (by0/ppi, (by1+1)/ppi, xs.min()/ppi, (xs.max()+1)/ppi, (xs.max()-xs.min()+1)/ppi))

o = load(ORIG)
analyze(o, 72.0, "ORIGINAL unique_slides/slide_001.jpg", (62, 46, 899, 514))

for name in sys.argv[1:]:
    r = load(os.path.join(V, "recreated_pptx/build", name))
    ppi = r.shape[0] / 7.5
    analyze(r, ppi, "RENDER " + name, (int(0.1*ppi), int(0.1*ppi), int(r.shape[1]-0.1*ppi), int(r.shape[0]-0.1*ppi)))
