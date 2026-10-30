#!/usr/bin/env python3
"""Hue-based ASCII map of an original lecture frame or render.
Usage: ascii_map.py <img> [cell] [x0 y0 x1 y1]"""
import sys
import numpy as np
from PIL import Image

def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    if mx - mn < 22:
        if mx > 225: return "."
        if mx > 200: return ":"
        if mx > 130: return "+"
        if mx > 60: return "%"
        return "#"
    if r > g and r > b:
        if g > 170 and b > 170: return "Y"          # pale yellow
        if g > 120: return "O"                       # orange
        if g > 60 and b > 60: return "M"             # magenta/rose
        return "R"                                   # red
    if g > r and g > b: return "G"                   # green
    if b > r and b > g:
        if r > 200 and g > 200: return "c"           # cyan-ish pale
        if r > 140: return "m"                       # purple
        return "B"                                   # blue
    return "?"

def main():
    path = sys.argv[1]
    cell = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    x0 = y0 = 0
    x1 = y1 = 10**9
    if len(sys.argv) > 6:
        x0, y0, x1, y1 = (int(v) for v in sys.argv[3:7])
    im = Image.open(path).convert("RGB")
    im = im.crop((max(0, x0), max(0, y0), min(im.size[0], x1), min(im.size[1], y1)))
    a = np.asarray(im).astype(int)
    H, W = a.shape[:2]
    print(f"# {path} {im.size} cell={cell} crop=({x0},{y0},{x1},{y1})")
    print("# legend: R red  O orange  Y peach/cream  M rose/magenta  G green")
    print("#         B blue  m purple  c pale-cyan  . near-white  : light-gray  + mid-gray  % dark-gray  # black")
    for y in range(0, H, cell):
        row = ""
        for x in range(0, W, cell):
            px = a[y:y + cell, x:x + cell].reshape(-1, 3)
            counts = {}
            for p in px:
                counts[classify(tuple(p))] = counts.get(classify(tuple(p)), 0) + 1
            counts.pop(".", None)
            row += (max(counts, key=counts.get) if counts else ".")
        print(row)

main()
