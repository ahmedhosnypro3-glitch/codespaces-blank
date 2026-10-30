#!/usr/bin/env python3
"""Horizontal-line scan of the slide-019 diagram: run-length of non-background
pixels across specified y-lines, plus a scan for the dashed arcs (a11)."""
import sys
import numpy as np
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
sc = W / 13.333
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
istam = (r > 175) & (g > 160) & (b < r) & ((r - b) < 90)
iswh = (r > 230) & (g > 230) & (b > 220)
ink = ~(istam | iswh)


def runs_on_line(yin, xlo=5.4, xhi=11.5, minrun=2):
    y = int(yin * sc)
    row = ink[y, int(xlo * sc):int(xhi * sc)]
    out = []
    i = 0
    while i < len(row):
        if row[i]:
            j = i
            while j < len(row) and row[j]:
                j += 1
            if j - i >= minrun:
                out.append((xlo + i / sc, xlo + j / sc))
            i = j
        else:
            i += 1
    return out


print(f"== {sys.argv[1]}")
for yin in [1.30, 1.50, 1.75, 1.90, 2.00, 2.10, 2.20, 2.30, 2.55, 2.75, 2.95, 3.15]:
    rr = runs_on_line(yin)
    print(f" y={yin:5.2f}: " + " ".join(f"[{p:.2f}-{q:.2f}]" for p, q in rr))

# vertical extents of ink in narrow x-windows around each candidate node column
print("\nCOLUMN vertical ink extents (x window -> y ranges):")
for xc in [5.60, 6.15, 6.50, 7.05, 7.95, 8.60, 9.60, 9.85, 10.70, 11.36, 11.75]:
    x = int(xc * sc)
    col = ink[int(1.0 * sc):int(3.3 * sc), x]
    ys = [i for i, v in enumerate(col) if v]
    bands = []
    if ys:
        cur = [ys[0]]
        for v in ys[1:]:
            if v - cur[-1] <= 2:
                cur.append(v)
            else:
                bands.append(cur)
                cur = [v]
        bands.append(cur)
    s = " ".join(f"{1.0 + b[0]/sc:.2f}-{1.0 + b[-1]/sc:.2f}" for b in bands if len(b) >= 2)
    print(f"  x={xc:6.2f}: {s}")
