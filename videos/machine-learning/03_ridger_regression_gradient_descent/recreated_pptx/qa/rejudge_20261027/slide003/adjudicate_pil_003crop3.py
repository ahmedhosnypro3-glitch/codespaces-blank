#!/usr/bin/env python3
"""Full-resolution checks for slide003 crop FAIL claims 2,3,6."""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"

o = Image.open(f"{NS}/unique_slides/slide_003.jpg").convert("RGB")
r = Image.open(f"{RJ}/slide003/render.png").convert("RGB")
sc = r.size[0] / 960.0
O = np.asarray(o).astype(int)
R = np.asarray(r).astype(int)

def red(A): return (A[:,:,0] > A[:,:,1]+60) & (A[:,:,0] > A[:,:,2]+60) & (A[:,:,0] > 100)
def blue(A): return (A[:,:,2] > A[:,:,0]+40) & (A[:,:,2] > A[:,:,1]+30) & (A[:,:,2] > 90)
def dark(A): return A.sum(axis=2) < 300
def purple(A): return (A[:,:,0] > A[:,:,2]+30) & (A[:,:,2] > A[:,:,1]+30) & (A[:,:,0] > 90)

print("== 1) In-General enclosure border, slide x600-880 y260-296")
for name, A, s in (("ORIG", O, 1.0), ("RENDER", R, sc)):
    x0, y0, x1, y1 = int(600*s), int(260*s), int(880*s), int(296*s)
    sub = A[y0:y1, x0:x1]
    print(f"  {name}: dark={dark(sub).sum()} blue={blue(sub).sum()} red={red(sub).sum()} purple={purple(sub).sum()}")
    km = dark(sub) | blue(sub)
    rows = km.sum(axis=1); cols = km.sum(axis=0)
    tr = [(y0+i, int(v)) for i, v in enumerate(rows) if v >= 40]
    tc = [(x0+i, int(v)) for i, v in enumerate(cols) if v >= 20]
    print(f"    long dark/blue rows (slide y, px): {[(round(y/s), n) for y, n in tr]}")
    print(f"    long dark/blue cols (slide x, px): {[(round(x/s), n) for x, n in tc]}")

print("\n== 2) '>>>' color, slide x700-800 y270-292")
for name, A, s in (("ORIG", O, 1.0), ("RENDER", R, sc)):
    x0, y0, x1, y1 = int(700*s), int(270*s), int(800*s), int(292*s)
    sub = A[y0:y1, x0:x1]
    print(f"  {name}: red={red(sub).sum()} blue={blue(sub).sum()} purple={purple(sub).sum()} dark={dark(sub).sum()}")
    # per slide-x column classification
    for cls, fn in (("R", red), ("B", blue), ("P", purple), ("K", dark)):
        m = fn(sub).sum(axis=0)
        xs = [round(700 + i/s) for i, v in enumerate(m) if v >= 2]
        if xs: print(f"    {cls} x: {xs}")

print("\n== 3) Remember-box equation line, slide x650-874 y182-218 (orig) — ink class map 1px")
def cmap(A, s, x0, y0, x1, y1, step=1):
    for y in range(int(y0*s), int(y1*s), max(1,int(step*s))):
        line = ""
        for x in range(int(x0*s), int(x1*s), max(1,int(step*s))):
            cell = A[y:y+max(1,int(step*s)), x:x+max(1,int(step*s))]
            r_, b_, p_, k_ = red(cell), blue(cell), purple(cell), dark(cell)
            n = cell.shape[0]*cell.shape[1]
            if r_.sum() >= n*0.3: line += "R"
            elif b_.sum() >= n*0.3: line += "B"
            elif p_.sum() >= n*0.3: line += "P"
            elif k_.sum() >= n*0.3: line += "K"
            else: line += "."
        print(f"  {round(y/s):3d} {line}")

print("-- ORIG eq line")
cmap(O, 1.0, 650, 182, 874, 218)
print("-- RENDER eq line (slide space via scale)")
cmap(R, sc, 650, 182, 874, 218)

print("\n== 4) underline under first y: orig box interior x652-680 y190-218 per-row dark runs")
for name, A, s in (("ORIG", O, 1.0), ("RENDER", R, sc)):
    km = dark(A)
    print(f"  {name}:")
    for y in range(int(190*s), int(219*s)):
        row = km[y, int(652*s):int(700*s)]
        best = cur = 0
        for v in row:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if row.sum() >= 4:
            print(f"    slide y={round(y/s)} dark={row.sum()} maxrun={round(best/s,1)}")
