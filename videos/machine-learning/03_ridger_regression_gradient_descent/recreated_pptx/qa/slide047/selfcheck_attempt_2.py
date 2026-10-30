import numpy as np
from PIL import Image
R='videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/render_1.png'
O='videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg'
def frame(p):
    a=np.asarray(Image.open(p).convert('RGB')).astype(int)
    lum=a.mean(axis=2); INK=lum<228
    return np.asarray(Image.fromarray((INK*255).astype(np.uint8)).resize((960,540),Image.LANCZOS))>40
rF=frame(R); oF=frame(O)
print("=== ORIGINAL element windows (measured) ===")
regs = {
 "top-left matrix digits":  (86,220,62,128),
 "'Initial W =' text":      (255,300,72,90),
 "W bracket+digits":        (328,360,56,110),
 "legend line":             (236,382,108,127),
 "aug header text":         (80,250,144,161),
 "aug matrix digits":       (86,220,164,244),
 "Z matrix digits":         (594,662,62,112),
 "'Check classes of' hdr":  (560,730,60,78),
 "calc box1 interior":      (280,860,143,196),
 "calc box2 interior":      (280,860,210,262),
 "calc box3 interior":      (280,860,275,328),
 "button":                  (75,245,274,308),
}
for n,(x0,x1,y0,y1) in regs.items():
    ro=rF[y0:y1,x0:x1].sum(); oo=oF[y0:y1,x0:x1].sum()
    ratio=(ro/oo) if oo else 0
    flag="OK " if 0.55<=ratio<=2.2 else ("HI " if ratio>2.2 else "LOW")
    print(f"  {flag} {n:24s} render={ro:5d} orig={oo:5d} ratio={ratio:.2f}")

print()
print("=== FRAME CONTAINMENT: render ink must not cross the house strokes ===")
print("  ink left of panel (x<54):", rF[:,0:54].sum())
print("  ink right of panel (x>903):", rF[:,904:960].sum())
print("  ink above panel (y<45):", rF[0:45,:].sum())
print("  ink below y=539:", rF[540:,:].sum())
# inner: no ink ON the vertical strokes except the strokes themselves
print("  ink on left stroke col x56..61 (excl stroke itself):", rF[45:538, 56:62].sum())
print("  ink on right stroke col x898..904 (excl stroke itself):", rF[45:538, 898:905].sum())

print()
print("=== TOP-LEFT MATRIX cell-by-cell ink parity ===")
# cells measured in the original
cells_x=[(88,105),(109,127),(131,150),(153,173),(176,195),(199,217)]
for ri,(y0,y1,tag) in enumerate([(63,74,"hdr"),(77,90,"r1"),(93,108,"r2"),(110,126,"cls")]):
    out=[]
    for (x0,x1) in cells_x:
        rc=rF[y0:y1,x0:x1].sum(); oc=oF[y0:y1,x0:x1].sum()
        out.append(f"{rc}/{oc}")
    print(f"  {tag}: r/o per cell: "+"  ".join(out))
