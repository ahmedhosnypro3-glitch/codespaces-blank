#!/usr/bin/env python3
"""Glyph-cluster color analysis of specific bands: each contiguous ink cluster with
dominant colors, for the equation line and dimension-note line of the green box."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def ink_mask(y0, y1, x0, x1):
    reg = a[y0:y1+1, x0:x1+1]
    # ink = anything notably darker or more saturated than the green fill (206,255,226)
    dist = np.abs(reg[:,:,0]-206) + np.abs(reg[:,:,1]-255) + np.abs(reg[:,:,2]-226)
    return dist > 90, reg

def clusters(y0, y1, x0, x1, label, gap=4):
    m, reg = ink_mask(y0, y1, x0, x1)
    colhit = m.any(axis=0)
    xs = []
    x = 0
    while x < len(colhit):
        if colhit[x]:
            x0c = x
            while x < len(colhit) and (colhit[x] or (x+gap < len(colhit) and any(colhit[x:x+gap]))):
                x += 1
            xs.append((x0c, x-1))
        else:
            x += 1
    print(f"\n== {label} y{y0}..{y1} x{x0}..{x1}: {len(xs)} clusters")
    for (cx0, cx1) in xs:
        sub = reg[:, cx0:cx1+1]
        mm = m[:, cx0:cx1+1]
        px = sub[mm]
        if len(px) == 0: continue
        dom = Counter(tuple(p) for p in px).most_common(2)
        yy = np.where(mm.any(axis=1))[0]
        print(f"  x{cx0+x0}-{cx1+x0} (w={cx1-cx0+1}) y{yy[0]+y0}..{yy[-1]+y0} n={len(px)} dom={dom}")

clusters(146, 190, 95, 780, "EQUATION LINE", gap=3)
clusters(191, 218, 95, 780, "DIMENSION NOTE LINE", gap=5)
clusters(110, 145, 95, 400, "RECALL LINE", gap=5)
