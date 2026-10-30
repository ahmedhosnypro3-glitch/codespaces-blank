#!/usr/bin/env python3
"""Detect box outlines, node circles and text bands on slide_028."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_028.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def segs(mask, min_len, axis):
    """all runs of True of length>=min_len along rows(axis=0) or cols(axis=1)"""
    out = []
    if axis == 0:
        n = mask.shape[0]
        for i in range(n):
            row = mask[i]
            j = 0
            while j < W:
                if row[j]:
                    k = j
                    while k + 1 < W and row[k + 1]:
                        k += 1
                    if k - j + 1 >= min_len:
                        out.append((j, k, i))
                    j = k + 1
                else:
                    j += 1
    else:
        n = mask.shape[1]
        for j in range(n):
            col = mask[:, j]
            i = 0
            while i < H:
                if col[i]:
                    k = i
                    while k + 1 < H and col[k + 1]:
                        k += 1
                    if k - i + 1 >= min_len:
                        out.append((i, k, j))
                    i = k + 1
                else:
                    i += 1
    return out

def cluster(items):
    """group (start,end,fixedpos) into contiguous bands"""
    items = sorted(items)
    groups = []
    cur = [items[0]]
    for it in items[1:]:
        if abs(it[2] - cur[-1][2]) <= 2:
            cur.append(it)
        else:
            groups.append(cur)
            cur = [it]
    groups.append(cur)
    res = []
    for grp in groups:
        s = min(x[0] for x in grp)
        e = max(x[1] for x in grp)
        p0 = min(x[2] for x in grp)
        p1 = max(x[2] for x in grp)
        res.append((s, e, p0, p1))
    return res

red = (r > 150) & (r - g > 60) & (r - b > 60)
blue = (b > 120) & (b - r > 60) & (b - g > 40)
orange = (r > 200) & (g > 60) & (g < 170) & (b < 90)
white = (r > 235) & (g > 235) & (b > 235)
dark = a.mean(axis=2) < 110

print("== RED horizontal segments (>=60px) ==")
for (s, e, p0, p1) in cluster(segs(red, 60, 0)):
    print(f"  x[{s}-{e}] y[{p0}-{p1}] len={e-s+1}")
print("== RED vertical segments (>=25px) ==")
for (s, e, p0, p1) in cluster(segs(red, 25, 1)):
    print(f"  y[{s}-{e}] x[{p0}-{p1}] len={e-s+1}")
print("== BLUE vertical segments (>=15px) ==")
for (s, e, p0, p1) in cluster(segs(blue, 15, 1)):
    print(f"  y[{s}-{e}] x[{p0}-{p1}] len={e-s+1}")
print("== ORANGE filled regions (>=8x8) ==")
om = orange
rows = np.where(om.any(axis=1))[0]
if len(rows):
    runs = []
    st = None
    for i in range(int(rows[0]), int(rows[-1]) + 2):
        on = i < H and om[i].any()
        if on and st is None:
            st = i
        elif not on and st is not None:
            runs.append((st, i - 1))
            st = None
    for (r0, r1) in runs:
        cols = np.where(om[r0:r1+1].any(axis=0))[0]
        print(f"  rows {r0}-{r1} cols {cols[0]}-{cols[-1]} ({r1-r0+1}x{cols[-1]-cols[0]+1})")
print("== WHITE box interiors (>=40x40 runs) ==")
rows = np.where(white.any(axis=1))[0]
if len(rows):
    runs = []
    st = None
    for i in range(int(rows[0]), int(rows[-1]) + 2):
        on = i < H and (white[i].sum() >= 40)
        if on and st is None:
            st = i
        elif not on and st is not None:
            runs.append((st, i - 1))
            st = None
    for (r0, r1) in runs:
        cols = np.where(white[r0:r1+1].sum(axis=0) >= (r1-r0+1)//2)[0]
        if len(cols):
            print(f"  y[{r0}-{r1}] x[{cols[0]}-{cols[-1]}]")
print("== DARK text rows (ink profile per 20px band) ==")
for y0 in range(0, H, 20):
    band = dark[y0:y0+20]
    if band.any():
        cnt = band.sum(axis=1)
        ys = np.where(cnt > 3)[0]
        if len(ys):
            cols = np.where(band.any(axis=0))[0]
            print(f"  y[{y0+ys[0]}-{y0+ys[-1]}] x[{cols[0]}-{cols[-1]}] px={int(band.sum())}")
