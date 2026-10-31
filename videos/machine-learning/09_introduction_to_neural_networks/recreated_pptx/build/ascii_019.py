#!/usr/bin/env python3
"""Coarse ASCII palette map of unique_slides/slide_019.jpg (960x540)."""
import os
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
V = os.path.join(ROOT, "videos/machine-learning/09_introduction_to_neural_networks")
im = Image.open(os.path.join(V, "unique_slides/slide_019.jpg")).convert("RGB")
W, H = im.size
px = im.load()

STEP = 12
print("cols x = 0,12,24,...  rows y = 0,12,24,...")
hdr = "      " + "".join(f"{x%100//10}" for x in range(0, W, STEP))
print(hdr)


def cls(c):
    r, g, b = c
    if r > 240 and g > 240 and b > 240:
        return "W"          # white
    if r < 60 and g < 60 and b < 60:
        return "k"          # black ink
    if r > 200 and 200 < g < 250 and b < 220 and g > b:
        return "Y"          # yellow badge
    if r > 150 and g < 110 and b < 110:
        return "R"          # red / rose
    if r > 180 and g > 120 and b > 100 and r - g > 30:
        return "P"          # peach
    if b > 130 and b - r > 40 and b - g > 40:
        return "B"          # blue
    if max(c) - min(c) < 20 and 190 < r < 250:
        return "n"          # near-white grey
    if max(c) - min(c) < 25 and 120 < r < 195:
        return "g"          # mid grey
    if r > 150 and g > 140 and b > 140 and r - g < 20:
        return "t"          # taupe
    return "."


for y in range(0, H, STEP):
    line = "".join(cls(px[x, y]) for x in range(0, W, STEP))
    print(f"y={y:4d} {line}")

# specific probe points
probes = [
    ("frame left border", 62, 300), ("frame top border", 480, 50),
    ("panel TL border top", 240, 60), ("panel TL border left", 100, 150),
    ("panel TL interior", 240, 120),
    ("caption TL fill", 240, 260), ("caption TR fill", 610, 260),
    ("caption BL fill", 240, 490), ("caption BR fill", 610, 490),
    ("badge", 820, 70),
]
print("\n-- probes --")
for name, x, y in probes:
    print(f"{name:24s} ({x},{y}) = {px[x, y]}")
