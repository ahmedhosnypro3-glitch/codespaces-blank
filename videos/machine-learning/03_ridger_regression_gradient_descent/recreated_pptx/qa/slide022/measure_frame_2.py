#!/usr/bin/env python3
"""Measure pass 2 for slide_022.jpg: panel-interior ink census (find the cursor),
precise title row profiles (dense core vs AA halo), badge numeral ink, and a
font-size advance fit using real Arial-metric fonts."""
import glob
import numpy as np
from PIL import Image, ImageFont

IM = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_022.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = im.shape[:2]
BG = np.array([233, 233, 231])  # panel E9E9E7 (measured)

# --- 1. sensitive census INSIDE the panel only --------------------------------
# panel x 54..903, y 45..540. Interior with margin off the strokes:
x0, x1 = 66, 894
y0, y1 = 52, 530
sub = im[y0:y1, x0:x1]
diff = np.abs(sub - BG).max(axis=2)
ink = diff > 18   # sensitive: catches light AA and pale artifacts
print(f"panel-interior sensitive ink px = {ink.sum()}")
rows = np.where(ink.sum(axis=1) > 2)[0]
bands = []
if len(rows):
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y - p > 5:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
print("census bands (panel-interior coords, add x0/y0 offsets):")
for (a, b) in bands:
    sel = ink[a:b + 1]
    xs_ = np.where(sel.any(axis=0))[0]
    print(f"  y {y0+a}..{y0+b}  x {x0+xs_.min()}..{x0+xs_.max()}  npx={sel.sum()}")

# --- 2. cursor hunt: pixels WHITE-ish (fill) or DARK-ish (outline) in panel ----
white = (sub[:, :, 0] > 243) & (sub[:, :, 1] > 243) & (sub[:, :, 2] > 243)
darkish = (sub.sum(axis=2) < 420) & ~((sub[:, :, 0] > 90) & (sub[:, :, 1] < 60))  # dark, non-red
print(f"\npanel pure-white-ish px = {white.sum()}; dark non-red px = {darkish.sum()}")
for name, mask in (("white", white), ("dark", darkish)):
    if mask.sum():
        rr = np.where(mask.sum(axis=1) > 0)[0]
        if len(rr):
            s = rr[0]; p = rr[0]
            for y in rr[1:]:
                if y - p > 4:
                    blk = mask[s:p + 1]
                    xb = np.where(blk.any(axis=0))[0]
                    print(f"  {name} band y {y0+s}..{y0+p} x {x0+xb.min()}..{x0+xb.max()} npx={blk.sum()}")
                    s = y
                p = y
            blk = mask[s:p + 1]
            xb = np.where(blk.any(axis=0))[0]
            print(f"  {name} band y {y0+s}..{y0+p} x {x0+xb.min()}..{x0+xb.max()} npx={blk.sum()}")

# --- 3. precise title row profiles (halo vs dense core) -------------------------
red = (im[:, :, 0] > 90) & ((im[:, :, 0] - im[:, :, 1]) > 40) & ((im[:, :, 0] - im[:, :, 2]) > 10)
for label, (ya, yb) in (("L1", (228, 282)), ("L2", (318, 372))):
    print(f"\n{label} row profile (red px per row, rows {ya}..{yb}):")
    for y in range(ya, yb):
        n = red[y, 100:900].sum()
        if n:
            xs_ = np.where(red[y, 100:900])[0]
            print(f"  y={y}: n={n:4d}  x {100+xs_.min()}..{100+xs_.max()}")

# --- 4. badge numeral ink on THIS frame -----------------------------------------
print("\nbadge window (x 862..891, y 59..88) near-black px per row:")
for y in range(59, 89):
    row = im[y, 862:892]
    darkpx = (row.sum(axis=1) < 330).sum()
    if darkpx:
        xs_ = np.where(row.sum(axis=1) < 330)[0]
        print(f"  y={y}: darkpx={darkpx} x {862+xs_.min()}..{862+xs_.max()}")

# --- 5. font-size advance fit -----------------------------------------------------
L1 = "[3] Inverse of High Dimension"
L2 = "(non-singular) Matrix"
MEAS = {"L1": (189, 726, 235, 274), "L2": (274, 652, 325, 364)}  # inclusive ink bbox

cands = []
for pat in ("/usr/share/fonts/**/LiberationSans-Bold.ttf",
            "/usr/share/fonts/**/Arial-Bold.ttf",
            "/usr/share/fonts/**/DejaVuSans-Bold.ttf"):
    cands += glob.glob(pat, recursive=True)
print("\nfont candidates:", cands)
if cands:
    fontpath = cands[0]
    print("using:", fontpath)
    for label, text in (("L1", L1), ("L2", L2)):
        mx = MEAS[label][1] - MEAS[label][0] + 1
        my = MEAS[label][3] - MEAS[label][2] + 1
        print(f"{label} measured ink w={mx} h={my}")
        best = []
        for size in range(30, 56):
            f = ImageFont.truetype(fontpath, size)
            # ink bbox via getbbox (includes bearing)
            bbox = f.getbbox(text)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            best.append((abs(w - mx), size, w, h, bbox))
        best.sort()
        for d, size, w, h, bbox in best[:4]:
            print(f"   size {size}: ink w={w} (d={d}) h={h} bbox={bbox}")
