#!/usr/bin/env python3
"""DECISIVE arbitration (w9-s027-20261021T0400): did the original frame genuinely
carry neutral-gray 'learning-step arrows' between the blue dots that the dying
worker (w8) claimed 'overturned' the attempt-3 refutation and drew into the live
build at 03:49?  Render_4 (the certified deliverable) has NO such arrows.

Method:
 1. Characterize the ORIGINAL's ink luminance inside the graph box (is the curve
    actually BLACK, or is it a mid-dark-gray video-captured stroke?).
 2. Build a NEUTRAL-gray mask (R~G~B, excludes violet dots/red/yellow) and a
    dark CORE mask; 'far-gray' = neutral gray farther than D frames-px from any
    dark core.  The worker's instrument: isolated gray, not stroke halo.
 3. MORPHOLOGY (the decisive test): count connected far-gray components over the
    WHOLE left-branch chain (dots present) vs a matched band of the RIGHT branch
    (same curve stroke, NO dots). Discrete arrowheads => ~8 separated components
    on the left AND ~0 on the right. A continuous AA ribbon of the SAME stroke =>
    a connected ribbon on BOTH branches.
 4. ASCII ink map of far-gray across two inter-dot gaps.
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA   = BASE + "/recreated_pptx/qa/slide027"
O = np.asarray(Image.open(BASE+"/unique_slides/slide_027.jpg").convert("RGB")).astype(np.int16)
H,W,_ = O.shape
Or,Og,Ob = O[...,0],O[...,1],O[...,2]
lum = 0.299*Or+0.587*Og+0.114*Ob
def dil(mask, fpx):
    n=int(fpx)*2+1
    return np.asarray(Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(n)))>0
def comps(mask, minsz):
    lbl,n=ndimage.label(mask)
    if n==0: return 0,0,[]
    sizes=ndimage.sum(np.ones_like(lbl),lbl,range(1,n+1))
    cents=ndimage.center_of_mass(np.ones_like(lbl),lbl,range(1,n+1))
    big=[(cents[i],sizes[i]) for i in range(n) if sizes[i]>=minsz]
    return int((sizes>=minsz).sum()), int(mask.sum()), big

print("="*74)
print("GRAY-ARROW HYPOTHESIS arbitration  (w9-s027-20261020T0400)".replace("T0400","T0400"))
print("ORIGINAL frame 960x540, native; NO upscale. Frame pixels.")
print("="*74)

# ---- 1. characterize ink luminance inside the graph box (x195..715,y169..505)
box = np.zeros((H,W),bool); box[169:506,195:716]=True
print("\n(1) ORIGINAL ink luminance inside graph box (saturated colors excluded):")
neut = (np.abs(Or.astype(int)-Og)<12)&(np.abs(Og.astype(int)-Ob)<12)&(np.abs(Or.astype(int)-Ob)<12)
mlum = lum[box&neut]
hist,edges = np.histogram(mlum, bins=[0,40,60,80,100,120,140,160,180,200,220,256])
for h,e in zip(hist,edges[:-1]):
    if h: print(f"    lum {e:>3}-{e+20:<3}: {h:>6} px")
print(f"    neutral-ink px total in box: {int((box&neut).sum())}; "
      f"lum<60 (deep black): {int((box&neut&(lum<60)).sum())}, "
      f"lum 120..204 (gray band): {int((box&neut&(lum>=120)&(lum<=204)).sum())}")

# ---- 2. neutral-gray mask + dark core
grayband = neut&(lum>=120)&(lum<=204)
core = (lum<95)                       # deepest stroke (black)
print(f"\n(2) neutral-gray px (lum120..204): {int(grayband.sum())}   dark-core (lum<95): {int(core.sum())}")

dots=[(262,263.5),(283,310.5),(306.5,342),(332,366.5),(354.5,380.5),(374.5,390),(392,396.5),(411,403.5),(426.5,403.5)]
yellow=(444.5,407)

def blkbox(c0,c1,pad=5):
    x0,x1=sorted([int(c0[0])-pad,int(c1[0])+pad]); y0,y1=sorted([int(c0[1])-pad,int(c1[1])+pad])
    m=np.zeros((H,W),bool); m[max(0,y0):y1,max(0,x0):x1]=True; return m

# ---- 3. MORPHOLOGY: connected far-gray components, L-branch chain vs R-branch
LB = np.zeros((H,W),bool); LB[int(228):int(410), int(248):int(436)]=True   # left branch w/ dots
RB = np.zeros((H,W),bool); RB[int(228):int(410), int(458):int(646)]=True    # right branch, no dots
print("\n(3) MORPHOLOGY — connected far-gray components (minsz>=8px), per far distance D:")
print(f"    {'D fpx':<6}{'LB comps':>10}{'LB px':>8}{'RB comps':>10}{'RB px':>8}   interpretation")
for D in (3,4,6,8):
    fg = grayband & ~dil(core,D)
    nlb,plb,_ = comps(fg&LB,8)
    nrb,prb,_ = comps(fg&RB,8)
    tag = "discrete arrows?" if (nlb>=6 and nrb<=1) else "continuous stroke halo (both branches)"
    print(f"    {D:<6}{nlb:>10}{plb:>8}{nrb:>10}{prb:>8}   {tag}")

# component centroids on the left branch (are they ~8 blob centres right of dots?)
fg = grayband & ~dil(core,6)
nlb,plb,biglb = comps(fg&LB,6)
print(f"\n    far-gray D=6 left-branch components >=6px: {nlb}; centroids/sizes (frame px):")
for c,s in sorted(biglb,key=lambda t:t[0][1]):
    print(f"       cy={c[0]:.0f} cx={c[1]:.0f}  size={int(s)}")

# ---- 4. ASCII far-gray map, gap dot2->dot3 and gap dot7->dot8
def ascii_gap(c0,c1,label):
    x0,x1=sorted([int(c0[0])-6,int(c1[0])+6]); y0,y1=sorted([int(c0[1])-8,int(c1[1])+8])
    sub=(grayband&~dil(core,6))[max(0,y0):y1,max(0,x0):x1]
    cm=(lum<95)[max(0,y0):y1,max(0,x0):x1]
    print(f"\n(4) far-gray map  {label}  (x{x0}..{x1}, y{y0}..{y1};  '.'=bg '@'=dark-core 'g'=far-gray)")
    for r in range(sub.shape[0]):
        row="".join('@' if cm[r,cc] else ('g' if sub[r,cc] else '.') for cc in range(sub.shape[1]))
        print("       "+row)
ascii_gap(dots[1],dots[2],"dot2->dot3")
ascii_gap(dots[6],dots[8],"dot7->dot8->dot9")

# ---- 5. reproduce the worker's 'far-gray = 256 px in windows, 0 off-chain' figure
print("\n(5) far-gray (D=6) totals — worker's 8 windows vs off-chain controls:")
tot_win=0
for i in range(8):
    d=int((fg&blkbox(dots[i],dots[i+1])).sum()); tot_win+=d
    print(f"       window dot{i+1}->dot{i+2}: {d} px")
ctrl_above = fg & (np.arange(H)[:,None]>=228)&(np.arange(H)[:,None]<=258)&(np.arange(W)[None,:]>=256)&(np.arange(W)[None,:]<=288)
ctrl_rbranch_clean = fg & RB
ctrl_empty = fg & (np.arange(H)[:,None]>=240)&(np.arange(H)[:,None]<=340)&(np.arange(W)[None,:]>=510)&(np.arange(W)[None,:]<=700)
print(f"       8 windows total: {tot_win}   above-dot1: {int(ctrl_above.sum())}   right-branch: {int(ctrl_rbranch_clean.sum())}   empty-box: {int(ctrl_empty.sum())}")

# ---- 6. DECISIVE: does the RIGHT branch carry the same-band gray (as it must if it is stroke AA)?
print("\n(6) right-branch (no dots) gray-band ink adjacent to its own dark stroke:")
# the right branch curve in the original; is there neutral gray hugging it just above the chord?
print("    If right-branch far-gray ~= left-branch scale relative to length -> the gray is the stroke's own AA halo,\n"
      "    NOT per-dot arrowheads.")
print("\nDONE.")
