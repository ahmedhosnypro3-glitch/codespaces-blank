#!/usr/bin/env python3
"""Decisive shape test: compare the ORIGINAL's disputed word bitmaps against the
RENDER's known-style instances of the SAME word (column-ink profiles + width).

The render contains both a REGULAR 'gradient' (rowD y243..256) and a BOLD
'gradient' (rowB y177..190), so the original's rowD 'gradient' can be matched
against ground truth rather than a font model.
"""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1]/960.0, ren.shape[0]/540.0
def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
mo, mb = blue(org), blue(ren)

def colprofile(mask, y0, y1, x0, x1, sx, sy, nbins=48):
    """ink count per frame-px column, resampled to nbins"""
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    prof = m.sum(axis=0).astype(float)
    if len(prof) < 2: return None
    xs = np.linspace(0, len(prof)-1, nbins)
    return np.interp(xs, np.arange(len(prof)), prof)

def width(mask, y0, y1, x0, x1, sx, sy):
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    ys, xs = np.where(m)
    return (xs.max()-xs.min()+1)/sx if len(xs) else None

def ink(mask, y0, y1, x0, x1, sx, sy):
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    return m.sum()/(sx*sy)

def compare(label, o_band, o_x, cands):
    op = colprofile(mo, *o_band, *o_x, 1.0, 1.0)
    ow = width(mo, *o_band, *o_x, 1.0, 1.0)
    oi = ink(mo, *o_band, *o_x, 1.0, 1.0)
    print("\n== %s ==" % label)
    print("   ORIGINAL: width %.1f ink %d  x%s..%s" % (ow, oi, o_x[0], o_x[1]))
    on = op/max(op.max(), 1)
    for cname, band, cx, style in cands:
        cp = colprofile(mb, *band, *cx, SX, SY)
        cw = width(mb, *band, *cx, SX, SY)
        ci = ink(mb, *band, *cx, SX, SY)
        cn = cp/max(cp.max(), 1)
        l1 = np.abs(on-cn).mean()
        corr = np.corrcoef(on, cn)[0,1]
        print("   %-26s width %6.1f (%+.1f) ink %6d  L1 %6.3f  corr %6.3f  [%s]"
              % (cname, cw, cw-ow, ci, l1, corr, style))

# ---- rowD 'gradient' (disputed) vs render's known regular + bold instances ----
compare("rowD 'gradient' — disputed",
        (244, 256), (288, 356),
        [("RENDER rowD 'gradient'", (244, 256), (287, 349), "REGULAR (build)"),
         ("RENDER rowB 'gradient'", (177, 190), (654, 719), "BOLD (build)")])

# ---- rowB 'negative gradient' (build BOLD) vs render's own bold + a size-scaled control ----
compare("rowB 'negative gradient' — build renders BOLD",
        (177, 190), (583, 715),
        [("RENDER rowB 'negative gradient'", (177, 190), (587, 719), "BOLD (build)")])

# ---- rowC 'moving step is a hyper parameter,' (build BOLD) ----
compare("rowC 'moving' — disputed (build already BOLD)",
        (210, 224), (230, 296),
        [("RENDER rowC 'moving'", (210, 224), (222, 288), "BOLD (build)"),
         ("RENDER rowB 'moving'", (177, 190), (350, 407), "REGULAR (build)")])

# ---- rowB 'moving' (disputed; build REGULAR) ----
compare("rowB 'moving' — disputed (build REGULAR)",
        (177, 190), (350, 407),
        [("RENDER rowB 'moving'", (177, 190), (350, 407), "REGULAR (build)")])
