#!/usr/bin/env python3
"""Att5 legA adjudication — PIL measurement of the 7 claims on UNCHANGED bytes.
Render: qa/slide_015/render_4.png (2001x1125, S=2001/960=2.0844). Original: 960x540.
Claims settled by prior banked measurements are re-referenced, not re-litigated;
this script measures the claims that were never measured: 1, 2 (recolor half),
5, 6, 7 — plus re-bank censuses for 2 (floating rows), 3, 4."""
from PIL import Image
import numpy as np

R = np.asarray(Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/render_4.png').convert('RGB'), dtype=int)
O = np.asarray(Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg').convert('RGB'), dtype=int)
S = R.shape[0] / O.shape[0]
print(f"S={S:.4f}  render {R.shape} orig {O.shape}")

def lum(img): return img.mean(axis=2)

def rows_in(img, fx0, fx1, fy0, fy1, thr=150, minpx=2, scale=1.0):
    x0, x1, y0, y1 = int(fx0*scale), int(fx1*scale), int(fy0*scale), int(fy1*scale)
    band = img[y0:y1, x0:x1]
    ink = (lum(band) < thr).sum(axis=1)
    out, inb = [], False
    for i, v in enumerate(ink):
        if v >= minpx and not inb: s = i; inb = True
        elif v < minpx and inb: out.append((round((s+y0)/scale, 1), round((i+y0)/scale, 1))); inb = False
    if inb: out.append((round((s+y0)/scale, 1), round((len(ink)+y0)/scale, 1)))
    return out

def green_mask(img):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    return (g > 100) & (g - r > 40) & (g - b > 40)

def red_mask(img):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    return (r > 120) & (r - g > 60) & (r - b > 60)

# ---- CLAIM 2: green ink rows across the cream eq box (floating duplicates?) ----
# cream rect A interior: frame x~95..800, y~100..270
for name, img in (("ORIG", O), ("REND", R)):
    gm = green_mask(img)
    sub = gm[int(98*S if img is R else 98):int(272*S if img is R else 272), int(90*S if img is R else 90):int(800*S if img is R else 800)]
    rows = sub.sum(axis=1)
    bands, inb = [], False
    off = int(98*S) if img is R else 98
    for i, v in enumerate(rows):
        if v > 3 and not inb: s = i; inb = True
        elif v <= 3 and inb: bands.append((round((s+off)/S, 1), round((i+off)/S, 1), int(rows[s:i].sum()))); inb = False
    if inb: bands.append((round((s+off)/S, 1), round((len(rows)+off)/S, 1), int(rows[s:].sum())))
    print(f"[claim2] {name} green row-bands in cream box (frame y, greenpx): {bands}")

# ---- CLAIM 3: J(W) cluster census per line band (top panel) ----
for name, img in (("ORIG", O), ("REND", R)):
    for li, (fy0, fy1) in enumerate([(103, 160), (160, 213), (213, 268)], 1):
        rows = rows_in(img, 90, 800, fy0, fy1, thr=120, minpx=4)
        print(f"[claim3] {name} L{li} dark row-bands (x90..800): {rows}")

# ---- CLAIM 4: gap ink between final eq and green box (frame x501..547, y466..521) ----
for name, img in (("ORIG", O), ("REND", R)):
    sc = S if img is R else 1.0
    x0, x1, y0, y1 = int(503*sc), int(545*sc), int(468*sc), int(519*sc)
    gap = lum(img)[y0:y1, x0:x1]
    n = int((gap < 200).sum())
    print(f"[claim4] {name} gap ink px (luma<200): {n}")

# ---- CLAIM 5: green ink near the green result box + final eq (frame x500..900, y420..535) ----
for name, img in (("ORIG", O), ("REND", R)):
    sc = S if img is R else 1.0
    gm = green_mask(img)
    sub = gm[int(420*sc):int(535*sc), int(500*sc):int(900*sc)]
    ys, xs = np.nonzero(sub)
    if len(ys):
        print(f"[claim5] {name} green px in region: {len(ys)}, frame bbox x{(xs.min())/sc+S*0:.1f}..{xs.max()/sc:.1f} y{(ys.min()+int(420*sc))/sc:.1f}..{(ys.max()+int(420*sc))/sc:.1f}")
    else:
        print(f"[claim5] {name} green px in region: 0")
    # green px INSIDE the green box interior only (x547..891, y468..521)
    sub2 = gm[int(468*sc):int(521*sc), int(547*sc):int(891*sc)]
    print(f"[claim5] {name} green px inside green box interior: {int(sub2.sum())}")

# ---- CLAIM 6: 'Best W' W color in pink box (frame y268..325, x73..710) ----
for name, img in (("ORIG", O), ("REND", R)):
    sc = S if img is R else 1.0
    sub = img[int(288*sc):int(312*sc), int(80*sc):int(300*sc)]
    rm = red_mask(sub); lm = lum(sub) < 120
    print(f"[claim6] {name} pinkbox text band: red px={int(rm.sum())} dark px={int(lm.sum())}")
    # locate the word W: scan for red column clusters
    rcols = rm.sum(axis=0)
    cl, inb = [], False
    for i, v in enumerate(rcols):
        if v > 0 and not inb: s = i; inb = True
        elif v == 0 and inb: cl.append((round((s+80)/S if img is R else s+80, 1), round((i+80)/S if img is R else i+80, 1))); inb = False
    print(f"[claim6] {name} red column clusters x: {cl}")

# ---- CLAIM 7: solution formula centering in green box ----
for name, img in (("ORIG", O), ("REND", R)):
    sc = S if img is R else 1.0
    band = lum(img)[int(468*sc):int(521*sc), int(555*sc):int(885*sc)]
    ink_rows = (band < 150).sum(axis=1)
    ys = np.nonzero(ink_rows > 1)[0]
    if len(ys):
        top, bot = ys.min(), ys.max()
        box_h = (521-468)
        print(f"[claim7] {name} formula ink y (frame): {(468+top/S if img is R else 468+top):.1f}..{(468+bot/S if img is R else 468+bot):.1f}; margins top={(top/S if img is R else top):.1f}px bottom={((521-468)-bot/S if img is R else (521-468)-bot):.1f}px (box h {box_h})")
