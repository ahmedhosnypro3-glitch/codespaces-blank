import sys
from PIL import Image
import numpy as np

n = int(sys.argv[1]); x0 = int(sys.argv[2]); x1 = int(sys.argv[3]); y0 = int(sys.argv[4]); y1 = int(sys.argv[5]); COLS = int(sys.argv[6])
im = Image.open(f"unique_slides/slide_{n:03d}.jpg").convert("RGB")
ar = np.array(im).astype(int)
g = ar.mean(2); sat = ar.max(2) - ar.min(2)
H = y1 - y0; W = x1 - x0
rows = max(1, int(COLS * H / W / 2.1))
print(f"# slide {n} region x[{x0},{x1}) y[{y0},{y1}) cols={COLS} rows={rows} (x per col={(x1-x0)/COLS:.1f}px, y per row={(y1-y0)/rows:.1f}px)")
hdr = "     "
for c in range(0, COLS, 10):
    hdr += f"{x0 + int(c*(x1-x0)/COLS):<10d}"
print(hdr)
for ry in range(rows):
    yy0, yy1 = y0 + int(ry*H/rows), y0 + int((ry+1)*H/rows)
    line = []
    for cx in range(COLS):
        xx0, xx1 = x0 + int(cx*W/COLS), x0 + int((cx+1)*W/COLS)
        blk = g[yy0:yy1, xx0:xx1]; sblk = sat[yy0:yy1, xx0:xx1]
        dark = (blk < 120).mean(); col = (sblk > 70).mean()
        if dark > 0.45: c = "#"
        elif dark > 0.18: c = "+"
        elif dark > 0.05: c = "."
        elif col > 0.45: c = "R"
        elif col > 0.15: c = "r"
        else: c = " "
        line.append(c)
    print(f"{yy0:4d}|" + "".join(line))
