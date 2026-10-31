#!/usr/bin/env python3
"""W5 PIL-first probe for slide012 FULL FAIL (judge_full.txt 01:10).
Claims: #1 title too small/not centered; #2 label 'X5 is Outlier' vs orig 'X8'.
Read-only. Slide space 960x540; render 2001x1125 scale 2.0844."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide012"
r = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_012.jpg").convert("RGB")).astype(int)
sc = r.shape[1] / 960.0
print(f"render {r.shape[1]}x{r.shape[0]} scale {sc:.4f}")

def to_slide_box(a, x0, y0, x1, y1):
    s = a.shape[1] / 960.0
    return a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]

def ink_bbox(a, thr=600):
    ink = a.sum(axis=2) < thr
    ys, xs = np.where(ink)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max(), ys.max(), int(ink.sum())

# title band y62-95 slide px, x60-900
for name, a in (("orig", o), ("render", r)):
    bb = ink_bbox(to_slide_box(a, 60, 60, 900, 96))
    if bb:
        x0, y0, x1, y1, n = bb
        s = a.shape[1] / 960.0
        print(f"{name} title ink bbox slide-px: x{x0/s:.1f}-{x1/s:.1f} y{y0/s:.1f}-{y1/s:.1f} h={(y1-y0)/s:.1f} ink={n} center={(x0+x1)/2/s:.1f}")

# outlier label boxes: build draws at (69,323,128,27) and (69,445,128,27) red text
for name, a in (("orig", o), ("render", r)):
    for (bx, by) in ((69, 323), (69, 445)):
        sub = to_slide_box(a, bx - 4, by - 4, bx + 140, by + 32)
        ink = sub.sum(axis=2) < 600
        # red-ish ink
        red = (sub[:, :, 0] > 120) & (sub[:, :, 0] > sub[:, :, 2] + 40) & (sub[:, :, 0] > sub[:, :, 1] + 40)
        ys, xs = np.where(red)
        if len(xs):
            s = a.shape[1] / 960.0
            print(f"{name} label@({bx},{by}) red-ink bbox slide-px: x{bx-4+xs.min()/s:.1f}-{bx-4+xs.max()/s:.1f} y{by-4+ys.min()/s:.1f}-{by-4+ys.max()/s:.1f} redpx={int(red.sum())}")
        # glyph height of the digit after X: crop x range of label, find columns
        ys2, xs2 = np.where(ink)
        if len(xs2):
            s = a.shape[1] / 960.0
            print(f"   all-ink bbox: x{bx-4+xs2.min()/s:.1f}-{bx-4+xs2.max()/s:.1f} y{by-4+ys2.min()/s:.1f}-{by-4+ys2.max()/s:.1f} h={(ys2.max()-ys2.min())/s:.1f}")

# digit shape discrimination: render label1 digit zone vs orig; compare the
# digit glyph (after 'X') pixel mask xor against templates is overkill; instead
# measure per-column ink profile of the label text in both images and print
for name, a in (("orig", o), ("render", r)):
    sub = to_slide_box(a, 69, 323, 200, 350)
    ink = sub.sum(axis=2) < 600
    cols = ink.sum(axis=0)
    prof = "".join("#" if c > 0 else "." for c in cols)
    print(f"{name} label1 col-profile (slide x69-200): {prof}")
