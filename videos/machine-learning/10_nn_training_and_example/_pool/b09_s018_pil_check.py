#!/usr/bin/env python3
"""b09 s018 closed-loop: measure original + banked attempt2 render, report deltas."""
import json, sys
from PIL import Image

SRC = "unique_slides/slide_018.jpg"
RND = "qa/slide018/rejudge/attempt2/render-1.png"

def load(p):
    im = Image.open(p).convert("RGB")
    print(f"== {p} size={im.size}")
    return im

def near(px, rgb, tol=28):
    return all(abs(px[i] - rgb[i]) <= tol for i in range(3))

def bbox_of(img, rgb, tol=28, region=None, min_hits=8):
    W, H = img.size
    x0, y0, x1, y1 = region or (0, 0, W, H)
    hits = 0
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if near(img.getpixel((x, y)), rgb, tol):
                xs.append(x); ys.append(y); hits += 1
    if hits < min_hits:
        return None
    return (min(xs), min(ys), max(xs), max(ys))

def panel_scan(img, label, pred, region):
    x0, y0, x1, y1 = region
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(img.getpixel((x, y))):
                xs.append(x); ys.append(y)
    if not xs:
        print(f"  {label}: NO HITS")
        return None
    print(f"  {label}: bbox=({min(xs)},{min(ys)})-({max(xs)},{max(ys)}) n={len(xs)}")
    return (min(xs), min(ys), max(xs), max(ys))

PROBES = [
    ("cream_panel", (247, 241, 228)),
    ("panel_border_maroon", (150, 40, 40)),
    ("error_bar_darkred", (204, 0, 0)),
    ("badge_yellow", (255, 249, 196)),
    ("badge_yellow2", (255, 217, 0)),
    ("magenta_dot", (204, 0, 204)),
    ("sigmoid_green", (184, 232, 168)),
    ("output_blue", (32, 32, 192)),
    ("title_maroon", (192, 0, 0)),
]

for path in (SRC, RND):
    im = load(path)
    for name, rgb in PROBES:
        b = bbox_of(im, rgb, 30)
        print(f"  {name:22s} {rgb} -> {b}")
    print()

print("=== ORIGINAL detail bands (960x540 coords) ===")
o = load(SRC)
panel_scan(o, "dark_ink_rows 60..210 x360..900",
           lambda p: sum(p) < 300, (360, 60, 900, 210))
print("=== RENDER detail bands (2000x1125 coords) ===")
r = load(RND)
panel_scan(r, "dark_ink_rows scaled",
           lambda p: sum(p) < 300, (750, 125, 1875, 437))
