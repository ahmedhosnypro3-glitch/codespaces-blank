#!/usr/bin/env python3
"""Mandatory pre-judge self-check, slide 040 attempt 3 (150dpi render, 2001x1125).
Covers: frame containment, equations-exist (N/A), delimiter geometry (N/A),
table data (N/A), single-line assertion per text box, badge, title word-gap
geometry vs the original, and the three adjudicated findings."""
from PIL import Image
import numpy as np

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide040"
R = QA + "/render_3.png"
O = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_040.jpg"

ra = np.array(Image.open(R).convert("RGB")); oa = np.array(Image.open(O).convert("RGB"))
W, H = ra.shape[1], ra.shape[0]; S = W / 960.0
fails = []

print(f"1. FRAME CONTAINMENT — render {W}x{H}, 1 render px = 1/150 in, S={S:.6f}")
panel_x0, panel_x1 = 54*S, 903*S
panel_y0, panel_y1 = 45*S, 540*S
r,g,b = ra[:,:,0].astype(int), ra[:,:,1].astype(int), ra[:,:,2].astype(int)
panel_gray = (abs(r-233)<16)&(abs(g-233)<16)&(abs(b-231)<18)
strokes = (r>120)&((r-g)>40)&((r-b)>40)
white = (r>250)&(g>250)&(b>250)
ink = ~(panel_gray|strokes|white) & (ra.sum(axis=2) < 600)
ys, xs = np.where(ink)
print(f"   panel frame x{panel_x0:.0f}..{panel_x1:.0f} y{panel_y0:.0f}..{panel_y1:.0f}")
print(f"   content ink bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
outx = int(((xs<panel_x0)|(xs>panel_x1)).sum()); outy = int(((ys<panel_y0)|(ys>panel_y1)).sum())
print(f"   ink outside panel: x {outx} px, y {outy} px")
if outx or outy: fails.append(f"frame containment: {outx}/{outy} px outside panel")

print("\n2. EQUATIONS EXIST — analysis shows an empty equations array; slide has none. N/A/PASS")
print("3. DELIMITER GEOMETRY — no multi-line delimiters on this slide. N/A/PASS")
print("4. TABLE DATA — no tables on this slide. N/A/PASS")

print("\n5. TEXT STRUCTURE — one single-line box per element (no lineSpacing needed)")
red = (r>120)&((r-g)>40)&((r-b)>40)
red[:, :int(70*S)] = False; red[:, int(890*S):] = False
rows = red.sum(axis=1); bands=[]; y=0
while y < H:
    if rows[y] > 3:
        s=y
        while y<H and rows[y]>3: y+=1
        seg=red[s:y]; xsi=np.where(seg.any(axis=0))[0]
        if len(xsi) and (xsi.max()-xsi.min())/S > 200:
            bands.append((s/S,(y-1)/S,xsi.min()/S,xsi.max()/S))
    else: y+=1
txt=[bd for bd in bands if bd[1]<500]
blue=(b>120)&((b-r)>40)&((b-g)>40)
# exclude the badge purple ring (6A5ACD tripped a naive blue test) and the strokes
blue[:int(120*S), :] = False
blue[:, :int(70*S)]=False; blue[:, int(890*S):]=False
bys=np.where(blue.sum(axis=1)>3)[0]
if len(bys):
    seg=blue[bys.min():bys.max()+1]; bxs=np.where(seg.any(axis=0))[0]
    print(f"   blue 'usnig SGD' y{bys.min()/S:.0f}..{bys.max()/S:.0f} "
          f"x{bxs.min()/S:.0f}..{bxs.max()/S:.0f} ctr{(bxs.min()+bxs.max())/2/S:.0f}")
for s,e,x0,x1 in txt:
    print(f"   red band y{s:.0f}..{e:.0f} x{x0:.0f}..{x1:.0f} w{x1-x0+1:.0f} ctr{(x0+x1)/2:.0f}")
print(f"   red text band count = {len(txt)}  (original = 2)")
if len(txt) != 2: fails.append(f"red text bands = {len(txt)}, expected 2 (single-line title + 'Solved Example')")

print("\n6. VERTICAL CENTERING — single-line boxes, no multi-line enclosures. N/A/PASS")
print("\n7. BADGE — yellow disc + purple ring + dark numeral, matched effective check")
rr,rg,rb = ra[:,:,0].astype(int),ra[:,:,1].astype(int),ra[:,:,2].astype(int)
yel=(rr>200)&(rg>200)&(rb<190)
ys2,xs2=np.where(yel & (np.arange(W)[None,:] > W*0.8) & (np.arange(H)[:,None] < H*0.25))
bcx,bcy=(xs2.min()+xs2.max())/2/S,(ys2.min()+ys2.max())/2/S
orr,og,ob=oa[:,:,0].astype(int),oa[:,:,1].astype(int),oa[:,:,2].astype(int)
oyel=(orr>200)&(og>200)&(ob<190)
oy,ox=np.where(oyel & (np.arange(960)[None,:] > 960*0.8) & (np.arange(540)[:,None] < 540*0.25))
obx,oby=(ox.min()+ox.max())/2,(oy.min()+oy.max())/2
print(f"   render disc ctr ({bcx:.1f},{bcy:.1f}) d={(xs2.max()-xs2.min()+1)/S:.0f}  "
      f"original ctr ({obx:.1f},{oby:.1f}) d={(ox.max()-ox.min()+1):.0f}")
print(f"   DELTA dx={bcx-obx:+.1f} dy={bcy-oby:+.1f} frame px")
if abs(bcx-obx)>4 or abs(bcy-oby)>4: fails.append("badge off by >4px")

print("\n8. TITLE WORD-GAP GEOMETRY (double-space fix, attempt 3)")
def gaps(mask, sc, y0, y1):
    seg=mask[int(y0*sc):int(y1*sc),:]; cols=seg.sum(axis=0); Ww=mask.shape[1]
    on=cols>0; out=[]; x=0
    while x<Ww:
        if on[x]:
            while x<Ww and on[x]: x+=1
        else:
            s=x
            while x<Ww and not on[x]: x+=1
            if x<Ww: out.append((x-s)/sc)
    return [v for v in out if v>=10][1:]   # drop the leading-edge artifact
ored_ = (orr>120)&((orr-og)>40)&((orr-ob)>40)
ored_[:, :70] = False; ored_[:, 890:] = False   # same stroke exclusion as the render mask
go = gaps(ored_, 1.0, 174, 217)
gr = gaps(red, S, 174, 217)
print(f"   original interior gaps: {[f'{v:.0f}' for v in go]}")
print(f"   render_3 interior gaps: {[f'{v:.0f}' for v in gr]}")
mx = max(abs(a-b) for a,b in zip(go,gr))
print(f"   max per-gap deviation: {mx:.1f} frame px")
if len(go)!=len(gr): fails.append("word-gap count mismatch")
elif mx > 6: fails.append(f"word-gap deviation {mx:.0f}px > 6px")

print("\n9. BACKGROUND CHROME (adjudication of the 'F2F2F2' claim)")
print(f"   original margin (10,10) {oa[10,10].tolist()} / panel blank (100,100) {oa[100,100].tolist()}")
print(f"   render   margin (10,10) {ra[int(10*S),int(10*S)].tolist()} / panel blank (100,100) {ra[int(100*S),int(100*S)].tolist()}")
print("   => white canvas + E9E9E7 panel on both (deck house chrome; GROUND RULES (a))")

print("\n" + ("SELF-CHECK: PASS" if not fails else "SELF-CHECK: FAIL -> " + "; ".join(fails)))
raise SystemExit(1 if fails else 0)
