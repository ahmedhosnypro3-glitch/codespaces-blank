import sys
from PIL import Image
import numpy as np

n = int(sys.argv[1]); x0 = int(sys.argv[2]); x1 = int(sys.argv[3]); y0 = int(sys.argv[4]); y1 = int(sys.argv[5]); COLS = int(sys.argv[6])
im = Image.open(f"unique_slides/slide_{n:03d}.jpg").convert("RGB")
ar = np.array(im).astype(int)
r, g, b = ar[:, :, 0], ar[:, :, 1], ar[:, :, 2]
mx = ar.max(2); mn = ar.min(2); sat = mx - mn
gray = ar.mean(2)
H = y1 - y0; W = x1 - x0
rows = max(1, int(COLS * H / W / 2.1))
print(f"# slide {n} color map x[{x0},{x1}) y[{y0},{y1}) cols={COLS} rows={rows} x/col={(x1-x0)/COLS:.1f} y/row={(y1-y0)/rows:.1f}")
print("legend: R=red P=pink O=orange Y=yellow G=green B=blue K=black d=dark-gray g=mid l=light w=white .=faint")
for ry in range(rows):
    yy0, yy1 = y0 + int(ry*H/rows), y0 + int((ry+1)*H/rows)
    line = []
    for cx in range(COLS):
        xx0, xx1 = x0 + int(cx*W/COLS), x0 + int((cx+1)*W/COLS)
        R = r[yy0:yy1, xx0:xx1].mean(); G = g[yy0:yy1, xx0:xx1].mean(); B = b[yy0:yy1, xx0:xx1].mean()
        S = sat[yy0:yy1, xx0:xx1].mean(); Gy = gray[yy0:yy1, xx0:xx1].mean()
        if S > 45:
            if R > G + 35 and B < G + 25:
                c = "R" if G < 130 else "P"
            elif R > G + 25 and G > B + 25:
                c = "O"
            elif R > 150 and G > 130 and B < G - 35:
                c = "Y"
            elif G > R + 20 and G > B + 20:
                c = "G"
            elif B > R + 20:
                c = "B"
            else:
                c = "R"
        elif Gy < 90: c = "K"
        elif Gy < 150: c = "d"
        elif Gy < 225: c = "g"
        elif Gy < 243: c = "l"
        else: c = "w"
        line.append(c)
    print(f"{yy0:4d}|" + "".join(line))
