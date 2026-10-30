#!/usr/bin/env python3
"""Attempt-7 verification: the rowC red tail, the blue paren, and their positions."""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_7.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1]/960.0, ren.shape[0]/540.0
def red(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (R-G>40)&(R-B>40)
def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
def info(mask, y0, y1, x0, x1, sx, sy, tag):
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    ys, xs = np.where(m)
    if len(xs)==0:
        print("   %-26s NONE" % tag); return None
    ext = ((int(x0*sx)+xs.min())/sx, (int(x0*sx)+xs.max())/sx,
           (int(y0*sy)+ys.min())/sy, (int(y0*sy)+ys.max())/sy)
    print("   %-26s x %6.1f..%6.1f  y %6.1f..%6.1f  ink %d" % (tag, ext[0], ext[1], ext[2], ext[3], m.sum()))
    return ext
print("rowC band y210..229:")
o_red = info(red(org), 210, 229, 140, 860, 1, 1, "ORIG red")
r_red = info(red(ren), 210, 229, 140, 860, SX, SY, "REN7 red")
o_blue = info(blue(org), 210, 229, 140, 860, 1, 1, "ORIG blue")
r_blue = info(blue(ren), 210, 229, 140, 860, SX, SY, "REN7 blue")
# paren runs: x670..700
for tag, im, mask, sx, sy in (("ORIG", org, blue(org), 1, 1), ("REN7", ren, blue(ren), SX, SY)):
    m = mask[int(205*sy):int(235*sy)+1, int(672*sx):int(700*sx)+1]
    ys, xs = np.where(m)
    if len(xs)==0: print("   %s paren NONE" % tag); continue
    cols = sorted(set(xs)); runs=[]
    for c in cols:
        if runs and c-runs[-1][-1] <= 1: runs[-1].append(c)
        else: runs.append([c])
    for r in runs:
        sel = m[:, r[0]:r[-1]+1]
        yy = np.where(sel.any(axis=1))[0]
        print("   %s paren run x%.1f..%.1f y%.1f..%.1f h%.1f ink %d" % (tag,
              (int(672*sx)+r[0])/sx, (int(672*sx)+r[-1])/sx,
              (int(205*sy)+yy.min())/sy, (int(205*sy)+yy.max())/sy, (yy.max()-yy.min()+1)/sy, sel.sum()))
print("\nDELTAS (ren7 - orig):")
if o_red and r_red: print("   red : left %+5.1f right %+5.1f top %+5.1f bottom %+5.1f" %
      tuple(r_red[i]-o_red[i] for i in range(4)))
if o_blue and r_blue: print("   blue: left %+5.1f right %+5.1f top %+5.1f bottom %+5.1f" %
      tuple(r_blue[i]-o_blue[i] for i in range(4)))
print("\nTARGETS: red 520..682 ; blue paren 684..688 h17 (original)")
