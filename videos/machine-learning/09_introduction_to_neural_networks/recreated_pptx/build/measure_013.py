#!/usr/bin/env python3
"""PIL measurement of slide_013 original frame (960x540) — region + color geometry.

Originals are 960x540 and LAYOUT_WIDE is 13.33x7.5in, so 1 px = 1 pt = 1/72 in.
"""
import sys
from collections import Counter
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_013.jpg"

im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()
print(f"SOURCE {SRC}")
print(f"SIZE {W}x{H}  -> 1px = {W/72:.3f}in wide, {H/72:.3f}in tall")

cnt = Counter(im.getdata())
print("\nTOP 18 COLORS")
for c, n in cnt.most_common(18):
    print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  {n:7d}  {100.0*n/(W*H):5.2f}%")

# ---- red frame detection (house chrome) -------------------------------------
def near(c, t, tol=28):
    return all(abs(c[i] - t[i]) <= tol for i in range(3))

RED = (192, 0, 0)
DARKRED = (178, 34, 34)
rows = []
for y in range(H):
    n = 0
    for x in range(W):
        c = px[x, y]
        if near(c, RED, 34) or near(c, DARKRED, 30):
            n += 1
    rows.append(n)
print("\nRED ROW PROFILE (rows with >150 red px)")
for y, n in enumerate(rows):
    if n > 150:
        print(f"  y={y} ({n})")

cols = []
for x in range(W):
    n = 0
    for y in range(H):
        c = px[x, y]
        if near(c, RED, 34) or near(c, DARKRED, 30):
            n += 1
    cols.append(n)
print("RED COL PROFILE (cols with >150 red px)")
for x, n in enumerate(cols):
    if n > 150:
        print(f"  x={x} ({n})")

# ---- non-background bounding boxes for content clusters ----------------------
BG = cnt.most_common(1)[0][0]
print(f"\nBG assumed #{BG[0]:02X}{BG[1]:02X}{BG[2]:02X}")

def ink_bbox(x0, y0, x1, y1, tol=18):
    minx, miny, maxx, maxy = x1, y1, x0, y0
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if max(abs(c[0]-BG[0]), abs(c[1]-BG[1]), abs(c[2]-BG[2])) > tol:
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)
    return minx, miny, maxx, maxy

# ---- scan for cyan / green table cell fills ---------------------------------
def find_color_fill(target, tol=14, minrun=6):
    """Return list of (x0,y0,x1,y1) bounding boxes of solid-ish target blobs."""
    mask = bytearray(W * H)
    for y in range(H):
        base = y * W
        for x in range(W):
            c = px[x, y]
            if all(abs(c[i] - target[i]) <= tol for i in range(3)):
                mask[base + x] = 1
    boxes = []
    seen = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if mask[i] and not seen[i]:
                stack = [i]
                seen[i] = 1
                minx, miny, maxx, maxy = x, y, x, y
                n = 0
                while stack:
                    j = stack.pop()
                    jy, jx = divmod(j, W)
                    n += 1
                    minx, miny = min(minx, jx), min(miny, jy)
                    maxx, maxy = max(maxx, jx), max(maxy, jy)
                    for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        ny, nx = jy + dj, jx + di
                        if 0 <= ny < H and 0 <= nx < W:
                            k = ny * W + nx
                            if mask[k] and not seen[k]:
                                seen[k] = 1
                                stack.append(k)
                if n >= minrun and (maxx - minx) > 3 and (maxy - miny) > 3:
                    boxes.append((minx, miny, maxx, maxy, n))
    return boxes

print("\nLIGHT-CYAN (#CCFFFF-ish) blobs")
for b in find_color_fill((204, 255, 255), tol=26):
    print(f"  x{b[0]}..{b[2]} y{b[1]}..{b[3]} n={b[4]}  ({(b[2]-b[0]+1)}x{(b[3]-b[1]+1)})")

print("\nLIGHT-GREEN (#CCFFCC-ish) blobs")
for b in find_color_fill((204, 255, 204), tol=26):
    print(f"  x{b[0]}..{b[2]} y{b[1]}..{b[3]} n={b[4]}  ({(b[2]-b[0]+1)}x{(b[3]-b[1]+1)})")

print("\nPEACH (#FFF0F0-ish) blobs")
for b in find_color_fill((255, 240, 240), tol=18):
    print(f"  x{b[0]}..{b[2]} y{b[1]}..{b[3]} n={b[4]}  ({(b[2]-b[0]+1)}x{(b[3]-b[1]+1)})")

print("\nDARK-BLUE (#191970-ish) blobs")
for b in find_color_fill((25, 25, 112), tol=45):
    print(f"  x{b[0]}..{b[2]} y{b[1]}..{b[3]} n={b[4]}  ({(b[2]-b[0]+1)}x{(b[3]-b[1]+1)})")

print("\nPURPLE (#9370DB-ish) blobs")
for b in find_color_fill((147, 112, 219), tol=50):
    print(f"  x{b[0]}..{b[2]} y{b[1]}..{b[3]} n={b[4]}  ({(b[2]-b[0]+1)}x{(b[3]-b[1]+1)})")

print("\nRED-X / firebrick (#B22222) blobs (>=40px)")
for b in find_color_fill((178, 34, 34), tol=26, minrun=40):
    print(f"  x{b[0]}..{b[2]} y{b[1]}..{b[3]} n={b[4]}  ({(b[2]-b[0]+1)}x{(b[3]-b[1]+1)})")
