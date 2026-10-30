import numpy as np
from PIL import Image
B="/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA=B+"/recreated_pptx/qa/slide003"
a=np.asarray(Image.open(B+"/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
r=np.asarray(Image.open(QA+"/render_18.png").convert("RGB").resize((960,540),Image.LANCZOS)).astype(int)
def runs(im,y0,y1,x0,x1,gap=13):
    m=(im[y0:y1,x0:x1].sum(axis=2)<330);pres=m.any(axis=0);out=[];s=None
    for i,p in enumerate(pres):
        if p and s is None:s=i
        elif not p and s is not None:out.append((s+x0,i-1+x0));s=None
    if s is not None:out.append((s+x0,x1-1))
    mg=[]
    for rn in out:
        if mg and rn[0]-mg[-1][1]<gap:mg[-1]=(mg[-1][0],rn[1])
        else:mg.append(rn)
    return mg
BANDS=[("Y r1",368,390),("C r2",397,423),("W r3",423,455),("P r4",456,478)]
print("=== render_18 vs ORIGINAL: matrix data-row ink runs ===")
for tag,im in (("ORIG",a),("REND18",r)):
    print(f"-- {tag} --")
    for nm,y0,y1 in BANDS:
        rr=runs(im,y0-2,y1+2,150,432)
        print(f"   {nm}: {len(rr)} runs [{' '.join(f'{x0}-{x1}' for x0,x1 in rr)}]")
# weight-vector: lowercase w + ellipsis cell present?
def wv(im):
    # entries around x455..525, stack y330..478
    return runs(im,330,478,450,528,gap=10)
print("\n=== weight-vector ink (x450..528, y330..478): ORIG vs REND18 ===")
print("  ORIG  :",wv(a))
print("  REND18:",wv(r))
