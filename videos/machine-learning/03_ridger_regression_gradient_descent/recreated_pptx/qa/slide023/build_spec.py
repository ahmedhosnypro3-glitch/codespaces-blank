#!/usr/bin/env python3
"""AUTHORITATIVE build spec for slide_023 (960x540 frame, 1px=1pt=1/72in)."""
import numpy as np
from collections import Counter
from PIL import Image, ImageFont

IM='/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a=np.array(Image.open(IM)).astype(int)
def mask(bg,y0,y1,x0,x1,thr=170):
    d=np.abs(a[y0:y1+1,x0:x1+1]-np.array(bg)).sum(axis=2)
    full=np.zeros(a.shape[:2],bool); full[y0:y1+1,x0:x1+1]=d>thr
    return full
def clss(p):
    r,g,b=p
    if r>120 and r-g>70 and r-b>70: return "RED"
    if b>r+40 and b>90 and g<120: return "NAVY"
    if r<110 and g<110 and b<110: return "BLK"
    if g>110 and g-r>50 and g-b>50: return "GRN"
    return "other"
def line(m,label,y0,y1,x0,x1,text=None,gap=4):
    sub=m[y0:y1+1,x0:x1+1]
    ys,xs=np.where(sub)
    if not len(xs): print(f" {label}: NO INK"); return
    lx,rx,ty,by=xs.min()+x0,xs.max()+x0,ys.min()+y0,ys.max()+y0
    cols=sub.any(axis=0); xi=np.where(cols)[0]
    grp=[];g0=p=xi[0]
    for x in xi[1:]:
        if x-p>gap: grp.append((int(g0+x0),int(p+x0))); g0=x
        p=x
    grp.append((int(g0+x0),int(p+x0)))
    seg=a[ty:by+1,lx:rx+1]; mm=m[ty:by+1,lx:rx+1].reshape(-1)
    sel=seg.reshape(-1,3)[mm]
    cc=Counter(clss(tuple(v)) for v in sel)
    tops=[(int(np.where(m[ty:by+1,s:e+1].any(axis=1))[0].max())+1) for s,e in grp]
    cap=max(tops)
    print(f" {label}: ink x{lx}..{rx} y{ty}..{by} w{rx-lx+1} h{by-ty+1} capmax={cap} col={cc.most_common(2)} nwords={len(grp)}")
    print(f"    groups={grp}")
    if text:
        for style,path in [("reg","/usr/share/fonts/TTF/Arial.TTF"),("bold","/usr/share/fonts/TTF/Arialbd.TTF"),
                           ("ital","/usr/share/fonts/TTF/Ariali.TTF"),("bi","/usr/share/fonts/TTF/Arialbi.TTF")]:
            for size in range(8,44):
                f=ImageFont.truetype(path,size*8)
                if abs(f.getlength(text)/8.0-(rx-lx+1))<3:
                    print(f"    >>> Arial-{style} {size}pt advance={f.getlength(text)/8.0:.0f} = ink {rx-lx+1}")
P=mask([233,233,231],40,120,60,900)     # panel bg
GF=mask([208,254,226],100,230,90,870)   # green fill bg
BF=mask([249,252,255],225,430,90,900)   # blue box fill bg
YF=mask([250,253,226],430,540,60,900)   # yellow fill bg
print("TITLE");      line(P,"title",74,112,200,700,"Inverse of High Dimension Matrix")
print("RECALL");     line(GF,"recall",112,148,92,400,"Recall:")
print("DIMNOTE");    line(GF,"dimnote",188,222,92,790)
print("BLUE L1");    line(BF,"blueL1",236,270,95,860,"The standard matrix inversion algorithm has a time",gap=5)
print("BLUE L2");    line(BF,"blueL2",270,304,95,860)
print("BLUE L3");    line(BF,"blueL3",304,340,95,860)
print("EX L1");      line(P,"exL1",356,394,92,860)
print("EX L2");      line(P,"exL2",392,428,92,560)
print("SOL label");  line(YF,"sollabel",444,474,95,420,"Solution:")
print("SOL L1");     line(YF,"solL1",470,504,230,790,"Instead of using Least Squares with Matrix inversion,")
print("SOL L2");     line(YF,"solL2",500,532,290,700,"use Gradient Descent iterative solution")
