#!/usr/bin/env python3
"""Focused orig-truth pass: table border, label colors, band extent,
paren ink, divider extents. render_19 vs slide_019, frame space."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_19.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
ri = Image.open(R).convert("RGB"); oi = Image.open(O).convert("RGB")
ra = np.asarray(ri).astype(int); oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0

def cf(a, x0, y0, x1, y1, s):
    return a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]

def inkish(c, t=420):
    return c.sum(axis=2) < t

def redm(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (r > 110) & (r - g > 55) & (r - b > 55)

def bluem(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (b > 120) & (b - r > 50) & (b - g > 40)

COLS = [124, 384, 644]
GYS = [205, 310, 420]

print("=== A. ORIG table-left border: tall ink cols (soft t=520), x cx+90..cx+150 ===")
for cx in COLS:
    c = cf(oa, cx + 90, 208, cx + 150, 292, 1.0)
    m = inkish(c, 520)
    colsum = m.sum(axis=0)
    cands = np.nonzero(colsum > 40)[0]
    print(f"  col{cx}: tall cols " + str([(round(cx+90+v,1), int(colsum[v])) for v in cands]))

print("=== B. ORIG x1/x2 label ink color + x-extent (cx+112..cx+165) ===")
for cx in COLS[:1]:
    for gy in GYS:
        for nm, yy in (("x1row", gy + 23), ("x2row", gy + 45)):
            c = cf(oa, cx + 110, yy, cx + 165, yy + 16, 1.0)
            r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
            ink = c.sum(axis=2) < 480
            blu = ink & (b_ - r_ > 40); red = ink & (r_ - b_ > 40) & (r_ - g_ > 40)
            blk = ink & ~blu & ~red
            xs = np.nonzero(ink.sum(axis=0))[0]
            ext = (cx + 110 + xs.min(), cx + 110 + xs.max()) if len(xs) else None
            print(f"  col{cx} gy{gy} {nm}: blue={int(blu.sum())} red={int(red.sum())} blk={int(blk.sum())} xext={ext}")

print("=== C. divider vlines y-extent+color: orig x205/466/724, render x205.5/466/724 ===")
for nm, a, s, xs in (("O", oa, 1.0, (203, 207)), ("R", ra, RS, (204, 209))):
    for xc, lbl in ((205.5, "NOREG"), (466, "R3"), (724, "R10")):
        x0i, x1i = int(xs[0] * s) if lbl != "R3" else int((xc - 3) * s), None
        c = cf(a, xc - 3, 195, xc + 5, 535, s)
        rm = redm(c); colsum = rm.sum(axis=0)
        best = colsum.argmax()
        rows = np.nonzero(rm[:, best])[0]
        ext = (195 + rows.min() / s, 195 + rows.max() / s, int(colsum[best] / s)) if len(rows) else None
        print(f"  {nm} {lbl}@x{xc}: red col x={xc-3+best/s:.1f} yext={ext}")

print("=== D. band A yellow x-extent (y272..303) ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = cf(a, 100, 272, 900, 303, s)
    r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
    yel = (r_ > 200) & (g_ > 180) & (b_ < 150)
    colsum = yel.sum(axis=0)
    nz = np.nonzero(colsum > 5 * s)[0]
    if len(nz):
        print(f"  {nm}: yellow cols x {100+nz.min()/s:.1f}..{100+nz.max()/s:.1f} (n cols={len(nz)})")
    else:
        print(f"  {nm}: NO yellow band found")

print("=== E. orig norm-text bbox (W area, gy205: y262..290, x130..210) ===")
c = cf(oa, 126, 258, 214, 292, 1.0)
m = inkish(c, 480)
ys, xs2 = np.nonzero(m)
if len(xs2):
    print(f"  O: ink x {126+xs2.min()}..{126+xs2.max()} y {258+ys.min()}..{258+ys.max()} n={len(xs2)}")
c = cf(ra, 126, 258, 214, 292, RS)
m = inkish(c, 480)
ys, xs2 = np.nonzero(m)
if len(xs2):
    print(f"  R: ink x {126+xs2.min()/RS:.1f}..{126+xs2.max()/RS:.1f} y {258+ys.min()/RS:.1f}..{258+ys.max()/RS:.1f} n={len(xs2)}")

print("=== F. orig W right-paren ink (soft t=520, x179..205, gy205) ===")
c = cf(oa, 179, 207, 205, 268, 1.0)
m = inkish(c, 520)
colsum = m.sum(axis=0)
nz = np.nonzero(colsum > 2)[0]
print("  O: ink cols " + str([(179 + v, int(colsum[v])) for v in nz[::max(1, len(nz)//10)]]))

print("=== G. render arrow bbox (pure: window right of paren, left of border) col124 gy205 ===")
c = cf(ra, 196, 225, 235, 275, RS)
bm = bluem(c)
ys, xs2 = np.nonzero(bm)
if len(xs2):
    print(f"  R arrow-only: x {196+xs2.min()/RS:.1f}..{196+xs2.max()/RS:.1f} y {225+ys.min()/RS:.1f}..{225+ys.max()/RS:.1f} n={len(xs2)}")
c = cf(oa, 196, 225, 236, 275, 1.0)
bm = bluem(c)
ys, xs2 = np.nonzero(bm)
if len(xs2):
    print(f"  O arrow-only: x {196+xs2.min()}..{196+xs2.max()} y {225+ys.min()}..{225+ys.max()} n={len(xs2)}")
