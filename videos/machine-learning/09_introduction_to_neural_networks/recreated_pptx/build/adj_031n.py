#!/usr/bin/env python3
"""Top-region geometry: title, subtitle box, badge for slide_031 original."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
PPI = 960/13.33
def inch(v): return round(v/PPI, 3)
r,g,b = O[...,0],O[...,1],O[...,2]

# light green fill (239,255,226)
for name, col, tol in [("LIGHTGREEN(239,255,226)", (239,255,226), 14),
                       ("LIGHTYELLOW(251,253,232)", (251,253,232), 12)]:
    m = (np.abs(O-np.array(col)).sum(axis=2) < tol*3)
    ys,xs=np.where(m)
    if len(xs):
        # split into connected row bands
        rows=m.sum(axis=1)
        bands=[]; inb=False
        for y in range(H):
            if rows[y]>3 and not inb: s=y; inb=True
            elif rows[y]<=3 and inb: bands.append((s,y-1)); inb=False
        if inb: bands.append((s,H-1))
        for (y0,y1) in bands:
            xs2=np.where(m[y0:y1+1].any(axis=0))[0]
            print(f"{name}: band y[{y0},{y1}] ({inch(y0)}-{inch(y1)}in) x[{xs2.min()},{xs2.max()}] ({inch(xs2.min())}-{inch(xs2.max())}in)")

# red text in top-left (title "Example")
redtxt=(r>120)&(g<110)&(b<110)&((r-g)>35)
sub=redtxt[46:90, 60:600]
ys,xs=np.where(sub)
if len(xs):
    print(f"\nRED TEXT top-left bbox: x[{60+xs.min()},{60+xs.max()}] ({inch(60+xs.min())}-{inch(60+xs.max())}in) y[{46+ys.min()},{46+ys.max()}] ({inch(46+ys.min())}-{inch(46+ys.max())}in) count={len(xs)}")
    rows=sub.sum(axis=1)
    bands=[]; inb=False
    for i,c in enumerate(rows):
        if c>0 and not inb: s=i; inb=True
        elif c==0 and inb: bands.append((46+s,46+i-1)); inb=False
    if inb: bands.append((46+s,46+len(rows)-1))
    print("red text bands:", bands)

# green text (Better Weights label)
gtxt=(g>80)&(g-r>40)&(g-b>40)
sub2=gtxt[46:90, 60:700]
ys,xs=np.where(sub2)
if len(xs):
    print(f"\nGREEN TEXT top-left bbox: x[{60+xs.min()},{60+xs.max()}] y[{46+ys.min()},{46+ys.max()}] count={len(xs)}")

# badge yellow circle top-right
yellow=(r>240)&(g>235)&(b>190)&(b<245)&((r-b)>10)
sub3=yellow[40:120, 840:960]
ys,xs=np.where(sub3)
if len(xs):
    print(f"\nYELLOW badge bbox: x[{840+xs.min()},{840+xs.max()}] ({inch(840+xs.min())}-{inch(840+xs.max())}in) y[{40+ys.min()},{40+ys.max()}] ({inch(40+ys.min())}-{inch(40+ys.max())}in)")

# 'Forward' blue italic label
blue=(r<120)&(g<120)&(b>100)
sub4=blue[46:540, 60:640]
ys,xs=np.where(sub4)
if len(xs):
    print(f"BLUE text (Forward?) bbox: x[{60+xs.min()},{60+xs.max()}] ({inch(60+xs.min())}-{inch(60+xs.max())}in) y[{46+ys.min()},{46+ys.max()}] ({inch(46+ys.min())}-{inch(46+ys.max())}in) count={len(xs)}")
    # rows bands in the x<400 region only
    sub5=blue[200:280, 60:400]
    ys2,xs2=np.where(sub5)
    if len(xs2):
        print(f"  'Forward' label: x[{60+xs2.min()},{60+xs2.max()}] ({inch(60+xs2.min())}-{inch(60+xs2.max())}in) y[{200+ys2.min()},{200+ys2.max()}] ({inch(200+ys2.min())}-{inch(200+ys2.max())}in)")

# text bands inside green boxes (finer)
BG=(231,233,230)
d=np.abs(O-np.array(BG)).sum(axis=2); ink=d>60
def bands(x0,x1,y0,y1,minc=1):
    rows=ink[y0:y1+1,x0:x1+1].sum(axis=1)
    out=[]; inb=False
    for i,c in enumerate(rows):
        if c>minc and not inb: s=i; inb=True
        elif c<=minc and inb:
            out.append((y0+s,y0+i-1)); inb=False
    if inb: out.append((y0+s,y0+len(rows)-1))
    return out
print("\ngreenbox1 text bands:", bands(641,877,268,403))
print("greenbox2 text bands:", bands(641,877,419,506))
print("bluebox2 text bands:", bands(74,628,420,506))

# column extents of text inside bluebox2 vs greenbox1 (widths)
for name,(x0,x1,y0,y1) in [("bluebox1",(73,432,268,404)),("bluebox2",(73,628,418,507)),
                            ("greenbox1",(638,879,265,406)),("greenbox2",(638,879,416,509))]:
    reg = ink[y0:y1+1, x0:x1+1]
    cols=reg.sum(axis=0)
    xs=np.where(cols>0)[0]
    print(f"{name} ink x extent: {x0+xs.min()}..{x0+xs.max()} ({inch(x0+xs.min())}..{inch(x0+xs.max())}in)")
