# Colour ASCII map with a 10px ruler, single-pixel strokes preserved.
import sys
import numpy as np
from PIL import Image

IMG = sys.argv[1]
X0, X1, Y0, Y1, ST = (int(v) for v in sys.argv[2:7])
img = Image.open(IMG).convert("RGB")
if img.size != (960, 540):
    img = img.resize((960, 540), Image.LANCZOS)
p = img.load()


def ch(x, y):
    r, g, b = p[x, y]
    if r > 240 and g > 240 and b > 240:
        return "."
    if r > 150 and g < 120 and b < 120:
        return "R"
    if b > 130 and r < 130:
        return "B"
    if r < 120 and g < 120 and b < 120:
        return "#"
    return "+"


ruler = "     " + "".join("%d" % ((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1, ST))
print("%s x%d..%d step%d" % (IMG, X0, X1, ST))
print(ruler)
for y in range(Y0, Y1, ST):
    print("y%4d %s" % (y, "".join(ch(x, y) for x in range(X0, X1, ST))))
