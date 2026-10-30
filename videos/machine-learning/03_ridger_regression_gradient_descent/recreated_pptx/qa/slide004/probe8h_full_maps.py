#!/usr/bin/env python3
"""Probe 8h: full ASCII maps - left/right Let boxes (orig+render) and where-block L1."""
from PIL import Image
import numpy as np

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB"))
REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB"))
S = REND.shape[0] / 540.0

def ascii_map(arr, sc, x0, y0, x1, y1, px=2, t=200, label=""):
    a = arr[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)].astype(int)
    dk = a.max(axis=2) < t
    red = (a[:,:,0] > 150) & (a[:,:,1] < 130) & (a[:,:,2] < 130)
    blu = (a[:,:,2] > 120) & (a[:,:,0] < 120) & (a[:,:,1] < 120)
    H, W = dk.shape
    fy = px * sc  # render px per char-row (px frame px)
    print(f"--- {label} x{x0}..{x1} y{y0}..{y1} ({px}px/char) ---")
    yy = 0
    while yy < H - 1:
        row = ""
        xx = 0
        while xx < W - 1:
            ya, yb = int(yy), min(H, int(yy + fy))
            xa, xb = int(xx), min(W, int(xx + fy))
            bd = dk[ya:yb, xa:xb].sum()
            br = red[ya:yb, xa:xb].sum()
            bb = blu[ya:yb, xa:xb].sum()
            if br >= max(1, (yb-ya)*(xb-xa)*0.10): row += "R"
            elif bb >= max(1, (yb-ya)*(xb-xa)*0.10): row += "B"
            elif bd >= max(1, (yb-ya)*(xb-xa)*0.25): row += "#"
            elif bd or br or bb: row += "+"
            else: row += "."
            xx += fy
        print(f"{y0 + int(yy/sc):3d} {row}")
        yy += fy

# 1. ORIG both boxes full
ascii_map(ORIG, 1.0, 78, 96, 770, 226, px=3, label="ORIG boxes")
# 2. REND both boxes full
ascii_map(REND, S, 78, 96, 770, 226, px=3, label="REND boxes")
# 3. ORIG where-block L1
ascii_map(ORIG, 1.0, 495, 240, 900, 290, px=2, label="ORIG L1")
# 4. REND where-block L1
ascii_map(REND, S, 495, 240, 900, 290, px=2, label="REND L1")
