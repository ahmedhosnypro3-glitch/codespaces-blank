#!/usr/bin/env python3
"""Probe 3: loose-mask dash termination, box borders, label hunt (slide 031)."""
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

print("### A3. full-width red rows (borders), graph crop, loose mask")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    rm = redloose(im)
    W = im.shape[1]
    hits = [(y, int(rm[y].sum())) for y in range(im.shape[0]) if rm[y].sum() > 0.5 * W]
    print(f"  {tag}: {hits}")

print()
print("### B3. dash band x244..268, LOOSE mask, all segments")
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    rm = redloose(im)
    rows = rm[:, 244:268].sum(axis=1)
    ink = np.nonzero(rows)[0]
    segs, s, prev = [], None, None
    for y in ink:
        if s is None: s = y
        elif y - prev > 2: segs.append((s, prev)); s = y
        prev = y
    if s is not None: segs.append((s, prev))
    print(f"  {tag}: {segs}")

print()
print("### B4. raw orig pixels in dash band rows 380..452 (are dashes there at all?)")
for tag, im in (("ORIG", go), ("RENDER", gr)):
    print(f"  --- {tag}: sample RGB at x252..258, rows 400..450 (every 4) ---")
    for y in range(400, 452, 4):
        vals = [tuple(im[y, x]) for x in range(250, 260, 3)]
        print(f"    y{y}: {vals}")

print()
print("### E2. label hunt: non-white, non-green ink map x330..430 y150..235 (t<165)")
def txtmask(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    grayish = (R < 165) & (abs(R - G) < 40) & (abs(G - B) < 40)
    return grayish
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    tm = txtmask(im)
    print(f"  --- {tag} (1x cols x330..430) ---")
    for y in range(150, 236, 2):
        line = "".join("#" if tm[y:y+2, x:x+2].any() else "." for x in range(330, 430, 2))
        print(f"    {y:3d} {line}")
