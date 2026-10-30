import sys
from PIL import Image
import numpy as np

n = int(sys.argv[1]) if len(sys.argv) > 1 else 18
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 150
im = Image.open(f"unique_slides/slide_{n:03d}.jpg").convert("RGB")
W, H = im.size
ar = np.array(im).astype(int)
rows = int(COLS * H / W / 2.1)
g = ar.mean(2)
sat = ar.max(2) - ar.min(2)
for ry in range(rows):
    y0, y1 = int(ry * H / rows), int((ry + 1) * H / rows)
    line = []
    for cx in range(COLS):
        x0, x1 = int(cx * W / COLS), int((cx + 1) * W / COLS)
        blk = g[y0:y1, x0:x1]
        sblk = sat[y0:y1, x0:x1]
        dark = (blk < 120).mean()
        col = (sblk > 70).mean()
        if dark > 0.45:
            c = "#"
        elif dark > 0.18:
            c = "+"
        elif dark > 0.05:
            c = "."
        elif col > 0.45:
            c = "R"
        elif col > 0.15:
            c = "r"
        else:
            c = " "
        line.append(c)
    print(f"{int(ry*H/rows):3d}|" + "".join(line))
