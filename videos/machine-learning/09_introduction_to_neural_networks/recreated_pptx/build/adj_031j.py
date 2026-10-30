#!/usr/bin/env python3
"""Precise geometry of slide_031 original: diagram panel border, calc box borders, text bands."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
BG = (231, 233, 230)
d = np.abs(O - np.array(BG)).sum(axis=2)
ink = d > 60

def h_runs(y, minlen=30):
    xs = np.where(ink[y])[0]
    if len(xs) == 0: return []
    out=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x!=p+1: out.append((s,p)); s=x
        p=x
    out.append((s,p))
    return [o for o in out if o[1]-o[0]>=minlen]

def v_runs(x, minlen=30):
    ys = np.where(ink[:,x])[0]
    if len(ys) == 0: return []
    out=[]; s=ys[0]; p=ys[0]
    for y in ys[1:]:
        if y!=p+1: out.append((s,p)); s=y
        p=y
    out.append((s,p))
    return [o for o in out if o[1]-o[0]>=minlen]

print("=== horizontal ink runs (>=60 px) — box top/bottom borders ===")
for y in range(H):
    rr = h_runs(y, 60)
    if rr:
        cols = [tuple(O[y,(a+b)//2]) for a,b in rr]
        print(f" y={y}: {rr} colors={cols}")

print("\n=== vertical ink runs (>=60 px) ===")
for x in range(W):
    vr = v_runs(x, 60)
    if vr:
        cols = [tuple(O[(a+b)//2,x]) for a,b in vr]
        print(f" x={x}: {vr} colors={cols}")

print("\n=== row ink profile (all ink, per row counts), y 40..530 ===")
rows = ink.sum(axis=1)
runs=[]; inrun=False
for y in range(H):
    if rows[y] > 0 and not inrun: s=y; inrun=True
    elif rows[y]==0 and inrun: runs.append((s,y-1)); inrun=False
if inrun: runs.append((s,H-1))
print("ink row bands:", runs)
