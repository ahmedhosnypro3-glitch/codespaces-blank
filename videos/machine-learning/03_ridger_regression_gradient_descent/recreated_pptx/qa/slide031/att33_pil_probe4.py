#!/usr/bin/env python3
"""Probe 4: M1 annotation gap, M4 label glyphs, M2 orig dash structure."""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide031"

def load(n):
    return np.asarray(Image.open(f"{D}/crop_33_{n}_render.png").convert("RGB")).astype(int), \
           np.asarray(Image.open(f"{D}/crop_33_{n}_orig.png").convert("RGB")).astype(int)

gr, go = load("graph")
tr, to = load("topblock")

def redloose(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R > 55) & (R - G > 22) & (R - B > 18)

print("### M2-confirm. orig dash band x240..275 map (3px rows, loose red; also plain dark)")
for tag, im in (("ORIG", go), ("RENDER", gr)):
    rm = redloose(im)
    dk = (im[..., 0] < 120) & (im[..., 1] < 120) & (im[..., 2] < 120)
    print(f"  --- {tag}: x240..275, y15..452 step 6 (R=red, #=dark, .=none) ---")
    for y in range(15, 452, 6):
        line = ""
        for x in range(240, 276):
            line += "R" if rm[y:y+3, x].any() else ("#" if dk[y:y+3, x].any() else ".")
        print(f"    {y:3d} {line}")

print()
print("### M1. annotation box line 1: green-excluded ink, box interior")
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

for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    ti = textink(im)
    # box interior: exclude 4px border margins; frame box x243..574 y230..320 -> crop x431..1121 y371..558
    x0, x1, y0, y1 = 437, 1115, 377, 552
    prof = ti[y0:y1, x0:x1].sum(axis=1)
    bands, s = [], None
    for i, c in enumerate(prof):
        if c > 2 and s is None: s = i
        if c <= 2 and s is not None:
            if i - s > 8: bands.append((y0 + s, y0 + i - 1))
            s = None
    if s is not None: bands.append((y0 + s, y0 + len(prof) - 1))
    print(f"  {tag}: interior text bands: {bands}")
    if len(bands) >= 1:
        ly0, ly1 = bands[0]
        c = clus(ti[ly0:ly1 + 1, x0:x1].sum(axis=0), x0)
        print(f"    L1 y{ly0}..{ly1} clusters: {c}")
        g = [(c[i + 1][0] - c[i][1], c[i][1], c[i + 1][0]) for i in range(len(c) - 1)]
        big = [x for x in g if x[0] >= 12]
        print(f"    L1 gaps>=12: {big}")
        r = clus(redloose(im)[ly0:ly1 + 1, x0:x1].sum(axis=0), x0)
        print(f"    L1 red clusters: {r}")

print()
print("### M4. '(?, ?)' glyphs x335..425 y170..200, grayish mask t<170, 1x")
def graym(im, t=170):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R < t) & (abs(R - G) < 45) & (abs(G - B) < 45) & ~((G > R + 20) & (G > B + 5))
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    gm = graym(im)
    print(f"  --- {tag} ---")
    for y in range(168, 202, 1):
        line = "".join("#" if gm[y, x] else "." for x in range(335, 425))
        if "#" in line:
            print(f"    {y:3d} {line}")
    # clusters on the label band
    ys = [y for y in range(168, 202) if gm[y, 335:425].any()]
    if ys:
        y0, y1 = min(ys), max(ys)
        c = clus(gm[y0:y1 + 1, 335:425].sum(axis=0), 335, gap=2)
        g = [(c[i + 1][0] - c[i][1], c[i][1], c[i + 1][0]) for i in range(len(c) - 1)]
        print(f"    band y{y0}..{y1} clusters: {c}")
        print(f"    gaps: {g}")
