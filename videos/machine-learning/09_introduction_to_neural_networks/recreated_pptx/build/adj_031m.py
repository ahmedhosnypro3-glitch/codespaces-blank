#!/usr/bin/env python3
"""Comprehensive region geometry for slide_031 original."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
r, g, b = O[...,0], O[...,1], O[...,2]
PPI = 960/13.33
def inch(v): return round(v/PPI, 3)

# --- diagram panel: reddish border pixels ---
red = (r>110)&(g<100)&(b<100)&((r-g)>40)
print("=== diagram panel red border lines ===")
for y in range(H):
    xs=np.where(red[y])[0]
    if len(xs)==0: continue
    out=[]; s=xs[0]; p=xs[0]
    for v in xs[1:]:
        if v!=p+1: out.append((s,p)); s=v
        p=v
    out.append((s,p))
    big=[o for o in out if o[1]-o[0]>=40]
    if big: print(f" H y={y} ({inch(y)}in): {big} rgb={tuple(O[y,(big[0][0]+big[0][1])//2])}")
for x in range(W):
    ys=np.where(red[:,x])[0]
    if len(ys)==0: continue
    out=[]; s=ys[0]; p=ys[0]
    for v in ys[1:]:
        if v!=p+1: out.append((s,p)); s=v
        p=v
    out.append((s,p))
    big=[o for o in out if o[1]-o[0]>=40]
    if big: print(f" V x={x} ({inch(x)}in): {big} rgb={tuple(O[(big[0][0]+big[0][1])//2,x])}")

# --- pinkish button (Better Weights?) ---
pink = (r>230)&(g>180)&(g<225)&(b>180)&(b<225)&((r-g)>30)
ys,xs=np.where(pink)
if len(xs): print(f"\nPINK button bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] count={len(xs)}  inches x[{inch(xs.min())},{inch(xs.max())}] y[{inch(ys.min())},{inch(ys.max())}]")
else: print("\nPINK: none")

# --- green-ish light fill (green box fill) ---
lg = (g>235)&(r>215)&(r<250)&(b>200)&(b<235)&((g-r)>8)
ys,xs=np.where(lg)
if len(xs): print(f"LIGHTGREEN fill bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] count={len(xs)} inches x[{inch(xs.min())},{inch(xs.max())}] y[{inch(ys.min())},{inch(ys.max())}]")

# --- white-ish box fill inside blue boxes ---
white = (r>248)&(g>248)&(b>246)
for label,(y0,y1,x0,x1) in [("bluebox1",(267,404,72,432)),("bluebox2",(418,507,72,629)),
                             ("greenbox1",(265,406,638,879)),("greenbox2",(416,509,638,879))]:
    reg = white[y0:y1+1, x0:x1+1]
    print(f"{label}: white-fill frac={reg.mean():.3f}")

# --- ink row bands inside blue box1 (text lines) ---
BG=(231,233,230)
d=np.abs(O-np.array(BG)).sum(axis=2)
ink=d>60
def rowbands(x0,x1,y0,y1,gap=2):
    rows = ink[y0:y1+1, x0:x1+1].sum(axis=1)
    bands=[]; inb=False
    for i,c in enumerate(rows):
        if c>0 and not inb: s=i; inb=True
        elif c==0 and inb:
            if i-s>=1: bands.append((y0+s, y0+i-1))
            inb=False
    if inb: bands.append((y0+s, y0+len(rows)-1))
    # merge bands separated by < gap
    merged=[]
    for bnd in bands:
        if merged and bnd[0]-merged[-1][1]<=gap: merged[-1]=(merged[-1][0],bnd[1])
        else: merged.append(list(bnd) if False else (bnd[0],bnd[1]))
    return merged
for label,(x0,x1,y0,y1) in [("bluebox1",(72,432,267,404)),("bluebox2",(72,629,418,507)),
                            ("greenbox1",(638,879,265,406)),("greenbox2",(638,879,416,509))]:
    print(f"{label} text bands:", rowbands(x0+3,x1-3,y0+3,y1-3))
