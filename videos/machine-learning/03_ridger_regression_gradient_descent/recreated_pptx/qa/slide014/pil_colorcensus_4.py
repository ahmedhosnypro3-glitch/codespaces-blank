#!/usr/bin/env python3
"""Definitive ink census: classify pixels into color classes (red/green/blue/black/fill),
print per-band text lines with per-color x-extents. Also dumps render for comparison.
"""
from PIL import Image
import numpy as np
from collections import Counter

def classify(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    s = r + g + b
    if s < 330:
        # dark: decide hue
        if r > g + 40 and r > b + 40: return "red"
        if b > r + 40: return "blue"
        if g > r + 25 and g > b + 25: return "green"
        return "black"
    if r > g + 45 and r > b + 45 and s < 620: return "red"
    if b > r + 35 and b > g + 20 and s < 720: return "blue"
    if g > r + 20 and g > b + 20 and s < 720: return "green"
    return "fill"

def band_census(a, name, x0, x1, y0, y1, fills):
    print(f"\n--- {name} x{x0}..{x1} y{y0}..{y1}")
    # ink per row per color
    for label_y in range(y0, y1 + 1):
        row = a[label_y]
        per = {}
        for x in range(x0, x1 + 1):
            c = classify(row[x])
            if c != "fill":
                per.setdefault(c, []).append(x)
        if per:
            desc = []
            for c, xs in sorted(per.items()):
                desc.append(f"{c}:{len(xs)}px x{min(xs)}..{max(xs)}")
            print(f"  y={label_y}: " + " | ".join(desc))

im = Image.open("unique_slides/slide_014.jpg").convert("RGB")
a = np.asarray(im).astype(int)
print("############ ORIGINAL ############")
# text interiors only (exclude border rows)
band_census(a, "ridge text", 92, 877, 252, 280, None)
band_census(a, "objective text", 91, 877, 310, 335, None)
band_census(a, "midband1 text", 94, 658, 353, 387, None)
band_census(a, "midband2 text", 94, 466, 407, 441, None)
band_census(a, "midband3 text", 538, 875, 408, 442, None)

# lower blue: summarize
print("\n--- lowerblue (full region) x91..883 y468..530 — ink rows only")
for y in range(468, 531):
    row = a[y]
    per = {}
    for x in range(91, 884):
        c = classify(row[x])
        if c != "fill":
            per.setdefault(c, []).append(x)
    if per:
        desc = []
        for c, xs in sorted(per.items()):
            desc.append(f"{c}:{len(xs)} x{min(xs)}..{max(xs)}")
        print(f"  y={y}: " + " | ".join(desc))
