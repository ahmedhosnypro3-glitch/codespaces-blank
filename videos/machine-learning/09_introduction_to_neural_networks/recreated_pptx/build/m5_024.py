#!/usr/bin/env python3
"""ASCII color map of slide_024 panel interiors (no vision calls)."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

def cls(y, x):
    R, G, B = r[y, x], g[y, x], b[y, x]
    if R > 235 and G > 235 and B > 235: return "."
    if R < 100 and G < 100 and B < 100: return "#"   # black ink
    if R - G > 55 and R - B > 55 and B < 95 and R < 215: return "r"  # crimson/red
    if R > 200 and R - G > 55 and G - B > 40 and B < 130: return "o"  # orange
    if R > 225 and G > 95 and B > 95 and R - G > 55: return "p"  # pink/salmon
    if B - R > 35 and B - G > 30: return "u"   # blue ink
    if R > 240 and G > 205 and B > 185: return " "  # peach/white fill
    if abs(R - G) < 14 and abs(G - B) < 14 and R > 150: return " "  # light gray fill
    return "?"

def dump(name, x0, x1, y0, y1, nx=72, ny=20):
    print(f"\n=== {name}  x{x0}-{x1} y{y0}-{y1} ===")
    dx, dy = (x1 - x0) / nx, (y1 - y0) / ny
    for j in range(ny):
        yy = int(y0 + (j + 0.5) * dy)
        line = ""
        for i in range(nx):
            xx = int(x0 + (i + 0.5) * dx)
            block = o[max(0, yy - 1):yy + 2, max(0, xx - 1):xx + 2].reshape(-1, 3).mean(axis=0)
            R, G, B = block
            if R > 235 and G > 235 and B > 235: c = "."
            elif R < 105 and G < 105 and B < 105: c = "#"
            elif R - G > 50 and R - B > 50 and B < 100 and R < 220: c = "r"
            elif R > 200 and R - G > 50 and G - B > 35 and B < 140: c = "o"
            elif R > 225 and G > 95 and B > 95 and R - G > 50: c = "p"
            elif B - R > 30 and B - G > 25: c = "u"
            elif abs(R - G) < 16 and abs(G - B) < 16 and R > 150: c = " "
            else: c = "?"
            line += c
        print(f"{yy:3d} {line}")

dump("P1 sigmoid", 78, 312, 100, 153, nx=60, ny=16)
dump("P2 remember", 592, 802, 100, 150, nx=60, ny=14)
dump("P5 desc", 600, 842, 240, 362, nx=60, ny=20)
dump("P7 final", 498, 817, 408, 454, nx=64, ny=12)
dump("TITLE", 60, 320, 55, 95, nx=70, ny=12)
print("\n=== badge sample ===")
for (yy, xx) in [(70,875),(72,873),(74,875),(76,878),(68,872)]:
    print(yy, xx, "#%02x%02x%02x" % tuple(o[yy, xx]))
print("\n=== black band x-extent at y=530 ===")
row = o[530]
blk = np.nonzero((row[:, 0] < 60) & (row[:, 1] < 60) & (row[:, 2] < 60))[0]
print("black x", blk.min(), blk.max(), "n", len(blk))
row = o[525]
for xx in range(60, 960, 60):
    print(xx, "#%02x%02x%02x" % tuple(row[xx]))
