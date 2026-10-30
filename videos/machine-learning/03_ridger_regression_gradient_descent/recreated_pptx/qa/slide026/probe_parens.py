#!/usr/bin/env python3
"""Paren colour/geometry check: the rowC ')' plus the rowA '(W)' parens as controls."""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1]/960.0, ren.shape[0]/540.0

def runinfo(mask, y0, y1, x0, x1, sx, sy, tag):
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    ys, xs = np.where(m)
    if len(xs) == 0:
        print("   %-34s NONE" % tag); return
    print("   %-34s frame x %.1f..%.1f  y %.1f..%.1f  ink %d"
          % (tag, (int(x0*sx)+xs.min())/sx, (int(x0*sx)+xs.max())/sx,
             (int(y0*sy)+ys.min())/sy, (int(y0*sy)+ys.max())/sy, m.sum()))

def core(im, sx, sy, x0, x1, y0, y1, tag):
    sub = im[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1].reshape(-1,3)
    lum = sub.sum(axis=1); core = sub[np.argsort(lum)[:max(1,len(sub)//8)]]
    r,g,b = [core[:,i].mean() for i in range(3)]
    kind = "RED" if r-g>40 and r-b>40 else ("BLUE" if b-r>40 and b-g>40 else "other")
    print("   %-34s core RGB (%.0f,%.0f,%.0f) -> %s" % (tag, r, g, b, kind))

def blue(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (B-R>40)&(B-G>40)
def red(im):
    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]; return (R-G>40)&(R-B>40)
mo, mr, mb, ma = blue(org), red(org), blue(ren), red(ren)

print("ORIGINAL rowC ')' (blue mask, band y211..228, x680..692):")
runinfo(mo, 211, 228, 680, 692, 1, 1, "blue-mask run")
core(org, 1, 1, 683, 689, 212, 224, "core probe x683..689 y212..224")
print("ORIGINAL rowA '(W)' parens (band y143..168, x140..480):")
runinfo(mo, 143, 168, 300, 480, 1, 1, "blue runs x300..480")
for x0, x1, tag in [(404, 409, "open paren"), (414, 419, "close paren"), (406, 418, "W inside")]:
    core(org, 1, 1, x0, x1, 143, 162, "rowA " + tag)
print("RENDER rowA '(W)':")
for x0, x1, tag in [(404, 409, "open paren"), (414, 419, "close paren")]:
    core(ren, SX, SY, x0, x1, 143, 162, "rowA " + tag)
print("RENDER rowC ')' (band y211..228):")
runinfo(ma, 211, 228, 660, 700, SX, SY, "red-mask run x660..700")
core(ren, SX, SY, 676, 684, 212, 224, "core probe x676..684 y212..224")
print("\nFULL-LINE mask extents, rowC band y210..229, x140..860:")
for tag, mask, sx, sy in (("ORIG blue", mo, 1, 1), ("ORIG red", mr, 1, 1),
                          ("REN  blue", mb, SX, SY), ("REN  red", ma, SX, SY)):
    runinfo(mask, 210, 229, 140, 860, sx, sy, tag)
