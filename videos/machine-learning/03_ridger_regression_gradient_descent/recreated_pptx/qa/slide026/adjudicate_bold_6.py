#!/usr/bin/env python3
"""Adjudicate the 3 MINOR bold-weight findings from crop_6_alg_judge.txt
(PIL-first, judging.md): compare ink WEIGHT of the flagged words against
known-bold and known-regular controls in the SAME line, original vs render_6.

Weight metric: ink pixels per word / word width (per-column mean ink density).
A bold glyph carries ~1.4x the ink of its regular counterpart in Liberation.
Lines are measured in the TEXT band only (bar rows excluded) so the underline
does not merge adjacent words in the original's mask.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
SX, SY = ren.shape[1] / 960.0, ren.shape[0] / 540.0

def blue(im):
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (B - R > 40) & (B - G > 40)
mb, mo_ = blue(ren), blue(org)

def words(mask, y0, y1, x0, x1, gap=3, sx=1.0, sy=1.0):
    sub = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    colink = sub.any(axis=0)
    out, start, miss = [], None, 0
    for i, v in enumerate(colink):
        if v:
            if start is None:
                start = i
            miss = 0
        elif start is not None:
            miss += 1
            if miss >= gap:
                out.append((int(x0*sx)+start, int(x0*sx)+i-miss, int(sub[:, start:i-miss].sum())))
                start = None
    if start is not None:
        out.append((int(x0*sx)+start, int(x0*sx)+len(colink), int(sub[:, start:].sum())))
    return [(a/sx, b/sx, n) for a, b, n in out]

LINES = [
    # (label, text band y range, x range)  -- text band excludes the bar rows
    ("rowB", 177, 190, 140, 860),   # bar at y192..194
    ("rowC", 211, 224, 140, 700),   # no bar on rowC
    ("rowD", 244, 256, 140, 860),   # bar at y257..259
]
for nm, y0, y1, x0, x1 in LINES:
    print("\n== %s words (orig vs render_6), ink px and density (ink/px-width) ==" % nm)
    wo = words(mo_, y0, y1, x0, x1)
    wr = words(mb, y0, y1, x0, x1, sx=SX, sy=SY)
    print("  ORIG: " + " ".join("%.0f-%.0f(w%.0f,d%.2f)" % (a, b, b-a, n/max(1,b-a)) for a, b, n in wo))
    print("  REN : " + " ".join("%.0f-%.0f(w%.0f,d%.2f)" % (a, b, b-a, n/max(1,b-a)) for a, b, n in wr))

# targeted: the flagged words' density vs same-line controls
print("\n== FLAGGED WORDS vs CONTROLS (density = ink px / ink width) ==")
TARGETS = [
    # (finding, line, word, band y range, approx frame x window)
    ("1 rowB 'moving'",      "rowB", 177, 190, 140, 500),
    ("2 rowC 'moving'",      "rowC", 211, 224, 140, 500),
    ("3 rowD 'gradient'",    "rowD", 244, 256, 140, 400),
]
for tag, nm, y0, y1, x0, x1 in TARGETS:
    print("  %s" % tag)
    for label, mask, sx, sy in (("ORIG", mo_, 1.0, 1.0), ("REN ", mb, SX, SY)):
        ws = words(mask, y0, y1, x0, x1, sx=sx, sy=sy)
        print("     %s: %s" % (label, " ".join("%.0f-%.0f d%.2f" % (a, b, n/max(1,b-a)) for a, b, n in ws)))
# controls: known bold spans' density in both images
print("\n== CONTROLS (known bold: rowB 'negative gradient' x350..470; known regular: rowB 'Update' x174..227) ==")
for label, mask, sx, sy in (("ORIG", mo_, 1.0, 1.0), ("REN ", mb, SX, SY)):
    for nm, cx0, cx1, y0, y1 in (("bold 'negative gradient'", 350, 470, 177, 190),
                                 ("reg  'Update the weights by'", 146, 343, 177, 190)):
        sub = mask[int(y0*sy):int(y1*sy)+1, int(cx0*sx):int(cx1*sx)+1]
        n = int(sub.sum())
        w = (cx1 - cx0)
        print("  %s %-30s ink %5d  density %.3f" % (label, nm, n, n/w))
