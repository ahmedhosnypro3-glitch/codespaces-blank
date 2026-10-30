#!/usr/bin/env python3
"""Find the exact border lines (long runs of a non-bg color) in original slide_031."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
BG = (231, 233, 230)
d = np.abs(O - np.array(BG)).sum(axis=2)
ink = d > 60

# Look for long horizontal runs per row (>=40 px) -> box top/bottom borders
print("=== horizontal long runs per row ===")
for y in range(H):
    row = ink[y]
    xs = np.where(row)[0]
    if len(xs) == 0: continue
    # contiguous groups
    groups = []
    start = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x != prev + 1:
            groups.append((start, prev)); start = x
        prev = x
    groups.append((start, prev))
    longs = [g for g in groups if g[1]-g[0] >= 40]
    if longs:
        # sample colors
        info = []
        for (a,b) in longs:
            mid = (a+b)//2
            info.append(f"x[{a},{b}] len={b-a+1} rgb={tuple(O[y,mid])}")
        print(f"y={y}: " + "; ".join(info))
