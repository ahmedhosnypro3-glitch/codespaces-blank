"""Pixel-classified ASCII map of slide_022 content area: reveals box borders per row."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

BLK = 4  # block size

def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    sat = mx - mn
    # pale yellow fill ~ (253,255,233)
    if r > 235 and g > 235 and b > 180 and b < 250 and (g - b) > 8:
        return "Y"
    # peach fill ~ (250,233,215)
    if r > 235 and 190 < g < 250 and 180 < b < 240 and (r - b) > 15 and (r - g) > 8:
        return "P"
    # white
    if mx > 240 and sat < 22:
        return "."
    # gray bg
    if abs(r - 240) < 14 and abs(g - 240) < 14 and abs(b - 240) < 14 and sat < 16:
        return " "
    # green text
    if g > 90 and (g - r) > 40 and (g - b) > 40:
        return "G"
    # red text (saturated, dark)
    if r > 110 and (r - g) > 70 and (r - b) > 70 and g < 115:
        return "R"
    # black text
    if mx < 130 and sat < 78:
        return "#"
    # anything else = border / other colored ink
    return "X"

print("Block size %d px.  Y=pale-yellow fill  P=peach fill  R=red text  G=green text  #=black  X=border/other" % BLK)
print("     " + "".join(str((bx * BLK // 100) % 10) for bx in range(W // BLK)))
for by in range(104, 520, BLK):
    line = ""
    for bx in range(40, 960, BLK):
        sub = a[by:by + BLK, bx:bx + BLK].reshape(-1, 3)
        # majority class over block, but X (border) wins if present
        cls = [classify(p) for p in sub]
        c = {}
        for x in cls:
            c[x] = c.get(x, 0) + 1
        if "X" in c and c["X"] >= len(cls) * 0.5:
            line += "X"
        else:
            best = max(c, key=lambda k: c[k])
            line += best
    print("y%3d|%s" % (by, line))
