#!/usr/bin/env python3
"""Fine geometry of slide_007: frame box, red axes, three decision lines, fills."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

red   = (R>100)&(R-G>40)&(R-B>40)
green = (G>70)&(G-R>40)&(G-B>40)
blue  = (B>100)&(B-R>60)&(B-G>50)

print("=== FRAME-LIKE RED LINES over whole slide (very saturated red, thin) ===")
strong = (R>150)&(R-G>100)&(R-B>100)
colsum = strong.sum(axis=0); rowsum = strong.sum(axis=1)
print("cols with >200 strong-red px:", [(c, int(colsum[c])) for c in np.where(colsum>200)[0]])
print("rows with >200 strong-red px:", [(r, int(rowsum[r])) for r in np.where(rowsum>200)[0]])

PX0, PX1, PY0, PY1 = 168, 795, 122, 504
def within(m):
    o = np.zeros_like(m); o[PY0:PY1+1, PX0:PX1+1] = m[PY0:PY1+1, PX0:PX1+1]; return o

print("\n=== RED AXIS CANDIDATES inside panel ===")
rp = within(red)
cs = rp.sum(axis=0); rs = rp.sum(axis=1)
print(" red cols >100:", [(int(c), int(cs[c])) for c in np.where(cs>100)[0]])
print(" red rows >100:", [(int(r), int(rs[r])) for r in np.where(rs>100)[0]])

print("\n=== per-column red counts (panel), sorted top 20 ===")
print(sorted([(int(c), int(cs[c])) for c in np.argsort(cs)[::-1][:20]], key=lambda t:-t[1]))
print("=== per-row red counts (panel), sorted top 20 ===")
print(sorted([(int(r), int(rs[r])) for r in np.argsort(rs)[::-1][:20]], key=lambda t:-t[1]))

print("\n=== GREEN line: per-row x-extent of green pixels (panel) ===")
gp = within(green)
for r in range(PY0, PY1+1, 20):
    xs = np.where(gp[r])[0]
    if len(xs):
        print(f"   y={r}: n={len(xs)} x {xs.min()}-{xs.max()}")

print("\n=== BLUE line: per-row x-extent of blue pixels (panel) ===")
bp = within(blue)
for r in range(PY0, PY1+1, 20):
    xs = np.where(bp[r])[0]
    if len(xs):
        print(f"   y={r}: n={len(xs)} x {xs.min()}-{xs.max()}")

print("\n=== RED line: per-row x-extent of red pixels (panel) ===")
for r in range(PY0, PY1+1, 20):
    xs = np.where(rp[r])[0]
    if len(xs):
        print(f"   y={r}: n={len(xs)} x {xs.min()}-{xs.max()}")

print("\n=== FILL tint density map (panel, 12x10 blocks) ===")
def cls(px):
    r,g,b = px
    if r>235 and g>235 and b>235: return "."
    if g>r+6 and g>b+6: return "G"
    if b>r+6 and b>g+6: return "B"
    if r>g+6 and r>b+6: return "R"
    if r<90 and g<90 and b<90: return "K"
    if r>190 and g>160 and b<150: return "Y"
    return "?"
for by in range(PY0, PY1+1, 38):
    row = ""
    for bx in range(PX0, PX1+1, 63):
        blk = a[by:min(by+38,PY1+1), bx:min(bx+63,PX1+1)].reshape(-1,3)
        # majority non-white class
        cs_ = []
        for px in blk:
            cs_.append(cls(px))
        vals, cnts = np.unique(cs_, return_counts=True)
        # prefer non-'.' if enough
        order = np.argsort(cnts)[::-1]
        pick = vals[order[0]]
        for i in order[1:]:
            if vals[i] != "." and cnts[i] > 40:
                pick = vals[i]; break
        row += pick
    print(f"   y{by:3d}: {row}")
print("   x ruler: ", "".join([str((PX0+i*63)//100%10) for i in range(11)]))
