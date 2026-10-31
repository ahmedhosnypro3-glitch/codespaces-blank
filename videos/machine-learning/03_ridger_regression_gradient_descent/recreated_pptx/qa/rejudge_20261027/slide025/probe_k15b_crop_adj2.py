#!/usr/bin/env python3
"""Round-2 targeted probes for the k15b crop FAIL claims (slide025)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide025"
SC = 2001 / 960.0
OX, OY = 592, 160
R = np.asarray(Image.open(f"{D}/crop_dense_render.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(f"{D}/crop_dense_orig.png").convert("RGB")).astype(int)
H, W = R.shape[:2]

def masks(A):
    r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    mx = A.max(axis=2); mn = A.min(axis=2); sat = mx - mn
    dark = A.sum(axis=2) < 330
    white = (r > 240) & (g > 240) & (b > 240)
    gray = (sat < 24) & (mx > 120) & (mx < 235)
    red = (r > 120) & (g < 110) & (b < 110) & (sat > 60)
    navy = (b > 90) & (b > r + 40) & (g < 120) & (r < 120)
    colored = (sat > 45) & ~red & ~dark & ~navy
    return dict(dark=dark, white=white, gray=gray, red=red, colored=colored, navy=navy)

MR, MO = masks(R), masks(O)

print("=== Q1: upper-left numeral region (crop x0-150 y0-83 = slide x592-664 y160-200) ===")
sub_r = MR["dark"][0:83, 0:150]; sub_o = MO["dark"][0:83, 0:150]
diff = (sub_r ^ sub_o).sum()
print(f"dark-ink px render={int(sub_r.sum())} orig={int(sub_o.sum())} differing={int(diff)} of {sub_r.size}")
# row profile of dark ink in that box, both
for nm, s in (("render", sub_r), ("orig", sub_o)):
    rows = s.sum(axis=1)
    bands = []
    st = None
    for i, v in enumerate(rows):
        if v > 2 and st is None: st = i
        elif v <= 2 and st is not None:
            if i - st >= 2: bands.append((st, i))
            st = None
    print(f"  {nm} text bands y: {bands}")

print("\n=== Q2: dark-ink row profile over whole crop (where are labels/lines?) ===")
for nm, M in (("render", MR), ("orig", MO)):
    rows = M["dark"].sum(axis=1)
    bands = []
    st = None
    for i, v in enumerate(rows):
        if v > 8 and st is None: st = i
        elif v <= 8 and st is not None:
            if i - st >= 3: bands.append((st, i, int(rows[st:i].sum())))
            st = None
    print(f"  {nm} dark bands (y0,y1,px): {bands}")

print("\n=== Q3: bottom band y300-434 dark ink by 20px rows ===")
for nm, M in (("render", MR), ("orig", MO)):
    out = []
    for y0 in range(300, H, 20):
        out.append(f"y{y0}-{min(H,y0+20)}:{int(M['dark'][y0:min(H,y0+20), :].sum())}")
    print(f"  {nm}: " + " ".join(out))

print("\n=== Q4: red horizontal lines (rows with >80 red px) ===")
for nm, M in (("render", MR), ("orig", MO)):
    rows = M["red"].sum(axis=1)
    hl = [(i, int(v)) for i, v in enumerate(rows) if v > 80]
    print(f"  {nm}: rows>80redpx: {hl}")

print("\n=== Q5: diagonal red in upper-left (crop x0-260 y0-220) ===")
for nm, M in (("render", MR), ("orig", MO)):
    red = M["red"][0:220, 0:260]
    ys, xs = np.where(red)
    print(f"  {nm}: red px in UL box = {len(xs)}", end="")
    if len(xs) > 30:
        A = np.polyfit(xs, ys, 1)
        pred = np.polyval(A, xs)
        r2 = 1 - ((ys - pred) ** 2).sum() / ((ys - ys.mean()) ** 2).sum()
        print(f"  fit y={A[0]:.3f}x+{A[1]:.1f} R2={r2:.3f} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
    else:
        print()

print("\n=== Q6: surface shape — colored px per row in interior x50-598 ===")
for nm, M in (("render", MR), ("orig", MO)):
    col = M["colored"][:, 50:598]
    rows = col.sum(axis=1)
    prof = [(i, int(v)) for i, v in enumerate(rows) if v > 20]
    # summarize: first/last row with surface, width profile quartiles
    if prof:
        print(f"  {nm}: surface rows y{prof[0][0]}-{prof[-1][0]}, widths: min={min(v for _,v in prof)} "
              f"q1={int(np.percentile([v for _,v in prof],25))} med={int(np.median([v for _,v in prof]))} "
              f"q3={int(np.percentile([v for _,v in prof],75))} max={max(v for _,v in prof)}")
    # column profile too
    cols = col.sum(axis=0)
    cprof = [(i, int(v)) for i, v in enumerate(cols) if v > 20]
    if cprof:
        print(f"        surface cols x{50+cprof[0][0]}-{50+cprof[-1][0]}")

print("\n=== Q7: navy label-box ink (left strip x0-50 and elsewhere) ===")
for nm, M in (("render", MR), ("orig", MO)):
    print(f"  {nm}: navy px whole crop={int(M['navy'].sum())} left strip x0-50={int(M['navy'][:, 0:50].sum())}")

print("\n=== Q8: per-row colored% profile difference (3D vs flat) rows 0..327 step 30 ===")
for nm, M in (("render", MR), ("orig", MO)):
    col = M["colored"][0:328, 50:598]
    prof = [f"{100.0*col[y:y+30].sum()/col[y:y+30].size:.0f}" for y in range(0, 328, 30)]
    print(f"  {nm}: row-band colored% = {prof}")

print("\n=== Q9: luminance column profile of colored surface (shading left->right) ===")
for nm, A, M in (("render", R, MR), ("orig", O, MO)):
    col = M["colored"][0:328, 50:598]
    lum = (0.299*A[:,:,0]+0.587*A[:,:,1]+0.114*A[:,:,2])[0:328, 50:598]
    out = []
    for x0 in range(0, col.shape[1], 55):
        m = col[:, x0:x0+55]
        v = lum[:, x0:x0+55][m]
        out.append(f"{np.mean(v) if v.size else float('nan'):.0f}")
    print(f"  {nm}: col-band lum = {out}")
