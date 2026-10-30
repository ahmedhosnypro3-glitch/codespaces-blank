#!/usr/bin/env python3
"""STEM-WIDTH test: the weight signature independent of font advance widths.

For a glyph with a clean vertical stem, measure the stem's horizontal thickness
inside the x-height band, in BOTH images. Liberation Sans regular stem / x-height
~0.133, bold ~0.183 (a +38% signal, far above noise). The original's stroke weight
differs from Arial overall, so every disputed word is read against this line's own
AGREED bold and AGREED regular controls measured with the identical predicate.
"""
import numpy as np
from PIL import Image, ImageFont
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1]/960.0, ren.shape[0]/540.0
def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
mo, mb = blue(org), blue(ren)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 175)

def stems(mask, cap_top, base, x0, x1, sx, sy):
    """return list of (stem_center_frame_x, stem_width_frame_px, col_ink_frac)"""
    xh_top = cap_top + 3.4            # Liberation: cap .716em, x-ht .519em @17.5px
    y0 = int(round(xh_top*sy)); y1 = int(round(base*sy))
    band_h = y1 - y0 + 1
    cols = {}
    out = []
    for c in range(int(x0*sx), int(x1*sx)+1):
        cnt = int(mask[y0:y1+1, c].sum())
        frac = cnt/band_h
        if frac >= 0.75:
            out.append((c, frac))
    # group contiguous
    groups = []
    for c, f in out:
        if groups and c - groups[-1][-1][0] <= 1: groups[-1].append((c, f))
        else: groups.append([(c, f)])
    res = []
    for g in groups:
        w = len(g)
        res.append(((g[0][0]+g[-1][0])/2/sx, w/sx, np.mean([x[1] for x in g])))
    return res

def glyph_x(word_start_x, word, letter_index, sx=1.0):
    """predicted x of letter[letter_index] using Liberation advances from the word start"""
    adv = fnt.getlength(word[:letter_index])/10.0
    return word_start_x + adv

CASES = [
  # (label, line, cap_top, base, word, word_ink_start, letters_idx, note)
  ("rowB 'moving'  DISPUTED (build REGULAR)", 177, 190, "moving", 350.0, [0,1,2,4], "m-stems / n"),
  ("rowB 'negative' DISPUTED (build BOLD)",   177, 190, "negative", 583.0, [0,5], "n / t"),
  ("rowB 'gradient' DISPUTED (build BOLD)",   177, 190, "gradient", 654.0, [4,7], "d / t"),
  ("rowC 'moving'  DISPUTED (build BOLD)",    210, 223, "moving", 230.0, [0,1,2,4], "m / n"),
  ("rowC 'hyper'   CONTROL bold (build BOLD)",210, 223, "hyper", 372.0, [1,2], "y / p"),
  ("rowD 'gradient'DISPUTED (build REGULAR)", 243, 256, "gradient", 288.0, [3,7], "d / t"),
  ("rowD 'almost'  CONTROL bold (brief+build BOLD)", 243, 256, "almost", 379.0, [2], "l"),
  ("rowD 'zero'    CONTROL bold (brief+build BOLD)", 243, 256, "zero", 438.0, [1], "e? r"),
  ("rowD 'Stop'    CONTROL regular",         243, 256, "Stop", 174.0, [0,1], "S / t"),
  ("rowD 'minimum' CONTROL regular",         243, 256, "minimum", 587.0, [1,6], "i / m"),
  ("rowD 'function)' CONTROL regular",       243, 256, "function)", 762.0, [5,0,1], "i / f / t"),
  ("rowB 'direction' CONTROL regular",       177, 190, "direction", 489.0, [4,7], "c? t / n?"),
  ("rowB 'weights' CONTROL regular",         177, 190, "weights", 262.0, [5], "t"),
  ("rowB 'function' CONTROL regular",        177, 190, "function", 783.0, [5,0,1], "i / f / t"),
  ("rowB 'along' CONTROL regular",           177, 190, "along", 414.0, [2], "o? n"),
  ("rowC '(w.r.t.' CONTROL regular",         210, 223, "(w.r.t.", 146.0, [5,3], "t / t"),
  ("rowD 'when' CONTROL regular",            243, 256, "when", 213.0, [1,3], "h / n"),
]
print("%-46s | %-22s | %-22s" % ("case", "ORIGINAL stems (frame px)", "RENDER stems (frame px)"))
print("-"*100)
for label, cap, base, word, wx, idxs, note in CASES:
    ro, rr = [], []
    for li in idxs:
        gx = glyph_x(wx, word, li)
        so = stems(mo, cap, base, gx-3.0, gx+11.0, 1.0, 1.0)
        sr = stems(mb, cap, base, gx-3.0, gx+11.0, SX, SY)
        ro += [("w%.2f@%.0f" % (w, c)) for c, w, f in so]
        rr += [("w%.2f@%.0f" % (w, c)) for c, w, f in sr]
    print("%-46s | %-22s | %-22s" % (label, ",".join(ro) or "-", ",".join(rr) or "-"))
print("\n(stem widths in FRAME px; 'l' in 'almost' is the AGREED-bold control)")
