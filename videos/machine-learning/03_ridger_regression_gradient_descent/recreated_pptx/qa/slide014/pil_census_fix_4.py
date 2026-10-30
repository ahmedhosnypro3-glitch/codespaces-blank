#!/usr/bin/env python3
"""Frame-truth census of the original's mid+lower regions (y240..540).
Classify every row into color segments; find ink lines within each band;
count text lines and their x extents so spec bullets can be mapped to bands.
"""
from PIL import Image
import numpy as np
import json, sys

ORIG = "unique_slides/slide_014.jpg"
im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("orig size", W, H)

# color classifiers (tolerance)
def seg(R, G, B):
    # returns segment label for a pixel
    if R < 60 and G < 60 and B < 60:
        return "ink"
    if R > 235 and G > 235 and B > 235:
        return "white"
    if abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 14:
        return "panel"
    if abs(R - 249) < 16 and abs(G - 223) < 16 and abs(B - 195) < 18:
        return "peach"
    if abs(R - 246) < 14 and abs(G - 252) < 10 and abs(B - 219) < 14:
        return "yellow"
    if abs(R - 255) < 8 and abs(G - 235) < 12 and abs(B - 238) < 12:
        return "pink"
    if abs(R - 123) < 20 and abs(G - 120) < 20 and abs(B - 201) < 24:
        return "blue"
    if R > 150 and G < 70 and B < 80:
        return "red"
    if abs(R - 143) < 25 and abs(G - 25) < 25 and abs(B - 40) < 25:
        return "maroon"
    return "other"

labels = ["ink", "white", "panel", "peach", "yellow", "pink", "blue", "red", "maroon", "other"]

# Row census for y 240..540: for each row, find x-runs of each label >= 3 px
out = []
for y in range(240, 540):
    row = a[y]
    segs = {}
    for x0 in range(62, 900):
        lab = seg(*row[x0])
        if lab in ("ink", "peach", "yellow", "pink", "blue", "maroon"):
            segs.setdefault(lab, []).append(x0)
    line = {"y": y}
    for lab, xs in segs.items():
        if len(xs) >= 3:
            line[lab] = [min(xs), max(xs), len(xs)]
    # panel/white baseline (first pixel class at x=100)
    line["base"] = seg(*row[100])
    out.append(line)

# ---- band finder: rows where peach/yellow/blue/pink present (fills)
fills = {}
for y in range(240, 540):
    line = out[y - 240]
    for lab in ("peach", "yellow", "pink", "blue"):
        if lab in line:
            fills.setdefault(lab, []).append(y)

print("\n=== FILL BANDS (label: y ranges with x extents) ===")
for lab, ys in fills.items():
    # split into contiguous bands
    bands = []
    start = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y - prev > 2:
            bands.append((start, prev)); start = y
        prev = y
    bands.append((start, prev))
    for (y0, y1) in bands:
        xs = []
        for y in range(y0, y1 + 1):
            line = out[y - 240]
            if lab in line:
                xs.append((line[lab][0], line[lab][1]))
        x0 = min(s[0] for s in xs); x1 = max(s[1] for s in xs)
        print(f"{lab:7s} y{y0}..{y1} (h={y1-y0+1}) x{x0}..{x1} (w={x1-x0+1})")

# ---- ink line census inside each fill band
print("\n=== INK LINES PER FILL BAND (text rows) ===")
for lab, ys in fills.items():
    bands = []
    start = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y - prev > 2:
            bands.append((start, prev)); start = y
        prev = y
    bands.append((start, prev))
    for (y0, y1) in bands:
        inkrows = [y for y in range(y0, y1 + 1) if "ink" in out[y - 240] and out[y - 240]["ink"][2] >= 4]
        # group into text lines
        lines = []
        if inkrows:
            s = inkrows[0]; p = inkrows[0]
            for y in inkrows[1:]:
                if y - p > 3:
                    lines.append((s, p)); s = y
                p = y
            lines.append((s, p))
        print(f"{lab:7s} band y{y0}..{y1}: ink rows {len(inkrows)}, text lines {len(lines)}")
        for (ly0, ly1) in lines:
            xs = [out[y - 240]["ink"] for y in range(ly0, ly1 + 1) if "ink" in out[y - 240]]
            xa = min(v[0] for v in xs); xb = max(v[1] for v in xs)
            npix = sum(v[2] for v in xs)
            print(f"    line y{ly0}..{ly1} (h={ly1-ly0+1}) x{xa}..{xb} (w={xb-xa+1}) inkpx={npix}")

