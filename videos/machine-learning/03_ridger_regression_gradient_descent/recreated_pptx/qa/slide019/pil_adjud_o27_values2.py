#!/usr/bin/env python3
"""O27 PIL adjudication — slide_019 original frame: read W-vector 3rd entries +
label/ink colors. numpy + block-classifier idiom (per a29_ascii)."""
from PIL import Image
import numpy as np

ROOT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(ROOT + "/unique_slides/slide_019.jpg").convert("RGB")).astype(int)

def cls(px):
    r, g, b = px
    if r > 200 and g > 200 and b > 200:
        return "."
    if r > 205 and g > 200 and b <= 200:
        return "y"          # yellow band
    if b > r + 25 and b > g + 15:
        return "B"
    if r > g + 40 and r > b + 40:
        return "R"
    if g > r + 25 and g > b + 25:
        return "G"
    if abs(r - g) < 35 and abs(g - b) < 35:
        return "#"
    return "+"

def amap(x0, x1, y0, y1, tag, ds=1, img=None, scale=(1.0, 1.0)):
    img = orig if img is None else img
    print(f"===== {tag} frame x{x0}..{x1} y{y0}..{y1} (ds={ds}) =====")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, ds))
    print(hdr)
    for yf in range(y0, y1, ds):
        row = []
        for xf in range(x0, x1, ds):
            block = img[int(yf*scale[1]):int((yf+ds)*scale[1]), int(xf*scale[0]):int((xf+ds)*scale[0])]
            classes = [cls(px) for px in block.reshape(-1, 3)]
            order = {"#": 0, "B": 1, "R": 2, "G": 3, "+": 4, "y": 5, ".": 6}
            best = min(classes, key=lambda c: order[c])
            row.append(best if best != "." else ("y" if all(c in ".y" for c in classes) else "."))
        print(f"{yf:4d} " + "".join(row))

def ink_hist(x0, y0, x1, y1, tag):
    h = {}
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = cls(orig[y, x])
            if c != ".":
                h[c] = h.get(c, 0) + 1
    print(f"{tag:44s} {h}")

# ── 1. VALUE READ: NO REG row 2 entries (build: x0=124, entries x173..189, gy=310)
amap(165, 200, 305, 382, "ORIG NO REG g2 W entries")
# ── 2. VALUE READ: RIDGE 10 row 3 entries (build: x0=644, entries x693..709, gy=420)
amap(685, 720, 415, 492, "ORIG RIDGE10 g3 W entries")

# ── 3. COLOR CENSUS (original) per cell type
for cname, x0 in [("NOREG", 124), ("RIDGE3", 384), ("RIDGE10", 644)]:
    for gi, gy in enumerate([205, 310, 420]):
        ink_hist(x0+44, gy+2, x0+72, gy+64, f"{cname} g{gi+1} W entries ink")
        ink_hist(x0+16, gy+20, x0+40, gy+40, f"{cname} g{gi+1} 'W =' label ink")
        ink_hist(x0+6, gy+66, x0+82, gy+86, f"{cname} g{gi+1} '||W||^2' label ink")
        v0 = x0 + 142
        gx1 = 380 if cname == "NOREG" else (640 if cname == "RIDGE3" else 888)
        colW = (gx1 - v0) / 3
        for ti in range(3):
            ink_hist(int(v0+ti*colW), gy+4, int(v0+(ti+1)*colW), gy+20, f"{cname} g{gi+1} Test header t{ti+1} ink")
        ink_hist(int(v0), gy+22, int(v0+46), gy+40, f"{cname} g{gi+1} x1 label col ink")
        ink_hist(int(v0), gy+42, int(v0+46), gy+62, f"{cname} g{gi+1} x2 label col ink")
        ink_hist(int(v0+46), gy+22, int(gx1), gy+40, f"{cname} g{gi+1} x1 value row ink")
        ink_hist(int(v0+46), gy+42, int(gx1), gy+62, f"{cname} g{gi+1} x2 value row ink")
        ink_hist(int(v0), gy+68, int(gx1), gy+88, f"{cname} g{gi+1} y row ink")

# ── 4. z labels in Test Data box (orig x156/246/342 bands y96..122)
for lx in (156, 246, 342):
    ink_hist(lx, 94, lx+40, 124, f"z label x{lx} ink")

# ── 5. header band background tints (sample px away from text)
def sample(x, y, tag):
    print(f"{tag:40s} px({x},{y}) = {tuple(orig[y, x])}")
for x0, x1, nm in [(124, 380, "NOREG"), (384, 640, "RIDGE3"), (644, 900, "RIDGE10")]:
    sample((x0+x1)//2, 174, f"{nm} header band bg (y174)")
    sample((x0+x1)//2, 200, f"{nm} header band bg (y200)")
# strip y515..523 tints
for sx, nm in [(130, "strip NOREG"), (390, "strip RIDGE3"), (644, "strip RIDGE10")]:
    sample(sx + 60, 519, f"{nm} strip bg")
