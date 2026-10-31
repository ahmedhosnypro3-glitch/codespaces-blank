#!/usr/bin/env python3
"""Locate saturated node circles precisely in original slide_031.jpg."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
PPI = W / 13.33
def inch(v): return round(v / PPI, 3)

pd, pg, pb = O[..., 0], O[..., 1], O[..., 2]
mx = np.maximum(np.maximum(pd, pg), pb); mn = np.minimum(np.minimum(pd, pg), pb)
sat = (mx - mn) / np.maximum(mx, 1)

def clusters(mask, name, min_sat=0.0, minpx=40):
    m = mask & (sat >= min_sat) if min_sat else mask
    ys, xs = np.where(m)
    print(f"\n{name}: {len(xs)} px")
    if not len(xs): return
    # connected-component-lite: split by rows with gaps
    ys_s = np.sort(ys)
    gaps = np.where(np.diff(ys_s) > 8)[0]
    starts = [0] + [g + 1 for g in gaps]
    ends = [g for g in gaps] + [len(ys_s) - 1]
    for s, e in zip(starts, ends):
        ysl = ys_s[s:e + 1]
        sel = (ys >= ysl[0]) & (ys <= ysl[-1])
        xl = xs[sel]
        if len(xl) < minpx: continue
        print(f"  rows {ysl[0]}-{ysl[-1]} x {xl.min()}-{xl.max()} => "
              f"center=({inch(xl.mean())},{inch(ysl.mean())})in  px={len(xl)}")

clusters((pd > 245) & (pg > 240) & (pb < 120), "pure yellow (~FFFF00)", min_sat=0.8)
clusters((pd > 240) & (pg > 130) & (pg < 200) & (pb < 90), "pure orange (~FFA500)", min_sat=0.85)
clusters((pd > 150) & (pg < 90) & (pb < 90), "pure red (~C00000/FF0000)", min_sat=0.7)
clusters((pd < 60) & (pg > 100) & (pb < 60), "pure green (~008000)", min_sat=0.7)
clusters((pd < 60) & (pg < 60) & (pb > 130), "pure blue (~000080)", min_sat=0.7)
