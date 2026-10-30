#!/usr/bin/env python3
"""Measure slide_003.jpg: ink bounding boxes, colors, font sizes, panel geometry."""
from PIL import Image
import collections, json

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
print(f"IMAGE SIZE: {W} x {H}")

px = im.load()

# 1. Background / dominant colors
cnt = collections.Counter()
for y in range(0, H, 2):
    for x in range(0, W, 2):
        cnt[px[x, y]] += 1
print("\nTOP 12 COLORS (rgb, share):")
for c, n in cnt.most_common(12):
    print(f"  {c}  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  {100*n/sum(cnt.values()):.1f}%")

# 2. Find the white panels: scan column x = W//2 for color transitions
print("\nCOLUMN PROFILE at x = W//2 (row: color, marking white runs):")
col = W // 2
runs = []
cur = None
start = 0
for y in range(H):
    c = px[col, y]
    key = "white" if all(v > 235 for v in c) else ("gray" if all(180 < v <= 235 for v in c) else "dark")
    if key != cur:
        if cur is not None:
            runs.append((cur, start, y - 1))
        cur = key
        start = y
runs.append((cur, start, H - 1))
for r in runs:
    print(f"  {r[0]:6s} y={r[1]:4d}..{r[2]:4d} h={r[2]-r[1]+1}")

# 3. Find red border columns: scan row y = H//2 for vertical white panel edges
print("\nROW PROFILE at y = H//2 (runs):")
row = H // 2
runs = []
cur = None
start = 0
for x in range(W):
    c = px[x, y]
    r, g, b = c
    if r > 120 and g < 90 and b < 90:
        key = "red"
    elif all(v > 235 for v in c):
        key = "white"
    elif all(v > 210 for v in c):
        key = "lightgray"
    else:
        key = "dark"
    if key != cur:
        if cur is not None:
            runs.append((cur, start, x - 1))
        cur = key
        start = x
runs.append((cur, start, W - 1))
for r in runs:
    print(f"  {r[0]:11s} x={r[1]:4d}..{r[2]:4d} w={r[2]-r[1]+1}")

# 4. Per-panel ink bounding boxes and text line segmentation
def ink_bbox(x0, y0, x1, y1, bg):
    """Bounding box of pixels differing from bg (approx)."""
    minx, miny, maxx, maxy = None, None, None, None
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if abs(c[0]-bg[0]) + abs(c[1]-bg[1]) + abs(c[2]-bg[2]) > 60:
                if minx is None or x < minx: minx = x
                if maxx is None or x > maxx: maxx = x
                if miny is None or y < miny: miny = y
                if maxy is None or y > maxy: maxy = y
    return (minx, miny, maxx, maxy)

# Panels detected from column profile will be re-detected per column scan
# Detect white panels per row band: for each y, find white segments
print("\nWHITE PANEL DETECTION (per row white segments -> vertical runs):")
panel_rows = []
for y in range(H):
    segs = []
    inrun = False
    for x in range(W):
        c = px[x, y]
        white = all(v > 235 for v in c)
        if white and not inrun:
            inrun = True; sx = x
        elif not white and inrun:
            inrun = False
            if x - sx > 200:
                segs.append((sx, x - 1))
    if inrun and W - sx > 200:
        segs.append((sx, W - 1))
    panel_rows.append(segs)

# cluster consecutive rows with similar seg
bands = []
cur = None
for y in range(H):
    if panel_rows[y]:
        sig = panel_rows[y][0]
        if cur is None:
            cur = {"y0": y, "y1": y, "segs": [sig]}
        elif abs(sig[0]-cur["segs"][-1][0]) < 6 and abs(sig[1]-cur["segs"][-1][1]) < 6:
            cur["y1"] = y
            cur["segs"].append(sig)
        else:
            bands.append(cur); cur = {"y0": y, "y1": y, "segs": [sig]}
    else:
        if cur is not None:
            bands.append(cur); cur = None
if cur: bands.append(cur)
for b in bands:
    if b["y1"] - b["y0"] < 30:
        continue
    xs = [s[0] for s in b["segs"]]; xe = [s[1] for s in b["segs"]]
    print(f"  PANEL y={b['y0']}..{b['y1']} (h={b['y1']-b['y0']+1}) x={min(xs)}..{max(xe)} (w={max(xe)-min(xs)+1})")
