#!/usr/bin/env python3
"""Compare my render vs the original: measure key element presence + geometry."""
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/qa/slide029/original.jpg"
REND = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/qa/slide029/render_1.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
print("orig", o.shape, "render", r.shape)

H, W = o.shape[:2]
OH, OW = r.shape[:2]
print(f"orig {W}x{H}  render {OW}x{OH}")

def report(name, mask_o, mask_r, label=""):
    no, nr = mask_o.sum(), mask_r.sum()
    print(f"{name:34s} orig_px={no:7d} ({no/(W*H)*100:5.2f}%)  rend_px={nr:7d} ({nr/(OW*OH)*100:5.2f}%)")

# normalize both to canvas of same size for fraction compare
def norm(mask, shape):
    im = Image.fromarray((mask*255).astype(np.uint8)).resize((400, 225), Image.BILINEAR)
    return np.asarray(im) > 100

# 1. red frame: outer border pixels
def red_dom(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (R>120)&(R-G>50)&(R-B>50)

ro, rr = red_dom(o), red_dom(r)
print("\n--- red-dominant ---")
print("orig red col-runs (frame left/right + error bar):")
c = ro.sum(axis=0); runs=[]; inr=False
for x in range(W):
    if c[x] > 100:
        if not inr: st=x; inr=True
    else:
        if inr: runs.append((st,x-1)); inr=False
if inr: runs.append((st,W-1))
print("  ", [(a,b,round(a/W*100,1),round(b/W*100,1)) for a,b in runs])
print("rend red col-runs:")
c = rr.sum(axis=0); runs=[]; inr=False
for x in range(OW):
    if c[x] > 100:
        if not inr: st=x; inr=True
    else:
        if inr: runs.append((st,x-1)); inr=False
if inr: runs.append((st,OW-1))
print("  ", [(a,b,round(a/OW*100,1),round(b/OW*100,1)) for a,b in runs])

print("\norig red row-runs:")
c = ro.sum(axis=1); runs=[]; inr=False
for y in range(H):
    if c[y] > 200:
        if not inr: st=y; inr=True
    else:
        if inr: runs.append((st,y-1)); inr=False
if inr: runs.append((st,H-1))
print("  ", [(a,b,round(a/H*100,1),round(b/H*100,1)) for a,b in runs])
print("rend red row-runs:")
c = rr.sum(axis=1); runs=[]; inr=False
for y in range(OH):
    if c[y] > 200:
        if not inr: st=y; inr=True
    else:
        if inr: runs.append((st,y-1)); inr=False
if inr: runs.append((st,OH-1))
print("  ", [(a,b,round(a/OH*100,1),round(b/OH*100,1)) for a,b in runs])

# 2. green-dominant
def gr_dom(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (G>110)&(G-R>40)&(G-B>25)
print("\n--- green-dominant (class boxes + current layer + green callout) ---")
go, gr_ = gr_dom(o), gr_dom(r)
print("orig:", go.sum(), "rend:", gr_.sum())
for x in range(W):
    pass
def colruns(mask, Wd, thr):
    c = mask.sum(axis=0); runs=[]; inr=False
    for x in range(Wd):
        if c[x] > thr:
            if not inr: st=x; inr=True
        else:
            if inr: runs.append((st,x-1)); inr=False
    if inr: runs.append((st,Wd-1))
    return [(a,b) for a,b in runs if b-a>2]
print("orig green col-runs:", colruns(go, W, 20))
print("rend green col-runs:", colruns(gr_, OW, 20))
print("orig green row-runs:", colruns(go.T, H, 20))
print("rend green row-runs:", colruns(gr_.T, OH, 20))

# 3. blue-dominant
def bl_dom(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (B>120)&(B-R>45)&(B-G>25)
print("\n--- blue-dominant (previous layer callout, w_ji, node outlines) ---")
bo, br = bl_dom(o), bl_dom(r)
print("orig:", bo.sum(), "rend:", br.sum())

# 4. magenta
def mg_dom(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (R>140)&(B>130)&(R-G>40)&(B-G>35)
print("\n--- magenta (input/target boxes) ---")
mo, mr = mg_dom(o), mg_dom(r)
for x in range(W):
    pass
print("orig magenta col-runs:", colruns(mo, W, 25))
print("rend magenta col-runs:", colruns(mr, OW, 25))
print("orig magenta row-runs:", colruns(mo.T, H, 25))
print("rend magenta row-runs:", colruns(mr.T, OH, 25))

# 5. pale yellow (formula boxes)
def yl_dom(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (R>245)&(G>245)&(B<240)&(B>200)
print("\n--- pale yellow (formula boxes) ---")
yo, yr = yl_dom(o), yl_dom(r)
print("orig:", yo.sum(), "(%0.2f%%)"%(yo.sum()/(W*H)*100), "rend:", yr.sum(), "(%0.2f%%)"%(yr.sum()/(OW*OH)*100))
print("orig yellow col-runs:", colruns(yo, W, 10))
print("rend yellow col-runs:", colruns(yr, OW, 10))
print("orig yellow row-runs:", colruns(yo.T, H, 10))
print("rend yellow row-runs:", colruns(yr.T, OH, 10))

# 6. beige panel
def bg_dom(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (abs(R-226)<26)&(abs(G-218)<26)&(abs(B-200)<34)
print("\n--- beige panel (diagram + legend) ---")
bo2, br2 = bg_dom(o), bg_dom(r)
print("orig:", bo2.sum(), "(%0.2f%%)"%(bo2.sum()/(W*H)*100), "rend:", br2.sum(), "(%0.2f%%)"%(br2.sum()/(OW*OH)*100))

# 7. Circle badge (yellow) top-right
print("\n--- yellow badge region check (top-right ~12.48/13.33..12.98, 0.30..0.80) ---")
def slice_pct(mask, Wd, Hd, x0,x1,y0,y1):
    return mask[int(y0/100*Hd):int(y1/100*Hd), int(x0/100*Wd):int(x1/100*Wd)].sum()
def yellow(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (R>245)&(G>235)&(B<215)&(B>150)
for name, m, Wd, Hd in [("orig", yellow(o), W, H), ("rend", yellow(r), OW, OH)]:
    print(f"  {name} badge area px:", slice_pct(m, Wd, Hd, 93.4, 97.5, 4.0, 10.5))

# 8. Title text presence (top band dark red text)
print("\n--- dark-red text in title band ---")
def dr_text(a):
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    return (R>150)&(R-G>60)&(R-B>60)
print("orig:", slice_pct(dr_text(o), W, H, 30, 70, 8, 16))
print("rend:", slice_pct(dr_text(r), OW, OH, 30, 70, 2.5, 10))
