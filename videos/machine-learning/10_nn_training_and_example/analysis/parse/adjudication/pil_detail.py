import sys
from PIL import Image
import numpy as np

def load(n): return Image.open(f'unique_slides/slide_{n}.jpg').convert('RGB')

def bands(mask, axis, min_px):
    if axis==0: v=mask.sum(0)
    else: v=mask.sum(1)
    out=[]; s=None
    for i,x in enumerate(v):
        if x>=min_px and s is None: s=i
        elif x<min_px and s is not None: out.append((s,i-1)); s=None
    if s is not None: out.append((s,len(v)-1))
    return out

def nodeboxes(n, kind='shape'):
    im=load(n); a=np.asarray(im).astype(int); H,W,_=a.shape
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    # non-background: differs from local bg significantly
    bg=np.median(a.reshape(-1,3),axis=0)
    diff=np.abs(a-bg).sum(2)
    m=diff>70
    m[:42,:]=False; m[H-28:,:]=False; m[:,:42]=False; m[:,W-42:]=False
    return m

for n in sys.argv[1:]:
    m=nodeboxes(n); H,W=m.shape
    print(f"===== slide {n} =====")
    rs=bands(m,1,25)
    print(" strong rows (>25 px):", rs[:20])
    for (y0,y1) in rs[:12]:
        if y1-y0<3: continue
        cs=bands(m[y0:y1+1],0,2)
        segs=[c for c in cs if c[1]-c[0]>=4]
        if segs:
            print(f"  y{y0}-{y1} xsegs {segs[:14]}")
