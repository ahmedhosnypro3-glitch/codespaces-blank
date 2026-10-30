#!/usr/bin/env python3
"""Print RGB along a node row of the slide-019 diagram (a11)."""
import sys
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
W, H = img.size
sc = W / 13.333
px = img.load()
y = int(float(sys.argv[2]) * sc)
x0, x1 = float(sys.argv[3]), float(sys.argv[4])
print(f"y={sys.argv[2]}in (row {y}px)")
run = []
for xi in range(int(x0 * sc), int(x1 * sc)):
    r, g, b = px[xi, y]
    # is it tan bg?
    if r > 170 and g > 155 and b < r and (r - b) < 95:
        key = "BG"
    elif r > 228 and g > 228 and b > 218:
        key = "WH"
    else:
        key = f"{r:02x}{g:02x}{b:02x}"
    run.append((xi / sc, key))
# compress consecutive identical keys
i = 0
while i < len(run):
    j = i
    while j + 1 < len(run) and run[j + 1][1] == run[i][1]:
        j += 1
    print(f"  x={run[i][0]:6.3f}..{run[j][0]:6.3f}  {run[i][1]}")
    i = j + 1
