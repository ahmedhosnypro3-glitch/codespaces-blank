#!/usr/bin/env python3
"""Pixel-level font fit: render each candidate text, normalize to the frame's
ink bbox, score by IoU. 960x540 frame, 1px=1pt."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM='/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a=np.array(Image.open(IM)).astype(int)
BG={'panel':[233,233,231],'green':[208,254,226],'blue':[249,252,255],'yellow':[250,253,226]}
def framemask(y0,y1,x0,x1,bg,thr=150):
    d=np.abs(a[y0:y1+1,x0:x1+1]-np.array(bg)).sum(axis=2)
    m=d>thr; ys,xs=np.where(m)
    if not len(xs): return None
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1], (int(xs.min()+x0),int(xs.max()+x0),int(ys.min()+y0),int(ys.max()+y0))
FONTS={
 'Arial':('/usr/share/fonts/TTF/Arial.TTF','/usr/share/fonts/TTF/Arialbd.TTF','/usr/share/fonts/TTF/Ariali.TTF','/usr/share/fonts/TTF/Arialbi.TTF'),
 'Verdana':('/usr/share/fonts/TTF/Verdana.TTF','/usr/share/fonts/TTF/Verdanab.TTF','/usr/share/fonts/TTF/Verdanai.TTF','/usr/share/fonts/TTF/Verdanai.TTF'),
 'Calibri':('/usr/share/fonts/TTF/calibri.ttf','/usr/share/fonts/TTF/calibrib.ttf','/usr/share/fonts/TTF/calibrii.ttf','/usr/share/fonts/TTF/calibriz.ttf'),
 'Carlito':('/usr/share/fonts/carlito/Carlito-Regular.ttf','/usr/share/fonts/carlito/Carlito-Bold.ttf','/usr/share/fonts/carlito/Carlito-Italic.ttf','/usr/share/fonts/carlito/Carlito-BoldItalic.ttf'),
 'LibSans':('/usr/share/fonts/liberation/LiberationSans-Regular.ttf','/usr/share/fonts/liberation/LiberationSans-Bold.ttf','/usr/share/fonts/liberation/LiberationSans-Italic.ttf','/usr/share/fonts/liberation/LiberationSans-BoldItalic.ttf'),
}
import os
FONTS={k:[p for p in v if os.path.exists(p)] for k,v in FONTS.items()}
SC=4
def render_mask(text,path,size):
    f=ImageFont.truetype(path,size*SC)
    im=Image.new('L',(len(text)*size*SC+80,size*SC*3),0); d=ImageDraw.Draw(im)
    d.text((20,size*SC),text,font=f,fill=255)
    m=np.array(im)>128; ys,xs=np.where(m)
    if not len(xs): return None
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1]
def iou(A,B):
    H=max(A.shape[0],B.shape[0]); W=max(A.shape[1],B.shape[1])
    Ap=np.zeros((H,W),bool); Bp=np.zeros((H,W),bool)
    Ap[:A.shape[0],:A.shape[1]]=A; Bp[:B.shape[0],:B.shape[1]]=B
    # center both
    def ctr(M):
        out=np.zeros((H,W),bool); y0=(H-M.shape[0])//2; x0=(W-M.shape[1])//2
        out[y0:y0+M.shape[0],x0:x0+M.shape[1]]=M; return out
    A=ctr(Ap); B=ctr(Bp)
    return (A&B).sum()/max((A|B).sum(),1)
LINES=[
 ("TITLE",  74,108,215,660,'panel',"Inverse of High Dimension Matrix"),
 ("RECALL", 114,140,100,180,'green',"Recall:"),
 ("DIM1",   190,217,100,400,'green',"if Feature vectors are of dimension d"),
 ("DIM2",   190,217,500,760,'green',"(X^T X) is of size d+1 x d+1"),
 ("BLUE1",  238,266, 95,860,'blue',"The standard matrix inversion algorithm has a time"),
 ("EX1",    358,390, 92,860,'blue',"For Example: if Features vector is of size 1000 then"),
 ("EX2",    394,424, 92,560,'blue',"Inverse calculation is or order 1,000,000,000 which is impractical"),
 ("SOLLBL", 444,468, 95,420,'yellow',"Solution:"),
 ("SOLL1",  470,500,230,790,'yellow',"Instead of using Least Squares with Matrix inversion,"),
 ("SOLL2",  500,532,285,705,'yellow',"use Gradient Descent iterative solution"),
]
for (lbl,y0,y1,x0,x1,bg,text) in LINES:
    r=framemask(y0,y1,x0,x1,BG[bg])
    if r is None: print(lbl,"NO INK"); continue
    fm,box=r
    scores=[]
    for fam,(reg,bold,ital,bi) in FONTS.items():
        for style,path in [("r",reg),("b",bold),("i",ital),("bi",bi)]:
            for size in range(11,42):
                rm=render_mask(text,path,size)
                if rm is None: continue
                # compare aspect-ratio-normalized shape: resize render to frame ink bbox size
                rz=Image.fromarray((rm*255).astype(np.uint8)).resize((fm.shape[1],fm.shape[0]),Image.LANCZOS)
                s=iou(fm,np.array(rz)>110)
                scores.append((s,fam,style,size))
    scores.sort(reverse=True)
    print(f"== {lbl}: frame ink w={fm.shape[1]} h={fm.shape[0]}")
    for (s,fam,style,size) in scores[:5]:
        print(f"    IoU={s:.3f}  {fam}-{style} {size}pt")
