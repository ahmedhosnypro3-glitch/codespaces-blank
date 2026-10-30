#!/usr/bin/env python3
"""Combined fit: advance width must match the frame ink width (+-2px), then
shape IoU (each normalized to its own ink bbox) ranks font/style/size."""
import numpy as np, os
from PIL import Image, ImageDraw, ImageFont
IM='/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a=np.array(Image.open(IM)).astype(int)
BG={'panel':[233,233,231],'green':[208,254,226],'blue':[249,252,255],'yellow':[250,253,226]}
def framemask(y0,y1,x0,x1,bg,thr=150):
    d=np.abs(a[y0:y1+1,x0:x1+1]-np.array(bg)).sum(axis=2); m=d>thr
    ys,xs=np.where(m)
    return (m[ys.min():ys.max()+1,xs.min():xs.max()+1],(int(xs.min()+x0),int(xs.max()+x0),int(ys.min()+y0),int(ys.max()+y0))) if len(xs) else None
F={'Arial':('/usr/share/fonts/TTF/Arial.TTF','/usr/share/fonts/TTF/Arialbd.TTF','/usr/share/fonts/TTF/Ariali.TTF','/usr/share/fonts/TTF/Arialbi.TTF'),
   'Verdana':('/usr/share/fonts/TTF/Verdana.TTF','/usr/share/fonts/TTF/Verdanab.TTF','/usr/share/fonts/TTF/Verdanai.TTF','/usr/share/fonts/TTF/Verdanai.TTF'),
   'Calibri':('/usr/share/fonts/TTF/calibri.ttf','/usr/share/fonts/TTF/calibrib.ttf','/usr/share/fonts/TTF/calibrii.ttf','/usr/share/fonts/TTF/calibriz.ttf'),
   'Carlito':('/usr/share/fonts/carlito/Carlito-Regular.ttf','/usr/share/fonts/carlito/Carlito-Bold.ttf','/usr/share/fonts/carlito/Carlito-Italic.ttf','/usr/share/fonts/carlito/Carlito-BoldItalic.ttf'),
   'LibSans':('/usr/share/fonts/liberation/LiberationSans-Regular.ttf','/usr/share/fonts/liberation/LiberationSans-Bold.ttf','/usr/share/fonts/liberation/LiberationSans-Italic.ttf','/usr/share/fonts/liberation/LiberationSans-BoldItalic.ttf')}
F={k:[p for p in v if os.path.exists(p)] for k,v in F.items()}
SC=4
def rmask(text,path,size):
    f=ImageFont.truetype(path,size*SC)
    im=Image.new('L',(len(text)*size*SC+80,size*SC*3),0); ImageDraw.Draw(im).text((20,size*SC),text,font=f,fill=255)
    m=np.array(im)>128; ys,xs=np.where(m)
    return m[ys.min():ys.max()+1,xs.min():xs.max()+1] if len(xs) else None
def iou(A,B):
    H=max(A.shape[0],B.shape[0]); W=max(A.shape[1],B.shape[1])
    def c(M):
        o=np.zeros((H,W),bool); y=(H-M.shape[0])//2; x=(W-M.shape[1])//2
        o[y:y+M.shape[0],x:x+M.shape[1]]=M; return o
    A=c(A);B=c(B); return (A&B).sum()/max((A|B).sum(),1)
LINES=[("TITLE",74,108,215,660,'panel',"Inverse of High Dimension Matrix"),
 ("RECALL",114,140,100,180,'green',"Recall:"),
 ("DIM1",190,217,100,400,'green',"if Feature vectors are of dimension d"),
 ("DIM2",190,217,500,760,'green',"(X^T X) is of size d+1 x d+1"),
 ("BLUE1",238,266,95,860,'blue',"The standard matrix inversion algorithm has a time"),
 ("EX1",358,390,92,860,'blue',"For Example: if Features vector is of size 1000 then"),
 ("EX2",394,424,92,560,'blue',"Inverse calculation is or order 1,000,000,000 which is impractical"),
 ("SOLLBL",444,468,95,420,'yellow',"Solution:"),
 ("SOLL1",470,500,230,790,'yellow',"Instead of using Least Squares with Matrix inversion,"),
 ("SOLL2",500,532,285,705,'yellow',"use Gradient Descent iterative solution")]
for (lbl,y0,y1,x0,x1,bg,text) in LINES:
    r=framemask(y0,y1,x0,x1,BG[bg])
    if not r: print(lbl,"NO INK"); continue
    fm,box=r; fw=box[1]-box[0]+1; fh=box[3]-box[2]+1
    out=[]
    for fam,(reg,bold,ital,bi) in F.items():
        for style,path in [("r",reg),("b",bold),("i",ital),("bi",bi)]:
            for size in range(11,44):
                f=ImageFont.truetype(path,size*SC); adv=f.getlength(text)/SC
                if abs(adv-fw)>2: continue
                rm=rmask(text,path,size)
                if rm is None: continue
                dh=abs(rm.shape[0]-fh)
                out.append((iou(fm,rm)-0.01*dh,fam,style,size,round(adv),rm.shape[0]))
    out.sort(reverse=True)
    print(f"== {lbl}: frame w={fw} h={fh}")
    for (s,fam,style,size,adv,h) in out[:4]:
        print(f"    score={s:.3f} {fam}-{style} {size}pt adv={adv} h={h}")
