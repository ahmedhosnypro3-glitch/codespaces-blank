#!/usr/bin/env python3
"""Precise per-region measurement of slide_004.jpg — pass 3.

For each approx region, dump 1px-resolution row/col ink profiles for
TEXT-colored ink (dark/red/blue/yellow), separated from the pink/pale-blue
fills, so text lines and box geometry can be placed exactly.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
H, W = im.shape[:2]

red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330
# pale-blue-ish fill mask (Remember box fill/border family)
paleblue = (b - r >= 5) & (b > 225) & (r > 200)
# pink fill family
pink = (r - b > 15) & (r > 238) & (g > 200)
# text ink = dark, red or blue (exclude fills)
text = dark | red | blue


def runs(mask_1d, min_len=1):
    out, d = [], np.diff(np.concatenate(([0], mask_1d.astype(int), [0])))
    for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0] - 1):
        if e - s + 1 >= min_len:
            out.append((int(s), int(e)))
    return out


def profile(name, x0, x1, y0, y1, masks=("text", "red", "blue", "dark")):
    sel = {"text": text, "red": red, "blue": blue, "dark": dark}
    print(f"\n### {name}: x {x0}..{x1}, y {y0}..{y1}")
    for mname in masks:
        m = sel[mname]
        sub = m[y0:y1 + 1, x0:x1 + 1]
        rb = runs(sub.sum(axis=1) > 0)
        print(f"  [{mname}] row bands (abs y):", [(y0 + s, y0 + e) for s, e in rb][:20])
        for s, e in rb[:12]:
            band = sub[s:e + 1]
            cols = np.where(band.sum(axis=0) > 0)[0]
            if len(cols):
                print(f"      y {y0+s}..{y0+e} (h {e-s+1}): x {x0+cols.min()}..{x0+cols.max()} (w {cols.max()-cols.min()+1})")


# --- Title zone
profile("TITLE", 250, 700, 50, 100)

# --- Box edges: find red/blue/paleblue verticals and horizontals in the body
print("\n### border census")
# red verticals (excluding house strokes at x58/901): columns with many red px in y 100..525
redcol = red[100:525, :].sum(axis=0)
for s, e in runs(redcol > 30, min_len=1):
    print(f"  red vertical col x {s}..{e} (px {redcol[s:e+1].max()})")
blucol = blue[100:525, :].sum(axis=0)
for s, e in runs(blucol > 30, min_len=1):
    print(f"  blue vertical col x {s}..{e} (px {blucol[s:e+1].max()})")
pcol = paleblue[100:525, :].sum(axis=0)
for s, e in runs(pcol > 40, min_len=1):
    print(f"  paleblue vertical col x {s}..{e} (px {pcol[s:e+1].max()})")
redrow = red[:, 62:900].sum(axis=1)
for s, e in runs(redrow > 40, min_len=1):
    print(f"  red horizontal row y {s}..{e} (px {redrow[s:e+1].max()})")
blurow = blue[:, 62:900].sum(axis=1)
for s, e in runs(blurow > 40, min_len=1):
    print(f"  blue horizontal row y {s}..{e} (px {blurow[s:e+1].max()})")
prow = paleblue[:, 62:900].sum(axis=1)
for s, e in runs(prow > 40, min_len=1):
    print(f"  paleblue horizontal row y {s}..{e} (px {prow[s:e+1].max()})")

# --- fill extents (pink / paleblue), as column/row bands with density
print("\n### fill extents")
psub = pink[:, :]
prowsum = psub.sum(axis=1)
for s, e in runs(prowsum > 200, min_len=1):
    band = psub[s:e + 1]
    cols = np.where(band.sum(axis=0) > (e - s + 1) * 0.5)[0]
    print(f"  pink rows y {s}..{e}: dense cols {cols.min()}..{cols.max()}")
bsub = paleblue[:, :]
browsum = bsub.sum(axis=1)
for s, e in runs(browsum > 200, min_len=1):
    band = bsub[s:e + 1]
    cols = np.where(band.sum(axis=0) > (e - s + 1) * 0.5)[0]
    print(f"  paleblue rows y {s}..{e}: dense cols {cols.min()}..{cols.max()}")

# --- per-box text profiles
profile("BOX1 interior (Original Labels)", 64, 408, 98, 222)
profile("BOX2 interior (Predicted Labels)", 426, 748, 98, 222)
profile("BOX3 interior (Remember)", 758, 896, 98, 222)
profile("RIGHT annotations", 496, 900, 240, 370)
profile("FORMULA box", 492, 890, 214, 238)
profile("OBJ box (Objective)", 64, 660, 380, 452)
profile("DEFINE box", 64, 660, 460, 528)
