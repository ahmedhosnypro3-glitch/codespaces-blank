#!/usr/bin/env python3
"""PIL-FIRST adjudication of the notes-crop MAJOR finding (crop_7_notes_judge.txt):

  "the underlined phrase after 'GD will' reads 'approximatly' in the ORIGINAL and
   'approximately' in the recreation (the recreation adds an 'e')" — MAJOR, high conf.

Identical predicates on BOTH images: column ink profile of the underlined word
(measured bar x177..277, N3 line, cap top 441 / baseline 454), glyph component count,
and total ink width. The original is 960x540 (1 frame px = 1 px); the render is 2001x1125
(scale SR = 2.0844) — all comparisons in frame px.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_7.png").convert("RGB")).astype(int)
SR = ren.shape[1] / 960.0

X0, X1, Y0, Y1 = 170, 285, 443, 456   # x-height band of the underlined word

def profile(im, sc):
    sub = im[int(round(Y0*sc)):int(round(Y1*sc)), int(round(X0*sc)):int(round(X1*sc))]
    lum = sub.sum(axis=2)
    ink = (lum < 500).sum(axis=0)
    return ink

def components(ink, sc, gapf=2.0, minw=1):
    g = max(1, int(round(gapf * sc)))
    xs = np.where(ink >= 1)[0]
    comps = []
    if len(xs):
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > g:
                comps.append((s, p)); s = x
            p = x
        comps.append((s, p))
    return [(int(round(X0 + a/sc)), int(round(X0 + b/sc)), b - a + 1) for a, b in comps if b - a + 1 >= minw]

for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ink = profile(im, sc)
    comps = components(ink, sc)
    print("=== %s: word window x%d..%d y%d..%d (x-height band) ===" % (tag, X0, X1, Y0, Y1))
    print("  ink columns present: x%d..x%d" % (X0 + int(np.argmax(ink > 0)), X0 + int(len(ink) - 1 - np.argmax(ink[::-1] > 0))))
    print("  glyph components (x-start..x-end, width px): %s" % comps)
    print("  component count: %d" % len(comps))
    print("  col profile: %s" % "".join("#" if v > 2 else ("+" if v > 0 else ".") for v in ink))
    print()

print("=== discriminating detail: the tail after 'approximat' ===")
for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ink = profile(im, sc)
    print("%s tail columns x230..280: %s" % (tag, "".join("#" if v > 2 else ("+" if v > 0 else ".") for v in ink[(230-X0):(280-X0)])))
