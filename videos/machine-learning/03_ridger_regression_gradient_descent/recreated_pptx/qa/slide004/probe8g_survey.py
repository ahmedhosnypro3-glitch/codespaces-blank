#!/usr/bin/env python3
"""Probe 8g: full survey of the two Let-boxes (orig vs render) + L2/L3 inline words."""
from PIL import Image
import numpy as np

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB"))
REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB"))
S = REND.shape[0] / 540.0

def census(arr, sc, x0, y0, x1, y1, cell=20):
    """ink census per cell in frame coords."""
    a = arr[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)].astype(int)
    dk = (a.max(axis=2) < 200)
    red = (a[:,:,0] > 140) & (a[:,:,1] < 120) & (a[:,:,2] < 120)
    blu = (a[:,:,2] > 120) & (a[:,:,0] < 110) & (a[:,:,1] < 110)
    ch, cw = int(cell*sc), int(cell*sc)
    print(f"     " + "".join(f"{(x0+i*cell)%100:02d} "[-3:] for i in range(int((x1-x0)/cell))))
    for yy in range(int((y1-y0)/cell)):
        row = f"y{y0+yy*cell:3d} "
        for xx in range(int((x1-x0)/cell)):
            ya, yb = yy*ch, (yy+1)*ch
            xa, xb = xx*cw, (xx+1)*cw
            d, r, b = dk[ya:yb, xa:xb].sum(), red[ya:yb, xa:xb].sum(), blu[ya:yb, xa:xb].sum()
            if r > 30: c = "R"
            elif b > 30: c = "B"
            elif d > 60: c = "#"
            elif d > 15: c = "+"
            elif r or b or d: c = "."
            else: c = " "
            row += c + " "
        print(row)

print("=== ORIG left+right box region x75..780 y94..226, 20px cells (#=dark R=red B=blue) ===")
census(ORIG, 1.0, 75, 94, 780, 226)
print("\n=== REND same region ===")
census(REND, S, 75, 94, 780, 226)

print("\n=== ORIG L2/L3/L4 full where-block x495..900 y280..370 ASCII (2x2) ===")
def ascii2(arr, sc, x0, y0, x1, y1, t=190):
    a = arr[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)].astype(int)
    dk = a.max(axis=2) < t
    red = (a[:,:,0] > 140) & (a[:,:,1] < 110) & (a[:,:,2] < 110)
    H, W = dk.shape
    step = 2
    for yy in range(0, H-1, step):
        row = ""
        for xx in range(0, W-1, step):
            bd = dk[yy:yy+step, xx:xx+step].sum()
            br = red[yy:yy+step, xx:xx+step].sum()
            row += "R" if br >= 2 else "#" if bd >= 2 else ("r" if br else ("+" if bd else "."))
        print(f"{y0+int(yy/sc):3d} {row}")
ascii2(ORIG, 1.0, 495, 280, 900, 370)
