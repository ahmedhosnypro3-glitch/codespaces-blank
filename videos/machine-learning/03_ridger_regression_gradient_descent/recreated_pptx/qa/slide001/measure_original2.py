#!/usr/bin/env python3
"""Detailed ink census for slide_001.jpg: band-by-band, color-classified."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# background = gray panel (231,233,230) or white canvas (254,255,253)
bg_dist = np.minimum(
    np.abs(IM - np.array([231, 233, 230])).sum(axis=2),
    np.abs(IM - np.array([254, 255, 253])).sum(axis=2),
)
ink = bg_dist > 60  # meaningfully non-background

print(f"ink px total: {ink.sum()}")
rows = np.where(ink.any(axis=1))[0]
# contiguous row bands
bands = []
start = prev = rows[0]
for y in rows[1:]:
    if y - prev > 4:
        bands.append((start, prev))
        start = y
    prev = y
bands.append((start, prev))
print(f"{len(bands)} ink bands:")

for (y0, y1) in bands:
    sub = ink[y0:y1 + 1]
    xs = np.where(sub.any(axis=0))[0]
    # classify band pixels by color classes
    seg = IM[y0:y1 + 1, :, :]
    segink = sub
    n = segink.sum()
    # dominant quantized colors among ink px
    pxs = seg[segink]
    q = (pxs // 32 * 32)
    cnt = Counter(map(tuple, q))
    top = cnt.most_common(6)
    print(f"\nband y {y0}..{y1} (h={y1-y0+1}), x {xs.min()}..{xs.max()} (w={xs.max()-xs.min()+1}), inkpx={n}")
    print(f"   top colors (quantized //32): {top}")
    # x-projection splits: find column gaps > 40 to see multi-column bands
    colmask = sub.any(axis=0)
    colson = np.where(colmask)[0]
    gaps = np.where(np.diff(colson) > 40)[0]
    if len(gaps):
        segs = []
        lo = colson[0]
        for gi in gaps:
            segs.append((lo, colson[gi]))
            lo = colson[gi + 1]
        segs.append((lo, colson[-1]))
        print(f"   col segments (gap>40): {segs}")

# Detailed color probes at specific spots
print("\n--- color probes ---")
for (name, y, x) in [
    ("title area probe1", 100, 480), ("title area probe2", 130, 600),
    ("title area probe3", 160, 500), ("band y314 center", 324, 470),
    ("band y378 center", 390, 490), ("band y404 center", 410, 480),
    ("band y450 left", 458, 200), ("logo teal", 495, 630),
    ("logo right panel bg", 495, 700), ("logo right panel bg2", 495, 760),
    ("below logo", 520, 700),
]:
    print(f"{name} ({x},{y}): {tuple(IM[y, x])}")

# yellow mask detail — where exactly?
yellow = (r > 200) & (g > 200) & (b < 190)
ys, xs = np.where(yellow)
if len(ys):
    # histogram of yellow by y-band
    import collections
    yh = collections.Counter((ys // 20) * 20)
    print("\nyellow px y-histogram (20px bins):", dict(sorted(yh.items())))
    # yellow outside badge region?
    out = (xs < 850)
    if out.any():
        oys, oxs = ys[out], xs[out]
        print(f"yellow OUTSIDE badge x<850: n={len(oys)}, bbox x {oxs.min()}..{oxs.max()} y {oys.min()}..{oys.max()}")
        # sample some
        samp = collections.Counter(map(tuple, IM[oys[:2000], oxs[:2000]]))
        print("sample colors:", samp.most_common(5))

# red text excluding strokes (x<70 or x>895 or y>525)
redtext = (r > 120) & (r - g > 55) & (r - b > 55)
redtext[:, :70] = False
redtext[:, 895:] = False
redtext[525:, :] = False
ys, xs = np.where(redtext)
if len(ys):
    print(f"\nRED TEXT (strokes excluded): n={len(ys)}, bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
    rbands = []
    rr = np.where(redtext.any(axis=1))[0]
    if len(rr):
        s = p = rr[0]
        for y in rr[1:]:
            if y - p > 4:
                rbands.append((s, p)); s = y
            p = y
        rbands.append((s, p))
    print("red text bands:", rbands)
    for (y0, y1) in rbands:
        xs2 = np.where(redtext[y0:y1+1].any(axis=0))[0]
        print(f"  red band y {y0}..{y1}: x {xs2.min()}..{xs2.max()} (w={xs2.max()-xs2.min()+1})")
else:
    print("\nRED TEXT (strokes excluded): NONE")
