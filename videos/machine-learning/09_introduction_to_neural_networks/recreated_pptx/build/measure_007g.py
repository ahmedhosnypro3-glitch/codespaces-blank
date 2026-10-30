#!/usr/bin/env python3
"""slide_007 original — comprehensive: robust line fits, axes, arrowheads,
'+ve' text blobs, d-label blobs, region-hatch semantics, dot inventory."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

pure_red   = (R>170)&(G<95)&(B<95)
pure_green = (G>105)&(R<95)&(B<95)
pure_blue  = (B>165)&(R<95)&(G<105)
black      = (R<90)&(G<90)&(B<90)

PLOT = (168, 795, 122, 504)

def ascii_map(mask, x0, x1, y0, y1, label):
    print(f"  --- {label}  x{x0}-{x1} y{y0}-{y1} ---")
    hdr = "      " + "".join(str((x0+i)//10%10) for i in range(x1-x0+1))
    hdr2 = "      " + "".join(str((x0+i)%10) for i in range(x1-x0+1))
    print(hdr); print(hdr2)
    for y in range(y0, y1+1):
        row = "".join("#" if mask[y, x] else "." for x in range(x0, x1+1))
        print(f"  {y:4d} {row}")

def runs_at(mask, r, x0=160, x1=800, gap=4):
    xs = np.where(mask[r, x0:x1])[0] + x0
    if len(xs) == 0: return []
    out=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>gap: out.append((int(s),int(p))); s=x
        p=x
    out.append((int(s),int(p)))
    return out

print("="*70); print("A. TITLE BANDS (word segmentation)"); print("="*70)
title = (R>110)&(R-G>60)&(R-B>60)
titleb = (B>110)&(B-R>60)&(B-G>60)
for lo, hi in [(50, 80), (80, 108)]:
    print(f"\n line band y{lo}-{hi}")
    for nm, m in [("red", title), ("blue", titleb)]:
        xs = np.where(m[lo:hi+1].any(axis=0))[0]
        if len(xs)==0: continue
        segs=[]; s=xs[0]; p=xs[0]
        for x in xs[1:]:
            if x-p>6: segs.append((int(s),int(p))); s=x
            p=x
        segs.append((int(s),int(p)))
        print(f"   {nm}: {segs}")

print("\n" + "="*70); print("B. RED AXIS (vertical) extent"); print("="*70)
colmask = pure_red[:, 305:316].sum(axis=1)
ys = np.where(colmask>0)[0]
segs=[]; s=ys[0]; p=ys[0]
for y in ys[1:]:
    if y-p>3: segs.append((int(s),int(p))); s=y
    p=y
segs.append((int(s),int(p)))
print("  red rows in x305-315:", segs)
ascii_map(pure_red, 300, 322, 130, 155, "red vertical axis top (arrowhead?)")

print("\n" + "="*70); print("C. RED HORIZONTAL AXIS extent"); print("="*70)
for r in [432, 433, 434, 435, 436, 437, 438]:
    print(f"  y={r}: {runs_at(pure_red, r, 160, 800)}")
ascii_map(pure_red, 640, 690, 424, 446, "red horiz axis right end (arrowhead?)")

print("\n" + "="*70); print("D. RED d1 diagonal — full-res trace (x<320 region)"); print("="*70)
for r in range(190, 275, 2):
    print(f"  y={r}: {runs_at(pure_red, r, 200, 330)}")

print("\n" + "="*70); print("E. ARROWHEAD REGIONS (ascii)"); print("="*70)
ascii_map(pure_red, 512, 552, 438, 472, "red arrowhead near bottom")
ascii_map(pure_blue, 648, 690, 124, 152, "blue arrowhead at top-right")
ascii_map(pure_green, 236, 276, 360, 392, "green arrowhead at left?")

print("\n" + "="*70); print("F. BLACK text components in plot (label + '+ve')"); print("="*70)
bm = black.copy(); bm[:125,:]=False; bm[505:,:]=False; bm[:,:170]=False; bm[:,795:]=False
lab, n = ndimage.label(bm, structure=np.ones((3,3)))
sizes = ndimage.sum(bm, lab, range(1, n+1))
groups = []
for i in np.argsort(sizes)[::-1]:
    if sizes[i] < 15: break
    yy, xx = np.where(lab == i+1)
    groups.append((int(sizes[i]), int(xx.min()), int(xx.max()), int(yy.min()), int(yy.max())))
for g in sorted(groups, key=lambda t: (t[3], t[1])):
    print(f"   area={g[0]:5d} bbox x {g[1]}-{g[2]} y {g[3]}-{g[4]}  (w{g[2]-g[1]+1} h{g[4]-g[3]+1})")

print("\n" + "="*70); print("G. COLORED label blobs (d1/d2/d3 text + C-box glyphs)"); print("="*70)
for nm, m in [("green", pure_green), ("blue", pure_blue), ("red", pure_red)]:
    mm = m.copy(); mm[:125,:]=False; mm[505:,:]=False; mm[:,:170]=False; mm[:,795:]=False
    lab, n = ndimage.label(mm, structure=np.ones((3,3)))
    sizes = ndimage.sum(mm, lab, range(1, n+1))
    print(f"  {nm}:")
    for i in np.argsort(sizes)[::-1]:
        if sizes[i] < 22: break
        yy, xx = np.where(lab == i+1)
        w_, h_ = xx.max()-xx.min()+1, yy.max()-yy.min()+1
        if w_ > 30 or h_ > 30:
            print(f"    area={int(sizes[i]):5d} BIG bbox x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} ({w_}x{h_}) fill={sizes[i]/(w_*h_):.2f}")

print("\n" + "="*70); print("H. REGION SEMANTICS — sample hue at probe points"); print("="*70)
probes = {
  "C1 box centre (545,170)": (545,170),
  "top-left above all (250,160)": (250,160),
  "C2 box centre (615,312)": (615,312),
  "right of d3 (760,300)": (760,300),
  "C3 box centre (281,412)": (281,412),
  "lower-left (230,470)": (230,470),
  "below d1 near (600,500)": (600,500),
  "below d2 right (700,420)": (700,420),
  "between d1 d2 (350,350)": (350,350),
  "above d1 left (200,300)": (200,300),
}
for nm, (x, y) in probes.items():
    patch = a[max(0,y-4):y+5, max(0,x-4):x+5].reshape(-1,3)
    mn = patch.mean(axis=0)
    print(f"  {nm:32s} mean rgb ({mn[0]:5.1f},{mn[1]:5.1f},{mn[2]:5.1f})  -> "
          f"{'GREEN' if mn[1]>mn[0]+3 and mn[1]>mn[2]+3 else ('BLUE' if mn[2]>mn[0]+3 and mn[2]>mn[1]+3 else ('RED/PINK' if mn[0]>mn[1]+3 else 'WHITE'))}")

print("\n" + "="*70); print("I. DOT INVENTORY (saturated blobs, 25..500 in plot, exclude lines)"); print("="*70)
def dots(m, exclude):
    mm = m.copy(); mm[:125,:]=False; mm[505:,:]=False; mm[:,:170]=False; mm[:,795:]=False
    for (x0,x1,y0,y1) in exclude:
        mm[y0:y1+1, x0:x1+1] = False
    lab, n = ndimage.label(mm, structure=np.ones((3,3)))
    sizes = ndimage.sum(mm, lab, range(1, n+1))
    out=[]
    for i in np.argsort(sizes)[::-1]:
        if sizes[i] < 120: break
        yy, xx = np.where(lab == i+1)
        w_, h_ = xx.max()-xx.min()+1, yy.max()-yy.min()+1
        out.append((int(xx.mean()), int(yy.mean()), int(sizes[i]), w_, h_))
    return sorted(out, key=lambda t:(t[1], t[0]))
for nm, m in [("green", pure_green), ("blue", pure_blue), ("red", pure_red)]:
    print(f"  {nm} dots:")
    for d in dots(m, exclude=[]):
        print(f"     x={d[0]:3d} y={d[1]:3d} area={d[2]:4d} size {d[3]}x{d[4]}")
