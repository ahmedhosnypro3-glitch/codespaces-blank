#!/usr/bin/env python3
"""Leader lines, class-region tints and arrowhead tips on slide_008.jpg."""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)

print("=== UNDEFINED leader lines: x 140..300, y 130..200 (any non-white, non-gray) ===")
for y in range(130, 200):
    s = ""
    for x in range(140, 301, 2):
        r, g, b = a[y, x]
        if r > 240 and g > 238 and b > 236: s += "."
        elif b - r > 25 and b > 110: s += "B"
        elif r > 130 and r - g > 45 and r - b > 45: s += "R"
        elif r < 110 and g < 110 and b < 110: s += "K"
        else: s += "+"
    print(f"{y:4d} {s}")

print()
print("=== class-region tint samples ===")
pts = {
    "upper-left green region": [(300, 200), (280, 250), (350, 180), (450, 220), (230, 230)],
    "right lavender region":   [(650, 350), (700, 300), (620, 450), (740, 400)],
    "lower-left region":       [(400, 420), (350, 460), (450, 390), (500, 460), (300, 340)],
    "left gray wedge":         [(210, 300), (230, 300), (190, 280), (240, 260)],
    "far bottom edge":         [(300, 495), (500, 495), (700, 495)],
}
for k, ps in pts.items():
    print(" ", k)
    for (x, y) in ps:
        print(f"    ({x},{y}) = {tuple(a[y, x])}")

print()
print("=== horizontal axis arrowhead: x 640..700, y 425..448 ===")
for y in range(424, 449):
    s = ""
    for x in range(640, 701):
        r, g, b = a[y, x]
        if r > 240 and g > 238 and b > 236: s += "."
        elif r > 130 and r - g > 40 and r - b > 40: s += "R"
        elif r < 110 and g < 110 and b < 110: s += "K"
        else: s += "+"
    print(f"{y:4d} {s}")

print()
print("=== vertical axis bottom end: x 295..325, y 425..460 ===")
for y in range(425, 461):
    s = ""
    for x in range(295, 326):
        r, g, b = a[y, x]
        if r > 240 and g > 238 and b > 236: s += "."
        elif r > 130 and r - g > 40 and r - b > 40: s += "R"
        elif r < 110 and g < 110 and b < 110: s += "K"
        else: s += "+"
    print(f"{y:4d} {s}")
