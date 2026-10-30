#!/usr/bin/env python3
"""Measure colored layout boxes in original frames + prior renders (a11)."""
from PIL import Image
import sys

def classify(rgb):
    r, g, b = rgb[:3]
    if r > 230 and g > 230 and b > 230:
        return "white"
    if r < 60 and g < 60 and b < 60:
        return "black"
    if r > 150 and g < 90 and b < 90:
        return "red"
    if r > 190 and g > 190 and b < 140:
        return "yellow"
    if b > 150 and r < 160 and g < 200:
        return "blue"
    if g > 120 and r < 160 and b < 120:
        return "green"
    if r > 190 and 120 < g < 200 and b < 110:
        return "orange"
    if r > 150 and g < 130 and b > 150:
        return "magenta"
    if r > 170 and 130 < g < 190 and 100 < b < 190:
        return "pink"
    if 150 < r < 230 and 140 < g < 220 and b < 140:
        return "tan"
    if r > 200 and g > 220 and b > 220:
        return "cyan"
    if r > 180 and g > 170 and 100 < b < 180:
        return "cream"
    return None

def boxes(img, scale, min_area=250):
    W, H = img.size
    px = img.load()
    # grid-scan: sample every 4px, accumulate colored cells
    counts = {}
    for y in range(0, H, 4):
        for x in range(0, W, 4):
            c = classify(px[x, y])
            if c:
                counts.setdefault(c, []).append((x, y))
    out = []
    for c, pts in counts.items():
        if len(pts) * 16 < min_area:
            continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        # skip the global red frame (touches most of image edges)
        out.append((c, round(min(xs)/scale, 3), round(min(ys)/scale, 3),
                    round((max(xs)-min(xs))/scale, 3), round((max(ys)-min(ys))/scale, 3),
                    len(pts)))
    return sorted(out, key=lambda t: -t[5])

path = sys.argv[1]
img = Image.open(path).convert("RGB")
W, H = img.size
print(f"{path}: {W}x{H}")
# assume render 2000x1125 (150dpi of 13.33x7.5in) or original ~960x540
scale = W / 13.333
for row in boxes(img, scale):
    print(f"  {row[0]:8s} x={row[1]:6.2f} y={row[2]:6.2f} w={row[3]:6.2f} h={row[4]:6.2f} n={row[5]}")
