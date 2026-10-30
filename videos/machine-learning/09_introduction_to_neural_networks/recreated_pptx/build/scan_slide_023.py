#!/usr/bin/env python3
"""Precise horizontal scan of slide_023 row bands to locate boxes and borders."""
from PIL import Image
import numpy as np

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg")
a = np.asarray(img.convert("RGB"))
H, W, _ = a.shape


def hexs(rgb):
    return "#%02X%02X%02X" % tuple(int(v) for v in rgb)


def classify(px):
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    if r > 235 and g > 245 and b > 235:
        return "W"          # white
    if r > 240 and 215 < g < 245 and 195 < b < 235:
        return "P"          # peach
    if r > 240 and g > 235 and 190 < b < 240 and r - b > 8:
        return "C"          # cream
    if r > 120 and g < 100 and b < 100:
        return "R"          # red
    if b > 150 and b - r > 50:
        return "V"          # violet/blue
    if g > 90 and r < 120 and b < 120:
        return "G"          # green
    if r < 80 and g < 80 and b < 80:
        return "K"          # black
    return "."


for label, y in [("row1", 165), ("row2", 245), ("row3", 320), ("row4", 400), ("row5", 470)]:
    line = a[y]
    s = "".join(classify(px) for px in line)
    # compress runs
    runs = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        runs.append((s[i], i, j - 1))
        i = j
    print(f"\n=== {label} (y={y}) ===")
    for c, a0, a1 in runs:
        if c != "W" or (a1 - a0) > 25:
            print(f"  {c} x{a0}-{a1}  ({a0/W:.3f}-{a1/W:.3f})  sample {hexs(line[a0])}")

print("\n=== vertical scan at x=100 (left box column) ===")
for x in [60, 70, 100, 500, 660, 700, 860, 895, 900]:
    col = a[:, x]
    s = "".join(classify(px) for px in col)
    runs = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        runs.append((s[i], i, j - 1))
        i = j
    out = [f"{c}{a0}-{a1}" for c, a0, a1 in runs if c in "RPC" and (a1 - a0) > 3]
    print(f"  x={x}: {' '.join(out)}")
