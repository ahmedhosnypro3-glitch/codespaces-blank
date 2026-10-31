import sys, json
from PIL import Image
import numpy as np

def load(n):
    return Image.open(f'unique_slides/slide_{n}.jpg').convert('RGB')

def ink_mask(im):
    a = np.asarray(im).astype(int)
    # dark ink: well below background gray 232
    dark = (a.sum(2) < 480)
    # red ink (house frame + red text)
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    red = (r > 110) & (r - g > 45) & (r - b > 45)
    return dark, red

def row_bands(mask, min_px=8):
    rows = mask.sum(1)
    bands=[]; s=None
    for y,v in enumerate(rows):
        if v>=min_px and s is None: s=y
        elif v<min_px and s is not None:
            bands.append((s,y-1,int(rows[s:y].max()))); s=None
    if s is not None: bands.append((s,len(rows)-1,int(rows[s:].max())))
    return bands

def col_bands(mask, y0,y1, min_px=3):
    sub = mask[y0:y1+1]
    cols = sub.sum(0)
    bands=[]; s=None
    for x,v in enumerate(cols):
        if v>=min_px and s is None: s=x
        elif v<min_px and s is not None:
            bands.append((s,x-1,int(cols[s:x].max()))); s=None
    if s is not None: bands.append((s,len(cols)-1,int(cols[s:].max())))
    return bands

for n in sys.argv[1:]:
    im = load(n); W,H = im.size
    dark, red = ink_mask(im)
    a = np.asarray(im).astype(int)
    print(f"=== slide {n}  {W}x{H} ===")
    print("  bg median:", [int(v) for v in np.median(a.reshape(-1,3),axis=0)])
    ys,xs = np.where(red)
    if len(xs): print(f"  red ink bbox: x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}  n={len(xs)}")
    # exclude outer red frame band from dark analysis
    d = dark.copy()
    d[:40,:] = False; d[H-30:,:] = False; d[:,:50] = False; d[:,W-40:] = False
    print("  dark row bands (y0,y1,maxpx):")
    for b in row_bands(d):
        print("    ", b, "-> y_norm %.4f-%.4f" % (b[0]/H, b[1]/H))
    # per-band col extents for the first few bands
    for b in row_bands(d)[:14]:
        cb = col_bands(d, b[0], b[1])
        if cb:
            print(f"      band y{b[0]}-{b[1]} cols {cb[0][0]}-{cb[-1][1]}  segments={len(cb)}")
