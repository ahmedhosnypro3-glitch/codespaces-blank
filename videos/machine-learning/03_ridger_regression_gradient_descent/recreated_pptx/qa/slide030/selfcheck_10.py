import numpy as np
from PIL import Image
from collections import Counter
DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540

def census(img, sc, x0,y0,x1,y1, tag):
    X0,Y0,X1,Y1 = int(x0*sc),int(y0*sc),int(x1*sc),int(y1*sc)
    sub = img[Y0:Y1, X0:X1].reshape(-1,3)
    cnt = Counter(tuple(p//8*8) for p in sub)
    top = sorted(cnt.items(), key=lambda kv:-kv[1])[:6]
    print(f"   {tag}: " + ", ".join("#%02X%02X%02X(%d)"%(k[0],k[1],k[2],v) for k,v in top))

print("== orig stop cell x590..634 y501..522 =="); census(orig, 1, 590,501,634,522, "orig stop")
print("== render stop cell =="); census(ren, SX, 590,501,634,522, "render stop")
print("== orig '5' cell (last value col) x590..634 y336..374 =="); census(orig, 1, 590,336,634,374, "orig 5-cell")
print("== orig '3' cell (first value col) x152..194 y336..374 =="); census(orig, 1, 152,336,194,374, "orig 3-cell")
print("== render '5' cell =="); census(ren, SX, 590,336,634,374, "render 5-cell")
# dark glyph count in orig 5-cell (is there a '5' glyph?)
for nm, img, sc in (("orig",orig,1),("render",ren,SX)):
    X0,Y0,X1,Y1 = int(590*sc),int(336*sc),int(634*sc),int(374*sc)
    sub = img[Y0:Y1, X0:X1]
    m = sub.sum(axis=2) < 500
    ys,xs = np.nonzero(m)
    if len(xs):
        print(f"   {nm} 5-cell glyph ink bbox: x{(X0+xs.min())/sc:.0f}..{(X0+xs.max())/sc:.0f} y{(Y0+ys.min())/sc:.0f}..{(Y0+ys.max())/sc:.0f} n={int(m.sum())}")
