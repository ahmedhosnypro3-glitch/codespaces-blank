"""Title shift (exact resize) + full iteration-table cell census (fill + text color)."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540

# ---------- title shift ----------
def band_exact(img, scx, scy, y0, y1, x0, x1, thr):
    X0, X1 = int(round(x0*scx)), int(round(x1*scx))
    Y0, Y1 = int(round(y0*scy)), int(round(y1*scy))
    sub = img[Y0:Y1, X0:X1]
    m = (sub.sum(axis=2) < thr)
    im2 = Image.fromarray((m*255).astype(np.uint8)).resize((x1-x0, y1-y0), Image.LANCZOS)
    return np.asarray(im2) > 60

R = band_exact(ren, SX, SY, 55, 105, 60, 570, 700)
O = band_exact(orig, 1, 1, 55, 105, 60, 570, 700)
best = None
for dy in range(-14, 15):
    for dx in range(-30, 11):
        h, w = O.shape
        ys0, xs0 = max(0, dy), max(0, dx)
        ys1, xs1 = min(h, h+dy), min(w, w+dx)
        if ys1-ys0 < 12 or xs1-xs0 < 20: continue
        A = O[ys0:ys1, xs0:xs1]
        B = R[ys0-dy:ys1-dy, xs0-dx:xs1-dx]
        score = (A ^ B).sum()
        if best is None or score < best[0]:
            best = (score, dx, dy)
print(f"TITLE alignment: render ink differs from original by dx={best[1]}, dy={best[2]} (positive=render is right/down)")
print(f"   -> to align: move title box x by {-best[1]}, y by {-best[2]}  =>  x={57-best[1]}, y={62-best[2]}")

# ---------- iteration table cell census ----------
# table frame x78..654, y325..530; label col 89..150; value cols 44px from 150..634
# row bands (build): g1 y334..377 (2 rows), g2 y380..423, g3 y427..470, slope y473..497, stop y499..523
def cell_census(img, sc, tag):
    x0,x1 = int(80*sc), int(655*sc)
    y0,y1 = int(326*sc), int(530*sc)
    sub = img[y0:y1, x0:x1]
    Rr,Gg,Bb = sub[:,:,0], sub[:,:,1], sub[:,:,2]
    print(f" -- {tag} cell fills (mode) --")
    # sample row-band fill at a text-free x (between cells? just use right edge x640..652)
    for lab, ya, yb in [("g1 rows", 336, 376), ("g2", 382, 422), ("g3", 429, 469), ("slope", 475, 495), ("stop", 501, 523)]:
        s2 = img[int(ya*sc):int(yb*sc), int(636*sc):int(652*sc)].reshape(-1,3)
        cnt = {}
        for p in s2:
            k = tuple(p//16*16)
            cnt[k] = cnt.get(k,0)+1
        top = sorted(cnt.items(), key=lambda kv:-kv[1])[:2]
        print(f"   {lab:8s} y{ya}..{yb}: " + ", ".join("#%02X%02X%02X(%d)" % (k[0],k[1],k[2],v) for k,v in top))
    # text color per row: hunt saturated red text
    print(f" -- {tag} red-text x-runs per row band --")
    m = (Rr>90)&((Rr-Gg)>40)&((Rr-Bb)>10)&(int(80*sc) <= np.arange(x0,x1)[None,:]) 
    for lab, ya, yb in [("x-row",334,378),("f(x)",336,378),("x-delta",380,424),("f(x-delta)",380,424),("x+delta",427,471),("f(x+delta)",427,471),("slope",473,497),("next-x",499,523)]:
        sub2 = img[int(ya*sc):int(yb*sc), int(85*sc):int(650*sc)]
        r2,g2,b2 = sub2[:,:,0], sub2[:,:,1], sub2[:,:,2]
        mm = (r2>90)&((r2-g2)>40)&((r2-b2)>10)
        cols = np.nonzero(mm.any(axis=0))[0]
        runs=[]
        if len(cols):
            s=cols[0]; p=cols[0]
            for v in cols[1:]:
                if v-p>3: runs.append((s,p)); s=v
                p=v
            runs.append((s,p))
        rr = [(round((int(85*sc)+a)/sc), round((int(85*sc)+b)/sc)) for a,b in runs]
        print(f"   {lab:10s}: red x-runs {rr}")
    # white text on red fill? stop cell: look for white px inside red fill
    sub2 = img[int(499*sc):int(523*sc), int(588*sc):int(636*sc)]
    r2,g2,b2 = sub2[:,:,0], sub2[:,:,1], sub2[:,:,2]
    redfill = (r2>90)&((r2-g2)>40)&((r2-b2)>10)
    white = (r2>235)&(g2>235)&(b2>235)
    print(f"   stop-cell (x588..636 y499..523): red px={int(redfill.sum())} white px={int(white.sum())}")

cell_census(orig, 1, "orig")
cell_census(ren, SX, "render")
