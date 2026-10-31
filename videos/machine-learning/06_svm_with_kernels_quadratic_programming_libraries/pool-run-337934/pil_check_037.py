#!/usr/bin/env python3
"""Closed-loop PIL check: recreated render vs original frame for slide 037."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
R = f"{NS}/recreated_pptx/renders/slide_037_recreated-1.png"
O = f"{NS}/qa/rejudge2/orig_png/slide_037.png"

r = Image.open(R).convert("RGB")
o = Image.open(O).convert("RGB")
print("render", r.size, "orig", o.size)
o = o.resize(r.size)

ra = np.asarray(r).astype(int)
oa = np.asarray(o).astype(int)

# ink = pixels notably darker than the light background
def ink(a):
    g = a.mean(axis=2)
    return g < 200

ri, oi = ink(ra), ink(oa)
print("ink px render", int(ri.sum()), "orig", int(oi.sum()),
      f"({100*ri.sum()/ri.size:.2f}% vs {100*oi.sum()/oi.size:.2f}%)")

# grid comparison: 13x8 cells, fraction of ink in each
GH, GW = 8, 13
print("cell ink% render vs orig (cells differing >15pp marked *):")
for gy in range(GH):
    row = []
    for gx in range(GW):
        rs = ri[gy*r.size[1]//GH:(gy+1)*r.size[1]//GH, gx*r.size[0]//GW:(gx+1)*r.size[0]//GW]
        os_ = oi[gy*o.size[1]//GH:(gy+1)*o.size[1]//GH, gx*o.size[0]//GW:(gx+1)*o.size[0]//GW]
        rp, op = 100*rs.mean(), 100*os_.mean()
        mark = "*" if abs(rp-op) > 15 else " "
        row.append(f"{rp:4.0f}/{op:4.0f}{mark}")
    print(" ".join(row))

# green highlight presence in render (90EE90) and original
def green_count(a):
    d = np.abs(a - np.array([0x90, 0xEE, 0x90])).sum(axis=2)
    return int((d < 60).sum())
print("green px render", green_count(ra), "orig", green_count(oa))

# red frame pixels (C00000) in render edges
def red_count(a):
    d = np.abs(a - np.array([0xC0, 0x00, 0x00])).sum(axis=2)
    return int((d < 60).sum())
print("red px render", red_count(ra), "orig", red_count(oa))

# dark-ink row profile (text lines) for both, normalized
def rowprof(m):
    p = m.mean(axis=1)
    return p
rp, op = rowprof(ri), rowprof(oi)
# print rows where ink fraction > 2% as bands
def bands(p, thr=0.02):
    out, start = [], None
    for i, v in enumerate(p):
        if v > thr and start is None:
            start = i
        elif v <= thr and start is not None:
            out.append((start, i)); start = None
    if start is not None:
        out.append((start, len(p)))
    return [(round(a/r.size[1], 3), round(b/r.size[1], 3)) for a, b in out]
print("render ink row bands (norm):", bands(rp))
print("orig   ink row bands (norm):", bands(op))
