#!/usr/bin/env python3
"""Adjudication #3 (decisive) — word-level segmentation of the whole N3 line in BOTH
images, identical predicate (band y441..456 x104..860, gap 4.0 frame px = one word space).
The third word is the disputed "approximately". Its WIDTH is compared against the
Liberation/Arial advances for the two candidate spellings, calibrated against the render
(which draws "approximately" verbatim from the spec) and against the original's other
words, which are shared between the two images.
"""
import numpy as np
from glob import glob
from PIL import Image, ImageFont

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_7.png").convert("RGB")).astype(int)
SR = ren.shape[1] / 960.0
FP = glob("/usr/share/fonts/**/LiberationSans-Regular.ttf", recursive=True)[0]
F = ImageFont.truetype(FP, 175)   # 175px = 17.5pt * 10
def adv(s): return F.getlength(s) / 10.0

def words(im, sc, x0, x1, y0, y1, gapf=4.0, thr=500):
    sub = im[int(round(y0*sc)):int(round(y1*sc)), int(round(x0*sc)):int(round(x1*sc))]
    ink = (sub.sum(axis=2) < thr).sum(axis=0)
    xs = np.where(ink >= 1)[0]
    g = max(1, int(round(gapf*sc)))
    ws = []
    if len(xs):
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > g: ws.append((s, p)); s = x
            p = x
        ws.append((s, p))
    return [(int(round(x0+a/sc)), int(round(x0+b/sc))) for a, b in ws]

for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ws = words(im, sc, 104, 860, 441, 456)
    print("=== %s N3 line words (band y441..456, gap 4.0 frame px) ===" % tag)
    for i, (a, b) in enumerate(ws):
        print("   w%-2d x%3d..%3d  width %3d" % (i+1, a, b, b-a+1))
    print()

print("Liberation 17.5pt advances:")
for s in ("GD", "will", "approximately", "approximatly", "find", "this", "minimum", "value", "but", "at", "a"):
    print("   %-14s %6.1f" % (s, adv(s)))
print()
for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ws = words(im, sc, 104, 860, 441, 456)
    if len(ws) >= 3:
        a, b = ws[2]
        w = b-a+1
        print("%-5s word3 width %3d -> matches 'approximately' (adv %.1f, ink/adv %.3f) or 'approximatly' (adv %.1f, ratio %.3f)"
              % (tag, w, adv("approximately"), w/adv("approximately"), adv("approximatly"), w/adv("approximatly")))
