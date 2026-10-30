#!/usr/bin/env python3
"""Word-level runs of the rowC RED tail in the original vs the render."""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1]/960.0, ren.shape[0]/540.0
def red(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (R-G>40)&(R-B>40)
mr, ma = red(org), red(ren)
def words(mask, y0, y1, x0, x1, gapf, sx, sy):
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
print("rowC red words (band y210..229):")
print("  ORIGINAL (gap 3):", ["%.1f..%.1f (w%.1f)" % (a, b, b-a+1) for a, b in words(mr, 210, 229, 500, 860, 3, 1, 1)])
print("  RENDER   (gap 3.4):", ["%.1f..%.1f (w%.1f)" % (a, b, b-a+1) for a, b in words(ma, 210, 229, 500, 860, 3.4, SX, SY)])
print("\nrowC red words tighter band (y212..226, excludes paren descender/ascender edges):")
print("  ORIGINAL (gap 3):", ["%.1f..%.1f (w%.1f)" % (a, b, b-a+1) for a, b in words(mr, 212, 226, 500, 860, 3, 1, 1)])
print("  RENDER   (gap 3.4):", ["%.1f..%.1f (w%.1f)" % (a, b, b-a+1) for a, b in words(ma, 212, 226, 500, 860, 3.4, SX, SY)])
# vertical extents of the last red run (the paren) in both
for tag, mask, sx, sy in (("ORIG", mr, 1, 1), ("REN", ma, SX, SY)):
    m = mask[int(205*sy):int(235*sy)+1, int(670*sx):int(700*sx)+1]
    ys, xs = np.where(m)
    if len(xs):
        cols = sorted(set(xs))
        # split into runs
        runs = []
        for c in cols:
            if runs and c-runs[-1][-1] <= 1: runs[-1].append(c)
            else: runs.append([c])
        for r in runs:
            sel = m[:, r[0]:r[-1]+1]
            yy = np.where(sel.any(axis=1))[0]
            print("  %s run x%.1f..%.1f  y%.1f..%.1f  ink %d" % (tag, (int(670*sx)+r[0])/sx, (int(670*sx)+r[-1])/sx,
                  (int(205*sy)+yy.min())/sy, (int(205*sy)+yy.max())/sy, sel.sum()))
