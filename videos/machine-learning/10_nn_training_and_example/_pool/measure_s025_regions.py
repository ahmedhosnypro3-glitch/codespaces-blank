#!/usr/bin/env python3
"""Segment slide_025.jpg into measurable regions (geometry only)."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]


def mask_of(fn):
    return fn(a)


def report(label, m):
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    if len(rows) == 0:
        print(f"{label}: EMPTY")
        return
    print(f"{label}: rows {rows[0]}..{rows[-1]} cols {cols[0]}..{cols[-1]} px={m.sum()}")


def runs(mask, axis=1, minlen=2):
    idx = np.where(mask.any(axis=axis))[0]
    out = []
    if len(idx) == 0:
        return out
    s = idx[0]
    p = idx[0]
    for i in idx[1:]:
        if i - p > 1:
            if p - s + 1 >= minlen:
                out.append((int(s), int(p)))
            s = i
        p = i
    if p - s + 1 >= minlen:
        out.append((int(s), int(p)))
    return out


r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (r > 140) & (r - g > 45) & (r - b > 45)
blue = (b > 140) & (b - r > 45) & (b - g > 35)
green = (g > 110) & (g - r > 35) & (g - b > 35)
purple = (r > 90) & (b > 90) & (r - g > 25) & (b - g > 25)
orange = (r > 200) & (g > 120) & (g < 200) & (b < 110)
yellow = (r > 200) & (g > 200) & (b < 170)
white = (r > 245) & (g > 245) & (b > 245)
peach = (r > 245) & (g > 215) & (g < 238) & (b > 190) & (b < 225)
cream = (r > 248) & (g > 238) & (b > 185) & (b < 225)

for name, m in [("red", red), ("blue", blue), ("green", green), ("purple", purple),
                ("orange", orange), ("yellow", yellow), ("white", white),
                ("peach", peach), ("cream", cream)]:
    report(name, m)
    for (s, e) in runs(m, axis=1):
        mm = m[s:e + 1]
        cc = np.where(mm.any(axis=0))[0]
        print(f"   rowband {s}-{e} (h={e-s+1}) cols {cc[0]}-{cc[-1]}")

print("\n--- red column histogram (top 20) ---")
colcount = red.sum(axis=0)
for c in np.argsort(-colcount)[:20]:
    print(f"   col {c}: {colcount[c]}")

print("\n--- red row histogram (top 20) ---")
rowcount = red.sum(axis=1)
for rr in np.argsort(-rowcount)[:20]:
    print(f"   row {rr}: {rowcount[rr]}")

print("\n--- background sample ---")
print("   (5,5)", a[5, 5], " (480,300)", a[300, 480], " (270,10)", a[270, 10])
