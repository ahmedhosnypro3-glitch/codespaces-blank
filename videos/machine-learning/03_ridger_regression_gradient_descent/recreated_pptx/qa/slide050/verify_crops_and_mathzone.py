#!/usr/bin/env python3
"""Independent verification of the banked slide-050 crop pairs + math-zone ink diff.

1. For each crop pair: confirm equal sizes, equal effective scale, and coarse
   content alignment (correlation of blurred downscaled versions).
2. Math zone: compare the vertical ink profile of the original frame
   (frame px x258..710, y50..130) against the render at matched scale.
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
NS = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
QA = os.path.join(NS, "recreated_pptx/qa/slide050")
ORIG = os.path.join(NS, "unique_slides/slide_050.jpg")

PAIRS = [("chart", 310, 171, 826, 483), ("tableeq", 60, 50, 722, 250),
         ("pinkbox", 735, 52, 836, 178), ("redstop", 60, 270, 240, 400)]

o = Image.open(ORIG).convert("RGB")
r = Image.open(os.path.join(QA, "render_2.png")).convert("RGB")
H = r.size[1]
SC = H / 540.0
print("render scale = %.5f" % SC)


def corr(a, b):
    a = a.astype(np.float64).ravel()
    b = b.astype(np.float64).ravel()
    a = a - a.mean()
    b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else 0.0


for name, x0, y0, x1, y1 in PAIRS:
    cr = Image.open(os.path.join(QA, "crop_2_%s_render.png" % name)).convert("L")
    co = Image.open(os.path.join(QA, "crop_2_%s_orig.png" % name)).convert("L")
    src = Image.open(os.path.join(QA, "render_2.png")).convert("L")
    exp = src.crop((int(x0 * SC), int(y0 * SC), int(np.ceil(x1 * SC)), int(np.ceil(y1 * SC))))
    same_src = cr.size == exp.size
    eff_r = cr.size[0] / float(x1 - x0)
    eff_o = co.size[0] / float(x1 - x0)
    # alignment: shrink both to 160px wide, blur, correlate
    w = 160
    h = max(1, int(cr.size[1] * w / cr.size[0]))
    a = cr.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
    b = co.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
    # render is dark-ink-on-light; correlation is sign-agnostic only if we invert one
    c1 = corr(np.array(a), np.array(b))
    c2 = corr(255 - np.array(a), np.array(b))
    print("%-8s render=%s orig=%s eff r=%.3f o=%.3f %s | corr %.3f (inv %.3f)"
          % (name, cr.size, co.size, eff_r, eff_o,
             "SRC-MATCH" if same_src else "SRC-DIFF", c1, c2))

print("\n=== math zone vertical ink profile (frame px) ==="
      )


def profile(img, box, scale=1.0, thr=500):
    x0, y0, x1, y1 = [int(round(v * scale)) for v in box]
    a = np.array(img.crop((x0, y0, x1, y1))).astype(np.int32)
    dark = (a.sum(axis=2) < thr)
    return dark.sum(axis=0), dark.sum(axis=1)


MZ = (258, 50, 712, 132)
prof_o, rprof_o = profile(o, MZ, 1.0)
prof_r, rprof_r = profile(r, MZ, SC)


def bands(prof, off, scale, minrun=2):
    out = []
    on = False
    for i, v in enumerate(prof):
        if v > 0 and not on:
            start = i
            on = True
        elif v == 0 and on:
            on = False
            if i - start >= minrun:
                out.append((round(start / scale + off), round(i / scale + off)))
    if on:
        out.append((round(len(prof) / scale + off), None))
    return out


print("orig COL bands:", bands(prof_o, MZ[0], 1.0))
print("rend COL bands:", bands(prof_r, MZ[0], SC))
print("orig ROW bands:", bands(rprof_o, MZ[1], 1.0))
print("rend ROW bands:", bands(rprof_r, MZ[1], SC))
print("orig ink cols=%d/%d  render ink cols=%d/%d"
      % (int((prof_o > 0).sum()), len(prof_o), int((prof_r > 0).sum()), len(prof_r)))
