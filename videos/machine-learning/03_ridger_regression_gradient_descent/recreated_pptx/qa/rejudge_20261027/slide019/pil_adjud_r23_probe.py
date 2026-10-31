#!/usr/bin/env python3
"""r23 probe: D2 same-font cross-check + D4 W-cell delimiter edge strips."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
S = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide019"
rp = Image.open(f"{S}/render.png").convert("RGB")
op = Image.open(f"{NS}/unique_slides/slide_019.jpg").convert("RGB")
W, H = rp.size
sx, sy = W / 960.0, H / 540.0
R = np.asarray(rp).astype(int)
O = np.asarray(op).astype(int)

def rbox(x0, y0, x1, y1):
    return R[int(y0*sy):int(y1*sy), int(x0*sx):int(x1*sx)]

def obox(x0, y0, x1, y1):
    return O[int(y0):int(y1), int(x0):int(x1)]

def ink(a):
    return a.sum(axis=2) < 600

def dark(a):
    return a.sum(axis=2) < 330

def diffpx(a, b):
    if a.shape != b.shape:
        b = np.asarray(Image.fromarray(b.astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)).astype(int)
    return int((np.abs(a - b).sum(axis=2) > 90).sum())

COLX = [124, 384, 644]
gys = [205, 310, 420]

print("## D2 probe — same-font cross-check (render col2 vs render col1; orig col2 vs orig col1)")
print("   if r16's misread were real (render col2 holds col1's digits), render-vs-render")
print("   diff would collapse toward 0 while orig-vs-orig stays large.")
for gi in range(3):
    def dcell(img, is_r, ci):
        x0 = COLX[ci] + 46; gy = gys[gi]
        return rbox(x0, gy, x0 + 26, gy + 64) if is_r else obox(x0, gy, x0 + 26, gy + 64)
    rr = diffpx(dcell(R, True, 2), dcell(R, True, 1))
    oo = diffpx(dcell(O, False, 2), dcell(O, False, 1))
    # and self-consistency: render col2 vs orig col2 (style diff) vs render col1 vs orig col1
    rc2o2 = diffpx(dcell(R, True, 2), dcell(O, False, 2))
    rc1o1 = diffpx(dcell(R, True, 1), dcell(O, False, 1))
    print(f"  row{gi}: diff(renderC2,renderC1)={rr}  diff(origC2,origC1)={oo}  "
          f"diff(renderC2,origC2)={rc2o2}  diff(renderC1,origC1)={rc1o1}")

print("\n## D4 probe — W-cell delimiter edge strips (inside red border), dark-ink census")
for ci in range(3):
    for gi in range(3):
        x0 = COLX[ci]; gy = gys[gi]
        ra = rbox(x0 + 5, gy - 5, x0 + 82, gy + 92)
        oa = obox(x0 + 5, gy - 5, x0 + 82, gy + 92)
        # render strips: left x+1..x+9, right x+68..x+76 (relative to box), full height minus border
        h, w = ra.shape[:2]
        ls = ra[4:h-4, 2:20]; rs = ra[4:h-4, w-20:w-2]
        dark_ls = int(dark(ls).sum()); dark_rs = int(dark(rs).sum())
        # orig same strips scaled
        oh, ow = oa.shape[:2]
        ols = oa[2:oh-2, 1:10]; ors = oa[2:oh-2, ow-10:ow-1]
        odark = int(dark(ols).sum()) + int(dark(ors).sum())
        print(f"  col{ci} row{gi}: render dark px in L/R delimiter strips = {dark_ls}/{dark_rs} "
              f"(0 = no bowed paren strokes) | orig dark px in strips = {odark}")
