#!/usr/bin/env python3
"""Probe 48: resolve the composite red marks definitively (shape + colour)."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
TRED = (r > 90) & (g < 75) & (b < 75) & ((r - g) > 60) & ((r - b) > 60)

print("=== LEFT blob region 1x1 map: x218..252 y226..258 ===")
for y in range(226, 259):
    print(f"  {y:4d} " + "".join("#" if TRED[y, x] else "." for x in range(218, 253)))

print("\n=== colour stats inside LEFT blob core (x230..246 y238..250) ===")
sub = a[238:251, 230:247].reshape(-1, 3)
import collections
c = collections.Counter(map(tuple, sub))
print("  top 12:", c.most_common(12))
core = sub[(sub[:, 0] > 90) & (sub[:, 1] < 75) & (sub[:, 2] < 75)]
print(f"  n_core={len(core)} mean core = {core.mean(axis=0).round(1) if len(core) else None}")

print("\n=== LEFT diagonal: per-row red extent x180..220 y150..235 ===")
for y in range(150, 236, 3):
    xs = [x for x in range(180, 221) if TRED[y, x]]
    if xs:
        print(f"  y={y}: x {min(xs)}..{max(xs)} (w={max(xs)-min(xs)+1}) n={len(xs)}")

print("\n=== RIGHT diagonal: per-row red extent x590..660 y140..270 ===")
for y in range(140, 271, 3):
    xs = [x for x in range(590, 661) if TRED[y, x]]
    if xs:
        print(f"  y={y}: x {min(xs)}..{max(xs)} (w={max(xs)-min(xs)+1}) n={len(xs)}")

print("\n=== RIGHT blob at end of diagonal: 1x1 map x626..656 y228..270 ===")
for y in range(228, 271):
    print(f"  {y:4d} " + "".join("#" if TRED[y, x] else "." for x in range(626, 657)))

print("\n=== LEFT panel x223..248 y231..254 mirrored to RIGHT +414: x637..662 ===")
n = int(TRED[231:255, 637:663].sum())
print(f"  RIGHT masked-region red px count = {n}")
print(f"  LEFT  masked-region red px count = {int(TRED[231:255, 223:249].sum())}")

print("\n=== is the LEFT blob a hollow ring? radial check ===")
cy, cx = 242.0, 235.5
for rad in range(0, 14):
    ring = []
    for t in range(0, 360, 10):
        yy = int(round(cy + rad * np.sin(np.radians(t))))
        xx = int(round(cx + rad * np.cos(np.radians(t))))
        ring.append(bool(TRED[yy, xx]))
    print(f"  r={rad:2d}: {sum(ring)}/{len(ring)}")
