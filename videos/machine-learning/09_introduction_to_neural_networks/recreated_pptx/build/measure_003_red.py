#!/usr/bin/env python3
"""Full geometry + color measurement of slide_003.jpg."""
from PIL import Image
import collections, json, sys

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 110 and r - g > 45 and r - b > 35

def is_ink(c):
    r, g, b = c
    return r + g + b < 560

# ---- locate all red pixels ----
red_cols = collections.Counter()
red_rows = collections.Counter()
for y in range(H):
    for x in range(W):
        if is_red(px[x, y]):
            red_cols[x] += 1
            red_rows[y] += 1

print("=== RED-DENSE COLUMNS (x, count) ===")
for x, n in sorted(red_cols.items()):
    if n >= 25:
        print(f"  x={x:4d} n={n}")

print("\n=== RED-DENSE ROWS (y, count) ===")
for y, n in sorted(red_rows.items()):
    if n >= 25:
        print(f"  y={y:4d} n={n}")

# ---- red pixel clusters: connected components over red mask (coarse) ----
print("\n=== RED CLUSTERS (bbox) ===")
mask = set()
for y in range(H):
    for x in range(W):
        if is_red(px[x, y]):
            mask.add((x, y))

seen = set()
clusters = []
for p in sorted(mask):
    if p in seen:
        continue
    stack = [p]; seen.add(p)
    comp = []
    while stack:
        cx, cy = stack.pop()
        comp.append((cx, cy))
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                q = (cx+dx, cy+dy)
                if q in mask and q not in seen:
                    seen.add(q); stack.append(q)
    if len(comp) >= 30:
        xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
        clusters.append((min(xs), min(ys), max(xs), max(ys), len(comp)))
clusters.sort(key=lambda c: (c[1], c[0]))
for c in clusters:
    x0, y0, x1, y1, n = c
    print(f"  x={x0:4d}..{x1:4d} (w={x1-x0+1:4d})  y={y0:4d}..{y1:4d} (h={y1-y0+1:4d})  n={n}")
