import sys
import numpy as np
from PIL import Image
SW, SH = 13.333, 7.5
def load(p):
    im = Image.open(p).convert("RGB")
    return np.array(im).astype(int), im.size[0], im.size[1]
def inches(x0,y0,x1,y1,W,H):
    return (round(x0/W*SW,3), round(y0/H*SH,3), round(x1/W*SW,3), round(y1/H*SH,3))

def report(path, label):
    a, W, H = load(path)
    print(f"\n===== {label} =====")
    r,g,b = a[:,:,0], a[:,:,1], a[:,:,2]
    red  = (r>150)&((r-g)>60)&((r-b)>60)
    # --- top-left table: ALL red h-lines and v-lines in region x<45% y<62% ---
    x0r,x1r = 0, int(W*0.45); y0r,y1r = 0, int(H*0.62)
    sub = red[y0r:y1r, x0r:x1r]
    hs = sub.sum(axis=1); vs = sub.sum(axis=0)
    hl=[(i+x0r*0+ y0r) for i,v in enumerate(hs) if v > sub.shape[1]*0.25]
    vl=[(i+x0r) for i,v in enumerate(vs) if v > sub.shape[0]*0.20]
    def group(idx):
        out=[]; 
        for i in idx:
            if out and i-out[-1][-1]<=1: out[-1].append(i)
            else: out.append([i])
        return [(p[0],p[-1]) for p in out]
    print("TABLE red h-lines (in inches, midpoints):", [round(np.mean(p)/H*SH,3) for p in group(hl)])
    print("TABLE red v-lines (in inches, midpoints):", [round(p[0]/W*SW,3) for p in group(vl)])
    # table bbox from those
    if group(hl) and group(vl):
        hy=[p for p in group(hl)]; vx=[p for p in group(vl)]
        print("  => table x", round(vx[0][0]/W*SW,3), "to", round(vx[-1][1]/W*SW,3),
              " y", round(hy[0][0]/H*SH,3), "to", round(hy[-1][1]/H*SH,3))
    # --- plot white box: pure white, top-right quadrant ---
    white = (r>242)&(g>242)&(b>242)
    qx0,qx1,qy0,qy1 = int(W*0.40), W, int(H*0.05), int(H*0.70)
    qw = white[qy0:qy1, qx0:qx1]
    colp = qw.sum(axis=0); rowp = qw.sum(axis=1)
    gc = [i+qx0 for i,v in enumerate(colp) if v > qw.shape[0]*0.35]
    gr = [i+qy0 for i,v in enumerate(rowp) if v > qw.shape[1]*0.35]
    if gc and gr:
        print("PLOT white box (in):", inches(gc[0], gr[0], gc[-1], gr[-1], W, H))
    # --- data markers (green/cyan) ---
    green = (g>170)&(r<140)&(b<140)
    cyan  = (g>190)&(b>190)&(r<150)
    blue  = (b>150)&(r<150)&(g<150)
    for nm,m in (("GREEN",green),("CYAN",cyan)):
        mm = m.copy(); mm[:int(H*0.10),:]=False; mm[int(H*0.72):,:]=False; mm[:, :int(W*0.40)]=False
        ys,xs = np.nonzero(mm)
        if not len(xs): print(nm, "none"); continue
        pts = np.stack([xs,ys],1); used=np.zeros(len(pts),bool); cents=[]
        for i in range(len(pts)):
            if used[i]: continue
            d=np.hypot(pts[:,0]-pts[i,0], pts[:,1]-pts[i,1]); sel=(d<0.025*W)&~used
            used|=sel; cents.append((pts[sel][:,0].mean(), pts[sel][:,1].mean(), sel.sum()))
        print(f"{nm} centroids (in): " + ", ".join(f"({c[0]/W*SW:.3f},{c[1]/H*SH:.3f}) n={c[2]}" for c in cents))
    # blue line bbox within plot
    bb = blue.copy(); bb[:int(H*0.10),:]=False; bb[int(H*0.72):,:]=False; bb[:,:int(W*0.40)]=False
    ys,xs=np.nonzero(bb)
    if len(xs): print("BLUE line bbox (in):", inches(xs.min(),ys.min(),xs.max(),ys.max(),W,H))
    # --- peach fill (exact) ---
    peach = (r>248)&(g>215)&(g<240)&(b>180)&(b<215)
    ys,xs=np.nonzero(peach)
    if len(xs)>200: print("PEACH box (in):", inches(xs.min(),ys.min(),xs.max(),ys.max(),W,H), f"n={len(xs)}")
    else: print("PEACH: n=", len(xs))
    # --- light blue sigma circle ---
    lblue = (r>150)&(r<210)&(g>190)&(b>215)
    ys,xs=np.nonzero(lblue)
    if len(xs)>50: print("SIGMA circle lightblue (in):", inches(xs.min(),ys.min(),xs.max(),ys.max(),W,H))
    # --- plum box ---
    plum = (r>190)&(r<240)&(g>140)&(g<190)&(b>190)&(b<235)
    ys,xs=np.nonzero(plum)
    if len(xs)>50: print("PLUM box (in):", inches(xs.min(),ys.min(),xs.max(),ys.max(),W,H))
    # --- bottom black bar ---
    dark = (r<70)&(g<70)&(b<70)
    prow = dark.sum(axis=1)
    rows=[i for i,v in enumerate(prow) if v>W*0.5]
    if rows: print("DARK bar rows y (in):", round(rows[0]/H*SH,3), "to", round(rows[-1]/H*SH,3))
    # --- title ink bbox (red text, top band) ---
    tband = red[:int(H*0.20), int(W*0.05):int(W*0.95)]
    ys,xs=np.nonzero(tband)
    if len(xs): print("TITLE red ink (in):", inches(xs.min()+int(W*0.05), ys.min(), xs.max()+int(W*0.05), ys.max(), W, H))
    # --- badge: yellow circle top-right ---
    yellow = (r>230)&(g>225)&(b>170)&(b<215)
    ys,xs=np.nonzero(yellow)
    if len(xs)>50: print("YELLOW badge (in):", inches(xs.min(),ys.min(),xs.max(),ys.max(),W,H), f"n={len(xs)}")

report(sys.argv[1], "ORIGINAL")
report(sys.argv[2], "RENDER")
