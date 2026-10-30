#!/usr/bin/env python3
"""Verify the diagram panel interior of the ORIGINAL: find nodes, arrows, labels.
Measures with PIL only (no vision needed). Outputs a structural map."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
PPI = 960/13.33
def inch(v): return round(v/PPI, 3)

# diagram panel: x 187..847, y 58..249 (with 1px border each side)
x0,x1,y0,y1 = 188,846,59,248
D = O[y0:y1+1, x0:x1+1]
print("panel interior size", D.shape, "=> inches", inch(x1-x0+1), "x", inch(y1-y0+1))
pd, pg, pb = D[...,0], D[...,1], D[...,2]
BG = np.array([231,233,230])
d = np.abs(D-BG).sum(axis=2)
ink = d>60
print("ink px", ink.sum(), "frac", round(ink.mean(),4))

# yellow circles (hidden nodes): r>240 g>230 b<200
yellow = (pd>240)&(pg>230)&(pb<200)&((pd-pb)>25)
ys,xs = np.where(yellow)
print("\nyellow px", len(xs))
if len(xs):
    print(" yellow bbox panel-coords x", xs.min(),xs.max()," y", ys.min(),ys.max())
    # connected components via simple flood by clustering rows
    rows = yellow.sum(axis=1)
    print(" yellow row profile (rows with >3):")
    for y in range(len(rows)):
        if rows[y]>3:
            xr=np.where(yellow[y])[0]
            print(f"   y={y0+y}: x[{x0+xr.min()},{x0+xr.max()}] n={rows[y]}")

# orange circles (output nodes)
orange = (pd>230)&(pg>120)&(pg<200)&(pb<120)
ys,xs=np.where(orange)
print("\norange px", len(xs))
if len(xs):
    rows = orange.sum(axis=1)
    for y in range(len(rows)):
        if rows[y]>3:
            xr=np.where(orange[y])[0]
            print(f"   y={y0+y}: x[{x0+xr.min()},{x0+xr.max()}] n={rows[y]}")

# dark ink (text) profile by row inside panel
print("\nALL-INK row bands in panel:")
rows = ink.sum(axis=1)
bands=[]; inb=False
for i,c in enumerate(rows):
    if c>0 and not inb: s=i; inb=True
    elif c==0 and inb:
        if i-s>=1: bands.append((y0+s,y0+i-1))
        inb=False
if inb: bands.append((y0+s,y0+len(rows)-1))
print(bands)
for (a,bb) in bands:
    cols = ink[a-y0:bb-y0+1].sum(axis=0)
    xs=np.where(cols>0)[0]
    print(f"  band y[{a},{bb}] ({inch(a)}-{inch(bb)}in) x[{x0+xs.min()},{x0+xs.max()}] ({inch(x0+xs.min())}-{inch(x0+xs.max())}in)")
