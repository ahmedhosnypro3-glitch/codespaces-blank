import sys
from PIL import Image
import numpy as np

n = int(sys.argv[1]); COLS = int(sys.argv[2]); thr = int(sys.argv[3]) if len(sys.argv) > 3 else 205
im = Image.open(f"unique_slides/slide_{n:03d}.jpg").convert("RGB")
W, H = im.size
ar = np.array(im).astype(int)
g = ar.mean(2); sat = ar.max(2) - ar.min(2)
rows = max(1, int(COLS * H / W / 2.1))
print(f"# slide {n} faint-ink map cols={COLS} rows={rows} thr={thr} bg≈{np.bincount(g.astype(int).ravel()).argmax()}")
for ry in range(rows):
    y0, y1 = int(ry * H / rows), int((ry + 1) * H / rows)
    line = []
    for cx in range(COLS):
        x0, x1 = int(cx * W / COLS), int((cx + 1) * W / COLS)
        blk = g[y0:y1, x0:x1]; sblk = sat[y0:y1, x0:x1]
        dark = (blk < thr).mean(); col = (sblk > 45).mean()
        if dark > 0.35: c = "#"
        elif dark > 0.15: c = "+"
        elif dark > 0.04: c = "."
        elif col > 0.35: c = "R"
        elif col > 0.10: c = "r"
        else: c = " "
        line.append(c)
    print(f"{int(ry*H/rows):3d}|" + "".join(line))
