#!/usr/bin/env python3
"""Adjudication #2 for the notes-crop MAJOR 'approximatly vs approximately' finding.

Same predicates on BOTH images, frame px:
  A) underline bar extent (y455..462, runs >= 30 frame px) — the bar spans exactly the
     underlined word, so its width is a direct read of the word's glyph count.
  B) glyph segmentation of the word (merged band y440..456, gap 3.0 frame px) with the
     per-glyph x-extents, so the tail after "approximat" is visible.
  C) Arial/Liberation advance comparison: which spelling's advance matches the original's
     measured word width.
"""
import numpy as np
from PIL import Image, ImageFont

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_7.png").convert("RGB")).astype(int)
SR = ren.shape[1] / 960.0

def sub_band(im, sc, x0, x1, y0, y1):
    return im[int(round(y0*sc)):int(round(y1*sc)), int(round(x0*sc)):int(round(x1*sc))]

def ink_cols(im, sc, x0, x1, y0, y1, thr=500):
    sub = sub_band(im, sc, x0, x1, y0, y1)
    lum = sub.sum(axis=2)
    return (lum < thr).sum(axis=0)

def runs_from(ink, sc, x0, gapf, minw):
    g = max(1, int(round(gapf * sc)))
    xs = np.where(ink >= 1)[0]
    out = []
    if len(xs):
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > g:
                out.append((s, p)); s = x
            p = x
        out.append((s, p))
    res = []
    for a, b in out:
        if b - a + 1 >= minw * sc:
            res.append((int(round(x0 + a/sc)), int(round(x0 + b/sc)), int(round((b-a+1)/sc))))
    return res

print("A) underline bars in the N3 band (y455..462):")
for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ink = ink_cols(im, sc, 100, 860, 455, 462)
    print("   %-5s bars >=20 frame px: %s" % (tag, runs_from(ink, sc, 100, 1.0, 20)))
print()

print("B) glyph segmentation of the underlined word (band y441..456, gap 3.0 frame px):")
for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ink = ink_cols(im, sc, 170, 285, 441, 456)
    gs = runs_from(ink, sc, 170, 3.0, 2)
    print("   %-5s %d glyph runs: %s" % (tag, len(gs), gs))
    print("        word ink extent: x%s..x%s (width %s frame px)" % (gs[0][0], gs[-1][1], gs[-1][1]-gs[0][0]+1) if gs else "")
print()

print("B2) tail detail — column ink profile x225..285, band y441..456 (frame px, '#'=ink>2, '+'=ink>0):")
for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ink = ink_cols(im, sc, 225, 285, 441, 456)
    s = ""
    for i, v in enumerate(ink):
        s += "#" if v > 2 else ("+" if v > 0 else ".")
    print("   %-5s %s" % (tag, s))
print("   x-axis tick: " + "".join(str((225+i)//10 % 10) for i in range(60)))
print()

print("C) Arial/Liberation advance check (which spelling fits the measured word width):")
fp = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
import os
if not os.path.exists(fp):
    import glob
    fp = glob.glob("/usr/share/fonts/**/LiberationSans-Regular.ttf", recursive=True)[0]
f = ImageFont.truetype(fp, 175)   # 175 px == 17.5pt * 10
a1 = f.getlength("approximately") / 10.0
a2 = f.getlength("approximatly") / 10.0
print("   Liberation 17.5pt advance: 'approximately' = %.1f frame px | 'approximatly' = %.1f frame px (delta %.1f)" % (a1, a2, a1-a2))
for tag, im, sc in (("ORIG", org, 1.0), ("REN7", ren, SR)):
    ink = ink_cols(im, sc, 170, 285, 441, 456)
    nz = np.where(ink >= 1)[0]
    w = (nz[-1]-nz[0]+1)/sc
    print("   %-5s measured word ink width = %.1f frame px -> fits %s" %
          (tag, w, "approximately" if abs(w-a1) <= abs(w-a2) else "approximatly"))
