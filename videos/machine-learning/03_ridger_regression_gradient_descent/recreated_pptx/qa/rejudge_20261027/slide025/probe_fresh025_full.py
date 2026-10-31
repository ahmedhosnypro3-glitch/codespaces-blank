#!/usr/bin/env python3
"""Targeted PIL probes for the 2026-10-31 fresh FULL FAIL claims on slide 025 (k14 render 03:37).
Compares render.png (downscaled to 960x540 slide space) vs unique_slides/slide_025.jpg.
Read-only wrt existing evidence; prints measurements for each judge claim."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
r = Image.open(f"{RJ}/slide025/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
R = np.asarray(r).astype(int)
O = np.asarray(o).astype(int)

def masks(A):
    red = (A[:, :, 0] > 120) & (A[:, :, 1] < 100) & (A[:, :, 2] < 100)
    dark = A.sum(axis=2) < 330
    panel = (np.abs(A[:, :, 0] - 233) < 12) & (np.abs(A[:, :, 1] - 233) < 12) & (np.abs(A[:, :, 2] - 231) < 12)
    white = (A[:, :, 0] > 245) & (A[:, :, 1] > 245) & (A[:, :, 2] > 245)
    surface = (~white) & (~panel) & (~red) & (~dark)  # colored surface fill
    return red, dark, panel, white, surface

rred, rdark, rpanel, rwhite, rsurf = masks(R)
ored, odark, opanel, owhite, osurf = masks(O)

def region(name, x0, y0, x1, y1):
    sl = (slice(y0, y1), slice(x0, x1))
    print(f"-- {name} x{x0}-{x1} y{y0}-{y1}")
    print(f"   red   render={rred[sl].sum():6d} orig={ored[sl].sum():6d}")
    print(f"   dark  render={rdark[sl].sum():6d} orig={odark[sl].sum():6d}")
    print(f"   surf  render={rsurf[sl].sum():6d} orig={osurf[sl].sum():6d}")
    print(f"   white render={rwhite[sl].sum():6d} orig={owhite[sl].sum():6d}")

# locate panels: scan for long dark/red horizontal+vertical lines to find plot boxes
def find_boxes(dark):
    rows = dark.sum(axis=1); cols = dark.sum(axis=0)
    hl = [y for y in range(540) if rows[y] > 150]
    vl = [x for x in range(960) if cols[x] > 150]
    return hl, vl
print("orig dark hlines y:", find_boxes(odark)[0])
print("orig dark vlines x:", find_boxes(odark)[1])
print("render dark hlines y:", find_boxes(rdark)[0])
print("render dark vlines x:", find_boxes(rdark)[1])

# quadrant guesses refined after seeing lines; use generous quadrants
region("TR panel", 590, 150, 900, 375)
region("BR panel", 470, 380, 900, 535)
region("BL panel", 60, 380, 460, 535)
region("TL panel", 60, 150, 460, 375)

# claim 2: BR containment — non-background ink in bottom rows of BR panel
for y0, y1 in [(520, 528), (528, 536), (536, 540)]:
    sl = (slice(y0, y1), slice(470, 900))
    rb = (~rwhite[sl]) & (~rpanel[sl])
    ob = (~owhite[sl]) & (~opanel[sl])
    print(f"BR bottom rows y{y0}-{y1}: non-bg render={rb.sum()} orig={ob.sum()}")

# claim 1: BR path — dark ink inside BR panel interior (exclude axes/labels: x500-890 y390-520)
sl = (slice(390, 520), slice(500, 890))
print(f"BR interior dark: render={rdark[sl].sum()} orig={odark[sl].sum()}")
sl = (slice(390, 520), slice(500, 890))
print(f"BR interior surf: render={rsurf[sl].sum()} orig={osurf[sl].sum()}")

# claim 3: BL label swap — dark text clusters in BL lower area; compare label boxes pairwise
def box(A, x0, y0, x1, y1):
    return (A[y0:y1, x0:x1] > 0).astype(np.uint8)
# find dark text rows in BL panel
bl = odark[380:535, 60:460]
rows = bl.sum(axis=1)
print("BL dark-text row bands (y offset from 380):", [(i, int(v)) for i, v in enumerate(rows) if v > 8])
