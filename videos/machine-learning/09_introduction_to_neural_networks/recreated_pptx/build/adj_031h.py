#!/usr/bin/env python3
"""Compare diagram-region ink: original vs render for slide_031."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
orig = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
rend = Image.open(f"{V}/recreated_pptx/build/slide_031_rendered-1.png").convert("RGB")
O = np.array(orig).astype(int)
R = np.array(rend).astype(int)

def ink_cols(A, x0, x1, y0, y1, bg=(231,233,230), thr=60):
    reg = A[y0:y1, x0:x1]
    d = np.abs(reg - np.array(bg)).sum(axis=2)
    m = d > thr
    cols = m.sum(axis=0)
    runs, inrun = [], False
    for x, c in enumerate(cols):
        if c > 0 and not inrun: s=x; inrun=True
        elif c == 0 and inrun: runs.append((x0+s, x0+x-1)); inrun=False
    if inrun: runs.append((x0+s, x0+len(cols)-1))
    return runs, cols

# Render is 2001x1125 for a 13.33x7.5in slide => 150.075 px/in
SC = 2001/13.33
print("render px/in", SC)
# diagram region in render: x 1.5..9.0 in, y 1.2..4.7 in
rx0, rx1 = int(1.5*SC), int(9.0*SC)
ry0, ry1 = int(1.2*SC), int(4.7*SC)
print("render diagram box", rx0, ry0, rx1, ry1)

# Original diagram: find red panel border in original (the big red rect)
ro = O
r,g,b = ro[...,0], ro[...,1], ro[...,2]
red = (r>120)&(g<80)&(b<80)
ys,xs = np.where(red)
# separate the outer house frame from the inner diagram panel: look at column x counts
print("\n=== ORIGINAL red mask, long horizontal runs ===")
for y in range(O.shape[0]):
    row = np.where(red[y])[0]
    if len(row)==0: continue
    groups=[]; s=row[0]; p=row[0]
    for x in row[1:]:
        if x!=p+1: groups.append((s,p)); s=x
        p=x
    groups.append((s,p))
    longs=[gg for gg in groups if gg[1]-gg[0]>=60]
    if longs: print(f" y={y}: {longs} color={tuple(O[y,(longs[0][0]+longs[0][1])//2])}")

print("\n=== RENDER diagram region ink column runs ===")
runs, cols = ink_cols(R, rx0, rx1, ry0, ry1, bg=(232,232,232), thr=60)
print(runs)
print("\n=== ORIGINAL full-frame ink column runs (excluding house frame) ===")
runs2, c2 = ink_cols(O, 0, 960, 0, 540, bg=(231,233,230), thr=60)
print(runs2)
