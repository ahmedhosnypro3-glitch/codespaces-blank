import sys, numpy as np
from PIL import Image

def masks(n):
    a = np.asarray(Image.open('unique_slides/slide_%03d.jpg' % n).convert('RGB')).astype(int)
    R,G,B = a[:,:,0], a[:,:,1], a[:,:,2]
    g = a.mean(axis=2)
    red_frame = (R>110)&(R<200)&(G<70)&(B<70)          # C00000-family
    yellow    = (R>200)&(G>190)&(B<190)                 # FFF9C4 badge
    dark      = g<170                                    # text / lines (body ink)
    bodydark  = dark & ~red_frame & ~yellow
    return a, (red_frame, yellow, bodydark, g), a.shape

def bands(v, gap, minlen=1):
    out=[]; inb=False
    for i,x in enumerate(v):
        if x>minlen-1 and not inb: s=i; inb=True
        elif x<=minlen-1 and inb:
            if out and s-out[-1][1]-1 <= gap: out[-1][1]=i-1
            else: out.append([s,i-1])
            inb=False
    if inb:
        if out and s-out[-1][1]-1 <= gap: out[-1][1]=len(v)-1
        else: out.append([s,len(v)-1])
    return out

def report(n):
    a, (rf,yw,bd,g),(H,W,_) = masks(n)
    print('=== slide %03d %dx%d red_frame=%d yellow=%d bodydark=%d frac=%.4f'
          % (n,W,H,rf.sum(),yw.sum(),bd.sum(),bd.sum()/(W*H)))
    rows = bd.sum(axis=1)
    print(' body row bands (y0-y1 : norm y):')
    for b in bands(rows, 8, 3)[:45]:
        print('   %4d-%4d   %.4f-%.4f' % (b[0],b[1],b[0]/H,b[1]/H))
    cols = bd.sum(axis=0)
    print(' body col bands (x0-x1 : norm x):')
    for b in bands(cols, 10, 3)[:45]:
        print('   %4d-%4d   %.4f-%.4f' % (b[0],b[1],b[0]/W,b[1]/W))
    # red frame geometry
    ys,xs = np.where(rf)
    if len(ys): print(' red frame bbox x %d-%d (%.4f-%.4f) y %d-%d (%.4f-%.4f)'
                      % (xs.min(),xs.max(),xs.min()/W,xs.max()/W,ys.min(),ys.max(),ys.min()/H,ys.max()/H))
    ys,xs = np.where(yw)
    if len(ys): print(' yellow badge bbox x %d-%d y %d-%d (norm %.4f,%.4f-%.4f,%.4f)'
                      % (xs.min(),xs.max(),ys.min(),ys.max(),xs.min()/W,xs.max()/W,ys.min()/H,ys.max()/H))

for n in [int(x) for x in sys.argv[1:]]:
    report(n)
