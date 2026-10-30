#!/usr/bin/env python3
"""Probe 2: per-row ink counts in box 4, orig vs render, frame-px resolution.

Purpose: the checker takes band END as the baseline. If the subscript `i` tail
accounts for the last few frame-px, the true main-ink bottom (baseline) is higher
than the band end and the box-4 FAIL is a measurement artifact. Print the row
profile so the main-vs-subscript split is unambiguous.
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_036.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp/s240-4.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
RH, RW = r.shape[:2]
s = RH / 540.0

def rowprof(img, y0, y1, x0=80, x1=860, thr=178, sc=1.0, tag=""):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2)
    m = lum < thr
    cnt = m.sum(axis=1)
    # collapse render rows back to frame-px resolution for a fair comparison
    nfr = int(y1 - y0)
    per = []
    for fy in range(nfr):
        a0, a1 = int(fy*sc), int((fy+1)*sc)
        per.append(int(cnt[a0:a1].sum()))
    print(f"  --- {tag} per-frame-row ink px (y0={y0}) ---")
    for i, c in enumerate(per):
        if c:
            print(f"    y={y0+i:3d}  {c:6d}  {'#' * min(60, c // 40)}")

print("=== BOX 4 ORIGINAL ===")
rowprof(o, 436, 534, tag="orig")
print("=== BOX 4 RENDER ===")
rowprof(r, 436, 534, sc=s, tag="rend")
print("=== BOX 2 ORIGINAL (calibration: no subscripts) ===")
rowprof(o, 226, 314, tag="orig-box2")
print("=== BOX 2 RENDER (calibration) ===")
rowprof(r, 226, 314, sc=s, tag="rend-box2")
