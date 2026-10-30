#!/usr/bin/env python3
"""Measure slide-3 original geometry: ring columns, input dots, outputs."""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()
sc = W / 960.0

def ring_pred(c, kind):
    r, g, b = c
    if kind == "red":   return r > 120 and g < 90 and b < 90
    if kind == "blue":  return b > 120 and g < 100 and r < 120
    if kind == "green": return g > 100 and r < 130 and b < 130

def purple(c):
    r, g, b = c
    return r > 100 and b > 100 and g < r - 35 and g < b - 35

def centroids(pred, x0, x1, y0, y1, min_px=25):
    seen = set(); out = []
    for y in range(int(y0 * H / 540), int(y1 * H / 540)):
        for x in range(int(x0 * sc), int(x1 * sc)):
            if (x, y) in seen or not pred(px[x, y]):
                continue
            stack = [(x, y)]; seen.add((x, y)); comp = []
            while stack:
                a, b = stack.pop(); comp.append((a, b))
                for da, db in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                    na, nb = a+da, b+db
                    if (na, nb) in seen or na < 0 or nb < 0 or na >= W or nb >= H:
                        continue
                    if pred(px[na, nb]):
                        seen.add((na, nb)); stack.append((na, nb))
            if len(comp) >= min_px:
                cx = sum(p[0] for p in comp) / len(comp) / sc
                cy = sum(p[1] for p in comp) / len(comp) * 540 / H
                out.append((round(cx, 1), round(cy, 1), len(comp)))
    return sorted(out)

for kind in ("red", "blue", "green"):
    print(kind, "rings:", centroids(lambda c, k=kind: ring_pred(c, k), 140, 780, 100, 400, 25))
print("purple dots x<160:", centroids(purple, 40, 160, 140, 360, 15))
