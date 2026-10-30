#!/usr/bin/env python3
"""Follow-up probes: (A) loose k11 TR asset vs render_12 TR region;
(B) BR near-black ink ASCII map (trajectory shape?); (C) BL tick-label
column profile left vs right + bottom; (D) TR left-edge dark ink ASCII."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ri = Image.open(BASE + "/recreated_pptx/qa/slide_025/render_12.png").convert("RGB")
ra = np.asarray(ri).astype(int)
RS = ra.shape[1] / 960.0

print("=== A. loose k11 asset vs render_12 TR (x616..879 y115..317) ===")
pa = Image.open(BASE + "/recreated_pptx/build/assets/plot_025_tr.png").convert("RGB")
tw, th = int(263 * RS), int(202 * RS)
pr = np.asarray(pa.resize((tw, th))).astype(int)
rb = ra[int(115*RS):int(115*RS)+th, int(616*RS):int(616*RS)+tw]
h = min(pr.shape[0], rb.shape[0]); w = min(pr.shape[1], rb.shape[1])
d = np.abs(pr[:h, :w] - rb[:h, :w]).sum(axis=2)
print(f"  mean|diff|={d.mean():.1f}  frac px >60: {(d > 60).mean():.4f}")

print("=== B. BR near-black ASCII map (render_12 x615..880 y344..531, 6px cells) ===")
c = ra[int(344*RS):int(531*RS), int(615*RS):int(880*RS)]
dm = (c.sum(axis=2) < 330)
cell = max(1, int(6 * RS))
H, W = dm.shape
for cy in range(0, H - cell + 1, cell):
    line = ""
    for cx in range(0, W - cell + 1, cell):
        n = dm[cy:cy+cell, cx:cx+cell].sum()
        line += "#" if n > cell*cell*0.25 else ("+" if n > cell*cell*0.08 else ".")
    print(f"{344 + cy/RS:5.0f} {line}")

print("=== C. BL dark tick-label ink: col profile strips ===")
def ink(a, s, x0, x1, y0, y1, t=460):
    c = a[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]
    return int((c.sum(axis=2) < t).sum()/s/s)
print(f"  R: left x84..112 n={ink(ra, RS, 84, 112, 300, 525)}  "
      f"right x350..376 n={ink(ra, RS, 350, 376, 300, 525)}  "
      f"bottom y508..527 x90..370 n={ink(ra, RS, 90, 370, 508, 527)}")
oa = np.asarray(Image.open(BASE + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
print(f"  O: left x84..112 n={ink(oa, 1.0, 84, 112, 300, 525)}  "
      f"right x350..376 n={ink(oa, 1.0, 350, 376, 300, 525)}  "
      f"bottom y508..527 x90..370 n={ink(oa, 1.0, 90, 370, 508, 527)}")

print("=== D. TR left-edge dark ASCII (x614..650 y120..320, render vs orig) ===")
oa_img = oa
for tag, a, s in (("R", ra, RS), ("O", oa_img, 1.0)):
    c = a[int(120*s):int(320*s), int(614*s):int(650*s)]
    dm = (c.sum(axis=2) < 480)
    cell = max(1, int(3 * s))
    H, W = dm.shape
    print(f"  -- {tag} --")
    for cy in range(0, H - cell + 1, cell):
        line = ""
        for cx in range(0, W - cell + 1, cell):
            n = dm[cy:cy+cell, cx:cx+cell].sum()
            line += "#" if n > cell*cell*0.3 else ("+" if n > cell*cell*0.1 else ".")
        print(f"  {120 + cy/s:5.0f} {line}")
