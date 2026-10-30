#!/usr/bin/env python3
"""Measure slide_029.jpg regions programmatically (PIL ground truth)."""
from PIL import Image
import numpy as np
import json

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_029.jpg").convert("RGB")
W, H = img.size
a = np.asarray(img).astype(int)
print("size:", W, H)

def find_color(target, tol=28, min_px=300):
    t = np.array(target)
    d = np.abs(a - t).sum(axis=2)
    mask = d < tol
    ys, xs = np.where(mask)
    if len(xs) < min_px:
        return None
    return {
        "count": int(len(xs)),
        "x0": int(xs.min()), "x1": int(xs.max()),
        "y0": int(ys.min()), "y1": int(ys.max()),
        "pct_x0": round(xs.min()/W*100,1), "pct_x1": round(xs.max()/W*100,1),
        "pct_y0": round(ys.min()/H*100,1), "pct_y1": round(ys.max()/H*100,1),
    }

print("\n--- distinct color scan (top 12 by area) ---")
flat = a.reshape(-1,3)
# quantize to reduce noise
q = (flat // 8 * 8)
uniq, counts = np.unique(q, axis=0, return_counts=True)
order = np.argsort(-counts)[:14]
for i in order:
    c = uniq[i]
    n = counts[i]
    if n < 800: continue
    r,g,b = c
    print(f"#{r:02X}{g:02X}{b:02X}  n={n}  ({n/(W*H)*100:.1f}%)")

print("\n--- targeted regions ---")
for name, tgt, tol in [
    ("red frame / dark red", (192,0,0), 45),
    ("beige panel", (232,224,208), 22),
    ("legend beige", (242,228,208), 18),
    ("pale green class", (217,234,211), 16),
    ("magenta fill", (230,160,230), 30),
    ("pale yellow", (255,253,231), 14),
    ("yellow badge", (255,249,196), 22),
    ("light blue callout", (221,235,247), 12),
    ("light green callout", (226,239,218), 12),
]:
    print(name, find_color(tgt, tol))

print("\n--- red frame bounds (strong C00000) ---")
d = np.abs(a - np.array([192,0,0])).sum(axis=2)
mask = d < 60
ys, xs = np.where(mask)
if len(xs):
    print("x", xs.min(), xs.max(), "y", ys.min(), ys.max(),
          "pct", round(xs.min()/W*100,1), round(xs.max()/W*100,1),
          round(ys.min()/H*100,1), round(ys.max()/H*100,1))

print("\n--- horizontal band scan: beige panel rows/cols ---")
d = np.abs(a - np.array([232,224,208])).sum(axis=2)
mask = d < 24
colsum = mask.sum(axis=0)
rowsum = mask.sum(axis=1)
cols = np.where(colsum > 20)[0]
rows = np.where(rowsum > 20)[0]
if len(cols): print("beige cols", cols.min(), cols.max(), "pct", round(cols.min()/W*100,1), round(cols.max()/W*100,1))
if len(rows): print("beige rows", rows.min(), rows.max(), "pct", round(rows.min()/H*100,1), round(rows.max()/H*100,1))

print("\n--- dark red vertical bar scan (strong C00000 in mid slide) ---")
d = np.abs(a - np.array([192,0,0])).sum(axis=2)
mask = d < 60
mid = mask[int(H*0.25):int(H*0.75), :]
colsum = mid.sum(axis=0)
for x in range(W):
    if colsum[x] > H*0.15:
        print("  bar col", x, "pct", round(x/W*100,2), "height px", colsum[x])
        break
runs = []
inrun = False
for x in range(W):
    if colsum[x] > H*0.15:
        if not inrun: start = x; inrun = True
    else:
        if inrun: runs.append((start, x-1)); inrun = False
if inrun: runs.append((start, W-1))
print("  bar col runs:", [(r[0], r[1], round(r[0]/W*100,1), round(r[1]/W*100,1)) for r in runs])

# bar vertical extent
if runs:
    bx0, bx1 = runs[0]
    sub = mask[:, bx0:bx1+1]
    rws = np.where(sub.sum(axis=1) > (bx1-bx0+1)*0.6)[0]
    if len(rws):
        print("  bar rows", rws.min(), rws.max(), "pct", round(rws.min()/H*100,1), round(rws.max()/H*100,1))
