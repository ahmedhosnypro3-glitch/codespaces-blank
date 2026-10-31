#!/usr/bin/env python3
"""Color-region segmentation of original slide_031.jpg: all distinct element blocks."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
O = np.array(Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
H, W = O.shape[:2]
PPI = W / 13.33
def inch(v): return round(v / PPI, 3)

pd, pg, pb = O[..., 0], O[..., 1], O[..., 2]

masks = {
  "red(~C00000)":   (pd > 150) & (pg < 90) & (pb < 90),
  "red(~FF0000)":   (pd > 200) & (pg < 80) & (pb < 80),
  "green(~008000)": (pd < 80) & (pg > 100) & (pb < 80),
  "blue(~000080)":  (pd < 80) & (pg < 80) & (pb > 120),
  "black":          (pd < 70) & (pg < 70) & (pb < 70),
  "white":          (pd > 245) & (pg > 245) & (pb > 245),
}
for name, m in masks.items():
    ys, xs = np.where(m)
    print(f"\n### {name}: {len(xs)} px")
    if not len(xs): continue
    # row clusters
    ys_s = np.sort(ys)
    gaps = np.where(np.diff(ys_s) > 10)[0]
    starts = [0] + [g + 1 for g in gaps]
    ends = [g for g in gaps] + [len(ys_s) - 1]
    for s, e in zip(starts, ends):
        ysl = ys_s[s:e + 1]
        sel = (ys >= ysl[0]) & (ys <= ysl[-1])
        xl = xs[sel]
        if len(xl) < 60: continue
        print(f"  y {ysl[0]:3d}-{ysl[-1]:3d} ({inch(ysl[0])}-{inch(ysl[-1])}in)"
              f"  x {xl.min():3d}-{xl.max():3d} ({inch(xl.min())}-{inch(xl.max())}in)  n={len(xl)}")
