#!/usr/bin/env python3
"""Pink-box border adjudication v2 — constrain to the pink-box neighborhood."""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide050"

o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")).astype(int)
r = Image.open(QA + "/render_13.png").convert("RGB")
SC = r.size[1] / 540.0
r = np.asarray(r).astype(int)

def find_pink(img, x0, y0, x1, y1):
    sub = img[y0:y1, x0:x1]
    m = (sub[:,:,0] > 200) & (sub[:,:,1] > 120) & (sub[:,:,1] < 215) & (sub[:,:,2] > 130) & (sub[:,:,2] < 220)
    ys, xs = np.where(m)
    return x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max(), int(m.sum())

ob = find_pink(o, 720, 40, 850, 200)
print("ORIG pink box bbox: x%d..%d y%d..%d n=%d" % ob)
rb = find_pink(r, int(720*SC), int(40*SC), int(850*SC), int(200*SC))
print("RENDER13 pink box bbox: %s (frame %s) n=%d" % (rb[:4], tuple(round(v/SC) for v in rb[:4]), rb[4]))

def profiles(img, bx, tag):
    bx0, by0, bx1, by1 = bx
    midx = slice(bx0+30, bx1-30)
    midy = slice(by0+ (by1-by0)//2 - 20, by0 + (by1-by0)//2 + 20)
    print("\n%s edge profiles (mean RGB):" % tag)
    print("  TOP rows:")
    for yy in range(by0-3, by0+6):
        print("    y%-4d %s" % (yy, img[yy, midx].mean(axis=0).round(0)))
    print("  BOTTOM rows:")
    for yy in range(by1-5, by1+3):
        print("    y%-4d %s" % (yy, img[yy, midx].mean(axis=0).round(0)))
    print("  LEFT cols:")
    for xx in range(bx0-3, bx0+6):
        print("    x%-4d %s" % (xx, img[midy, xx].mean(axis=0).round(0)))
    print("  RIGHT cols:")
    for xx in range(bx1-5, bx1+3):
        print("    x%-4d %s" % (xx, img[midy, xx].mean(axis=0).round(0)))

profiles(o, ob, "ORIG")
profiles(r, rb, "RENDER13")
