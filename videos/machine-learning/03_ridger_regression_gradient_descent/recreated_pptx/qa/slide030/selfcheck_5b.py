import numpy as np
from PIL import Image
from collections import Counter

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
def bbox(fx0,fy0,fx1,fy1): return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))
def hexc(rgb): return '#%02X%02X%02X' % tuple(int(v) for v in rgb)

print("== 1. TITLE ink extent (crop x40..565, avoids plot frame) ==")
def inkbbox(img, box, sx, sy, mask=None):
    x0,y0,x1,y1 = box
    sub = img[y0:y1, x0:x1]
    m = (sub.sum(axis=2) < 640) if mask is None else mask(sub)
    ys, xs = np.nonzero(m)
    if not len(xs): return None
    return (round((x0+xs.min())/sx,1), round((y0+ys.min())/sy,1), round((x0+xs.max())/sx,1), round((y0+ys.max())/sy,1), int(m.sum()))
print("   render:", inkbbox(ren, bbox(40,50,565,100), SX, SY))
print("   orig  :", inkbbox(orig, (40,50,565,100), 1, 1))

print("== 2. ITER navy frame top edge: navy cols only (x76..84) y-scan ==")
def isnavy(s): return (s[:,:,2]>s[:,:,0]+30)&(s[:,:,2]>90)&(s[:,:,0]<120)
for nm, img, sc in (("render", ren,(SX,SY)), ("orig", orig,(1,1))):
    if nm=="render":
        x0,y0,x1,y1 = bbox(76,300,84,340)
    else:
        x0,y0,x1,y1 = 76,300,84,340
    sub = img[y0:y1, x0:x1]
    m = isnavy(sub)
    rows = np.nonzero(m.sum(axis=1) >= 2)[0]
    if len(rows):
        print(f"   {nm}: navy left-edge frame px y{(y0+rows.min())/sc[1]:.0f}..{(y0+rows.max())/sc[1]:.0f}")
    # horizontal top edge: cols x80..650 at y325..330
    if nm=="render":
        x0,y0,x1,y1 = bbox(80,320,650,332)
    else:
        x0,y0,x1,y1 = 80,320,650,332
    sub = img[y0:y1, x0:x1]
    m = isnavy(sub)
    rows = np.nonzero(m.sum(axis=1) >= 100)[0]
    if len(rows):
        print(f"   {nm}: navy top-edge frame px y{(y0+rows.min())/sc[1]:.0f}..{(y0+rows.max())/sc[1]:.0f}")

print("== 3. X-ROW cell colors in ORIGINAL (cells centered 172,216,...,612; y336..355) ==")
for k in range(11):
    cx = 150 + 22 + 44*k
    x0, x1 = cx-18, cx+18
    sub = orig[336:355, x0:x1].reshape(-1,3)
    cnt = Counter(hexc(p) for p in sub)
    top = cnt.most_common(3)
    print(f"   cell{k:2d} x{x0}..{x1}: " + ", ".join(f"{c}({n})" for c,n in top))
print("   -- render same cells --")
for k in range(11):
    cx = 150 + 22 + 44*k
    x0r, x1r = bbox(cx-18,336,cx+18,355)[0], bbox(cx-18,336,cx+18,355)[2]
    sub = ren[bbox(cx-18,336,cx+18,355)[1]:bbox(cx-18,336,cx+18,355)[3], x0r:x1r].reshape(-1,3)
    cnt = Counter(hexc(p) for p in sub)
    top = cnt.most_common(3)
    print(f"   cell{k:2d}: " + ", ".join(f"{c}({n})" for c,n in top))
