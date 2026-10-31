import sys, numpy as np
from PIL import Image

def boxes(n, thr=175, ring=6, gapy=3, gapx=5, minpix=12):
    a = np.asarray(Image.open('unique_slides/slide_%03d.jpg' % n).convert('RGB')).astype(int)
    H, W, _ = a.shape
    g = a.mean(axis=2)
    d = g < thr
    # kill frame border rows/cols measured
    d[:46,:] = False; d[536:,:] = False; d[:,:40] = False; d[:,918:] = False
    # row segments -> text lines
    rows = d.sum(axis=1)
    segs = []; inb = False
    for y, v in enumerate(rows):
        if v >= minpix and not inb: s = y; inb = True
        elif v < minpix and inb:
            if segs and s - segs[-1][1] - 1 <= gapy: segs[-1][1] = y-1
            else: segs.append([s, y-1])
            inb = False
    if inb:
        if segs and s - segs[-1][1] - 1 <= gapy: segs[-1][1] = H-1
        else: segs.append([s, H-1])
    out = []
    for (y0, y1) in segs:
        sub = d[y0:y1+1, :]
        cols = sub.sum(axis=0)
        cs = []; inb = False
        for x, v in enumerate(cols):
            if v > 0 and not inb: s = x; inb = True
            elif v == 0 and inb:
                if cs and s - cs[-1][1] - 1 <= gapx: cs[-1][1] = x-1
                else: cs.append([s, x-1])
                inb = False
        if inb:
            if cs and s - cs[-1][1] - 1 <= gapx: cs[-1][1] = W-1
            else: cs.append([s, W-1])
        for (x0, x1) in cs:
            if x1-x0+1 >= minpix:
                out.append((x0, y0, x1, y1))
    return a.shape, out

for n in [int(x) for x in sys.argv[1:]]:
    (H, W, _), bs = boxes(n)
    print('=== slide %03d  %d line-boxes' % (n, len(bs)))
    for (x0,y0,x1,y1) in bs:
        print('  x %4d-%4d (%.3f-%.3f)  y %4d-%4d (%.3f-%.3f)  %dx%d'
              % (x0,x1,x0/W,x1/W,y0,y1,y0/H,y1/H,x1-x0+1,y1-y0+1))
