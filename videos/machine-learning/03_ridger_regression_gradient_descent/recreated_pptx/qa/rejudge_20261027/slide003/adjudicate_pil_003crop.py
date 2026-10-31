#!/usr/bin/env python3
"""PIL measurements for slide003 crop-FAIL adjudication (read-only).

Region: 568,136-872,344 (slide space). Render 2001x1125, scale 2.0844.
Measures: Remember box + In General enclosure geometry in BOTH images,
>>> color in orig vs render, underline under first y.
"""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"

o = Image.open(f"{NS}/unique_slides/slide_003.jpg").convert("RGB")
r = Image.open(f"{RJ}/slide003/render.png").convert("RGB")
sc = r.size[0] / 960.0
print("render", r.size, "scale", sc)
# downscale render to slide space for direct comparison
rs = r.resize((960, 540), Image.LANCZOS)
O = np.asarray(o).astype(int)
R = np.asarray(rs).astype(int)

X0, Y0, X1, Y1 = 568, 136, 872, 344

def blue_mask(A):
    # blue-ish ink: b high, b > r+40, b > g+30
    return (A[:, :, 2] > A[:, :, 0] + 40) & (A[:, :, 2] > A[:, :, 1] + 30) & (A[:, :, 2] > 90)

def red_mask(A):
    return (A[:, :, 0] > A[:, :, 1] + 60) & (A[:, :, 0] > A[:, :, 2] + 60) & (A[:, :, 0] > 100)

def dark_mask(A):
    return (A.sum(axis=2) < 300)

for name, A in (("ORIG", O), ("RENDER", R)):
    sub = A[Y0:Y1, X0:X1]
    bm = blue_mask(sub)
    print(f"\n== {name} region x{X0}-{X1} y{Y0}-{Y1}: blue px {bm.sum()}, red px {red_mask(sub).sum()}, dark px {dark_mask(sub).sum()}")
    # column profile of blue ink -> vertical borders of boxes
    cols = bm.sum(axis=0)
    rows = bm.sum(axis=1)
    top_cols = np.argsort(cols)[-12:]
    top_rows = np.argsort(rows)[-12:]
    print("  blue-heavy cols (slide x):", sorted((int(c) + X0, int(cols[c])) for c in top_cols))
    print("  blue-heavy rows (slide y):", sorted((int(rw) + Y0, int(rows[rw])) for rw in top_rows))

# Remember box: find its border rectangle in each image.
# Scan for long horizontal blue runs (top/bottom edges) and vertical blue runs.
for name, A in (("ORIG", O), ("RENDER", R)):
    bm = blue_mask(A)
    print(f"\n== {name} long horizontal blue runs (len>=60) in y{Y0}-{Y1}:")
    for y in range(Y0, Y1):
        row = bm[y]
        x = 0
        while x < 960:
            if row[x]:
                x2 = x
                while x2 < 960 and row[x2]:
                    x2 += 1
                if x2 - x >= 60:
                    print(f"   y={y} x={x}..{x2-1} len={x2-x}")
                x = x2
            else:
                x += 1
    print(f"== {name} long vertical blue runs (len>=40) in x{X0}-{X1}:")
    for x in range(X0, X1):
        col = bm[:, x]
        y = Y0
        while y < Y1:
            if col[y]:
                y2 = y
                while y2 < Y1 and col[y2]:
                    y2 += 1
                if y2 - y >= 40:
                    print(f"   x={x} y={y}..{y2-1} len={y2-y}")
                y = y2
            else:
                y += 1

# ">>>" color: locate red/blue ink in the In-General line. First find the
# "In General" text row band: scan region for rows with red ink in orig.
for name, A in (("ORIG", O), ("RENDER", R)):
    rm = red_mask(A)
    bm = blue_mask(A)
    print(f"\n== {name} red/blue ink per row in x{X0}-{X1} y{Y0}-{Y1} (rows with >=8 red or blue px):")
    for y in range(Y0, Y1):
        rr = rm[y, X0:X1].sum()
        bb = bm[y, X0:X1].sum()
        if rr >= 8 or bb >= 8:
            print(f"   y={y} red={rr} blue={bb}")
