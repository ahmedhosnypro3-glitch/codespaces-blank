import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
def bbox(fx0,fy0,fx1,fy1): return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))

print("== TITLE band column profile: ink x-runs (glyph clusters) ==")
def runs_of(mask_cols, x0, sc):
    xs = np.nonzero(mask_cols)[0]
    runs = []
    if len(xs):
        s = xs[0]; p = xs[0]
        for v in xs[1:]:
            if v-p > 4: runs.append((s,p)); s=v
            p = v
        runs.append((s,p))
    return [(round((x0+a)/sc,1), round((x0+b)/sc,1)) for a,b in runs]

# render title band y62..96
x0r,y0r,x1r,y1r = bbox(50,62,600,96)
subr = ren[y0r:y1r, x0r:x1r]
mr = subr.sum(axis=2) < 640
print("   render runs:", runs_of(mr.sum(axis=0)>0, x0r, SX))
# orig title band y62..96
subo = orig[62:96, 50:600]
mo = subo.sum(axis=2) < 640
print("   orig   runs:", runs_of(mo.sum(axis=0)>0, 50, 1))

print("\n== TITLE band y extents per cluster (orig vs render) ==")
def yruns(mask_rows, y0, sc):
    ys = np.nonzero(mask_rows)[0]
    if not len(ys): return None
    return (round((y0+ys.min())/sc,1), round((y0+ys.max())/sc,1))
print("   render:", yruns(mr.sum(axis=1)>0, y0r, SY))
print("   orig  :", yruns(mo.sum(axis=1)>0, 62, 1))

print("\n== RED X-ROW glyphs: exact scan both images ==")
# red pixels anywhere in iter-table rows 1 (y334..378)
for nm, img, sc in (("render", ren), ("orig", orig)):
    if nm=="render":
        x0,y0,x1,y1 = bbox(80,330,660,380)
    else:
        x0,y0,x1,y1 = 80,330,660,380
    sub = img[y0:y1, x0:x1]
    R,G,B = sub[:,:,0], sub[:,:,1], sub[:,:,2]
    m = (R>110)&(R>G+45)&(R>B+30)
    ys, xs = np.nonzero(m)
    if len(xs):
        print(f"   {nm}: red ink frame x{(x0+xs.min())/sc[0]:.0f}..{(x0+xs.max())/sc[0]:.0f} y{(y0+ys.min())/sc[1]:.0f}..{(y0+ys.max())/sc[1]:.0f} n={len(xs)}")
        runs = []
        cols = np.nonzero(m.any(axis=0))[0]
        s=cols[0]; p=cols[0]
        for v in cols[1:]:
            if v-p>3: runs.append((s,p)); s=v
            p=v
        runs.append((s,p))
        print(f"      col-runs: {[(round((x0+a)/sc[0],0), round((x0+b)/sc[0],0)) for a,b in runs]}")
    else:
        print(f"   {nm}: NO red ink in x-row band")
