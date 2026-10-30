#!/usr/bin/env python3
"""Span-level width test for rowB/rowC/rowD: original vs render vs Liberation
regular/bold advances. Calibrates the original-font offset on spans whose
bold/regular status is AGREED, then reads the disputed spans."""
import numpy as np
from PIL import Image, ImageFont
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1]/960.0, ren.shape[0]/540.0
fr = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 175)
fb = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 175)
ADV = lambda f, t: f.getlength(t)/10.0

def extent(mask, y0, y1, x0, x1, sx, sy):
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    ys, xs = np.where(m)
    if len(xs) == 0: return None
    return (int(x0*sx)+xs.min())/sx, (int(x0*sx)+xs.max())/sx
def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
def red(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (R-G>40)&(R-B>40)
mb, mr, mo, mor = blue(ren), red(ren), blue(org), red(org)

CASES = [
 # (label, y0,y1, mask_key, mask_orig, orig_x_lo, orig_x_hi, ren_x_lo, ren_x_hi, text, build_style)
 ("rowB 'moving along the direction of ' (underlined, build REGULAR)", 177,190,"blue", "moving along the direction of ", "REGULAR"),
 ("rowB 'negative gradient' (underlined, build BOLD)",                177,190,"blue", "negative gradient", "BOLD"),
 ("rowB ' of Loss function' (build REGULAR)",                         177,190,"blue", " of Loss function", "REGULAR"),
 ("rowC '(w.r.t. W) (' (build REGULAR)",                              210,224,"blue", "(w.r.t. W) (", "REGULAR"),
 ("rowC 'moving step is a hyper parameter,' (build BOLD)",            210,224,"blue", "moving step is a hyper parameter,", "BOLD"),
 ("rowD 'gradient is ' (underlined, build REGULAR)",                  243,256,"blue", "gradient is ", "REGULAR"),
 ("rowD 'almost zero' (underlined, build BOLD)",                      243,256,"blue", "almost zero", "BOLD"),
 ("rowD ' (this is at the minimum value of the function)' (REGULAR)", 243,256,"blue", " (this is at the minimum value of the function)", "REGULAR"),
]
print("== span ink widths: ORIGINAL vs RENDER vs Liberation advances ==")
print("%-58s %-22s %-22s %s" % ("span", "ORIGINAL ink", "RENDER ink", "adv(reg/bold)"))
rows = []
for label, y0, y1, mk, text, style in CASES:
    mo_ = mo if mk == "blue" else mor
    mb_ = mb if mk == "blue" else mr
    # original: full line-blue scan inside the span's neighbourhood gives the merge;
    # use per-word boundaries instead for the original (merged runs), so scan the
    # WHOLE line and split by word list
    pass
# Simpler: per-word accumulation using the word lists already validated
def wordlist(mask, y0, y1, x0, x1, gapf, sx, sy):
    g = max(1, int(round(gapf*sx)))
    sub = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    ci = sub.any(axis=0); out, st, miss = [], None, 0
    for i, v in enumerate(ci):
        if v:
            if st is None: st = i
            miss = 0
        elif st is not None:
            miss += 1
            if miss >= g:
                out.append(((int(x0*sx)+st)/sx, (int(x0*sx)+i-miss)/sx)); st = None
    if st is not None: out.append(((int(x0*sx)+st)/sx, (int(x0*sx)+len(ci))/sx))
    return out

SPANS = [
 dict(line="rowB", y=(177,190), mk="blue",
      toks="[2] Update the weights by moving along the direction of negative gradient of Loss function".split(),
      want=[("moving","along","the","direction","of"), ("negative","gradient"), ("of","Loss","function")]),
 dict(line="rowC", y=(210,224), mk="blue",
      toks="(w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate )".split(),
      want=[("(w.r.t.","W)","(",), ("moving","step","is","a","hyper","parameter,"), ("AKA","Learning","Rate"), (")",)]),
 dict(line="rowD", y=(243,256), mk="blue",
      toks="[3] Stop when the gradient is almost zero (this is at the minimum value of the function)".split(),
      want=[("gradient","is"), ("almost","zero")]),
]
for S in SPANS:
    y0, y1 = S["y"]
    m_o = mo if S["mk"] == "blue" else mor
    m_r = mb if S["mk"] == "blue" else mr
    wo = wordlist(m_o, y0, y1, 140, 860, 3, 1.0, 1.0)
    wr = wordlist(m_r, y0, y1, 140, 860, 3.4, SX, SY)
    print("\n-- %s: %d orig runs / %d ren runs / %d tokens" % (S["line"], len(wo), len(wr), len(S["toks"])))
    if len(wo) != len(S["toks"]) or len(wr) != len(S["toks"]):
        print("   count mismatch; orig:", ["%.0f..%.0f" % t for t in wo]); print("   ren :", ["%.0f..%.0f" % t for t in wr]); continue
    for grp in S["want"]:
        idx = [S["toks"].index(g) for g in grp]
        text = "".join(S["toks"][i] + ("" if i == idx[-1] else " ") for i in range(idx[0], idx[-1]+1))
        text = " ".join(S["toks"][i] for i in range(idx[0], idx[-1]+1))
        ow = wo[idx[-1]][1] - wo[idx[0]][0]
        rw = wr[idx[-1]][1] - wr[idx[0]][0]
        ar, ab = ADV(fr, text), ADV(fb, text)
        # ink width ~ advance minus trailing space advance
        ar_ink, ab_ink = ar - ADV(fr, " "), ab - ADV(fb, " ")
        print("   %-40s orig %6.1f (reg %6.1f x%.3f | bold %6.1f x%.3f)  ren %6.1f (reg x%.3f | bold x%.3f)"
              % ("'" + text + "'", ow, ar_ink, ow/ar_ink, ab_ink, ow/ab_ink, rw, rw/ar_ink, rw/ab_ink))
