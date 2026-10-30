#!/usr/bin/env python3
"""slide_007 original — pure-color line fits, hatch orientation, label blobs, dots."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# ---------- pure saturated inks ----------
pure_red   = (R>170)&(G<95)&(B<95)
pure_green = (G>105)&(R<95)&(B<95)
pure_blue  = (B>165)&(R<95)&(G<105)

print("=== RED: per-row pure-red x runs (plot y122..504) ===")
for r in range(122, 505, 6):
    xs = np.where(pure_red[r, 160:800])[0] + 160
    if len(xs) == 0: continue
    runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>4: runs.append((int(s),int(p))); s=x
        p=x
    runs.append((int(s),int(p)))
    print(f"  y={r}: {runs}")

print("\n=== GREEN: per-row pure-green x runs ===")
for r in range(122, 505, 6):
    xs = np.where(pure_green[r, 160:800])[0] + 160
    if len(xs) == 0: continue
    runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>4: runs.append((int(s),int(p))); s=x
        p=x
    runs.append((int(s),int(p)))
    print(f"  y={r}: {runs}")

print("\n=== BLUE: per-row pure-blue x runs ===")
for r in range(122, 505, 6):
    xs = np.where(pure_blue[r, 160:800])[0] + 160
    if len(xs) == 0: continue
    runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>4: runs.append((int(s),int(p))); s=x
        p=x
    runs.append((int(s),int(p)))
    print(f"  y={r}: {runs}")

print("\n=== hatch stroke orientation test: run lengths of tinted strokes in a C1 patch ===")
# green hatch region near (x520..600, y150..200)? use band y=160..190 x=430..520
tint = (G>R+6)&(G>B+6)
patch = tint[150:200, 430:520]
rowsum = patch.sum(axis=1); colsum = patch.sum(axis=0)
print("  green-tint row counts (y150-199):", rowsum.tolist())
print("  green-tint col counts (x430-519):", colsum.tolist())

print("\n=== blue hatch patch row/col counts (x620..780,y340..430) ===")
tb = (B>R+6)&(B>G+6)
p2 = tb[340:430, 620:780]
print("  rows:", p2.sum(axis=1).tolist())
print("  cols:", p2.sum(axis=0).tolist())

print("\n=== red/pink hatch patch row/col counts (x250..380,y420..490) ===")
tr = (R>G+6)&(R>B+3)
p3 = tr[420:490, 250:380]
print("  rows:", p3.sum(axis=1).tolist())
print("  cols:", p3.sum(axis=0).tolist())

print("\n=== colored TEXT blobs (saturated) inside plot, excluding long thin strokes ===")
for name, m in [("red", pure_red), ("green", pure_green), ("blue", pure_blue)]:
    mm = m.copy(); mm[:122,:]=False; mm[505:,:]=False; mm[:,:160]=False; mm[:,800:]=False
    lab, n = ndimage.label(mm, structure=np.ones((3,3)))
    sizes = ndimage.sum(mm, lab, range(1,n+1))
    print(f"  {name}: {n} comps")
    for i in np.argsort(sizes)[::-1][:14]:
        if sizes[i] < 20: break
        yy, xx = np.where(lab == i+1)
        w_, h_ = xx.max()-xx.min()+1, yy.max()-yy.min()+1
        fill = sizes[i]/(w_*h_)
        print(f"    area={int(sizes[i]):5d} bbox x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} "
              f"({w_}x{h_}) fill={fill:.2f}")
