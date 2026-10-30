#!/usr/bin/env python3
"""HEAD-TO-HEAD (w9-s027-20261021T0400): does render_4 reproduce the original's
thin neutral-gray ribbon along the upper-left dot chain, or does it under-ink it?
Applies IDENTICAL neutral-gray / far-from-dark-core methodology to BOTH images at
render resolution (original upscaled LANCZOS to match effective scale).
Decision: Scenario X (render reproduces ribbon -> no missing element; the
dying worker's discrete triangle-arrow drawing is a fabrication) vs
Scenario Y (render lacks a real gray feature -> but the feature is a ribbon,
not arrows, so the correct reading is still 'no fabricated arrows').
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA   = BASE + "/recreated_pptx/qa/slide027"
W,H = 2001,1125; sc=(W/960.0+H/540.0)/2.0
orig_up = Image.open(BASE+"/unique_slides/slide_027.jpg").convert("RGB").resize((W,H),Image.LANCZOS)
R = np.asarray(Image.open(QA+"/render_4.png").convert("RGB")).astype(np.int16)
O = np.asarray(orig_up).astype(np.int16)

def masks(a):
    rr,gg,bb=a[...,0],a[...,1],a[...,2]
    lum=0.299*rr+0.587*gg+0.114*bb
    neut=(np.abs(rr.astype(int)-gg)<14)&(np.abs(gg.astype(int)-bb)<14)&(np.abs(rr.astype(int)-bb)<14)
    grayband=neut&(lum>=120)&(lum<=204)
    core=(lum<95)
    return grayband,core,lum
def dil(mask,fpx):
    n=int(round(fpx*sc))*2+1
    return np.asarray(Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n)))>0

def far_gray(a,D):
    g,c,_=masks(a); return g & ~dil(c,D)

dots=[(262,263.5),(283,310.5),(306.5,342),(332,366.5),(354.5,380.5),(374.5,390),(392,396.5),(411,403.5),(426.5,403.5)]
xr=lambda v: v*W/960.0; yr=lambda v: v*H/540.0
def box(m,c0,c1,pad=5):
    x0,x1=sorted([xr(c0[0]-pad),xr(c1[0]+pad)]); y0,y1=sorted([yr(c0[1]-pad),yr(c1[1]+pad)])
    out=np.zeros((H,W),bool); out[int(y0):int(y1),int(x0):int(x1)]=True; return out
def chain_box(m,x0f,x1f,y0f,y1f):
    out=np.zeros((H,W),bool); out[int(yr(y0f)):int(yr(y1f)),int(xr(x0f)):int(xr(x1f))]=True; return out

print("="*74); print("HEAD-TO-HEAD far-gray ribbon: ORIGINAL vs RENDER_4 (both at render res)")
print(f"neutral-gray band lum120..204, excluded >{ '{:.0f}'.format(3*sc) }rpx (~3fpx) from lum<95 core"); print("="*74)
for D in (3,4,6):
    fo=far_gray(O,D); fr=far_gray(R,D)
    print(f"\nD={D} fpx   per-window far-gray px (ORIGINAL | RENDER_4):")
    to=tr=0
    for i in range(8):
        b=box(None,dots[i],dots[i+1])
        o=int((fo&b).sum()); r=int((fr&b).sum()); to+=o; tr+=r
        print(f"   dot{i+1}->dot{i+2}: {o:>4} | {r:>4}")
    print(f"   TOTAL 8 windows: ORIG {to}  RENDER {tr}   (render/orig = {tr/max(to,1):.2f})")
    # full left-branch ribbon vs right branch, both images
    blob = chain_box(None,248,436,228,410); rbr=chain_box(None,458,646,228,410)
    print(f"   left-branch chain-box far-gray:  ORIG {int((fo&blob).sum())}  RENDER {int((fr&blob).sum())}")
    print(f"   right-branch   chain-box far-gray: ORIG {int((fo&rbr).sum())}  RENDER {int((fr&rbr).sum())}")
    # connected-ribbon morphology, original vs render, whole left chain
    lo,_=ndimage.label if False else (0,0)
    fgo=fo&blob; fgr=fr&blob
    def nc(m):
        l,n=ndimage.label(m); return n
    print(f"   left-chain far-gray components:    ORIG {nc(fgo)}  RENDER {nc(fgr)}")

# ASCII of RENDER far-gray in the dot2->dot3 gap (compare to original ribbon)
fo=far_gray(O,6); fr=far_gray(R,6)
co=(masks(O)[2]<95); cr=(masks(R)[2]<95)
x0,x1=int(xr(277)),int(xr(312)); y0,y1=int(yr(302)),int(yr(350))
def imap(fg,core,label):
    print(f"\n{label}")
    sub_fg=fg[y0:y1,x0:x1]; sub_c=core[y0:y1,x0:x1]
    for r in range(sub_fg.shape[0]):
        print("   "+"".join('@' if sub_c[r,cc] else ('g' if sub_fg[r,cc] else '.') for cc in range(sub_fg.shape[1])))
imap(fr,cr,"RENDER_4 far-gray map  dot2->dot3  (@dark-core gfar-gray)")
print("\nDONE.")
