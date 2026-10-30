#!/usr/bin/env python3
"""Verify each text line by rendering candidate strings and comparing the ink
column-run profile against the frame's (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
IM='/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a=np.array(Image.open(IM)).astype(int)
BG={'panel':[233,233,231],'green':[208,254,226],'blue':[249,252,255],'yellow':[250,253,226]}
def frame_runs(y0,y1,x0,x1,bg,thr=150,gap=2):
    d=np.abs(a[y0:y1+1,x0:x1+1]-np.array(bg)).sum(axis=2); m=d>thr
    cols=m.any(axis=0); xi=np.where(cols)[0]
    if not len(xi): return None,(0,0)
    runs=[];s=p=xi[0]
    for x in xi[1:]:
        if x-p>gap: runs.append((s,p)); s=x
        p=x
    runs.append((s,p))
    runs=[(int(s+x0),int(e+x0)) for s,e in runs if e-s>=0]
    return runs,(int(xi.min()+x0),int(xi.max()+x0))
SC=4
def rend_runs(text,path,size,gap=2):
    f=ImageFont.truetype(path,size*SC)
    im=Image.new('L',(len(text)*size*SC+100,size*SC*3),0); ImageDraw.Draw(im).text((20,size*SC),text,font=f,fill=255)
    m=np.array(im)>128; cols=m.any(axis=0); xi=np.where(cols)[0]
    if not len(xi): return None,(0,0)
    runs=[];s=p=xi[0]
    for x in xi[1:]:
        if x-p>gap: runs.append((int((s)/SC),int((p)/SC))); s=x
        p=x
    runs.append((int(s/SC),int(p/SC)))
    return runs,(int(xi.min()/SC),int(xi.max()/SC))
def score(fr,rr,fw,rw):
    if fr is None or rr is None: return 0
    F=set()
    for s,e in fr: F.update(range(s,e+1))
    R=set()
    for s,e in rr: R.update(range(s,e+1))
    j=len(F&R)/max(len(F|R),1)
    dw=abs(fw-rw)/max(fw,1)
    nr=abs(len(fr)-len(rr))
    return j-0.6*dw-0.02*nr
FONTS={
 'Arial-r':('/usr/share/fonts/TTF/Arial.TTF','r'),'Arial-b':('/usr/share/fonts/TTF/Arialbd.TTF','b'),
 'Arial-i':('/usr/share/fonts/TTF/Ariali.TTF','i'),'Arial-bi':('/usr/share/fonts/TTF/Arialbi.TTF','bi'),
 'LibSans-r':('/usr/share/fonts/liberation/LiberationSans-Regular.ttf','r'),
 'LibSans-b':('/usr/share/fonts/liberation/LiberationSans-Bold.ttf','b'),
 'Calibri-r':('/usr/share/fonts/TTF/calibri.ttf','r'),'Calibri-b':('/usr/share/fonts/TTF/calibrib.ttf','b'),
 'Calibri-i':('/usr/share/fonts/TTF/calibrii.ttf','i'),
 'Verdana-r':('/usr/share/fonts/TTF/Verdana.TTF','r'),'Verdana-b':('/usr/share/fonts/TTF/Verdanab.TTF','b'),
}
CASES=[
 # (label, y0,y1,x0,x1,bg, [candidate texts])
 ("DIM1",190,218,100,412,'green',["if Feature vectors are of dimension d","if Feature vectors are of dimension d+1","if Feature vectors are of dimension d"]),
 ("DIM2",190,218,498,752,'green',["(X^T X) is of size d+1 x d+1"]),
 ("EX1",358,390,92,860,'blue',["For Example: if Features vector is of size 1000 then Inverse calculation is"]),
 ("EX2",394,424,92,560,'blue',["or order 1,000,000,000 which is impractical","is or order 1,000,000,000 which is impractical"]),
 ("BLUE1",238,266,95,860,'blue',["The standard matrix inversion algorithm has a time complexity of O(n^3)","The standard matrix inversion algorithm has a time complexity of O(n^3),"]),
 ("BLUE2",272,302,95,860,'blue',["which means that the computation time increases rapidly with the size of the matrix","which means that the computation time increases rapidly with the size of"]),
 ("BLUE3",304,338,95,770,'blue',["the matrix (increasing cubically with the number of components)."]),
 ("SOLL1",470,500,230,800,'yellow',["Instead of using Least Squares with Matrix inversion,"]),
 ("SOLL2",500,532,285,710,'yellow',["use Gradient Descent iterative solution"]),
]
for (lbl,y0,y1,x0,x1,bg,texts) in CASES:
    fr,fw=frame_runs(y0,y1,x0,x1,BG[bg])
    print(f"== {lbl}: frame ink x{fw[0]}..{fw[1]} (w{fw[1]-fw[0]+1}) runs={len(fr)}")
    if fr is None: continue
    print("   frame runs:",fr)
    best=[]
    for fname,(path,st) in FONTS.items():
        for text in texts:
            for size in range(11,30):
                rr,rw=rend_runs(text,path,size)
                s=score(fr,rr,fw[1]-fw[0]+1,rw[1]-rw[0]+1)
                best.append((s,fname,text[:38],size,rw[1]-rw[0]+1,len(rr)))
    best.sort(reverse=True)
    for (s,fname,t,size,w,nr) in best[:6]:
        print(f"    score={s:.3f} {fname} {size}pt w={w} runs={nr}  '{t}'")
