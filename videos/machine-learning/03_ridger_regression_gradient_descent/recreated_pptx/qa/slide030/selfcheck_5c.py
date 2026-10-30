import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
def bbox(fx0,fy0,fx1,fy1): return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))

print("== ITER TABLE vertical gridlines in ORIGINAL (x-row band region) ==")
dark = orig.sum(axis=2) < 450
colcnt = dark[340:520, 70:660].sum(axis=0)
vlines = [70+i for i, c in enumerate(colcnt) if c > 120]
groups = []
for x in vlines:
    if groups and x - groups[-1][-1] <= 2: groups[-1].append(x)
    else: groups.append([x])
vc = [int(round(sum(g)/len(g))) for g in groups]
print("   vline centers:", vc)

print("== X-ROW band: red-pixel x-runs (orig vs render) ==")
def redruns(img, sc, tag):
    if tag == 'render':
        x0,x1,y0,y1 = bbox(86,334,636,356)
    else:
        x0,x1,y0,y1 = 86,334,636,356
    sub = img[y0:y1, x0:x1]
    R,G,B = sub[:,:,0], sub[:,:,1], sub[:,:,2]
    m = (R>120)&(G<100)&(B<110)
    xs = np.nonzero(m.any(axis=0))[0]
    runs = []
    if len(xs):
        s = xs[0]; p = xs[0]
        for v in xs[1:]:
            if v-p > 3: runs.append((s,p)); s=v
            p = v
        runs.append((s,p))
    print(f"   {tag}: red x-runs (frame px): " + str([(round((x0+a)/sc[0],0), round((x0+b)/sc[0],0)) for a,b in runs]))
redruns(orig, (1,1), 'orig')
redruns(ren, (SX,SY), 'render')

print("== x-row cell ink colors per cell (darkest-pixel census, orig) ==")
for i, vx in enumerate(vc[:-1]):
    cx0, cx1 = vx+3, vc[i+1]-3
    sub = orig[337:354, cx0:cx1].reshape(-1,3)
    red = ((sub[:,0]>120)&(sub[:,1]<100)&(sub[:,2]<110)).sum()
    blk = ((sub.sum(axis=1))<420).sum()
    tot = len(sub)
    print(f"   cell{i:2d} x{cx0}..{cx1}: red={red} black={blk}")

print("== TITLE ink extent excluding left stroke (crop x64..565) ==")
def inkbbox(img, box, sx, sy):
    x0,y0,x1,y1 = box
    sub = img[y0:y1, x0:x1]
    m = (sub.sum(axis=2) < 640)
    ys, xs = np.nonzero(m)
    if not len(xs): return None
    return (round((x0+xs.min())/sx,1), round((y0+ys.min())/sy,1), round((x0+xs.max())/sx,1), round((y0+ys.max())/sy,1), int(m.sum()))
print("   render:", inkbbox(ren, bbox(64,50,565,100), SX, SY))
print("   orig  :", inkbbox(orig, (64,50,565,100), 1, 1))
