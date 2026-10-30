#!/usr/bin/env python3
"""M1 final adjudication: annotation box line 1 'bold'->'5.1' gap, frame coords.

Cross-checks the two banked scans (att33_pil_adjudicate vs att33_pil_probe4)
against the actual crop geometry. Topblock crop = frame [36,52]-[648,342] at
1276x604 (scale 2.085). Graph crop = frame [565,58]-[817,275].
"""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide031"

def load(n):
    return (np.asarray(Image.open(f"{D}/crop_33_{n}_render.png").convert("RGB")).astype(int),
            np.asarray(Image.open(f"{D}/crop_33_{n}_orig.png").convert("RGB")).astype(int))

tr, to = load("topblock")
SX = tr.shape[1] / 612.0   # crop px per frame px (x)
SY = tr.shape[0] / 290.0
FX0, FY0 = 36.0, 52.0      # crop origin in frame px

def fr(cxy):
    x, y = cxy
    return (FX0 + x / SX, FY0 + y / SY)

def redloose(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R > 55) & (R - G > 22) & (R - B > 18)

def textink(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    red = redloose(im)
    blue = (B > R + 25) & (B > G + 10) & (B > 90)
    black = (R < 140) & (G < 140) & (B < 140) & (G < R + 30) & (G < B + 30) & ~((G > R + 20) & (G > B + 5))
    return red | blue | black

def clus(cols, x0, gap=4):
    runs, s = [], None
    for i, c in enumerate(cols):
        if c > 0 and s is None: s = i
        if c == 0 and s is not None: runs.append((x0 + s, x0 + i - 1)); s = None
    if s is not None: runs.append((x0 + s, x0 + len(cols) - 1))
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return merged

print("### 1. what ink bands exist in the topblock crop (full width), frame-annotated")
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    ti = textink(im)
    prof = ti.sum(axis=1)
    bands, s = [], None
    for i, c in enumerate(prof):
        if c > 3 and s is None: s = i
        if c <= 3 and s is not None:
            if i - s > 6: bands.append((s, i - 1))
            s = None
    if s is not None: bands.append((s, len(prof) - 1))
    fb = [(round(FY0 + a / SY, 1), round(FY0 + b / SY, 1)) for a, b in bands]
    print(f"  {tag}: ink bands crop-y {bands}")
    print(f"  {tag}:            frame-y {fb}")

print()
print("### 2. annotation box line 1 word clusters (frame coords), box = frame x243..574 y230..320")
WORDS = ["X", "is", "in", "between", "4.8", "and", "color", "red", "bold", "5.1"]
res = {}
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    ti = textink(im)
    x0, x1, y0, y1 = 437, 1115, 377, 445   # line-1 band only (crop y416..437 / 409..437 + margin)
    # detect line-1 band precisely inside the box top half
    prof = ti[377:460, x0:x1].sum(axis=1)
    ys = np.nonzero(prof > 2)[0]
    ly0, ly1 = 377 + ys.min(), 377 + ys.max()
    c = clus(ti[ly0:ly1 + 1, x0:x1].sum(axis=0), x0)
    fc = [(round(FX0 + a / SX, 1), round(FX0 + b / SX, 1)) for a, b in c]
    g = [(c[i + 1][0] - c[i][1], c[i][1], c[i + 1][0]) for i in range(len(c) - 1)]
    r = clus(redloose(im)[ly0:ly1 + 1, x0:x1].sum(axis=0), x0)
    print(f"  {tag}: L1 band crop-y {ly0}..{ly1} (frame-y {round(FY0+ly0/SY,1)}..{round(FY0+ly1/SY,1)})")
    print(f"    clusters crop-x: {c}")
    print(f"    clusters frame-x: {fc}")
    print(f"    gaps(crop px): {[(gg[0], round(gg[1]), round(gg[2])) for gg in g]}")
    print(f"    red clusters frame-x: {[(round(FX0+a/SX,1), round(FX0+b/SX,1)) for a,b in r]}")
    res[tag] = (c, g)

print()
print("### 3. bold->5.1 gap verdict")
for tag in ("RENDER", "ORIG  "):
    c, g = res[tag]
    # find cluster whose end abuts the red 5.1 start
    print(f"  {tag}: last-4 gaps: {[x[0] for x in g[-4:]]}  (crop px; 1 frame px = {SX:.3f} crop px)")
