#!/usr/bin/env python3
"""Probe: raw ink-band structure in box4 (and box2 as calibration), orig vs s240-4.

Question: the checker's "band END = baseline" assumes no descenders, but box 4's
subscript `i` ink sits BELOW the baseline. Separate the main-row ink bottom (true
baseline) from the subscript-ink bottom, then compare against TARGETS.
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_036.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp/s240-4.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
RH, RW = r.shape[:2]
s = RH / 540.0
print(f"scale s={s:.4f}  render {RW}x{RH}")

def bands(img, x0, x1, y0, y1, thr, sc):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2)
    rows = (lum < thr).any(axis=1)
    cnt = (lum < thr).sum(axis=1)
    out = []
    st = None
    for i, v in enumerate(rows):
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i)); st = None
    if st is not None:
        out.append((st, len(rows)))
    return [(round(y0+a0/sc,1), round(y0+a1/sc,1), int(cnt[a0:a1].max())) for a0, a1 in out]

print("\n=== BOX 4 (targets [461,487,514]) ===")
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    print(f"{tag}:")
    for b in bands(img, 79, 860, 437, 539, 178, sc):
        print(f"   ink y {b[0]:7.1f} .. {b[1]:7.1f}   h={b[1]-b[0]:5.1f}  maxrow={b[2]}")

print("\n=== BOX 2 (targets [248,279,307]) ===")
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    print(f"{tag}:")
    for b in bands(img, 79, 860, 226, 314, 178, sc):
        print(f"   ink y {b[0]:7.1f} .. {b[1]:7.1f}   h={b[1]-b[0]:5.1f}  maxrow={b[2]}")

print("\n=== BOX 1 (targets [117,149,177,206]) ===")
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    print(f"{tag}:")
    for b in bands(img, 79, 860, 94, 212, 178, sc):
        print(f"   ink y {b[0]:7.1f} .. {b[1]:7.1f}   h={b[1]-b[0]:5.1f}  maxrow={b[2]}")

# column profile of box4 render line1 to locate the subscript ink x-range
print("\n=== BOX4 render, per-band column extents (find the subscript x) ===")
a = r[int(441*s):int(534*s), int(79*s):int(860*s)]
lum = a.mean(axis=2)
for (y0, y1, _) in bands(r, 79, 860, 441, 534, 178, s):
    sub = lum[int((y0-441)*s):int((y1-441)*s)+1, :]
    m = sub < 178
    cols = np.where(m.any(axis=0))[0]
    print(f"   band y{y0:.1f}..{y1:.1f}: x {79+cols.min()/s:.1f} .. {79+cols.max()/s:.1f}  ({m.sum()} px)")
