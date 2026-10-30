import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
def bbox(fx0,fy0,fx1,fy1): return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))

print("== TITLE: per-word clusters (crop x60..565 avoids plot frame) ==")
def clusters(img, box, sc, tag):
    x0,y0,x1,y1 = box
    sub = img[y0:y1, x0:x1]
    m = sub.sum(axis=2) < 640
    colsum = m.sum(axis=0)
    runs = []; s=None
    for i,c in enumerate(colsum):
        if c>0 and s is None: s=i
        if c==0 and s is not None:
            if i-s>3: runs.append((s,i-1))
            s=None
    if s is not None: runs.append((s,len(colsum)-1))
    out=[]
    for a,b in runs:
        g = m[:, a:b+1]
        rows = np.nonzero(g.any(axis=1))[0]
        out.append((round((x0+a)/sc,1), round((x0+rows.min())/sc,1), round((x0+b)/sc,1), round((x0+rows.max())/sc,1)))
    print(f"   {tag}: " + ", ".join(f"[x{r[0]}..{r[2]} y{r[1]}..{r[3]}]" for r in out))
clusters(ren, bbox(60,50,565,100), SX, "render")
clusters(orig, (60,50,565,100), 1, "orig")

print("\n== RED glyphs in x-row (y330..380), robust mask ==")
for nm, img, sc in (("render", ren, (SX,SY)), ("orig", orig, (1,1))):
    x0,y0,x1,y1 = bbox(80,330,660,380) if nm=="render" else (80,330,660,380)
    sub = img[y0:y1, x0:x1]
    R,G,B = sub[:,:,0], sub[:,:,1], sub[:,:,2]
    m = (R>110)&(R>G+40)&(R>B+25)
    ys, xs = np.nonzero(m)
    if len(xs):
        cols = np.nonzero(m.any(axis=0))[0]
        runs=[]; s=cols[0]; p=cols[0]
        for v in cols[1:]:
            if v-p>3: runs.append((s,p)); s=v
            p=v
        runs.append((s,p))
        rr = [(round((x0+a)/sc[0],0), round((x0+b)/sc[0],0), round((y0+ys[m[:,a:b+1].any(axis=1)].min())/sc[1],0)) for a,b in runs]
        print(f"   {nm}: red col-runs (x0,x1,ytop): {rr} n={len(xs)}")
    else:
        print(f"   {nm}: NO red in x-row band")

print("\n== BLACK text x-row: first/last value glyph positions (orig vs render) ==")
for nm, img, sc in (("render", ren,(SX,SY)), ("orig", orig,(1,1))):
    x0,y0,x1,y1 = bbox(80,334,660,376) if nm=="render" else (80,334,660,376)
    sub = img[y0:y1, x0:x1]
    m = sub.sum(axis=2) < 480
    colsum = m.sum(axis=0)
    runs=[]; s=None
    for i,c in enumerate(colsum):
        if c>1 and s is None: s=i
        if c<=1 and s is not None:
            if i-s>2: runs.append((s,i-1))
            s=None
    if s is not None: runs.append((s,len(colsum)-1))
    print(f"   {nm}: {len(runs)} dark runs; first 3: {[(round((x0+a)/sc[0],0),round((x0+b)/sc[0],0)) for a,b in runs[:3]]}; last 3: {[(round((x0+a)/sc[0],0),round((x0+b)/sc[0],0)) for a,b in runs[-3:]]}")
