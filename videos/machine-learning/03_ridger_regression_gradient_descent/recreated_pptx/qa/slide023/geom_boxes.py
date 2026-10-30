#!/usr/bin/env python3
"""Authoritative consolidated geometry for slide_023. 960x540, 1px=1pt.
Reports per-box fill bbox, border position each side, corner radius, fill modal color,
AND lets me eyeball the green-box width question. Also equation ink + text bands."""
import numpy as np
from PIL import Image

IM = 'unique_slides/slide_023.jpg'
IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
H, W = a.shape[:2]

def bbox_rows_cols(m):
    ys, xs = np.where(m)
    if not len(ys): return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

# ---- fill masks ----
green = (G > R + 6) & (G > B + 6) & (G > 200) & (G < 255)
blue  = (B > R + 4) & (B > G - 2) & (B > 235) & (R > 235) & (G > 240)  # very pale blue
yellow= (R > 245) & (G > 245) & (B > 205) & (B < 242)  # pale yellow FFF2CC-ish
panel_gray = (R < 238) & (R > 222) & (abs(R-G)<4) & (abs(G-B)<4)

def report(name, m, y0,y1,x0,x1):
    sub = np.zeros_like(m); sub[y0:y1+1, x0:x1+1] = True
    mm = m & sub
    bb = bbox_rows_cols(mm)
    ib = bbox_rows_cols(mm)
    # border = rows/cols where this mask has long horizontal/vertical runs
    rows = np.where(mm[y0:y1+1, x0:x1+1].sum(axis=1) > 300)[0] + y0
    cols = np.where(mm[y0:y1+1, x0:x1+1].sum(axis=0) > 60)[0] + x0
    # modal color of the fill (interior)
    ys,xs = np.where(mm)
    if len(ys):
        from collections import Counter
        c = Counter((a[y,x,0],a[y,x,1],a[y,x,2]) for y,x in zip(ys,xs) if y0+8<y<y1-8 and x0+8<x<x1-8)
        modal = c.most_common(2)
    else:
        modal = None
    print(f"{name}: fill bbox x{bb[0]}..{bb[2]} y{bb[1]}..{bb[3]} (w{bb[2]-bb[0]+1} h{bb[3]-bb[1]+1})")
    print(f"   long rows: {list(rows[:4])}{'..' if len(rows)>8 else ''}{list(rows[-4:]) if len(rows)>8 else ''} n={len(rows)}")
    print(f"   long cols: {list(cols[:4])}{'..' if len(cols)>8 else ''}{list(cols[-4:]) if len(cols)>8 else ''} n={len(cols)}")
    print(f"   modal fill: {modal}")

report("GREEN recall", green, 95,240, 60, 900)
report("BLUE complexity", blue, 222,430, 60, 900)
report("YELLOW solution", yellow, 425,540, 60, 900)

# ---- corner radius: for green box, top edge leftmost x per row ----
print("\n== GREEN top-left corner profile (leftmost green x per y) ==")
for y in range(100, 125):
    xs = np.where(green[y, 60:180])[0]
    print(f" y{y}: x{xs.min()+60 if len(xs) else None}")
print("== GREEN top-right corner (rightmost green x per y) ==")
for y in range(100, 125):
    xs = np.where(green[y, 700:900])[0]
    print(f" y{y}: x{xs.max()+700 if len(xs) else None}")

print("\n== BLUE top corners (leftmost/rightmost blue x per y 224..245) ==")
for y in range(224, 246):
    xl = np.where(blue[y, 60:300])[0]; xr = np.where(blue[y, 700:899])[0]
    print(f" y{y}: L x{xl.min()+60 if len(xl) else None}  R x{xr.max()+700 if len(xr) else None}")

print("\n== SOL top corners (leftmost/rightmost yellow x per y 430..455) ==")
for y in range(430, 456):
    xl = np.where(yellow[y, 60:300])[0]; xr = np.where(yellow[y, 700:899])[0]
    print(f" y{y}: L x{xl.min()+60 if len(xl) else None}  R x{xr.max()+700 if len(xr) else None}")
