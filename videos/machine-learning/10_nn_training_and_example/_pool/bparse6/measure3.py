import sys, numpy as np
from PIL import Image

def body(n, ring=7):
    a = np.asarray(Image.open('unique_slides/slide_%03d.jpg' % n).convert('RGB')).astype(int)
    H,W,_ = a.shape
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    g = a.mean(axis=2)
    rf = (R>100)&(R<210)&(G<80)&(B<80)&(R-G>70)
    bd = (g<175).copy()
    ys,xs = np.where(rf)
    if len(ys):
        x0,x1,y0,y1 = xs.min(),xs.max(),ys.min(),ys.max()
        bd[max(0,y0-ring):y1+ring+1, max(0,x0-ring):x1+ring+1] = False
    # exclude yellow-ish (nodes)
    yw = (R>190)&(G>170)&(B<200)&(R-B>25)
    bd = bd & ~yw
    # exclude blue-ish and green-ish? no - keep, but report separately
    return a, bd, (H,W)

def bands(v, gap, minlen=1):
    out=[]; inb=False
    for i,x in enumerate(v):
        if x>=minlen and not inb: s=i; inb=True
        elif x<minlen and inb:
            if out and s-out[-1][1]-1 <= gap: out[-1][1]=i-1
            else: out.append([s,i-1])
            inb=False
    if inb:
        if out and s-out[-1][1]-1 <= gap: out[-1][1]=len(v)-1
        else: out.append([s,len(v)-1])
    return out

def report(n):
    a,bd,(H,W) = body(n)
    print('=== slide %03d %dx%d bodyink=%d frac=%.4f' % (n,W,H,bd.sum(),bd.sum()/(W*H)))
    print(' ROW bands (y0-y1 : norm y0-norm y1):')
    for b in bands(bd.sum(axis=1), 9, 2)[:50]:
        print('   %4d-%4d   %.4f-%.4f' % (b[0],b[1],b[0]/H,b[1]/H))
    print(' COL bands (x0-x1 : norm x0-norm x1):')
    for b in bands(bd.sum(axis=0), 12, 2)[:50]:
        print('   %4d-%4d   %.4f-%.4f' % (b[0],b[1],b[0]/W,b[1]/W))

for n in [int(x) for x in sys.argv[1:]]:
    report(n)
