#!/usr/bin/env python3
"""Precise pixel measurements of unique_slides/slide_008.jpg (960x540)."""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{name}: EMPTY")
        return None
    print(f"{name}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}  n={len(xs)}")
    return (xs.min(), ys.min(), xs.max(), ys.max())

def cluster_rows(mask, thr):
    rows = mask.sum(axis=1)
    groups, cur = [], None
    for y in range(len(rows)):
        if rows[y] > thr:
            if cur is None: cur = [y, y]
            else: cur[1] = y
        elif cur is not None:
            groups.append(tuple(cur)); cur = None
    if cur: groups.append(tuple(cur))
    return groups

def cluster_cols(mask, thr):
    cols = mask.sum(axis=0)
    groups, cur = [], None
    for x in range(len(cols)):
        if cols[x] > thr:
            if cur is None: cur = [x, x]
            else: cur[1] = x
        elif cur is not None:
            groups.append(tuple(cur)); cur = None
    if cur: groups.append(tuple(cur))
    return groups

print("=== TITLE REGION (y < 115) ===")
title_red = (R > 130) & (R - G > 55) & (R - B > 55) & (np.arange(H)[:, None] < 115)
title_blue = (B > 120) & (B - R > 60) & (B - G > 40) & (np.arange(H)[:, None] < 115)
for g in cluster_rows(title_red, 2):
    m = title_red.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"title red rows {g}")
for g in cluster_rows(title_blue, 1):
    m = title_blue.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"title blue rows {g}")

print()
print("=== RED STRUCTURES (all frame) ===")
red = (R > 120) & (R - G > 45) & (R - B > 45)
print("red rows>120:", [(int(y), int(red[y].sum())) for y in np.where(red.sum(axis=1) > 120)[0]])
print("red cols>120:", [(int(x), int(red[:, x].sum())) for x in np.where(red.sum(axis=0) > 120)[0]])

print()
print("=== PLOT PANEL BORDER (thin red lines) ===")
# horizontal thin red lines: rows where red run is long but not full-frame
for y in range(H):
    row = red[y]
    xs = np.where(row)[0]
    if len(xs) > 200:
        print(f"  row {y}: red span x {xs.min()}-{xs.max()} n={len(xs)}")
for x in range(W):
    col = red[:, x]
    ys = np.where(col)[0]
    if len(ys) > 200:
        print(f"  col {x}: red span y {ys.min()}-{ys.max()} n={len(ys)}")

print()
print("=== BLACK AXES ===")
black = (R < 90) & (G < 90) & (B < 90)
for y in range(H):
    if black[y].sum() > 150:
        xs = np.where(black[y])[0]
        print(f"  black row {y}: x {xs.min()}-{xs.max()} n={len(xs)}")
for x in range(W):
    if black[:, x].sum() > 120:
        ys = np.where(black[:, x])[0]
        print(f"  black col {x}: y {ys.min()}-{ys.max()} n={len(ys)}")

print()
print("=== BLUE BOUNDARY + Undefined ===")
blue = (B > 110) & (B - R > 45) & (B - G > 25)
for g in cluster_rows(blue, 12):
    m = blue.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"blue band rows {g}")
print("blue cols>25:", [(int(x), int(blue[:, x].sum())) for x in np.where(blue.sum(axis=0) > 25)[0]])

print()
print("=== GREEN BOUNDARY ===")
green = (G > 110) & (G - R > 35) & (G - B > 25)
for g in cluster_rows(green, 12):
    m = green.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"green band rows {g}")

print()
print("=== YELLOW (C tags + badge) ===")
yellow = (R > 190) & (G > 170) & (B < 170) & (R - B > 45)
for g in cluster_rows(yellow, 4):
    m = yellow.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"yellow band rows {g}")

print()
print("=== MAGENTA / PURPLE (New Class, badge ring, tiny ?) ===")
mag = (R > 130) & (B > 130) & (G < R - 40) & (G < B - 40)
for g in cluster_rows(mag, 2):
    m = mag.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"magenta band rows {g}")

print()
print("=== SALMON (? boxes) ===")
salmon = (R > 230) & (G > 200) & (G < 235) & (B > 190) & (B < 225) & (R - B > 15)
for g in cluster_rows(salmon, 4):
    m = salmon.copy(); m[:g[0], :] = False; m[g[1] + 1:, :] = False
    bbox(m, f"salmon band rows {g}")

print()
print("=== BOTTOM BLACK BAND ===")
for y in range(H - 40, H):
    if black[y].sum() > 500:
        xs = np.where(black[y])[0]
        print(f"  band row {y}: x {xs.min()}-{xs.max()}")
        break
