#!/usr/bin/env python3
"""PIL-FIRST adjudication of the two MINOR findings from judge_attempt_3.txt (Template A
full-slide leg on render_7). Identical predicates, identical windows, BOTH images.

F1 "underline coverage in bullet 1 may extend slightly differently over 'objective
   function' vs 'is a convex function'"
F2 "possible subtle color tone difference in the 'moving step is a hyper parameter,'
   phrase (blue vs. reddish)"
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = QA + "/../../../unique_slides/slide_026.jpg"
REN = QA + "/render_7.png"

o = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REN).convert("RGB")).astype(int)
SR = r.shape[1] / o.shape[1]   # 2.0844

SC = {"ORIG": 1.0, "REN7": SR}
def band_runs(im, y0, y1, x0, x1, scale=1.0, minrun=3):
    """horizontal ink runs in a band (frame px coords, scaled per-image)"""
    sub = im[int(round(y0*scale)):int(round(y1*scale)), int(round(x0*scale)):int(round(x1*scale))]
    lum = sub.sum(axis=2)
    ink = lum < 430   # any non-pale pixel
    colsum = ink.sum(axis=0)
    xs = np.where(colsum >= max(1, int(round(minrun*scale))))[0]
    out = []
    if len(xs):
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > max(2, int(round(6*scale))):
                out.append((s, p)); s = x
            p = x
        out.append((s, p))
    return [(int(round((x0 + a/scale))), int(round((x0 + b/scale)))) for a, b in out], ink

def core_rgb(im, x0, x1, y0, y1, scale=1.0, frac=8):
    sub = im[int(round(y0*scale)):int(round(y1*scale)), int(round(x0*scale)):int(round(x1*scale))].reshape(-1,3)
    lum = sub.sum(axis=1)
    n = max(4, len(sub)//frac)
    c = sub[np.argsort(lum)[:n]]
    return c[:,0].mean(), c[:,1].mean(), c[:,2].mean()

print("=== F1: underline bars — N1 band (bullet 1) ===")
print("N1 baseline 355, ink top 342; underline would sit y356..364")
for tag, im in (("ORIG", o), ("REN7", r)):
    runs, _ = band_runs(im, 356, 364, 100, 860, SC[tag])
    print("  %-5s bar runs: %s" % (tag, runs))
print("  measured bank (frame px): N3 bars x177..277 and x538..728 at y458 — NO N1 bar")
print()
print("=== F1 control: underline bars — N3 band (bullet 2, y455..465) ===")
for tag, im in (("ORIG", o), ("REN7", r)):
    runs, _ = band_runs(im, 455, 465, 100, 860, SC[tag])
    print("  %-5s bar runs: %s" % (tag, runs))
print()
print("=== F2: core RGB of the disputed phrase + accepted blue controls ===")
def rgb(txt):
    return "(%3.0f,%3.0f,%3.0f) b-r=%+.0f" % (txt[0], txt[1], txt[2], txt[2]-txt[0])
# disputed phrase: rowC "moving step is a hyper parameter," blue run x146..517, band y210..227
DIS = (146, 517, 208, 228)
# accepted control A: rowB blue "moving along the direction of" x350..660 band y177..196
CA  = (350, 660, 176, 197)
# accepted control B: rowA blue "Start with initial" x146..290 band y143..163
CB  = (146, 290, 142, 164)
# accepted control C: N2 black text x109..500 band y376..396 (should be BLACK not blue)
CC  = (109, 500, 376, 396)
for nm, bb in (("disputed rowC blue", DIS), ("ctrl rowB blue", CA), ("ctrl rowA blue", CB), ("ctrl N2 black", CC)):
    for tag, im in (("ORIG", o), ("REN7", r)):
        print("  %-18s %-5s %s" % (nm, tag, rgb(core_rgb(im, *bb, SC[tag]))))
    print()
