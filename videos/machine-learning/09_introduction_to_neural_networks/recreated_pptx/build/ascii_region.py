#!/usr/bin/env python3
"""ASCII-art dump of a region so the text layout can be read from pixels."""
import sys
from PIL import Image
import numpy as np

path = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg"
img = Image.open(path).convert("RGB")
a = np.asarray(img).astype(int)

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 2

reg = a[y0:y1, x0:x1]
r, g, b = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
mx = reg.max(axis=2)
mn = reg.min(axis=2)

ink = mx < 205
red = (r - g > 40) & (r - b > 40)
green = (g - r > 30) & (g - b > 30)
blue = (b - r > 55) & (b - g > 55)

ch = np.full(reg.shape[:2], " ", dtype="<U1")
ch[ink] = "#"
ch[red & ink] = "R"
ch[green & ink] = "G"
ch[blue & ink] = "B"

print(f"region x{x0}-{x1} y{y0}-{y1}  (step {step})")
for yy in range(0, reg.shape[0], step):
    print(f"{y0+yy:4d} " + "".join(ch[yy, xx] for xx in range(0, reg.shape[1], step)))
