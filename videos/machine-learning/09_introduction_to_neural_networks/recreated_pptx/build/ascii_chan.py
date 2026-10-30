#!/usr/bin/env python3
"""Per-channel ASCII dump: show only RED / GREEN / BLUE / BLACK ink of a region."""
import sys
import numpy as np
from PIL import Image

path = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg"
img = Image.open(path).convert("RGB")
a = np.asarray(img).astype(int)

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 2
channel = sys.argv[6].lower() if len(sys.argv) > 6 else "all"

reg = a[y0:y1, x0:x1]
r, g, b = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
mx = reg.max(axis=2)

ink = mx < 205
red = (r - g > 40) & (r - b > 40)
green = (g - r > 30) & (g - b > 30)
blue = (b - r > 55) & (b - g > 55)
black = ink & ~(red | green | blue)

sel = {"red": red, "green": green, "blue": blue, "black": black}.get(channel, ink)
mask = sel & ink

print(f"region x{x0}-{x1} y{y0}-{y1} channel={channel} step={step}")
for yy in range(0, reg.shape[0], step):
    print(f"{y0+yy:4d} " + "".join("#" if mask[yy, xx] else " " for xx in range(0, reg.shape[1], step)))