# ---- vector box region census (y95..245)
print("\n=== VECTOR BOX REGION (y95..245) ===")
for y0, y1, name in [(95, 245, "boxes")]:
    inkrows = [y for y in range(y0, y1 + 1) if y < H and "ink" in out[y - 240] and out[y - 240]["ink"][2] >= 4]
    lines = []
    if inkrows:
        s = inkrows[0]; p = inkrows[0]
        for y in inkrows[1:]:
            if y - p > 3:
                lines.append((s, p)); s = y
            p = y
        lines.append((s, p))
    print(f"{name}: ink rows {len(inkrows)}, lines {len(lines)}")
    for (ly0, ly1) in lines:
        xs = [out[y - 240]["ink"] for y in range(ly0, ly1 + 1) if "ink" in out[y - 240]]
        xa = min(v[0] for v in xs); xb = max(v[1] for v in xs)
        npix = sum(v[2] for v in xs)
        print(f"    line y{ly0}..{ly1} (h={ly1-ly0+1}) x{xa}..{xb} (w={xb-xa+1}) inkpx={npix}")

# separate left/right halves for box text
print("\n=== VECTOR BOX halves (left x<460, right x>=460) ===")
for half, (lo, hi) in [("left", (60, 460)), ("right", (460, 900))]:
    inkrows = []
    for y in range(95, 245):
        row = a[y]
        cnt = 0; xs = []
        for x in range(lo, hi):
            if seg(*row[x]) == "ink":
                cnt += 1; xs.append(x)
        if cnt >= 3:
            inkrows.append((y, min(xs), max(xs), cnt))
    lines = []
    if inkrows:
        s = inkrows[0][0]; p = inkrows[0][0]
        for t in inkrows[1:]:
            if t[0] - p > 3:
                lines.append((s, p)); s = t[0]
            p = t[0]
        lines.append((s, p))
    print(f"{half}: lines {len(lines)}")
    for (ly0, ly1) in lines:
        xs = [t for t in inkrows if ly0 <= t[0] <= ly1]
        xa = min(t[1] for t in xs); xb = max(t[2] for t in xs)
        npix = sum(t[3] for t in xs)
        print(f"    line y{ly0}..{ly1} (h={ly1-ly0+1}) x{xa}..{xb} (w={xb-xa+1}) inkpx={npix}")

# ---- box borders and interior fill (sample rows y150 and y230)
print("\n=== VECTOR BOX geometry samples ===")
for y in (110, 150, 200, 230):
    row = a[y]
    # find white interior runs and maroon border columns
    whites = [x for x in range(60, 900) if seg(*row[x]) == "white"]
    maroons = [x for x in range(60, 900) if seg(*row[x]) == "maroon"]
    print(f"y={y}: white x {min(whites) if whites else None}..{max(whites) if whites else None} ({len(whites)}) | maroon x {min(maroons) if maroons else None}..{max(maroons) if maroons else None} ({len(maroons)})")

# border columns per row: maroon verticals
print("\n=== MAROON vertical border scan (rows 104..232) ===")
cols = {}
for y in range(104, 233):
    row = a[y]
    for x in range(60, 900):
        if seg(*row[x]) == "maroon":
            cols.setdefault(x, []).append(y)
verticals = {x: (len(ys), min(ys), max(ys)) for x, ys in cols.items() if len(ys) > 40}
print("maroon verticals (x: count,y0..y1):", verticals)
# interior pink?
interior = []
for y in (120, 160, 200, 220):
    row = a[y]
    # between the box borders
    pinks = [x for x in range(60, 900) if abs(row[x][0]-255)<10 and abs(row[x][1]-235)<15 and abs(row[x][2]-240)<15]
    interior.append((y, pinks[:3], pinks[-3:] if pinks else None, len(pinks)))
print("interior pink scan:", interior)

# ---- text color inside blue lower region
print("\n=== LOWER BLUE region text colors (y470..528) ===")
for y in (472, 480, 490, 500, 510, 520, 525):
    if y >= H: continue
    row = a[y]
    inks = [tuple(row[x]) for x in range(92, 883) if seg(*row[x]) == "ink"]
    whites_ = [x for x in range(92, 883) if seg(*row[x]) == "white"]
    if inks:
        print(f"y={y}: ink px {len(inks)}, sample ink colors {inks[:3]}, white runs {len(whites_)}")
    else:
        print(f"y={y}: no ink; white runs {len(whites_)}")
