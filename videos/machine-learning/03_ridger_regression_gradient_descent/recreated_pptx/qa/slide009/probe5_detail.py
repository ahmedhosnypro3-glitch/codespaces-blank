#!/usr/bin/env python3
"""Probe 5: annotation boxes, chart panel rects, axes, labels, captions."""
import numpy as np
from PIL import Image
from collections import Counter

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(idx, gap=1):
    idx = [int(v) for v in idx]
    if not idx:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v <= p + gap:
            p = v
            continue
        out.append((s, p))
        s = p = v
    out.append((s, p))
    return out

# ---------- A. chart-panel white rects (fill = white OR pale blue) ----------
print("=== CHART PANEL rectangles ===")
fill = ((r > 240) & (g > 238) & (b > 240) & ((b - r) > -12)) | \
       ((r > 250) & (g > 250) & (b > 250))
# column profile in the body rows
for nm, c0, c1 in (("LEFT", 60, 470), ("RIGHT", 480, 910)):
    # find columns whose body is >70% fill
    body = fill[130:465, c0:c1]
    cf = body.mean(axis=0)
    good = np.where(cf > 0.7)[0] + c0
    print(f"  {nm} body-fill cols: {runs(good, gap=3)}")
    # rows
    sub = fill[100:480, :]
    rf = sub[:, c0:c1].mean(axis=1)
    print(f"  {nm} fill rows(>0.5): {runs(np.where(rf>0.5)[0]+100, gap=3)}")
    # exact rect using strict white
    sw = (r > 252) & (g > 252) & (b > 252)
    ys, xs = np.where(sw[100:480, c0:c1])
    print(f"  {nm} strict-white bbox x {xs.min()+c0}..{xs.max()+c0} "
          f"y {ys.min()+100}..{ys.max()+100}")

print("\n=== per-column fill fraction sample (every 8 px, rows 130..465) ===")
for x in range(50, 910, 8):
    col = fill[130:465, x]
    print(f"  x={x:4d} fillfrac={col.mean():.2f}  "
          f"{'#'*int(col.mean()*40)}")

# ---------- B. pale-blue annotation boxes ----------
print("\n=== PALE-BLUE ANNOTATION BOX (strict: b-r>=6, b>=235, not white) ===")
pb = (b - r >= 5) & (b >= 232) & (r < 252)
print("  total:", int(pb.sum()))
for nm, c0, c1 in (("LEFT", 60, 470), ("RIGHT", 480, 910)):
    m = pb[:, c0:c1]
    if not m.any():
        print(f"  {nm}: none")
        continue
    ys, xs = np.where(m)
    print(f"  {nm}: raw bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()}..{ys.max()} n={int(m.sum())}")
    rh = m.sum(axis=1)
    print(f"    rows>15: {runs(np.where(rh>15)[0])}")
    for (b0, b1) in runs(np.where(rh > 15)[0]):
        ch = m[b0:b1+1].sum(axis=0)
        print(f"      band y{b0}..{b1}: cols>2 {runs(np.where(ch>2)[0]+c0)}")
        sub_colors = a[b0:b1 + 1, c0:c1][m[b0:b1 + 1, c0:c1]]
        print(f"        colors: {Counter(map(tuple, sub_colors)).most_common(6)}")

# ---------- C. red axes detail ----------
print("\n=== RED AXES detail ===")
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
for nm, ax in (("LEFT", 126), ("RIGHT", 540)):
    col = np.where(red[:, ax])[0]
    print(f"  {nm} y-axis at x={ax}: y {col.min()}..{col.max()} n={len(col)}")
    print(f"    row runs: {runs(col)}")
for nm, x0, x1 in (("LEFT", 120, 450), ("RIGHT", 530, 860)):
    row = np.where(red[434, x0:x1])[0]
    print(f"  {nm} x-axis at y=434: x {row.min()+x0}..{row.max()+x0} n={len(row)}")
    print(f"    col runs: {runs(row+x0)}")
# check for arrowheads at axis ends
print("  LEFT y-axis top rows 144..155 red cols:")
for y in range(142, 158):
    xs = np.where(red[y, 110:150])[0]
    if len(xs):
        print(f"    y={y}: x {xs.min()+110}..{xs.max()+110} n={len(xs)}")
