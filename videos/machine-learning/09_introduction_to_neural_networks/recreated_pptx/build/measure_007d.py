#!/usr/bin/env python3
"""slide_007: outer layout (gray surround, red border), plot panel bounds,
and per-hatch-color region masks."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

print("=== GRAY surround E7E9E6 bbox ===")
gray = (abs(R-231)<8)&(abs(G-233)<8)&(abs(B-230)<8)
yy, xx = np.where(gray)
print(f"  n={len(yy)} bbox x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()}")

print("\n=== near-white FEFFFD bbox ===")
nw = (R>248)&(G>248)&(B>246)
lab, n = ndimage.label(nw)
sz = ndimage.sum(nw, lab, range(1, n+1))
order = np.argsort(sz)[::-1][:6]
for i in order:
    yy, xx = np.where(lab == i+1)
    print(f"  comp area={int(sz[i])} bbox x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()}")

print("\n=== column profile of gray at x=30 / x=940 (outside) ===")
for x in [5, 30, 57, 58, 59, 60, 100, 167, 168, 795, 796, 901, 902, 903, 930]:
    print(f"  x={x}: {a[100, x]}  y300:{a[300,x]}")

print("\n=== row profile at x=100 (outside plot) ===")
for y in [40, 45, 50, 53, 54, 110, 115, 120, 121, 122, 123, 500, 503, 504, 505, 506, 515, 516, 517, 518, 530]:
    print(f"  y={y}: {a[y, 100]}")

print("\n=== red border lines (saturated red) outside plot ===")
sred = (R>130)&(R-G>80)&(R-B>80)
cs = sred.sum(axis=0); rs = sred.sum(axis=1)
print("  cols >250:", [(int(c), int(cs[c])) for c in np.where(cs>250)[0]])
print("  rows >250:", [(int(r), int(rs[r])) for r in np.where(rs>250)[0]])
print("  cols >100:", [(int(c), int(cs[c])) for c in np.where(cs>100)[0]][:20])
print("  rows >100:", [(int(r), int(rs[r])) for r in np.where(rs>100)[0]][:20])

# ---- plot region hatch masks (restrict to x170..793, y124..502) ----
PX0, PX1, PY0, PY1 = 170, 793, 124, 502
reg = np.zeros_like(R, dtype=bool); reg[PY0:PY1+1, PX0:PX1+1] = True

print("\n=== HATCH COLOR MASKS inside plot ===")
masks = {}
masks["green"] = (G>80)&(G-R>35)&(G-B>35)&reg
masks["blue"]  = (B>90)&(B-R>50)&(B-G>40)&reg
masks["red"]   = (R>140)&(R-G>60)&(R-B>60)&reg

for name, m in masks.items():
    print(f"\n  --- {name}: n={int(m.sum())} ---")
    # per-row x extent
    for r in range(PY0, PY1+1, 24):
        xs = np.where(m[r])[0]
        if len(xs):
            # cluster x runs
            runs = []
            s = xs[0]; p = xs[0]
            for x in xs[1:]:
                if x-p > 12: runs.append((s,p)); s=x
                p=x
            runs.append((s,p))
            print(f"    y={r}: n={len(xs):5d} runs={[(int(a1),int(b1)) for a1,b1 in runs][:8]}")

print("\n=== per-row: fraction of plot row that is each hatch color (step 20 rows) ===")
print("   y    green%  blue%  red%")
for r in range(PY0, PY1+1, 20):
    row = slice(r, r+1)
    n = PX1-PX0+1
    g = masks["green"][row, PX0:PX1+1].sum()/n*100
    b = masks["blue"][row, PX0:PX1+1].sum()/n*100
    rr = masks["red"][row, PX0:PX1+1].sum()/n*100
    print(f"  {r:4d}  {g:6.1f}  {b:6.1f}  {rr:6.1f}")
