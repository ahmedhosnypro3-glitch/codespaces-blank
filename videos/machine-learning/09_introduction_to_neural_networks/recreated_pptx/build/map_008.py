#!/usr/bin/env python3
"""Character map of slide_008.jpg distinguishing pure white / gray / hatch tints."""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W, _ = a.shape


def cls(r, g, b):
    if r > 245 and g > 245 and b > 243:
        return "W"          # pure white
    if abs(r - g) < 8 and abs(g - b) < 8 and 215 < r < 245:
        return "g"          # light gray
    if r > 130 and r - g > 45 and r - b > 45:
        return "R"
    if b > 140 and b - r > 80 and b - g > 60:
        return "B"
    if g > 130 and g - r > 40 and g - b > 25:
        return "G"
    if r > 230 and g > 200 and g < 240 and b > 180 and b < 232 and r - b > 18:
        return "p"          # pale pink/salmon
    if r > 200 and g > 190 and b < 150 and r - b > 70:
        return "Y"
    if r < 90 and g < 90 and b < 90:
        return "K"
    if g > r + 8 and g > b + 8 and r > 180:
        return "h"          # pale green
    if b > r + 8 and b > g + 8 and r > 180:
        return "l"          # pale lavender
    return "."


step = 10
print("     " + "".join(str((x // 100) % 10) for x in range(40, 921, step)))
print("     " + "".join(str((x // 10) % 10) for x in range(40, 921, step)))
for y in range(40, 521, step):
    line = ""
    for x in range(40, 921, step):
        blk = a[y:y + step, x:x + step].reshape(-1, 3)
        # majority class
        cs = [cls(int(r), int(g), int(b)) for r, g, b in blk]
        line += max(set(cs), key=cs.count)
    print(f"{y:4d} {line}")
