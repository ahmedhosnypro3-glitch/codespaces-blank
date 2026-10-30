#!/usr/bin/env python3
"""Per-cell ink census for slide 003's bottom design matrix and weight vector.

Frame space = 960x540 (1px = 1pt); render_19 (2001x1125) is sampled both
full-resolution and LANCZOS-resampled. Cell boxes come from the CURRENT pptx
shape geometry (96dpi EMU coords x 0.75 -> frame coords), so each box is where
the shape actually sits rather than a guessed region.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"
S = 2001 / 960.0

o = np.asarray(Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(QA + "/render_19.png").convert("RGB")).astype(int)
r960 = np.asarray(Image.open(QA + "/render_19.png")
                  .convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int)


def dark(img):
    return (np.minimum(np.minimum(img[:, :, 0], img[:, :, 1]), img[:, :, 2]) < 100)


def box(img, x, y, w, h, sc=1.0):
    x, y, w, h = int(x * sc), int(y * sc), int(w * sc), int(h * sc)
    return img[y:y + h, x:x + w]


def ink(img, x, y, w, h, sc=1.0):
    return int(dark(box(img, x, y, w, h, sc)).sum())


COLS = [181.5, 225.75, 270.0, 313.5]
CW = 39.75
ROWS = [367.5, 396.75, 426.75, 456.0]
RH = 24.75

print("DESIGN MATRIX — dark-ink px per cell box (frame coords from pptx geometry)")
print("row  y      cell |   ORIG  RENDER(full)  RENDER(960)")
for ri, ry in enumerate(ROWS):
    for ci, cx in enumerate(COLS):
        print(f"  {ri+1}  {ry:6.2f}  c{ci+1}  | "
              f"{ink(o, cx, ry, CW, RH):6d} {ink(r, cx, ry, CW, RH, S):10d} "
              f"{ink(r960, cx, ry, CW, RH):11d}")
print()
print("WEIGHT VECTOR — dark-ink px per cell box")
WV = {"b": 349.5, "w1": 387.75, "w2": 415.5, "ellipsis": 453.0, "wd": 469.5}
WX = 462.0
for k, wy in WV.items():
    print(f"  {k:9s} | {ink(o, WX, wy, 55.5, 24):6d} {ink(r, WX, wy, 55.5, 24, S):10d} "
          f"{ink(r960, WX, wy, 55.5, 24):11d}")
