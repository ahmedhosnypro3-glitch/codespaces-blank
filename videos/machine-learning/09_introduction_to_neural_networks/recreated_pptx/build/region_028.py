"""Region map for slide_028 original: quantize colors, find contiguous region bounds."""
import numpy as np
from PIL import Image
from collections import Counter

ORIG = Image.open("../../unique_slides/slide_028.jpg").convert("RGB")
o = np.asarray(ORIG).astype(int)

def q(c):
    return tuple((v // 24) * 24 for v in c)

# coarse region map at 4px blocks
H, W, _ = o.shape
bs = 4
rows = []
for y in range(0, H, bs):
    line = ""
    for x in range(0, W, bs):
        block = o[y:y+bs, x:x+bs].reshape(-1, 3)
        c = Counter(map(q, block)).most_common(1)[0][0]
        # classify
        r, g, b = c
        if r > 220 and g > 220 and b > 220:
            ch = "."      # near white
        elif abs(r-218) < 26 and abs(g-208) < 26 and abs(b-196) < 26:
            ch = "T"      # tan body
        elif abs(r-231) < 12 and abs(g-233) < 12 and abs(b-230) < 12:
            ch = "G"      # gray house
        elif r > 150 and g < 90 and b < 90:
            ch = "R"      # red
        elif r < 90 and g < 90 and b < 90:
            ch = "K"      # black
        elif b > 120 and r < 110:
            ch = "B"      # blue
        elif g > 120 and r < 130:
            ch = "G2"     # green
        elif r > 140 and b > 140 and g < 120:
            ch = "P"      # purple
        elif r > 180 and g > 140 and b < 110:
            ch = "O"      # orange
        else:
            ch = "?"
        line += ch
    rows.append(line)

print("    " + "".join(str((x//bs)//10 % 10) for x in range(0, W, bs)))
for i, line in enumerate(rows):
    print("%3d %s" % (i * bs, line))
