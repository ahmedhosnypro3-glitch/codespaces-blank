#!/usr/bin/env python3
"""Blob census for slide 3 original: purple input dots + colored node rings."""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
W, H = im.size
px = im.load()

def blobs(pred, x0, x1, y0, y1, min_px=20):
    seen = set()
    out = []
    for y in range(int(y0 * H / 540), int(y1 * H / 540)):
        for x in range(int(x0 * W / 960), int(x1 * W / 960)):
            if (x, y) in seen:
                continue
            c = px[x, y]
            if not pred(c):
                continue
            stack = [(x, y)]
            seen.add((x, y))
            comp = []
            while stack:
                a, b = stack.pop()
                comp.append((a, b))
                for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                    na, nb = a+da, b+db
                    if (na, nb) in seen or na < 0 or nb < 0 or na >= W or nb >= H:
                        continue
                    if pred(px[na, nb]):
                        seen.add((na, nb))
                        stack.append((na, nb))
            if len(comp) >= min_px:
                xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
                out.append((len(comp), min(xs), max(xs), min(ys), max(ys),
                            tuple(sum(px[a, b][i] for a, b in comp)//len(comp) for i in range(3))))
    return sorted(out, key=lambda t: t[3])

purple = lambda c: c[0] > 110 and c[2] > 110 and c[1] < c[0] - 40 and c[1] < c[2] - 40
red    = lambda c: c[0] > 110 and c[1] < 80 and c[2] < 80
blue   = lambda c: c[2] > 110 and c[1] < 90 and c[0] < 110
green  = lambda c: c[1] > 90 and c[0] < 120 and c[2] < 120

print("== purple blobs (whole frame, >=60px) ==")
for b in blobs(purple, 0, 960, 0, 540, 60):
    print(f"  n={b[0]:6d} x[{b[1]:4d}-{b[2]:4d}] y[{b[3]:4d}-{b[4]:4d}] c={b[5]}")
for name, pred in (("red", red), ("blue", blue), ("green", green)):
    print(f"== {name} blobs (>=60px) ==")
    for b in blobs(pred, 0, 960, 0, 540, 60):
        print(f"  n={b[0]:6d} x[{b[1]:4d}-{b[2]:4d}] y[{b[3]:4d}-{b[4]:4d}] c={b[5]}")
