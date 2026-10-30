import numpy as np
from PIL import Image
R='videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/render_2.png'
O='videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg'
def frame(p):
    a=np.asarray(Image.open(p).convert('RGB')).astype(int)
    lum=a.mean(axis=2); INK=lum<228
    return np.asarray(Image.fromarray((INK*255).astype(np.uint8)).resize((960,540),Image.LANCZOS))>40
rF=frame(R); oF=frame(O)
def report(x0,x1,y0,y1,tag):
    rc=rF[y0:y1,x0:x1].sum(); oc=oF[y0:y1,x0:x1].sum()
    if rc or oc:
        rx=np.where(rF[y0:y1,x0:x1].sum(axis=0))[0]
        ry=np.where(rF[y0:y1,x0:x1].sum(axis=1))[0]
        re=f"x{x0+rx.min()}-{x0+rx.max()} y{y0+ry.min()}-{y0+ry.max()}" if len(rx) else "-"
        ox=np.where(oF[y0:y1,x0:x1].sum(axis=0))[0]
        oy=np.where(oF[y0:y1,x0:x1].sum(axis=1))[0]
        oe=f"x{x0+ox.min()}-{x0+ox.max()} y{y0+oy.min()}-{y0+oy.max()}" if len(ox) else "-"
        print(f"  {'OK ' if abs(rc-oc)<oc*0.6 else 'CHK'} {tag:26s} r/n={rc:5d} o/n={oc:5d}")
        print(f"       render bbox {re}   orig bbox {oe}")
    else:
        print(f"  EMPTY {tag}")
print("=== fix verification (render_2 vs original) ===")
report(360,440,60,84,"Step eta = 2")
report(494,590,74,93,"Check classes of")
report(594,662,60,112,"Z matrix")
report(260,360,70,90,"Initial W =")
report(236,520,106,128,"legend")
report(327,358,55,110,"W vector")
print()
print("=== containment ===")
print("  left-of-panel:",rF[:,0:54].sum()," right:",rF[:,904:].sum()," above:",rF[0:45,:].sum()," below:",rF[540:,:].sum())
