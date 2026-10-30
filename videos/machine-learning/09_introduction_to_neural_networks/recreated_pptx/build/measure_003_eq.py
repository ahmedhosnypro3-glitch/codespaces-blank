#!/usr/bin/env python3
"""Deep-dive: page extents, panel C equation row column profile, per-word color spans."""
from PIL import Image
import collections

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()

def is_red(c):
    r, g, b = c
    return r > 105 and r - g > 40 and r - b > 30

print("=== SAMPLE outer-frame pixels ===")
for (x, y) in [(58,250),(59,250),(60,250),(57,250),(56,250),(40,250),(901,250),(902,250),(903,250),(910,250),
               (500,42),(500,43),(500,41),(500,516),(500,517),(500,518),(500,515),(30,250),(930,250)]:
    print(f"  ({x},{y}) = {px[x,y]}")

print("\n=== ROW x=480 profile y=0..60 ===")
for y in range(0, 60):
    print(f"  y={y:3d} {px[480,y]}")

print("\n=== PANEL C EQUATION ROW: column profile y=340..400, x=73..865 ===")
# per-column ink counts and color class
cols = []
for x in range(73, 866):
    cn = collections.Counter()
    for y in range(340, 400):
        c = px[x, y]
        if abs(c[0]-254)+abs(c[1]-255)+abs(c[2]-253) > 150:
            r, g, b = c
            if r > 105 and r-g > 40 and r-b > 30: k = "R"
            elif b > r+25 and b > g+20: k = "B"
            elif g-r > 22 and g-b > 18 and g > 60: k = "G"
            elif c[0]+c[1]+c[2] < 560: k = "K"
            else: k = "."
            cn[k] += 1
    cols.append((x, cn))

# print compact ascii map: rows 340..400 (every 2px), cols 73..865 (every 2px)
print("  ascii map (x 73..865 step 2, y 340..400 step 2):")
hdr = "      " + "".join(str((x//10)%10) if x%10==0 else " " for x in range(73, 866, 2))
print(hdr)
for y in range(340, 400, 2):
    row = ""
    for x in range(73, 866, 2):
        c = px[x, y]
        if abs(c[0]-254)+abs(c[1]-255)+abs(c[2]-253) > 150:
            r, g, b = c
            if r > 105 and r-g > 40 and r-b > 30: row += "R"
            elif b > r+25 and b > g+20: row += "B"
            elif g-r > 22 and g-b > 18 and g > 60: row += "G"
            elif c[0]+c[1]+c[2] < 560: row += "#"
            else: row += "."
        else:
            row += " "
    print(f"  y={y:3d} {row}")

print("\n=== PANEL C: ink bbox per column-group (word gaps) ===")
groups = []
cur = None
for x, cn in cols:
    has = sum(v for k, v in cn.items() if k in "RBGK") > 0
    if has:
        if cur is None: cur = [x, x]
        else: cur[1] = x
    else:
        if cur is not None and cur[1]-cur[0] >= 1:
            groups.append(tuple(cur))
        cur = None
if cur: groups.append(tuple(cur))
# merge groups separated by < 6px
merged = []
for g in groups:
    if merged and g[0]-merged[-1][1] <= 6:
        merged[-1] = (merged[-1][0], g[1])
    else:
        merged.append(g)
for g in merged:
    cc = collections.Counter()
    for x, cn in cols:
        if g[0] <= x <= g[1]:
            for k, v in cn.items():
                if k in "RBGK": cc[k] += v
    print(f"  x={g[0]:4d}..{g[1]:4d} (w={g[1]-g[0]+1:3d})  {dict(cc)}")
