"""Analyze the 4 graph panels of slide_021.jpg: axes, grid, curves, labels."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)

GRAPHS = {
    "TL": (121, 109, 400, 271),
    "TR": (564, 109, 842, 274),
    "BL": (122, 346, 400, 508),
    "BR": (564, 346, 842, 508),
}

for name, (x0, y0, x1, y1) in GRAPHS.items():
    print(f"\n########## {name} graph  px x[{x0},{x1}] y[{y0},{y1}] ##########")
    sub = a[y0 + 2:y1 - 1, x0 + 2:x1 - 1]
    h, w, _ = sub.shape
    r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    dark = (r < 140) & (g < 140) & (b < 140)
    red = (r > 150) & (r - g > 50) & (r - b > 40)
    grayline = (np.abs(r - g) < 12) & (np.abs(g - b) < 12) & (r > 190) & (r < 225)

    # dark horizontal lines (axis) and vertical lines
    dr = dark.sum(axis=1)
    dc = dark.sum(axis=0)
    print("  dark rows>30%:", [(y0 + 2 + i, int(dr[i])) for i in range(h) if dr[i] > w * 0.3])
    print("  dark cols>30%:", [(x0 + 2 + j, int(dc[j])) for j in range(w) if dc[j] > h * 0.3])

    gr = grayline.sum(axis=1)
    gc = grayline.sum(axis=0)
    print("  grid rows>30%:", [(y0 + 2 + i, int(gr[i])) for i in range(h) if gr[i] > w * 0.3])
    print("  grid cols>30%:", [(x0 + 2 + j, int(gc[j])) for j in range(w) if gc[j] > h * 0.3])

    # red curve extent + leftmost/rightmost/lowest points
    ys, xs = np.where(red)
    if len(xs):
        print(f"  red ink: x [{x0+2+xs.min()},{x0+2+xs.max()}] y [{y0+2+ys.min()},{y0+2+ys.max()}] n={len(xs)}")
        # per-column min/max y of red (curve trace at 8 sample columns)
        for frac in (0.05, 0.2, 0.4, 0.5, 0.6, 0.8, 0.95):
            cx = int(frac * (w - 1))
            col = np.where(red[:, cx])[0]
            if len(col):
                print(f"    col@{frac:.2f} (x={x0+2+cx}): red y [{y0+2+col.min()},{y0+2+col.max()}]")
    # black text clusters (tick labels) - connected dark blobs outside plot area
    print("  dark ink bbox:", end=" ")
    ys2, xs2 = np.where(dark)
    if len(xs2):
        print(f"x [{x0+2+xs2.min()},{x0+2+xs2.max()}] y [{y0+2+ys2.min()},{y0+2+ys2.max()}]")
    else:
        print("none")
