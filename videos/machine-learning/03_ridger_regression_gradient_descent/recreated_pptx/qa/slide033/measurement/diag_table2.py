#!/usr/bin/env python3
"""Extract exact column x-positions of table gridlines and the text rows."""
import numpy as np
from PIL import Image

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

def dist(c1, c2):
    return abs(int(c1[0])-int(c2[0])) + abs(int(c1[1])-int(c2[1])) + abs(int(c1[2])-int(c2[2]))

print("=== TABLE vertical gridlines: columns with persistent dark-ish vertical ink ===")
# A gridline pixel is dark-ish OR a border-like color change. Scan each col
# for rows where the cell fill differs -> detect fill-boundary columns.
# Use rows in the middle of each band
bands = [(336, 366), (378, 408), (422, 453), (462, 478), (484, 501)]
cand = []
for x in range(80, 875):
    # check if col x is a boundary: colors at x-1 vs x differ in >=2 bands by >60
    n = 0
    for y0, y1 in bands:
        d = dist(tuple(o[(y0+y1)//2, x]), tuple(o[(y0+y1)//2, x-1]))
        if d > 80:
            n += 1
    if n >= 2:
        cand.append(x)
# cluster
groups = []
for x in cand:
    if groups and x - groups[-1][-1] <= 2:
        groups[-1].append(x)
    else:
        groups.append([x])
print("gridline cols:", [(gp[0], gp[-1], (gp[0]+gp[-1])//2) for gp in groups])

print("\n=== TABLE horizontal band boundaries (rows where fill changes across full width) ===")
for y in range(318, 524):
    n = 0
    for x in range(90, 868, 8):
        d = dist(tuple(o[y, x]), tuple(o[y-1, x]))
        if d > 70:
            n += 1
    if n > 15:
        print(f"  row {y}: {n} col-changes")

print("\n=== TABLE text rows: dark ink row-extents per band ===")
for bi, (y0, y1) in enumerate([(334, 367), (376, 410), (420, 455), (460, 480), (482, 503)]):
    dark = (r[y0:y1, 86:868] < 120) & (g[y0:y1, 86:868] < 120) & (b[y0:y1, 86:868] < 120)
    ys_, xs_ = np.where(dark)
    if len(ys_):
        print(f"  band{bi} y{y0}-{y1}: dark ink rows {y0+ys_.min()}-{y0+ys_.max()} cols {86+xs_.min()}-{86+xs_.max()} ({len(ys_)}px)")
        # col histogram of dark ink
        h, e = np.histogram(xs_ + 86, bins=54, range=(86, 868))
        print("    col hist:", [(int(e[i]), int(c)) for i, c in enumerate(h) if c > 20])

print("\n=== Yellow highlight cells: locate precisely ===")
yellow = (r > 190) & (g > 190) & (b < 170)
# restrict to table area
Y = np.zeros_like(yellow); Y[330:520, 86:868] = yellow[330:520, 86:868]
ys_, xs_ = np.where(Y)
print(f"  total yellow in table: {len(ys_)} px, rows {ys_.min()}-{ys_.max()} cols {xs_.min()}-{xs_.max()}")
if len(ys_):
    # per row band
    h, e = np.histogram(ys_, bins=54, range=(330, 520))
    for i, c in enumerate(h):
        if c > 40:
            m = (ys_ >= e[i]) & (ys_ < e[i+1])
            print(f"    rows {int(e[i])}-{int(e[i+1])}: {c}px cols {xs_[m].min()}-{xs_[m].max()}")

print("\n=== Red bold cells in table ===")
red = (r > 140) & (r - g > 60) & (r - b > 60)
R = np.zeros_like(red); R[330:520, 86:868] = red[330:520, 86:868]
ys_, xs_ = np.where(R)
if len(ys_):
    print(f"  {len(ys_)} px, rows {ys_.min()}-{ys_.max()} cols {xs_.min()}-{xs_.max()}")
    h, e = np.histogram(ys_, bins=54, range=(330, 520))
    for i, c in enumerate(h):
        if c > 10:
            m = (ys_ >= e[i]) & (ys_ < e[i+1])
            print(f"    rows {int(e[i])}-{int(e[i+1])}: {c}px cols {xs_[m].min()}-{xs_[m].max()}")
    h2, e2 = np.histogram(xs_, bins=54, range=(86, 868))
    print("    col hist:", [(int(e2[i]), int(c)) for i, c in enumerate(h2) if c > 20])

print("\n=== Table row label text: dark ink in x 86-175 ===")
for bi, (y0, y1) in enumerate([(334, 367), (376, 410), (420, 455), (460, 480), (482, 503)]):
    dark = (r[y0:y1, 86:180] < 120) & (g[y0:y1, 86:180] < 120) & (b[y0:y1, 86:180] < 120)
    ys_, xs_ = np.where(dark)
    if len(ys_):
        print(f"  band{bi}: {len(ys_)}px rows {y0+ys_.min()}-{y0+ys_.max()} cols {86+xs_.min()}-{86+xs_.max()}")

print("\n=== CENTER green box: columns of white (glyph) ink ===")
green = (g - r > 18) & (g - b > 18) & (g > 80)
# box x 244-599 y 252-301
sub_dark = (r[254:302, 246:600] < 150) & (g[254:302, 246:600] < 150) & (b[254:302, 246:600] < 150)
ys_, xs_ = np.where(sub_dark)
if len(ys_):
    print(f"  dark ink in box: {len(ys_)}px rows {254+ys_.min()}-{254+ys_.max()} cols {246+xs_.min()}-{246+xs_.max()}")
    h, e = np.histogram(ys_ + 254, bins=16, range=(254, 302))
    print("  row hist:", [(int(e[i]), int(c)) for i, c in enumerate(h) if c])
    h2, e2 = np.histogram(xs_ + 246, bins=71, range=(246, 600))
    print("  col hist:", [(int(e2[i]), int(c)) for i, c in enumerate(h2) if c > 3])

print("\n=== PARAM BOX text (x 75-175, y 245-309): dark ink ===")
for band in [(248, 262), (264, 276), (278, 292), (294, 306)]:
    y0, y1 = band
    dark = (r[y0:y1, 76:180] < 120) & (g[y0:y1, 76:180] < 120) & (b[y0:y1, 76:180] < 120)
    ys_, xs_ = np.where(dark)
    if len(ys_):
        print(f"  y{y0}-{y1}: {len(ys_)}px rows {y0+ys_.min()}-{y0+ys_.max()} cols {76+xs_.min()}-{76+xs_.max()}")
