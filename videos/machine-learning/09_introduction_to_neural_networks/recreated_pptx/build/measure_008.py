#!/usr/bin/env python3
"""Objective pixel measurement: original slide_008.jpg vs current render."""
import sys
from collections import Counter
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_008_rendered_resized.png"

COLORS = {
    "yellow_C":  ((241, 196, 15),  (255, 249, 196), 70),
    "orange_Q":  ((230, 126, 34),  (255, 160, 80), 70),
    "green_C1":  ((46, 204, 113),  (120, 230, 170), 70),
    "blue_C2":   ((41, 128, 185),  (110, 170, 220), 70),
    "red_C3":    ((192, 57, 43),   (230, 110, 100), 70),
}


def load(p, size=(960, 540)):
    im = Image.open(p).convert("RGB")
    if im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(int)


def mask_for(arr, target, tol):
    d = np.abs(arr - np.array(target)).sum(axis=2)
    return d < tol


def report(name, arr):
    print(f"\n=== {name} ({arr.shape[1]}x{arr.shape[0]}) ===")
    for cname, (t1, t2, tol) in COLORS.items():
        m = mask_for(arr, t1, tol) | mask_for(arr, t2, tol)
        n = int(m.sum())
        if n == 0:
            print(f"  {cname:10s} count=0")
            continue
        ys, xs = np.nonzero(m)
        # cluster blobs: label connected components crudely by grid bucketing
        buckets = Counter((int(x // 40), int(y // 40)) for x, y in zip(xs, ys))
        top = buckets.most_common(6)
        print(f"  {cname:10s} count={n:6d} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
        print(f"             blobs(40px grid): {top}")


def title_strip(arr):
    """Measure non-background pixels in title band to detect clipping/overflow."""
    band = arr[10:75, :, :]
    bg = arr[10:75, 10:80, :].reshape(-1, 3).mean(axis=0)
    d = np.abs(band - bg).sum(axis=2)
    m = d > 60
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print("  title band: empty")
        return
    print(f"  title band ink: x[{xs.min()},{xs.max()}] y[{ys.min()+10},{ys.max()+10}] count={m.sum()}")
    # row profile to detect cut-off rows
    rows = m.sum(axis=1)
    nz = [i + 10 for i, v in enumerate(rows) if v > 0]
    print(f"  title ink rows: {nz[0]}..{nz[-1]} (contiguous gap check: "
          f"{'OK' if nz[-1]-nz[0]+1==len(nz) else 'GAPS'})")


orig = load(ORIG)
rend = load(REND)
report("ORIGINAL", orig)
report("RENDER", rend)
print("\n=== title bands ===")
title_strip(orig)
title_strip(rend)

# overall similarity
d = np.abs(orig - rend).sum(axis=2)
print(f"\nmean abs diff per px: {d.mean():.1f}  pct pixels >90 diff: {(d > 90).mean()*100:.1f}%")
