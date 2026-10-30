#!/usr/bin/env python3
"""slide_031 original: find diagram panel border + calc box borders, ignoring top letterbox rows."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
BG = (231, 233, 230)
d = np.abs(O - np.array(BG)).sum(axis=2)
ink = d > 60

# content region only: y >= 46 (below letterbox)
C = ink.copy(); C[:46, :] = False

def groups(vals, minlen=25, axis=0, arr=None):
    if len(vals)==0: return []
    out=[]; s=vals[0]; p=vals[0]
    for v in vals[1:]:
        if v!=p+1: out.append((s,p)); s=v
        p=v
    out.append((s,p))
    return [o for o in out if o[1]-o[0]>=minlen]

# long vertical lines: cells where a whole column segment is ink
colink = C.sum(axis=0)
print("=== vertical lines: columns with >=200 ink px ===")
for x in range(W):
    if colink[x] >= 200:
        ys = np.where(C[:,x])[0]
        gg = groups(ys, 25)
        if gg: print(f" x={x}: {gg} rgb={tuple(O[(gg[0][0]+gg[0][1])//2, x])}")

print("\n=== vertical lines: columns with >=80 ink px ===")
for x in range(W):
    if colink[x] >= 80:
        ys = np.where(C[:,x])[0]
        gg = groups(ys, 20)
        if gg: print(f" x={x}: {gg} rgb={tuple(O[(gg[0][0]+gg[0][1])//2, x])}")

rowink = C.sum(axis=1)
print("\n=== horizontal lines: rows with >=300 ink px ===")
for y in range(H):
    if rowink[y] >= 300:
        xs = np.where(C[y])[0]
        gg = groups(xs, 40)
        if gg: print(f" y={y}: {gg} rgb={tuple(O[y,(gg[0][0]+gg[0][1])//2])}")

print("\n=== horizontal lines: rows with >=150 ink px ===")
for y in range(H):
    if rowink[y] >= 150:
        xs = np.where(C[y])[0]
        gg = groups(xs, 40)
        if gg: print(f" y={y}: {gg} rgb={tuple(O[y,(gg[0][0]+gg[0][1])//2])}")
