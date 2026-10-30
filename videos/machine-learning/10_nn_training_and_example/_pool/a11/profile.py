#!/usr/bin/env python3
"""Row/column ink-density profile comparison: original vs render (a11)."""
from PIL import Image
import sys

def profile(path, label):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    g = img.convert("L")
    px = g.load()
    # ink = darker than 200
    def density(y0, y1, x0, x1, step=4):
        tot = hit = 0
        for y in range(int(y0), int(y1), step):
            for x in range(int(x0), int(x1), step):
                tot += 1
                if px[x, y] < 200:
                    hit += 1
        return hit / max(tot, 1)
    print(f"-- {label} ({W}x{H}) rows (x 5%..95%):")
    for i in range(10):
        y0, y1 = H * i / 10, H * (i + 1) / 10
        print(f"   row {i}: y={y0:.0f}..{y1:.0f} ink={density(y0, y1, W*0.05, W*0.95):.3f}")
    print(f"-- {label} cols (y 5%..95%):")
    for i in range(12):
        x0, x1 = W * i / 12, W * (i + 1) / 12
        print(f"   col {i}: x={x0:.0f}..{x1:.0f} ink={density(H*0.05, H*0.95, x0, x1):.3f}")

profile(sys.argv[1], sys.argv[1].split('/')[-1])
