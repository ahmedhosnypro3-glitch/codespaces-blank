#!/usr/bin/env python3
"""Precise region map for slide 31: text line boxes per color, node circles, rules."""
from PIL import Image
import numpy as np
from scipy import ndimage

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
PPI = 13.33 / 960
a = np.asarray(Image.open(f"{BASE}/slide_031.jpg").convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]


def groups(idx, gap=3):
    idx = sorted(idx)
    out, start, prev = [], None, None
    for v in idx:
        if start is None:
            start = prev = v
        elif v - prev <= gap:
            prev = v
        else:
            out.append((start, prev)); start = prev = v
    if start is not None:
        out.append((start, prev))
    return out


def lines(mask, name, minpx=2):
    prof = mask.sum(axis=1)
    print(f"-- {name} text lines:")
    for y0, y1 in groups([y for y in range(H) if prof[y] >= minpx]):
        sub = mask[y0:y1 + 1]
        cc = np.where(sub.any(axis=0))[0]
        print(f"   y {y0}..{y1} ({y0*PPI:.2f}..{y1*PPI:.2f}in) x {cc.min()}..{cc.max()} "
              f"({cc.min()*PPI:.2f}..{cc.max()*PPI:.2f}in) px={int(prof[y0:y1+1].sum())}")


red = (r > 140) & (r - g > 60) & (r - b > 60)
blue = (b > 140) & (b - r > 60) & (b - g > 35)
lines(red, "RED")
print()
lines(blue, "BLUE")
print()
# black text lines
blk = (r < 90) & (g < 90) & (b < 90)
lines(blk, "BLACK", minpx=3)
print()
# yellow circles (nodes) - full yellow including light
yel = (r > 195) & (g > 180) & (b < 175)
lab, n = ndimage.label(yel, np.ones((3, 3)))
sizes = ndimage.sum(yel, lab, range(1, n + 1))
objs = ndimage.find_objects(lab)
print("-- YELLOW blobs:")
for i in np.argsort(sizes)[::-1][:12]:
    if sizes[i] < 40:
        continue
    sl = objs[i]
    cx = (sl[1].start + sl[1].stop) / 2
    cy = (sl[0].start + sl[0].stop) / 2
    print(f"   blob {i+1} size {int(sizes[i])} x {sl[1].start}..{sl[1].stop} "
          f"y {sl[0].start}..{sl[0].stop} center ({cx:.0f},{cy:.0f}) "
          f"-> in ({cx*PPI:.2f},{cy*PPI:.2f})")
