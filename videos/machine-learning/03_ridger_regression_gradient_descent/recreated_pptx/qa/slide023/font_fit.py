#!/usr/bin/env python3
"""Definitive per-line font fit for slide_023: measured ink box vs candidate
fonts (advance width AND cap/x-height of a probe glyph). 960x540, 1px=1pt."""
import numpy as np
from PIL import Image, ImageFont

IM='/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a=np.array(Image.open(IM)).astype(int)
BGS={'panel':[233,233,231],'green':[208,254,226],'blue':[249,252,255],'yellow':[250,253,226]}
def inkbox(y0,y1,x0,x1,bg,thr=170):
    d=np.abs(a[y0:y1+1,x0:x1+1]-np.array(bg)).sum(axis=2)
    m=d>thr
    ys,xs=np.where(m)
    if not len(xs): return None
    return (int(xs.min()+x0),int(xs.max()+x0),int(ys.min()+y0),int(ys.max()+y0))
FONTS={
 'Arial':('/usr/share/fonts/TTF/Arial.TTF','/usr/share/fonts/TTF/Arialbd.TTF','/usr/share/fonts/TTF/Ariali.TTF'),
 'Verdana':('/usr/share/fonts/TTF/Verdana.TTF','/usr/share/fonts/TTF/Verdanab.TTF','/usr/share/fonts/TTF/Verdanai.TTF'),
 'Calibri':('/usr/share/fonts/TTF/calibri.ttf','/usr/share/fonts/TTF/calibrib.ttf','/usr/share/fonts/TTF/calibrii.ttf'),
 'Carlito':('/usr/share/fonts/carlito/Carlito-Regular.ttf','/usr/share/fonts/carlito/Carlito-Bold.ttf','/usr/share/fonts/carlito/Carlito-Italic.ttf'),
 'LibSans':('/usr/share/fonts/liberation/LiberationSans-Regular.ttf','/usr/share/fonts/liberation/LiberationSans-Bold.ttf','/usr/share/fonts/liberation/LiberationSans-Italic.ttf'),
}
LINES=[
 # label, y0,y1,x0,x1, bg, text, probe(cap letter + its x window), redwords
 ("TITLE",   74,107,215,665,'panel',"Inverse of High Dimension Matrix",('I',216,236,72,108)),
 ("RECALL", 114,140,100,180,'green',"Recall:",('R',101,122,114,140)),
 ("DIMNOTE1",190,217,100,400,'green',"if Feature vectors are of dimension d",('F',296,320,190,217)),
 ("DIMNOTE2",190,217,500,760,'green',"(X^T X) is of size d+1 x d+1",('X',505,520,190,217)),
 ("BLUE1",  238,266, 95,860,'blue',"The standard matrix inversion algorithm has a time",('T',97,118,238,266)),
 ("BLUE2",  272,302, 95,860,'blue',"complexity O(n^3)",('T',96,120,272,302)),
 ("BLUE3",  304,338, 95,860,'blue',"",('I',97,112,304,338)),
 ("EX1",    358,390, 92,860,'blue',"Example: if n = 1000 inverting n x n matrix",('E',150,170,358,390)),
 ("EX2",    394,424, 92,560,'blue',"takes 1,000,000,000 operations",('t',180,200,394,424)),
 ("SOLLBL", 444,468, 95,420,'yellow',"Solution:",('S',96,112,444,468)),
 ("SOLL1",  470,500,230,790,'yellow',"Instead of using Least Squares with Matrix inversion,",('I',244,258,470,500)),
 ("SOLL2",  500,532,285,705,'yellow',"use Gradient Descent iterative solution",('G',288,306,500,532)),
]
for (lbl,y0,y1,x0,x1,bg,text,probe) in LINES:
    b=inkbox(y0,y1,x0,x1,BGS[bg])
    if not b:
        print(f"{lbl}: NO INK"); continue
    lx,rx,ty,by=b
    pb=inkbox(probe[3],probe[4],probe[1],probe[2],BGS[bg])
    ph = (pb[3]-pb[2]+1) if pb else None
    pw = (pb[1]-pb[0]+1) if pb else None
    print(f"{lbl:9s} ink x{lx}..{rx} y{ty}..{by} w={rx-lx+1} h={by-ty+1} | probe '{probe[0]}' w={pw} h={ph}")
    if not text: continue
    res=[]
    for fam,(reg,bold,ital) in FONTS.items():
        for style,path in [("r",reg),("b",bold),("i",ital)]:
            for size in range(10,44):
                f=ImageFont.truetype(path,size*4)
                adv=f.getlength(text)/4.0
                if abs(adv-(rx-lx+1))<=2:
                    # cap height of probe letter at this size
                    g=ImageFont.truetype(path,size*4)
                    im=Image.new('L',(int(adv)+60,size*4+60),0); d=ImageDraw=im # noqa
                    from PIL import ImageDraw as ID
                    dd=ID.Draw(im); dd.text((20,20),probe[0],font=g,fill=255)
                    mm=np.array(im)>128; yy,xx=np.where(mm)
                    gh=yy.max()-yy.min()+1 if len(yy) else 0
                    res.append((abs(gh-(ph or 0)),fam,style,size,round(adv,1),gh))
    res.sort()
    for (df,fam,style,size,adv,gh) in res[:4]:
        print(f"     -> {fam}-{style} {size}pt adv={adv} cap={gh}px (measured {ph})  dc={df}")
