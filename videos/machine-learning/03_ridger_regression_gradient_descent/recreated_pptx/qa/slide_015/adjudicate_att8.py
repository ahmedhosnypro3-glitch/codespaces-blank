import numpy as np
from PIL import Image
NS="/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA=f"{NS}/recreated_pptx/qa/slide_015"
R=Image.open(f"{QA}/render_6.png").convert("RGB")
O=Image.open(f"{NS}/unique_slides/slide_015.jpg").convert("RGB")
r=np.asarray(R).astype(int); o=np.asarray(O).astype(int)
sx,sy=r.shape[1]/960.0, r.shape[0]/540.0
def cls(px):
    rr,gg,bb=px
    if gg>140 and gg>rr+30 and gg>bb+20: return "green"
    if bb>110 and bb>rr+25 and bb>gg+15: return "blue"
    if rr>120 and rr>gg+25 and rr>bb+25: return "red"
    if rr+gg+bb<330: return "black"
    return None
def census(img, x0,x1,y0,y1, label):
    x0r,y0r=int(x0*sx),int(y0*sy); x1r,y1r=int(x1*sx),int(y1*sy)
    from collections import Counter
    c=Counter()
    for y in range(y0r,y1r):
        for x in range(x0r,x1r):
            k=cls(img[y,x])
            if k: c[k]+=1
    print(f"{label}: {dict(c)}")
print("== deriv_stack L1 head (frame x71..200, y343..375) ==")
census(r,71,200,343,375,"render L1 head")
census(o,71,200,343,375,"orig   L1 head")
print("== deriv_stack L2 tail lambda I W (frame x400..518, y417..466) ==")
census(r,400,518,417,466,"render L2 tail")
census(o,400,518,417,466,"orig   L2 tail")
print("== peachbox eq (frame x783..898, y271..337) ==")
census(r,783,898,271,337,"render peach eq")
census(o,783,898,271,337,"orig   peach eq")
print("== solution eq (frame x545..893, y466..523) ==")
census(r,545,893,466,523,"render solution")
census(o,545,893,466,523,"orig   solution")
print("== solution final Y (frame x840..893, y480..516) ==")
census(r,840,893,480,516,"render sol-Y")
census(o,840,893,480,516,"orig   sol-Y")
# underline check under final Y in solution: rows just below baseline
def underline(img,x0,x1,y0,y1,label):
    x0r,y0r=int(x0*sx),int(y0*sy); x1r,y1r=int(x1*sx),int(y1*sy)
    sub=img[y0r:y1r,x0r:x1r]
    dark=(sub.sum(axis=2)<450).sum(axis=1)
    print(f"{label} darkpx per row y{y0}..{y1}: {dark.tolist()}")
underline(r,840,893,505,516,"render sol-Y underline band")
underline(o,840,893,505,516,"orig   sol-Y underline band")
# J presence in deriv L1: dark ink between d and ( at x~88..96
print("== deriv L1: dark ink census x84..100 y346..372 (J slot) ==")
def darkc(img,x0,x1,y0,y1,label):
    x0r,y0r=int(x0*sx),int(y0*sy); x1r,y1r=int(x1*sx),int(y1*sy)
    sub=img[y0r:y1r,x0r:x1r]
    print(f"{label}: dark px={int((sub.sum(axis=2)<450).sum())}")
darkc(r,84,100,346,372,"render J slot")
darkc(o,84,100,346,372,"orig   J slot")
