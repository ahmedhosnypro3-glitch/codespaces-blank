#!/usr/bin/env python3
"""Red-pixel analysis: does the original have a red diagram panel border?"""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.array(Image.open(f"{V}/recreated_pptx/build/slide_031_rendered-1.png").convert("RGB")).astype(int)

def runs_1d(arr, minlen=20):
    out, inrun, s = [], False, 0
    for i, c in enumerate(arr):
        if c and not inrun: s=i; inrun=True
        elif not c and inrun: out.append((s, i-1)); inrun=False
    if inrun: out.append((s, len(arr)-1))
    return [r for r in out if r[1]-r[0] >= minlen]

for name, A, H, W in [("ORIGINAL", O, 540, 960), ("RENDER", R, 1125, 2001)]:
    r,g,b = A[...,0], A[...,1], A[...,2]
    red = (r>120)&(g<80)&(b<80)
    print(f"\n=== {name} red pixel count: {red.sum()} ===")
    rows = red.sum(axis=1)
    print("long horizontal red runs (>=30):")
    for y in range(H):
        if rows[y] >= 30:
            xs = np.where(red[y])[0]
            # contiguous groups
            groups=[]; s=xs[0]; p=xs[0]
            for x in xs[1:]:
                if x!=p+1: groups.append((s,p)); s=x
                p=x
            groups.append((s,p))
            big=[gg for gg in groups if gg[1]-gg[0]>=30]
            if big: print(f"  y={y}: {big} rgb={tuple(A[y,(big[0][0]+big[0][1])//2])}")
    cols = red.sum(axis=0)
    print("long vertical red runs (>=30):")
    for x in range(W):
        if cols[x] >= 30:
            ys = np.where(red[:,x])[0]
            groups=[]; s=ys[0]; p=ys[0]
            for y in ys[1:]:
                if y!=p+1: groups.append((s,p)); s=y
                p=y
            groups.append((s,p))
            big=[gg for gg in groups if gg[1]-gg[0]>=30]
            if big: print(f"  x={x}: {big} rgb={tuple(A[(big[0][0]+big[0][1])//2,x])}")
