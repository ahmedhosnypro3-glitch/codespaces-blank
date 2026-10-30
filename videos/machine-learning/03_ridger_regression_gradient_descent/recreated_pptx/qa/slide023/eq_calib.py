#!/usr/bin/env python3
"""Measure the slide-023 equation band from the frame and calibrate a mathtext
render (size/paren style) against it. 960x540 frame, 1px = 1pt."""
import numpy as np, json, sys
from PIL import Image

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)

# ---- ink = anything not the green fill and not near-fill ----
fill = (abs(a[:,:,0]-208)+abs(a[:,:,1]-254)+abs(a[:,:,2]-226)) < 60
dark = a.sum(axis=2) < 620          # black/dark ink
red  = (a[:,:,0] > 130) & (a[:,:,0]-a[:,:,1] > 70) & (a[:,:,0]-a[:,:,2] > 70)
grn  = (a[:,:,1] > 110) & (a[:,:,1]-a[:,:,0] > 50) & (a[:,:,1]-a[:,:,2] > 50)
ink = (~fill) & (dark | red | grn)
band = ink[140:190, 90:460]
ys, xs = np.where(band)
print("ink bbox x%d..%d y%d..%d  (w=%d h=%d)" % (xs.min()+90, xs.max()+90,
      ys.min()+140, ys.max()+140, xs.max()-xs.min()+1, ys.max()-ys.min()+1))

# groups by gap>2
cols = band.any(axis=0); xi = np.where(cols)[0]
grp=[]; g0=p=xi[0]
for x in xi[1:]:
    if x-p > 2: grp.append((g0,p)); g0=x
    p=x
grp.append((g0,p))
print("groups (gap>2):")
for (s,e) in grp:
    sub = band[:, s:e+1]; yy = np.where(sub.any(axis=1))[0]
    # color of the darkest pixels
    seg = a[140:190, s+90:e+91].reshape(-1,3)
    m = sub.reshape(-1) > 0
    sel = seg[m[m | np.zeros(len(m),bool)]] if False else seg[sub.reshape(-1)]
    k = sel.sum(axis=1).argmin()
    print("  x%3d..%3d w%2d  y%3d..%3d h%2d  core=%s" % (s+90, e+90, e-s+1,
          yy.min()+140, yy.max()+140, yy.max()-yy.min()+1, tuple(int(v) for v in sel[k])))

# underline rows: dark bars with wide horizontal run but short vertical extent
print("underline candidates (rows 176..190):")
for y in range(176, 192):
    rr = [x for x in range(90, 470) if dark[y, x] and not dark[y-1, x] if y>0]
    dark[y] = dark[y]
    runs=[]
    xs2 = np.where(dark[y, 90:470])[0]
    if len(xs2):
        s=pr=xs2[0]
        for x in xs2[1:]:
            if x-pr>3: runs.append((s+90,pr+90)); s=x
            pr=x
        runs.append((s+90,pr+90))
    big = [(s0,e0) for s0,e0 in runs if e0-s0 >= 4]
    if big: print("  y%d: %s" % (y, big))
