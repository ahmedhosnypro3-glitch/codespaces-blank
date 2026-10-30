#!/usr/bin/env python3
"""Characterize slide_003.jpg: letterbox bands, title, badge, panel interiors."""
from PIL import Image
import collections

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 110 and r - g > 45 and r - b > 35

def is_dark(c):
    return c[0]+c[1]+c[2] < 300

print("=== ROW MEAN BRIGHTNESS (bottom 60 rows) ===")
for y in range(H-60, H):
    vals = [sum(px[x,y])/3 for x in range(0, W, 8)]
    print(f"  y={y:4d} mean={sum(vals)/len(vals):6.1f}")

print("\n=== COLUMN MEAN BRIGHTNESS (left/right 80 cols) ===")
for x in list(range(0, 80, 4)) + list(range(W-80, W, 4)):
    vals = [sum(px[x,y])/3 for y in range(0, H, 4)]
    print(f"  x={x:4d} mean={sum(vals)/len(vals):6.1f}")

# Title region: between outer top frame (y=42) and panel A top (y=89)
print("\n=== TITLE REGION y=45..88 ===")
# red text bbox
minx=miny=None; maxx=maxy=None
redcols=collections.Counter(); redrows=collections.Counter()
for y in range(45, 88):
    for x in range(W):
        if is_red(px[x,y]) and not (x<62 or x>899):
            if minx is None or x<minx: minx=x
            if maxx is None or x>maxx: maxx=x
            if miny is None or y<miny: miny=y
            if maxy is None or y>maxy: maxy=y
            redcols[x]+=1; redrows[y]+=1
print(f"  red text bbox x={minx}..{maxx} y={miny}..{maxy}  h={maxy-miny+1}")
if redcols:
    xs = sorted(redcols)
    # find word gaps
    groups=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>6:
            groups.append((s,p)); s=x
        p=x
    groups.append((s,p))
    print("  red x-gaps (words):")
    for g in groups:
        print(f"    x={g[0]}..{g[1]} (w={g[1]-g[0]+1})")
    print("  red row extent per y:", sorted(redrows.items())[:3], "...", sorted(redrows.items())[-3:])

# Badge: search top-right inside frame
print("\n=== BADGE SEARCH (x>840, y<95) ===")
for y in range(0, 96, 3):
    line = ""
    for x in range(830, 960, 3):
        c = px[x,y]
        if is_dark(c): line += "#"
        elif is_red(c): line += "r"
        elif c[0]>230 and c[1]>220 and c[2]<190: line += "Y"
        elif c[0]>240 and c[1]>240 and c[2]>240: line += "."
        else: line += "-"
    print(f"  y={y:3d} {line}")
