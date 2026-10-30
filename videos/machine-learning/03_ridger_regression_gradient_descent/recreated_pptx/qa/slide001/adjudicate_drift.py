#!/usr/bin/env python3
"""Independent w4 adjudication of the banked selfcheck_render v2 drift items (2026-10-20).

For every flagged band: re-measure render + original with SEVERAL masks, print
cap-height, ink width, left/right edges, center, so a drift can be classified as
( ) font-metric jitter (center preserved, width off by <=2%),
(*) a real placement defect, or
(a) a mask artifact (e.g. the red mask catching the logo's mauve JPEG background).
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gescent"
VID = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
R = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide001/render_1.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(f"{VID}/unique_slides/slide_001.jpg").convert("RGB")).astype(int)
S = R.shape[0] / 540.0
print(f"render {R.shape[1]}x{R.shape[0]} scale {S:.4f}\n")

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red_loose = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    red_core = (r > 120) & ((r - g) > 80) & ((r - b) > 60)
    blue_loose = (b > 120) & ((b - r) > 60) & ((b - g) > 60)
    blue_core = (b > 150) & ((b - r) > 90) & ((b - g) > 90)
    return dict(red_loose=red_loose, red_core=red_core, blue_loose=blue_loose, blue_core=blue_core)

MR, MO = masks(R), masks(O)

def band(mask, x0, x1, y0, y1, scale):
    x0i, x1i, y0i, y1i = int(x0*scale), int(x1*scale), int(y0*scale), int(y1*scale)
    sub = mask[y0i:y1i, x0i:x1i]
    rows = np.where(sub.sum(axis=1) > 2)[0]
    if not len(rows):
        return None
    a0, a1 = rows[0], rows[-1]
    cols = np.where(sub[a0:a1+1].sum(axis=0) > 0)[0]
    return (y0 + a0/scale, y0 + a1/scale, x0 + cols.min()/scale, x0 + cols.max()/scale)

# The flagged bands: (name, mask-key, window x0,x1,y0,y1 frame-px)
BANDS = [
    ("title L1 (red b0)",   "red_loose",  270, 690, 118, 175),
    ("title L2 (red b1)",   "red_loose",  270, 690, 174, 226),
    ("title L3 (red b2)",   "red_loose",  270, 690, 226, 290),
    ("Instructors (red b4)","red_loose",   70, 300, 414, 445),
    ("logo band y509 (red b6)","red_loose",585, 899, 499, 517),
    ("email ctr (blue b2)", "blue_loose", 340, 660, 400, 420),
    ("email1 (blue b4)",    "blue_loose",  70, 400, 468, 492),
    ("name2 (blue b5)",     "blue_loose",  70, 400, 490, 514),
    ("email2 (blue b6)",    "blue_loose",  70, 400, 512, 536),
]
print(f"{'band':24s} {'img':4s} {'y0':>6s} {'y1':>6s} {'x0':>6s} {'x1':>6s} {'w':>6s} {'ctr':>7s} {'h':>5s}")
for name, mk, x0, x1, y0, y1 in BANDS:
    for tag, masks_d, scale in (("orig", MO, 1.0), ("rend", MR, S)):
        b = band(masks_d[mk], x0, x1, y0, y1, scale)
        if b is None:
            print(f"{name:24s} {tag:4s}   EMPTY")
            continue
        print(f"{name:24s} {tag:4s} {b[0]:6.1f} {b[1]:6.1f} {b[2]:6.1f} {b[3]:6.1f} {b[3]-b[2]:6.1f} {(b[2]+b[3])/2:7.1f} {b[1]-b[0]:5.1f}")
    print()

# ---- logo deep-dive: compare embedded asset vs the same region of the original ----
print("=== LOGO REGION COMPARISON (x592..889 y456..533 frame-px) ===")
def crop(im, scale, box):
    x0, y0, x1, y1 = box
    return im[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
box = (592, 456, 889, 533)
cr = crop(R, S, box)   # render crop at 150dpi
co = crop(O, 1.0, box) # original crop 1:1
# upsample original crop to render pixel size for a diff
co_up = np.asarray(Image.fromarray(co.astype(np.uint8)).resize((cr.shape[1], cr.shape[0]), Image.LANCZOS)).astype(int)
d = np.abs(cr - co_up)
print(f"render crop {cr.shape[1]}x{cr.shape[0]}, original upscaled {co_up.shape[1]}x{co_up.shape[0]}")
n = int((d.max(axis=2) > 40).sum())
print(f"pixels differing >40: {n} of {d.shape[0]*d.shape[1]} ({100.0*n/(d.shape[0]*d.shape[1]):.3f}%)")
ys, xs = np.where(d.max(axis=2) > 40)
if n:
    print(f"strong-diff bbox (frame px, relative to x592 y456): x {592+xs.min()/S:.0f}..{592+xs.max()/S:.0f} y {456+ys.min()/S:.0f}..{456+ys.max()/S:.0f}")
# row-profile of strong diffs to localize
rowsum = (d.max(axis=2) > 40).sum(axis=1)
for yy in range(0, cr.shape[0], 10):
    print(f"  row {456+yy/S:6.1f} fp: strongdiff px={int(rowsum[yy:yy+10].sum())}")
# and the asset itself
print("\n=== ASSET vs ORIGINAL CROP (native px) ===")
A = np.asarray(Image.open(f"{VID}/recreated_pptx/build/assets/logo_slide001.png").convert("RGB")).astype(int)
print(f"asset {A.shape[1]}x{A.shape[0]}")
same = crop(O, 1.0, (592, 456, 592+A.shape[1], 456+A.shape[0]))
if same.shape == A.shape:
    da = np.abs(A - same)
    na = int((da.max(axis=2) > 8).sum())
    print(f"asset vs original same-box px differing >8: {na} of {A.shape[0]*A.shape[1]} ({100.0*na/(A.shape[0]*A.shape[1]):.3f}%)")
    if na:
        ys2, xs2 = np.where(da.max(axis=2) > 8)
        print(f"diff bbox in asset px: x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()}")
else:
    print(f"shape differs from same-box original crop {same.shape}")
