import sys
import numpy as np
from PIL import Image

# Crop the 4 equation lines of slide_019 bottom-right panel from the ORIGINAL,
# upscale heavily, and save for vision reading.
o = Image.open(sys.argv[1]).convert("RGB")
bands = [(247, 280), (304, 342), (363, 402), (423, 461)]
x0, x1 = 640, 875
out = sys.argv[2]
for i, (y0, y1) in enumerate(bands, 1):
    c = o.crop((x0, y0 - 3, x1, y1 + 3))
    c = c.resize((c.width * 8, c.height * 8), Image.LANCZOS)
    c.save(f"{out}/line{i}.png")
    print(f"line{i}.png {c.size}")