print("  LEFT x-axis right end cols 420..445:")
for x in range(420, 448):
    ys = np.where(red[:, x])[0]
    ys = [v for v in ys if 425 <= v <= 445]
    if ys:
        print(f"    x={x}: y {min(ys)}..{max(ys)} n={len(ys)}")
print("  RIGHT y-axis top rows 142..158 red cols (x 520..560):")
for y in range(142, 158):
    xs = np.where(red[y, 520:565])[0]
    if len(xs):
        print(f"    y={y}: x {xs.min()+520}..{xs.max()+520} n={len(xs)}")
print("  RIGHT x-axis right end cols 830..860:")
for x in range(830, 865):
    ys = [v for v in np.where(red[:, x])[0] if 425 <= v <= 445]
    if ys:
        print(f"    x={x}: y {min(ys)}..{max(ys)} n={len(ys)}")

# ---------- D. the 'mm' labels (dark text near axis) ----------
print("\n=== DARK text regions (all, clustered) ===")
from scipy import ndimage
dark = (r < 95) & (g < 95) & (b < 95)
# group dark px into row-bands then col-runs
dr = dark.sum(axis=1)
bands = runs(np.where(dr > 2)[0], gap=4)
for (b0, b1) in bands:
    m = dark[b0:b1+1]
    ch = m.sum(axis=0)
    print(f"  band y {b0}..{b1} (h={b1-b0+1}) n={int(m.sum())}: "
          f"col runs {runs(np.where(ch>0)[0], gap=6)}")

# ---------- E. red outlier point (left panel) ----------
print("\n=== RED outlier (solid red blob >=100px inside panels) ===")
lab_r, n = ndimage.label(red, structure=np.ones((3, 3)))
sizes = ndimage.sum(red, lab_r, range(1, n+1))
objs = ndimage.find_objects(lab_r)
for i, (sl, sz) in enumerate(zip(objs, sizes), 1):
    if sz >= 150:
        print(f"  comp{i}: x {sl[1].start}..{sl[1].stop-1} y {sl[0].start}..{sl[0].stop-1} "
              f"n={int(sz)} w={sl[1].stop-sl[1].start} h={sl[0].stop-sl[0].start}")

# ---------- F. blue fitted line endpoints ----------
print("\n=== BLUE line endpoints (first/last column with blue in body) ===")
blue = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
for nm, c0, c1 in (("LEFT", 60, 460), ("RIGHT", 480, 900)):
    columns = []
    for x in range(c0, c1):
        ys = np.where(blue[195:432, x])[0]
        if len(ys):
            grp, s, p = [], ys[0], ys[0]
            for v in ys[1:]:
                if v <= p + 2:
                    p = v
                    continue
                grp.append((s, p))
                s = p = v
            grp.append((s, p))
            grp.sort(key=lambda t: t[1]-t[0], reverse=True)
            s0, s1 = grp[0]
            columns.append((x, (s0+195+s1+195)/2, s0+195, s1+195))
    if columns:
        print(f"  {nm}: blue x-range {columns[0][0]}..{columns[-1][0]}")
        print(f"    first: x={columns[0][0]} mid={columns[0][1]:.1f}")
        print(f"    last : x={columns[-1][0]} mid={columns[-1][1]:.1f}")
        xs = np.array([c[0] for c in columns], float)
        ys = np.array([c[1] for c in columns], float)
        A = np.vstack([xs, np.ones_like(xs)]).T
        m_, c_ = np.linalg.lstsq(A, ys, rcond=None)[0]
        resid = ys - (m_*xs + c_)
        print(f"    LSQ y = {m_:.5f}x + {c_:.2f}; max|r|={np.abs(resid).max():.2f} rms={resid.std():.2f}")
        # endpoints of fit
        print(f"    at x={columns[0][0]}: y={m_*columns[0][0]+c_:.1f}; "
              f"at x={columns[-1][0]}: y={m_*columns[-1][0]+c_:.1f}")
        # 5px endpoints
        print(f"    endpoints (ink): x{columns[0][0]} y{columns[0][2]}..{columns[0][3]}, "
              f"x{columns[-1][0]} y{columns[-1][2]}..{columns[-1][3]}")
