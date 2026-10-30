#!/usr/bin/env python3
"""Controlled bold adjudication.

test_bold_026.pptx renders the SAME words twice through the SAME pipeline
(LibreOffice + Arial/Liberation 17.5pt) — once REGULAR, once BOLD, at known
frame-px positions. The original's disputed instances are then read against both
candidates with IDENTICAL predicates, and scored as a "bold fraction"
(orig - regular) / (bold - regular): 0 = regular, 1 = bold, ~0.5 = no signal.
Font-weight differences between the original's font and Arial cancel because
they shift regular and bold equally.
"""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
BT = "/home/ahmed/Projects/ai_llm_slides/scratch/tmp/lo_boldtest/bt-1.png"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
bt  = np.asarray(Image.open(BT).convert("RGB")).astype(int)
S = bt.shape[1]/960.0          # uniform scale (square slide)
print("boldtest render %dx%d  scale %.4f" % (bt.shape[1], bt.shape[0], S))
def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
mo, mb = blue(org), blue(bt)

def measure(mask, y0, y1, x0, x1, sx):
    """ink extent + count + x-height stem stats inside a window (frame px)"""
    sub = mask[int(y0*sx):int(y1*sx)+1, int(x0*sx):int(x1*sx)+1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    x_lo, x_hi = (int(x0*sx)+xs.min())/sx, (int(x0*sx)+xs.max())/sx
    w = x_hi - x_lo + 1/sx
    ink = sub.sum()/(sx*sx)
    # x-height band: use the ink's own vertical extent (cap top .. base) and
    # take the tallest column-ink profile as the stem signature
    y_lo, y_hi = (int(y0*sx)+ys.min())/sx, (int(y0*sx)+ys.max())/sx
    h = y_hi - y_lo + 1/sx
    # stem widths: columns whose ink spans >=75% of (y_lo+? .. y_hi_baseline)
    base = y_hi                       # descenders/baseline proxy
    cap = y_lo
    xh_top = cap + (y_hi-cap)*0.32    # cap->x-height offset ~3.4px at 9.6 x-height
    return dict(w=w, ink=ink, dens=ink/(w*h), x0=x_lo, x1=x_hi, y0=y_lo, y1=y_hi)

def stems(mask, cap_top, base, x0, x1, sx):
    xh = cap_top + 3.4
    y0, y1 = int(round(xh*sx)), int(round(base*sx))
    band = y1-y0+1
    cols = [c for c in range(int(x0*sx), int(x1*sx)+1) if mask[y0:y1+1, c].sum() >= 0.75*band]
    groups = []
    for c in cols:
        if groups and c-groups[-1][-1] <= 1: groups[-1].append(c)
        else: groups.append([c])
    return [len(g)/sx for g in groups]

# test-instance windows (frame px): regular col x=100.., bold col x=500..
YROWS = {"moving": 60, "gradient": 106, "negative gradient": 152,
         "almost zero": 198, "minimum": 244, "Loss function": 290}
TESTS = {}
for w, y in YROWS.items():
    for style, x0 in (("regular", 100), ("bold", 500)):
        m = measure(mb, y, y+26, x0, x0+380, S)
        st = stems(mb, m["y0"], m["y1"], m["x0"], m["x1"], S)
        TESTS[(w, style)] = (m, st)

# original disputed/control instances (frame px), with the x-height band from the line
ORIG = [
 ("rowB 'moving'  DISPUTED",      "moving",            350, 407, 177, 190),
 ("rowC 'moving'  CONTROL bold",  "moving",            230, 296, 210, 223),
 ("rowD 'gradient' DISPUTED",     "gradient",          288, 356, 243, 256),
 ("rowB 'gradient' CONTROL bold", "gradient",          654, 715, 177, 190),
 ("rowB 'negative gradient' CTL", "negative gradient", 583, 715, 177, 190),
 ("rowD 'almost zero' CONTROL",   "almost zero",       379, 472, 243, 256),
 ("rowD 'minimum' CTL regular",   "minimum",           587, 659, 243, 256),
 ("rowB 'Loss function' CTL reg", "Loss function",     743, 845, 177, 190),
]
print("\n%-30s %-8s | %-19s | %-19s | bold-fraction" % ("instance", "word", "ORIGINAL", "vs REG / vs BOLD"))
print("-"*118)
for label, w, x0, x1, y0, y1 in ORIG:
    o = measure(mo, y0, y1, x0, x1, 1.0)
    os_ = stems(mo, y0, y1, x0, x1, 1.0)
    r, rb = TESTS[(w, "regular")], TESTS[(w, "bold")]
    rs, bs = TESTS[(w, "regular")][1], TESTS[(w, "bold")][1]
    # width fraction
    def frac(o, a, b):
        return None if abs(b-a) < 1e-6 else (o-a)/(b-a)
    fw = frac(o["w"], r[0]["w"], rb[0]["w"])
    fd = frac(o["dens"], r[0]["dens"], rb[0]["dens"])
    # stem fraction: compare the max stem width
    def smax(st): return max(st) if st else 0
    fs = frac(smax(os_), smax(rs), smax(bs))
    def fmt(v): return "  n/a " if v is None else "%+5.2f" % v
    print("%-30s %-8s | w%6.1f d%5.2f s%4.1f | w%6.1f d%5.2f s%4.1f | w %s  d %s  s %s"
          % (label, w[:8], o["w"], o["dens"], smax(os_),
             rb[0]["w"], rb[0]["dens"], smax(bs), fmt(fw), fmt(fd), fmt(fs)))
print("\nbold-fraction: 0.00 = matches the REGULAR test instance, 1.00 = matches the BOLD instance")
print("test-instance widths/stems for reference:")
for (w, style), (m, st) in TESTS.items():
    print("   %-18s %-8s w%6.1f ink%6d dens%5.2f stems %s" % (w, style, m["w"], m["ink"], m["dens"],
          ["%.1f" % s for s in st]))
