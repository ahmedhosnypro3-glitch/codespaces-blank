#!/usr/bin/env python3
"""Glyph-cluster + ink-color analysis of the blue box, example, and solution text."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def ink(y0, y1, x0, x1, bg):
    """mask of pixels far from bg color"""
    reg = a[y0:y1+1, x0:x1+1]
    d = np.abs(reg[:,:,0]-bg[0]) + np.abs(reg[:,:,1]-bg[1]) + np.abs(reg[:,:,2]-bg[2])
    return d > 100, reg

def clusters(y0, y1, x0, x1, bg, label, gap=5):
    m, reg = ink(y0, y1, x0, x1, bg)
    colhit = m.any(axis=0)
    xs = []
    x = 0
    while x < len(colhit):
        if colhit[x]:
            s = x
            while x < len(colhit) and (colhit[x] or (x+gap < len(colhit) and colhit[x:x+gap].any())):
                x += 1
            xs.append((s, x-1))
        else:
            x += 1
    print(f"\n== {label} y{y0}..{y1} x{x0}..{x1} bg={bg}: {len(xs)} clusters")
    for s, e in xs:
        sub = m[:, s:e+1]
        px = reg[:, s:e+1][sub]
        ys = np.where(sub.any(axis=1))[0]
        if len(px) == 0: continue
        # core ink = darkest 40%
        srt = sorted(px.tolist())
        core = srt[:max(1, len(srt)//3)]
        dom = Counter(tuple(p) for p in core).most_common(1)[0][0]
        print(f"  x[{s+x0}..{e+x0}] w={e-s+1} y[{ys[0]+y0}..{ys[-1]+y0}] core={dom}")

# blue box text: bg = (254,255,255)-ish white-blue
clusters(238, 300, 90, 870, (253, 255, 255), "BLUE BOX lines", gap=6)
# example lines
clusters(360, 390, 90, 870, (254, 255, 255), "EXAMPLE line 1", gap=6)
clusters(392, 420, 90, 870, (254, 255, 255), "EXAMPLE line 2", gap=6)
# solution box text: bg = (250,253,226)
clusters(445, 528, 90, 870, (250, 253, 226), "SOLUTION box all", gap=6)
