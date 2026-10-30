#!/usr/bin/env python3
"""Read the charSpacing calibration render: red extent + paren position per value."""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/scratch/tmp/lo_boldtest/rc-1.png").convert("RGB")).astype(int)
S = im.shape[1]/960.0
print("scale %.4f" % S)
def red(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (R-G>40)&(R-B>40)
def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
mr, mb = red(im), blue(im)
YS = [80, 140, 200, 260, 320, 380]     # test-line BOX TOPS (frame px); baseline = y+17.5
SP = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50]
print("%-7s | %-24s | %-24s | %s" % ("spc", "RED extent", "BLUE extent", "paren"))
for y, s in zip(YS, SP):
    def ext(mask):
        m = mask[int((y-4)*S):int((y+26)*S)+1, int(140*S):int(720*S)+1]
        ys, xs = np.where(m)
        if len(xs) == 0: return None
        return ((int(140*S)+xs.min())/S, (int(140*S)+xs.max())/S)
    e = ext(mr); b = ext(mb)
    # paren: the rightmost red run taller than 12px (ascender+descender)
    m = mr[int((y-4)*S):int((y+26)*S)+1, int(660*S):int(720*S)+1]
    ys, xs = np.where(m)
    p = None
    if len(xs):
        cols = sorted(set(xs)); runs = []
        for c in cols:
            if runs and c-runs[-1][-1] <= 1: runs[-1].append(c)
            else: runs.append([c])
        last = runs[-1]
        sel = m[:, last[0]:last[-1]+1]
        yy = np.where(sel.any(axis=1))[0]
        p = ((int(660*S)+last[0])/S, (int(660*S)+last[-1])/S, (yy.max()-yy.min()+1)/S)
    print("%-7s | x %6.1f..%6.1f       | x %6.1f..%6.1f       | %s"
          % (s, e[0], e[1], b[0], b[1],
             ("%.1f..%.1f h%.1f" % p) if p else "none"))
print("\nTARGET (original): red x520..682 ; blue paren x684..688 h17")
