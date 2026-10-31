#!/usr/bin/env python3
"""b09 s018: colour grid map of the original's panels (960-space)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
o = np.asarray(Image.open(NS + "unique_slides/slide_018.jpg").convert("RGB")).astype(np.int16)

def cls(p):
    r, g, b = p
    if abs(r - 231) < 12 and abs(g - 233) < 12 and abs(b - 230) < 12: return "G"   # light grey
    if abs(r - 218) < 12 and abs(g - 206) < 12 and abs(b - 194) < 12: return "C"   # cream
    if r > 240 and g > 240 and b > 180 and g - r > -5 and b < 220: return "Y"       # badge yellow
    if r > 190 and g < 80 and b < 80: return "R"                                     # red
    if abs(r - 210) < 25 and abs(g - 165) < 30 and abs(b - 172) < 30 and r > g: return "P"  # pink border
    if r > 150 and b > 150 and g < 120: return "M"                                   # magenta
    if r < 110 and g < 110 and b > 110: return "B"                                   # blue
    if g > 190 and r > 140 and b < 200: return "V"                                   # green
    return "."

hdr_x = "     " + "".join(f"{x%100//10}" for x in range(300, 960, 20))
print(hdr_x)
for y in range(50, 215, 4):
    print(f"{y:4d} " + "".join(cls(o[y, x]) for x in range(300, 960, 20)))
print()
print("legend: G=grey C=cream Y=yellow R=red P=pink-border M=magenta B=blue V=green .=other")
print()
print("== fine: x 740..800 step 2, y 56..72 ==")
for y in range(56, 74, 2):
    print(f" {y:3d} " + "".join(cls(o[y, x]) for x in range(740, 802, 2)))
print("== fine: x 880..960 step 2, y 56..72 ==")
for y in range(56, 74, 2):
    print(f" {y:3d} " + "".join(cls(o[y, x]) for x in range(880, 960, 2)))
print("== fine: x 860..960 step 2, y 180..200 ==")
for y in range(180, 200, 2):
    print(f" {y:3d} " + "".join(cls(o[y, x]) for x in range(860, 960, 2)))
print("== fine: x 60..140 step 2, y 40..70 ==")
for y in range(40, 70, 2):
    print(f" {y:3d} " + "".join(cls(o[y, x]) for x in range(60, 140, 2)))
