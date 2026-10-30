#!/usr/bin/env python3
"""Probe the rowC closing paren colour + per-word density for rowC/rowD."""
import numpy as np
from PIL import Image
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
org = np.asarray(Image.open(QA + "/../../../unique_slides/slide_026.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(QA + "/render_6.png").convert("RGB")).astype(int)
SX, SY = ren.shape[1] / 960.0, ren.shape[0] / 540.0

def probe(im, sx, sy, label, fx0, fx1, fy0, fy1):
    sub = im[int(fy0*sy):int(fy1*sy)+1, int(fx0*sx):int(fx1*sx)+1].reshape(-1, 3)
    # darkest 30% pixels = ink core
    lum = sub.sum(axis=1)
    order = np.argsort(lum)
    core = sub[order[:max(1, len(order)//10)]]
    print("  %-28s core mean RGB (%3.0f,%3.0f,%3.0f)  min (%3.0f,%3.0f,%3.0f)" %
          (label, core[:,0].mean(), core[:,1].mean(), core[:,2].mean(),
            core[:,0].min(), core[:,1].min(), core[:,2].min()))
    # classify
    r, g, b = core[:,0].mean(), core[:,1].mean(), core[:,2].mean()
    print("      -> classified: %s" % ("RED (r-g=%.0f r-b=%.0f)" % (r-g, r-b) if r-g>40 and r-b>40 else
          "BLUE (b-r=%.0f b-g=%.0f)" % (b-r, b-g) if b-r>40 and b-g>40 else
          "BLACK/other (r%.0f g%.0f b%.0f)" % (r,g,b)))

print("rowC closing ')' zone (frame x680..692, y211..224):")
probe(org, 1, 1, "ORIGINAL x684..688", 684, 688, 211, 224)
probe(org, 1, 1, "ORIGINAL red tail x640..682", 640, 682, 211, 224)
probe(ren, SX, SY, "RENDER ')': fx 684..688", 684, 688, 211, 224)
probe(ren, SX, SY, "RENDER 'param' fx 425..511", 425, 511, 211, 224)

def maskc(im, kind):
    R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
    return (R-G>40)&(R-B>40) if kind=="red" else (B-R>40)&(B-G>40)
print("\noriginal rowC: red-mask extent vs blue-mask extent in band y211..224, x140..860")
for kind in ("red", "blue"):
    m = maskc(org, kind)[211:225, 140:861]
    ys, xs = np.where(m)
    print("   %-5s %s" % (kind, ("x %d..%d" % (140+xs.min(), 140+xs.max())) if len(xs) else "NONE"))
for kind in ("red", "blue"):
    m = maskc(ren, kind)[int(211*SY):int(225*SY)+1, int(140*SX):int(860*SX)+1]
    ys, xs = np.where(m)
    print("   REN %-5s %s" % (kind, ("x %.1f..%.1f" % ((140*SX+xs.min())/SX, (140*SX+xs.max())/SX)) if len(xs) else "NONE"))

def dens(im, sx, sy, mask, y0, y1, x0, x1):
    m = mask[int(y0*sy):int(y1*sy)+1, int(x0*sx):int(x1*sx)+1]
    if not m.any(): return None
    return (int(m.sum()), m.sum()/ (x1-x0))
mb = maskc(ren, "blue"); mbk = (np.abs(ren-255).max(axis=2) > 30)
mo = maskc(org, "blue"); mok = (np.abs(org-255).max(axis=2) > 30)

print("\n== rowC per-word ink/density (frame px) — original vs render ==")
ROWC = [("(w.r.t.",146,188,147,186),("W)",200,224,194,214),("moving",230,296,222,288),
        ("step",302,334,295,330),("is",340,351,337,349),("a",357,366,356,364),
        ("hyper",372,419,371,418),("parameter,",425,512,425,511)]
print("   %-11s | %-18s | %-18s" % ("word", "ORIGINAL ink/d", "RENDER ink/d"))
for w, oa, ob, ra, rb in ROWC:
    o = dens(org,1,1,mo,211,224,oa,ob); r = dens(ren,SX,SY,mb,211,224,ra,rb)
    print("   %-11s | %5d/%5.2f        | %6d/%6.2f" % (w, o[0], o[1], r[0], r[1]))
print("\n== rowD per-word ink/density (frame px) — original vs render ==")
ROWD = [("gradient",259,281,258,271),("is",288,356,287,320),("almost",362,373,373,381),
        ("zero",379,433,388,401),("(this",438,472,434,469),("is",483,516,476,494)]
for w, oa, ob, ra, rb in ROWD:
    # note: original rowD runs merged words; use exact printed runs
    pass
ROWDr = [("[3]",146,166,147,164),("Stop",174,207,170,195),("when",213,253,211,242),
         ("the",259,281,258,271),("gradient",288,356,287,320),("is",362,373,373,381),
         ("almost",379,433,388,401),("zero",438,472,434,469),("(this",483,516,476,494),
         ("is",523,533,497,517),("at",540,552,533,547),("the",559,580,569,577),
         ("minimum",587,659,584,629),("value",666,706,661,679),("of",712,727,685,692),
         ("the",733,755,710,724),("function)",762,830,760,812)]
print("   %-11s | %-18s | %-18s" % ("word", "ORIGINAL ink/d", "RENDER ink/d"))
for w, oa, ob, ra, rb in ROWDr:
    o = dens(org,1,1,mo,244,256,oa,ob); r = dens(ren,SX,SY,mb,244,256,ra,rb)
    print("   %-11s | %5d/%5.2f        | %6d/%6.2f" % (w, o[0], o[1], r[0], r[1]))
