#!/usr/bin/env python3
"""Per-panel text-line segmentation with color classification for slide_003.jpg."""
from PIL import Image
import collections, json

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()

BG = (254, 255, 253)

def is_red(c):
    r, g, b = c
    return r > 105 and r - g > 40 and r - b > 30

def is_blue(c):
    r, g, b = c
    return b > r + 25 and b > g + 20

def is_green(c):
    r, g, b = c
    return g - r > 22 and g - b > 18 and g > 60

def is_ink(c):
    return abs(c[0]-BG[0]) + abs(c[1]-BG[1]) + abs(c[2]-BG[2]) > 150

def cls(c):
    if is_red(c): return "red"
    if is_blue(c): return "blue"
    if is_green(c): return "green"
    if c[0]+c[1]+c[2] < 560: return "dark"
    return "other"

PANELS = {
    "A": (73, 96, 865, 200),
    "B": (73, 222, 865, 297),
    "C": (73, 320, 865, 399),
    "D": (73, 423, 865, 498),
}

out = {}
for name, (x0, y0, x1, y1) in PANELS.items():
    print(f"\n########## PANEL {name}: x {x0}..{x1}  y {y0}..{y1} ##########")
    # row ink profile
    rows = []
    for y in range(y0, y1 + 1):
        n = sum(1 for x in range(x0, x1 + 1) if is_ink(px[x, y]))
        rows.append((y, n))
    # segment into lines
    lines = []
    cur = None
    for y, n in rows:
        if n > 0:
            if cur is None: cur = {"y0": y, "y1": y, "ink": n}
            else:
                cur["y1"] = y; cur["ink"] += n
        else:
            if cur is not None and cur["y1"] - cur["y0"] >= 4:
                lines.append(cur)
            cur = None
    if cur and cur["y1"] - cur["y0"] >= 4: lines.append(cur)
    pinfo = []
    for ln in lines:
        ly0, ly1 = ln["y0"], ln["y1"]
        minx = miny = None; maxx = maxy = 0
        colcnt = collections.Counter()
        percol = {}
        for y in range(ly0, ly1 + 1):
            for x in range(x0, x1 + 1):
                c = px[x, y]
                if is_ink(c):
                    k = cls(c)
                    colcnt[k] += 1
                    percol.setdefault(k, [x, x])
                    percol[k][0] = min(percol[k][0], x)
                    percol[k][1] = max(percol[k][1], x)
                    if minx is None or x < minx: minx = x
                    if maxx is None or x > maxx: maxx = x
                    if miny is None or y < miny: miny = y
                    if maxy is None or y > maxy: maxy = y
        info = {
            "y0": ly0, "y1": ly1, "h": ly1 - ly0 + 1,
            "x0": minx, "x1": maxx, "w": maxx - minx + 1,
            "colors": dict(colcnt),
            "color_spans": {k: v for k, v in percol.items()},
        }
        pinfo.append(info)
        cols = ", ".join(f"{k}={v}" for k, v in colcnt.most_common())
        print(f"  LINE y={ly0}..{ly1} (h={ly1-ly0+1})  x={minx}..{maxx} (w={maxx-minx+1})  [{cols}]")
    out[name] = pinfo
    # gaps between lines
    for i in range(1, len(pinfo)):
        gap = pinfo[i]["y0"] - pinfo[i-1]["y1"]
        print(f"    ^ gap above = {gap}")
    if pinfo:
        print(f"    top pad = {pinfo[0]['y0'] - y0}, bottom pad = {y1 - pinfo[-1]['y1']}")

with open("measure_003_lines.json", "w") as f:
    json.dump(out, f, indent=1)
print("\nSaved measure_003_lines.json")
