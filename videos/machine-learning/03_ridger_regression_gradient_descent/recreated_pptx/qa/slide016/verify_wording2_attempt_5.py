#!/usr/bin/env python3
"""Supplemental glyph checks (attempt 5, worker-016-finish-20261024):
1. b2a last word: original 'model' vs render 'model' vs synth 'and'/'model'
2. b3b: 'know' vs 'known' cluster count + paren-space gap (attempt-3 fix verification)
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

oa = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = Image.open(f"{QA}/render_4.png").resize((960, 540), Image.LANCZOS)
fa = np.asarray(r).astype(int)

def ink(a): return a.min(axis=2) < 160

def clusters(mask, gap=2, min_w=2, x0=0):
    col = mask.any(axis=0)
    out, x, W = [], 0, mask.shape[1]
    while x < W:
        if col[x]:
            a = x; g = 0; b = a
            while x < W and (col[x] or g < gap):
                if col[x]: b = x; g = 0
                else: g += 1
                x += 1
            if b - a + 1 >= min_w: out.append((a + x0, b + x0, b - a + 1))
        else: x += 1
    return out

def synth_w(text, size=18):
    f = ImageFont.truetype(FONT, size)
    im = Image.new("L", (1400, 120), 0)
    ImageDraw.Draw(im).text((10, 20), text, font=f, fill=255)
    m = np.asarray(im) > 0
    c = np.where(m.any(axis=0))[0]
    return c.max() - c.min() + 1

print("synth @18px: 'and'=%d 'model'=%d 'know'=%d 'known'=%d"
      % (synth_w("and"), synth_w("model"), synth_w("know"), synth_w("known")))

print("\n== b2a (y228..250) tail: last word of each image ==")
for tag, a in [("original", oa), ("render_4", fa)]:
    cl = clusters(ink(a)[228:250, 400:830])
    print(f"  {tag}: last 3 clusters {cl[-3:]}")
    print(f"    -> last word x{cl[-1][0]}..{cl[-1][1]} w={cl[-1][2]}")

print("\n== b3b (y355..376): 'know'/'known' + paren gap ==")
for tag, a in [("original", oa), ("render_4", fa)]:
    cl = clusters(ink(a)[355:376, 140:840])
    print(f"  {tag} clusters: {cl}")
    # paren: gap between last blue word end and ')'
    m = ink(a)[355:376, :]
    colsum = m.sum(axis=0)
    # find the ')' cluster near x685..700 (original) / x675..690 (render)
    print(f"    total clusters in band: {len(cl)}")
o_m = ink(oa)[355:376, 660:720]
cols = np.where(o_m.any(axis=0))[0] + 660
print(f"  original x660..720 ink cols: {list(cols)}")
r_m = ink(fa)[355:376, 660:720]
cols2 = np.where(r_m.any(axis=0))[0] + 660
print(f"  render_4 x660..720 ink cols: {list(cols2)}")
print("\nDONE")
