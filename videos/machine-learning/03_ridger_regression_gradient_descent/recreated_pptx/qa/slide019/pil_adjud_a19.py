#!/usr/bin/env python3
"""PIL adjudication of attempt-19 judge findings, frame space (960x540).
render_19.png (2001x1125, 150dpi) vs unique_slides/slide_019.jpg.
Targets: A-leg #1/#2/#3 (arrow/x2/border), #4 (parens), #5 (stray red
vertical x~1503 render), #7 (outlier colors), #10 (top stroke);
table_left #1/#2/#3 (arrow+paren+band).
"""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_19.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"

ri = Image.open(R).convert("RGB")
oi = Image.open(O).convert("RGB")
ra = np.asarray(ri).astype(int)
oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0

def crop_frame(a, x0, y0, x1, y1, scale):
    return a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]

def blue_mask(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (b > 120) & (b - r > 50) & (b - g > 40)

def dark_mask(c):
    return c.sum(axis=2) < 260

def red_mask(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return (r > 110) & (r - g > 55) & (r - b > 55)

def bbox(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (xs.min(), ys.min(), xs.max(), ys.max(), len(xs))

# blocks: (col_x0, gy) — col x0: 124/384/644; gy: 205/310/420
COLS = [124, 384, 644]
GYS = [205, 310, 420]

print("=== 1. ARROW ink vs TABLE LEFT BORDER (9 blocks) ===")
for cx in COLS:
    for gy in GYS:
        # search window: gutter+label zone frame x cx+70..cx+120, y gy+30..gy+65
        for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
            c = crop_frame(a, cx + 70, gy + 28, cx + 125, gy + 68, s)
            bm = blue_mask(c)
            bb = bbox(bm)
            if bb:
                print(f"  col{cx} gy{gy} {nm}: blue ink x {cx+70+bb[0]/s:.1f}..{cx+70+bb[2]/s:.1f}"
                      f" y {gy+28+bb[1]/s:.1f}..{gy+28+bb[3]/s:.1f} n={bb[4]}")
            else:
                print(f"  col{cx} gy{gy} {nm}: NO blue ink")

print("=== 2. TABLE LEFT BORDER x (leftmost long vertical dark run) ===")
for cx in COLS:
    for gy in GYS[:1]:
        for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
            c = crop_frame(a, cx + 75, gy + 5, cx + 130, gy + 90, s)
            dm = dark_mask(c)
            colsum = dm.sum(axis=0)
            thresh = (90 * s) * 0.5
            cands = np.nonzero(colsum > thresh)[0]
            if len(cands):
                print(f"  col{cx} {nm}: vertical candidates x "
                      f"{[round(cx+75+v/s,1) for v in cands[:8]]}")

print("=== 3. W RIGHT-PAREN ink right edge vs border (row gy=205) ===")
for cx in COLS:
    for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
        c = crop_frame(a, cx + 55, 207, cx + 90, 268, s)
        dm = dark_mask(c)
        colsum = dm.sum(axis=0)
        nz = np.nonzero(colsum)[0]
        if len(nz):
            print(f"  col{cx} {nm}: dark ink cols {cx+55+nz.min()/s:.1f}..{cx+55+nz.max()/s:.1f}"
                  f"  profile n/col {[int(colsum[v]/s) for v in nz[::max(1,len(nz)//12)]]}")

print("=== 4. STRAY RED VERTICAL scan frame x690..760 y190..530 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = crop_frame(a, 690, 190, 760, 530, s)
    rm = red_mask(c)
    colsum = rm.sum(axis=0)
    top = colsum.argsort()[::-1][:6]
    print(f"  {nm}: top red cols " + str([(round(690+v/s,1), int(colsum[v]/s)) for v in sorted(top)]))

print("=== 5. OUTLIER DIGIT COLORS (rows at y203..218 / y426..441) ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    for lbl, (x0, x1, y0, y1) in (("row1(11/3/22)", (78, 120, 203, 220)),
                                  ("row3(60/3/22)", (78, 120, 426, 443))):
        c = crop_frame(a, x0, y0, x1, y1, s)
        # classify dark-ish ink pixels: blue vs red vs black
        r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
        ink = c.sum(axis=2) < 420
        blu = ink & (b_ - r_ > 40)
        red = ink & (r_ - b_ > 40) & (r_ - g_ > 40)
        blk = ink & ~blu & ~red
        print(f"  {nm} {lbl}: blue={int(blu.sum()/s/s)} red={int(red.sum()/s/s)} black={int(blk.sum()/s/s)}")

print("=== 6. TOP STROKE scan y88..100 x60..900 ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = crop_frame(a, 60, 88, 900, 100, s)
    rm = red_mask(c)
    rowsum = rm.sum(axis=1)
    print(f"  {nm}: red rows " + str([(round(88+v/s,1), int(rowsum[v]/s)) for v in np.nonzero(rowsum > 50 * s)[0]]))

print("=== 7. YELLOW BAND vs NORM TEXT (NO REG gy=205: norm y~262..280) ===")
for nm, a, s in (("R", ra, RS), ("O", oa, 1.0)):
    c = crop_frame(a, 126, 255, 210, 305, s)
    r_, g_, b_ = c[..., 0], c[..., 1], c[..., 2]
    yel = (r_ > 200) & (g_ > 180) & (b_ < 140)
    dm = dark_mask(c)
    yrows = np.nonzero(yel.sum(axis=1) > 10 * s)[0]
    drows = np.nonzero(dm.sum(axis=1) > 2 * s)[0]
    print(f"  {nm}: yellow rows y {[round(255+v/s,1) for v in (yrows[:3].tolist()+yrows[-3:].tolist())]}"
          f" | dark(text) rows y {[round(255+v/s,1) for v in (drows[:3].tolist()+drows[-3:].tolist())]}")
