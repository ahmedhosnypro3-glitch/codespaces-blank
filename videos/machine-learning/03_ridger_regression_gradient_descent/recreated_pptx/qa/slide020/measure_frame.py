#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_020.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_020.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
print("size:", W, "x", H)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

# red ink (title C00000 + strokes)
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
ys, xs = np.where(red)
print("red ink total px:", red.sum())
if red.sum():
    print("red bbox: x", xs.min(), "-", xs.max(), " y", ys.min(), "-", ys.max())

# red rows profile (which rows hold red ink)
rows = np.where(red.sum(axis=1) > 0)[0]
print("red rows span:", rows.min() if len(rows) else None, "-", rows.max() if len(rows) else None)

# separate title rows from chrome strokes: strokes are at x~58-59, x~901, y~538 band
# title red = red ink NOT in stroke columns/stroke rows
title_red = red.copy()
title_red[:, :62] = False
title_red[:, 898:] = False
title_red[533:, :] = False
title_red[:52, :] = False
ys2, xs2 = np.where(title_red)
print("title red px:", title_red.sum())
if title_red.sum():
    print("title red bbox: x", xs2.min(), "-", xs2.max(), " y", ys2.min(), "-", ys2.max())
    # row profile clusters
    tr_rows = np.where(title_red.sum(axis=1) > 0)[0]
    # find contiguous bands
    bands = []
    start = tr_rows[0]; prev = tr_rows[0]
    for y in tr_rows[1:]:
        if y > prev + 3:
            bands.append((start, prev)); start = y
        prev = y
    bands.append((start, prev))
    print("title red row bands (y0,y1) + px/row sample:")
    for (y0, y1) in bands:
        band = title_red[y0:y1+1]
        cols = np.where(band.any(axis=0))[0]
        print(f"  band y {y0}-{y1}  h={y1-y0+1}  x {cols.min()}-{cols.max()}  px={band.sum()}")

# yellow badge
yel = (r > 200) & (g > 200) & (b < 190)
ys3, xs3 = np.where(yel)
if yel.sum():
    print("yellow bbox: x", xs3.min(), "-", xs3.max(), " y", ys3.min(), "-", ys3.max(),
          "center:", (xs3.min()+xs3.max())/2, (ys3.min()+ys3.max())/2,
          "d:", xs3.max()-xs3.min()+1)

# dark ink (numeral, underline? underlines in this deck are usually red if title is red)
dark = (r < 100) & (g < 100) & (b < 100)
ys4, xs4 = np.where(dark)
print("dark ink px:", dark.sum())
if dark.sum():
    print("dark bbox: x", xs4.min(), "-", xs4.max(), " y", ys4.min(), "-", ys4.max())
    dr_rows = np.where(dark.sum(axis=1) > 0)[0]
    bands = []
    if len(dr_rows):
        start = dr_rows[0]; prev = dr_rows[0]
        for y in dr_rows[1:]:
            if y > prev + 3:
                bands.append((start, prev)); start = y
            prev = y
        bands.append((start, prev))
    print("dark row bands:")
    for (y0, y1) in bands:
        band = dark[y0:y1+1]
        cols = np.where(band.any(axis=0))[0]
        print(f"  band y {y0}-{y1}  h={y1-y0+1}  x {cols.min()}-{cols.max()}  px={band.sum()}")

# any other ink on the gray panel? sample far-from-text rows for surprises
# non-bg, non-red, non-yellow, non-dark ink on the panel interior
gray_panel = (abs(r-233)<16) & (abs(g-233)<16) & (abs(b-231)<18)
white = (r>245)&(g>245)&(b>245)
other = ~(red | yel | dark | gray_panel | white)
other[:40,:]=False; other[:, :64]=False; other[:, 896:]=False; other[535:,:]=False  # margins/chrome
ys5, xs5 = np.where(other)
print("other ink px (panel interior, excl chrome/colors):", other.sum())
if other.sum():
    print("other bbox: x", xs5.min(), "-", xs5.max(), " y", ys5.min(), "-", ys5.max())
    # sample colors
    samp = im[ys5, xs5]
    print("other ink mean color:", samp.mean(axis=0))
    or_rows = np.where(other.sum(axis=1) > 0)[0]
    print("other rows:", or_rows.min(), "-", or_rows.max())
