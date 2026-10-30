#!/usr/bin/env python3
"""Measure the middle-table yellow highlight bands in the ORIGINAL vs the build."""
import sys
from PIL import Image
import numpy as np

ROOT = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{ROOT}/unique_slides/slide_021.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{ROOT}/recreated_pptx/qa/slide021/render_9.png").convert("RGB")).astype(int)
SC = 2001 / 960.0

COLS = [90, 158, 226, 294]      # frame px
ROWS = [342, 360, 377, 395]
CELLS = {0: ("r1c1", 0), 1: ("r2c2", 1), 2: ("r3c3", 2)}

def cellbox(ci, ri):
    return COLS[ci], COLS[ci+1], ROWS[ri], ROWS[ri+1]

for ci_row, ri in [(0, 0), (1, 1), (2, 2)]:
    x0, x1, y0, y1 = cellbox(ci_row, ri)
    # interior: skip 3px gridlines
    ix0, ix1, iy0, iy1 = x0+3, x1-3, y0+3, y1-3
    sub = o[iy0:iy1+1, ix0:ix1+1]
    pale = (sub[:,:,0]>150)&(sub[:,:,1]>150)&(sub[:,:,2]<190)&(sub[:,:,0]-sub[:,:,2]>25)
    olive = (sub[:,:,0]>180)&(sub[:,:,1]>180)&(sub[:,:,2]<190)&(sub[:,:,0]-sub[:,:,2]>20)
    m = pale | olive
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"ORIG {CELLS[ci_row][0]} cell x{x0}..{x1} y{y0}..{y1}: highlight x{ix0+xs.min()}..{ix0+xs.max()} y{iy0+ys.min()}..{iy0+ys.max()}  (w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1})")
    # digit ink (dark) in the interior
    dark = sub.mean(axis=2) < 120
    yd, xd = np.nonzero(dark)
    if len(xd):
        print(f"     digit ink bbox x{ix0+xd.min()}..{ix0+xd.max()} y{iy0+yd.min()}..{iy0+yd.max()}  (w={xd.max()-xd.min()+1} h={yd.max()-yd.min()+1})")

print()
print("=== RENDER_9 same cells ===")
for ci_row, ri in [(0, 0), (1, 1), (2, 2)]:
    x0, x1, y0, y1 = cellbox(ci_row, ri)
    ix0, ix1, iy0, iy1 = x0+3, x1-3, y0+3, y1-3
    X0, X1, Y0, Y1 = [int(round(v*SC)) for v in (ix0, ix1+1, iy0, iy1+1)]
    sub = r[Y0:Y1, X0:X1]
    yel = (sub[:,:,0]>200)&(sub[:,:,1]>200)&(sub[:,:,2]<170)
    ys, xs = np.nonzero(yel)
    if len(xs):
        print(f"REND {CELLS[ci_row][0]}: saturated-yellow px={int(yel.sum())}  bbox frame x{round((X0+xs.min())/SC,1)}..{round((X0+xs.max())/SC,1)} y{round((Y0+ys.min())/SC,1)}..{round((Y0+ys.max())/SC,1)}")
    dark = sub.mean(axis=2) < 120
    yd, xd = np.nonzero(dark)
    if len(xd):
        print(f"     digit ink bbox x{round((X0+xd.min())/SC,1)}..{round((X0+xd.max())/SC,1)} y{round((Y0+yd.min())/SC,1)}..{round((Y0+yd.max())/SC,1)}")
    from collections import Counter
    c = Counter(map(tuple, sub.reshape(-1,3)))
    print(f"     dominant colors: {[(tuple(int(v) for v in k), n) for k,n in c.most_common(4)]}")
