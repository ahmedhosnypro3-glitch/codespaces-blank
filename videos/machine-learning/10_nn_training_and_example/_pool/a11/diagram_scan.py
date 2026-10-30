#!/usr/bin/env python3
"""Row-scan: find tan/canvas extents and node columns in the NN diagram (a11)."""
from PIL import Image
import sys

def tanish(p):
    r, g, b = p[:3]
    return 185 <= r <= 235 and 175 <= g <= 225 and 155 <= b <= 210 and r > b + 8

def scan(path):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    scale = W / 13.333
    print(f"== {path} {W}x{H} scale={scale:.1f}px/in")
    # row extents of tan
    rows = []
    for y in range(H):
        xs = [x for x in range(W) if tanish(px[x, y])]
        if len(xs) > W * 0.02:
            rows.append((y, min(xs), max(xs), len(xs)))
    if rows:
        print(f"  tan rows y={rows[0][0]/scale:.2f}..{rows[-1][0]/scale:.2f}")
        for y, x0, x1, n in rows[::max(1, len(rows)//12)]:
            print(f"    y={y/scale:5.2f} tan x={x0/scale:5.2f}..{x1/scale:5.2f} n={n}")
    # column extent of tan across the diagram band
    band = (rows[0][0], rows[-1][0]) if rows else (0, H)
    cols = []
    for x in range(W):
        n = sum(1 for y in range(band[0], band[1]) if tanish(px[x, y]))
        cols.append(n)
    mx = max(cols) if cols else 0
    thresh = mx * 0.25
    xs = [i for i, n in enumerate(cols) if n >= thresh]
    if xs:
        print(f"  tan cols x={min(xs)/scale:.2f}..{max(xs)/scale:.2f} (maxcol n={mx})")
    # saturated node colors in diagram band: find x-clusters of strong color
    def sat(p):
        r, g, b = p[:3]
        mx, mn = max(p[:3]), min(p[:3])
        return (mx - mn) > 70 and mx > 90
    colhits = []
    for x in range(W):
        n = sum(1 for y in range(band[0], band[1]) if sat(px[x, y]))
        colhits.append(n)
    print("  saturated-color column profile (x_in: hits):")
    line = []
    for x in range(0, W, 4):
        n = sum(colhits[x:x+4])
        if n:
            line.append(f"{x/scale:.2f}:{n}")
    print("   " + " ".join(line[:90]))

scan(sys.argv[1])
