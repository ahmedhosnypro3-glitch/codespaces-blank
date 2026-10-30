#!/usr/bin/env python3
"""Refined probe for att33 MINORs 1, 2, 4 (slide 031, crop_33 pairs)."""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide031"

def load(n):
    return np.asarray(Image.open(f"{D}/crop_33_{n}_render.png").convert("RGB")).astype(int), \
           np.asarray(Image.open(f"{D}/crop_33_{n}_orig.png").convert("RGB")).astype(int)

gr, go = load("graph")
tr, to = load("topblock")

def redmask(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R > 90) & (G < 0.72 * R) & (B < 0.78 * R)

def inkmask(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    red = redmask(im)
    blue = (B > R + 25) & (B > G + 10) & (B > 90)
    dark = (R < 150) & (G < 160) & (B < 170)
    return dark | red | blue

def clusters(cols, x0, gap=4):
    runs, s = [], None
    for i, c in enumerate(cols):
        if c > 0 and s is None: s = i
        if c == 0 and s is not None:
            runs.append((x0 + s, x0 + i - 1)); s = None
    if s is not None: runs.append((x0 + s, x0 + len(cols) - 1))
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return merged

print("### A. plot-box horizontal red borders (graph crop, red runs > 60% width)")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    rm = redmask(im)
    W = im.shape[1]
    for y in range(im.shape[0]):
        c = rm[y].sum()
        if c > 0.6 * W:
            print(f"  {tag} row {y}: red {c}/{W}")
    print(f"  {tag}: (rows above)")

print()
print("### B. dashed-line band x240..270 full row profile (graph crop)")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    rm = redmask(im)
    rows = rm[:, 240:270].sum(axis=1)
    ink = np.nonzero(rows)[0]
    # group consecutive rows into dash segments
    segs, s = [], None
    prev = None
    for y in ink:
        if s is None: s = y
        elif y - prev > 2:
            segs.append((s, prev)); s = y
        prev = y
    if s is not None: segs.append((s, prev))
    print(f"  {tag}: dash segments y: {segs}")

print()
print("### C. pixels below orig/render border in dash band — raw view")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    print(f"  --- {tag} rows 425..451, cols 244..268 (R=red, .=bg) ---")
    rm = redmask(im)
    for y in range(425, min(452, im.shape[0])):
        line = "".join("R" if rm[y, x] else "." for x in range(244, 268))
        print(f"    {y:3d} {line}")

print()
print("### D. annotation box line 1 glyph clusters (topblock crop, box region x420..1130 y365..565)")
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    imk = inkmask(im)
    # line bands inside box
    prof = imk[365:565, 420:1130].sum(axis=1)
    bands, s = [], None
    for i, c in enumerate(prof):
        if c > 3 and s is None: s = i
        if c <= 3 and s is not None:
            if i - s > 6: bands.append((365 + s, 365 + i - 1))
            s = None
    if s is not None: bands.append((365 + s, 365 + len(prof) - 1))
    print(f"  {tag}: text bands y: {bands}")
    if bands:
        y0, y1 = bands[0]
        cl = clusters(imk[y0:y1 + 1, 420:1130].sum(axis=0), 420)
        print(f"    line1 y{y0}..{y1} clusters: {cl}")
        gaps = [(cl[i + 1][0] - cl[i][1], cl[i][1], cl[i + 1][0]) for i in range(len(cl) - 1)]
        print(f"    line1 gaps: {gaps}")
        # red clusters in line 1
        rcl = clusters(redmask(im)[y0:y1 + 1, 420:1130].sum(axis=0), 420)
        print(f"    line1 RED clusters: {rcl}")

print()
print("### E. '(?, ?)' label region ASCII map (graph crop) — dark ink, x255..420 y150..235")
def darkm(im, t=120):
    return (im[..., 0] < t) & (im[..., 1] < t) & (im[..., 2] < t)
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    dm = darkm(im)
    print(f"  --- {tag} (2x downsample, x255..420) ---")
    for y in range(150, 235, 2):
        line = "".join("#" if dm[y:y+2, x:x+2].any() else "." for x in range(255, 420, 2))
        print(f"    {y:3d} {line}")
