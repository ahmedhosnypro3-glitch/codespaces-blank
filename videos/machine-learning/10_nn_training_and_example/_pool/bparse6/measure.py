import sys, numpy as np
from PIL import Image

def load(n):
    im = Image.open('unique_slides/slide_%03d.jpg' % n).convert('RGB')
    return np.asarray(im).astype(int), im.size

def ink_profile(a, thr=150):
    # dark-ish ink mask
    g = a.mean(axis=2)
    m = g < thr
    return m

def report(n):
    a, (W,H) = load(n)
    m = ink_profile(a)
    print('=== slide %03d  %dx%d  ink_frac=%.4f' % (n, W, H, m.mean()))
    # row bands of ink
    rows = m.sum(axis=1)
    bands=[]
    inb=False
    for y,v in enumerate(rows):
        if v>0 and not inb: s=y; inb=True
        elif v==0 and inb: bands.append((s,y-1,int(rows[s:y].max()))); inb=False
    if inb: bands.append((s,H-1,int(rows[s:H].max())))
    # merge bands separated by <4 px
    merged=[]
    for b in bands:
        if merged and b[0]-merged[-1][1] <= 4:
            merged[-1] = (merged[-1][0], b[1], max(merged[-1][2], b[2]))
        else:
            merged.append(list(b) if False else (b[0],b[1],b[2]))
    merged=[list(x) for x in merged]
    out=[]
    for b in merged:
        if out and b[0]-out[-1][1] <= 4:
            out[-1][1]=b[1]; out[-1][2]=max(out[-1][2],b[2])
        else: out.append(list(b))
    print(' row bands (y0,y1,maxrowink, norm_y):')
    for b in out[:40]:
        print('   %4d-%4d  %4d   %.4f-%.4f' % (b[0],b[1],b[2],b[0]/H,b[1]/H))
    # column bands
    cols = m.sum(axis=0)
    cb=[]; inb=False
    for x,v in enumerate(cols):
        if v>0 and not inb: s=x; inb=True
        elif v==0 and inb: cb.append((s,x-1)); inb=False
    if inb: cb.append((s,W-1))
    merged=[]; 
    for b in cb:
        if merged and b[0]-merged[-1][1] <= 6: merged[-1][1]=b[1]
        else: merged.append([b[0],b[1]])
    print(' col bands (x0,x1, norm_x):')
    for b in merged[:40]:
        print('   %4d-%4d   %.4f-%.4f' % (b[0],b[1],b[0]/W,b[1]/W))

for n in [int(x) for x in sys.argv[1:]]:
    report(n)
