#!/usr/bin/env python3
"""Forensics on slide_011 original: plot axes/line/points, table cell fills, NN diagram."""
import numpy as np
from PIL import Image

IMG = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/unique_slides/slide_011.jpg")

a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def m(*conds):
    out = np.ones((H, W), bool)
    for c in conds:
        out &= c
    return out

RED = m(R > 110, R - G > 45, R - B > 45)
DARK = m(R < 120, G < 120, B < 130)
BLUE = m(B - R > 45, B > 100)
CYAN = m(G - R > 25, B - R > 25, G > 110)
GREEN = m(G - R > 40, G - B > 25, G > 110)

def runs_h(mask, y, x0=0, x1=None):
    x1 = x1 or W
    out, x = [], x0
    while x < x1:
        if mask[y, x]:
            x2 = x
            while x2 + 1 < x1 and mask[y, x2 + 1]:
                x2 += 1
            out.append((x, x2))
            x = x2 + 1
        else:
            x += 1
    return out

def runs_v(mask, x, y0=0, y1=None):
    y1 = y1 or H
    out, y = [], y0
    while y < y1:
        if mask[y, x]:
            y2 = y
            while y2 + 1 < y1 and mask[y2 + 1, x]:
                y2 += 1
            out.append((y, y2))
            y = y2 + 1
        else:
            y += 1
    return out

def clusters(mask, region, minsize=12):
    """Return connected components (bbox, size) of mask inside region."""
    x0, y0, x1, y1 = region
    sub = mask[y0:y1, x0:x1].copy()
    seen = np.zeros_like(sub, bool)
    comps = []
    for yy in range(sub.shape[0]):
        for xx in range(sub.shape[1]):
            if not sub[yy, xx] or seen[yy, xx]:
                continue
            stack = [(yy, xx)]
            seen[yy, xx] = True
            pts = []
            while stack:
                cy, cx = stack.pop()
                pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < sub.shape[0] and 0 <= nx < sub.shape[1] \
                                and sub[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
            if len(pts) >= minsize:
                ys = [p[0] for p in pts]
                xs = [p[1] for p in pts]
                comps.append((x0 + min(xs), x0 + max(xs), y0 + min(ys), y0 + max(ys), len(pts)))
    return comps

print("=== PLOT REGION (right column) ===")
PLOT = (520, 100, 860, 380)
print("red components:", clusters(RED, PLOT, 20))
print("blue components:", clusters(BLUE, PLOT, 20))
print("cyan components:", clusters(CYAN, PLOT, 20))
print("green components:", clusters(GREEN, PLOT, 20))
print("dark components:", clusters(DARK, PLOT, 20))

print()
print("blue pixels per row (y: xmin-xmax count):")
for y in range(150, 360, 5):
    xs = np.nonzero(BLUE[y, 520:860])[0]
    if len(xs):
        print(f"  y={y}: x {520+xs.min()}..{520+xs.max()} n={len(xs)}")

print()
print("=== TABLE REGION (top-left) cell fill colors ===")
# table borders: x 96..313, y 138..306 ; header row 138..176, data rows below
for y in [150, 160, 190, 200, 240, 250, 290, 300]:
    row = []
    for x in [110, 140, 170, 200, 230, 260, 290, 305]:
        row.append((x, tuple(a[y, x])))
    print(f"  y={y}: {row}")

print()
print("vertical red borders in table:")
for x in range(90, 330):
    rs = runs_v(RED, x, 130, 315)
    long_rs = [r for r in rs if r[1] - r[0] > 10]
    if long_rs:
        print(f"  x={x}: {long_rs}")

print()
print("horizontal red borders in table (long runs):")
for y in range(130, 315):
    rs = [r for r in runs_h(RED, y, 90, 330) if r[1] - r[0] > 20]
    if rs:
        print(f"  y={y}: {rs}")
