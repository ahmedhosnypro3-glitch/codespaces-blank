#!/usr/bin/env python3
"""Adjudicate the 3 MINOR bold-weight findings by ADVANCE WIDTH (the bank's
validated discriminator, per build_026.js's REGULAR section):
compare the ORIGINAL's per-word ink widths against Liberation Sans REGULAR and
BOLD advances at 17.5px, calibrated on this slide's known-regular and
known-bold controls in the SAME line, and against the RENDER's own measured
widths (the render's bold/regular is known exactly from build_026.js).

gap is given in FRAME px on both sides so both images produce WORD-level runs.
"""
import numpy as np, statistics as st
from PIL import Image, ImageFont

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = QA + "/../../../unique_slides/slide_026.jpg"
REN = QA + "/render_6.png"
fr = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 175)
fb = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 175)
adv_r = lambda w: fr.getlength(w) / 10.0
adv_b = lambda w: fb.getlength(w) / 10.0

org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
SX, SY = ren.shape[1] / 960.0, ren.shape[0] / 540.0
def blue(im):
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (B - R > 40) & (B - G > 40)
mo, mb = blue(org), blue(ren)

def words(mask, fy0, fy1, fx0, fx1, gapf, sx, sy):
    """gapf in frame px; returns word runs in FRAME px."""
    g = max(1, int(round(gapf * sx)))
    sub = mask[int(fy0 * sy):int(fy1 * sy) + 1, int(fx0 * sx):int(fx1 * sx) + 1]
    colink = sub.any(axis=0)
    out, start, miss = [], None, 0
    for i, v in enumerate(colink):
        if v:
            if start is None: start = i
            miss = 0
        elif start is not None:
            miss += 1
            if miss >= g:
                out.append((int(fx0 * sx) + start, int(fx0 * sx) + i - miss)); start = None
    if start is not None:
        out.append((int(fx0 * sx) + start, int(fx0 * sx) + len(colink)))
    return [(a / sx, b / sx) for a, b in out]

LINES = [
 dict(name="rowB", band=(177, 190),
      toks="[2] Update the weights by moving along the direction of negative gradient of Loss function".split(),
      bold={"negative", "gradient"}),
 dict(name="rowC", band=(211, 224),
      toks="(w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate )".split(),
      bold={"moving", "step", "is", "a", "hyper", "parameter,"}),
 dict(name="rowD", band=(244, 256),
      toks="[3] Stop when the gradient is almost zero (this is at the minimum value of the function)".split(),
      bold={"almost", "zero"}),
]
for L in LINES:
    y0, y1 = L["band"]
    wo = words(mo, y0, y1, 140, 860, 3, 1.0, 1.0)
    wr = words(mb, y0, y1, 140, 860, 3.4, SX, SY)
    toks = L["toks"]
    print("\n== %s: %d tokens | orig %d runs | ren %d runs ==" % (L["name"], len(toks), len(wo), len(wr)))
    if len(wo) != len(toks) or len(wr) != len(toks):
        print("  MISMATCH — raw:")
        print("  ORIG:", ["%.0f..%.0f" % t for t in wo])
        print("  REN :", ["%.0f..%.0f" % t for t in wr])
        continue
    ro, rr, bo_, br_ = [], [], [], []
    for tok, (oa, ob), (ra, rb) in zip(toks, wo, wr):
        ow, rw = ob - oa, rb - ra
        ar, ab = adv_r(tok), adv_b(tok)
        ro.append(ow / ar); rr.append(rw / ar); bo_.append(ow / ab); br_.append(rw / ab)
    reg = [i for i, t in enumerate(toks) if t not in L["bold"]]
    bld = [i for i, t in enumerate(toks) if t in L["bold"]]
    print("  %-13s %-9s %-22s %-22s" % ("token", "style", "ORIG w / adv(reg,bold)", "REN w / adv(reg,bold)"))
    for i, tok in enumerate(toks):
        print("  %-13s %-9s orig %5.1f (%4.2f,%4.2f)   ren %5.1f (%4.2f,%4.2f)"
              % (tok, "BOLD" if i in bld else "reg", wo[i][1]-wo[i][0], ro[i], bo_[i],
                 wr[i][1]-wr[i][0], rr[i], br_[i]))
    off_r = st.mean([ro[i] for i in reg]); off_b = st.mean([bo_[i] for i in reg])
    print("  -- calibration on REGULAR controls: orig/reg-adv x%.3f  orig/bold-adv x%.3f"
          % (off_r, off_b))
    print("  -- render (truth): regular x%.3f | bold x%.3f -> bold/regular ratio %.3f"
          % (st.mean([rr[i] for i in reg]), st.mean([br_[i] for i in bld]),
             st.mean([br_[i] for i in bld]) / st.mean([rr[i] for i in reg])))
    for i, tok in enumerate(toks):
        print("  ** %-10s ORIG/reg-adv %4.2f (resid %+5.2f vs calibr %.2f) | ORIG/bold-adv %4.2f | REN/reg-adv %4.2f"
              % (tok, ro[i], ro[i] - off_r, off_r, bo_[i], rr[i]))
