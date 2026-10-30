#!/usr/bin/env python3
"""Measure remaining ground truth: clusters, +ve text, d-labels, Undefined/New Class boxes."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(ORIG).convert("RGB").resize((960, 540), Image.LANCZOS)
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)

PL, PR, PT, PB = 166, 800, 120, 506
def IN(x, y):
    return (x * 13.3333 / 960.0, y * 7.5 / 540.0)

def dots(mask, name, minsz=8, maxsz=500):
    lbl, n = ndi.label(mask)
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lbl == i)
        if not (minsz <= len(xs) <= maxsz):
            continue
        bw = xs.max() - xs.min() + 1
        bh = ys.max() - ys.min() + 1
        fill = len(xs) / (bw * bh)
        if fill < 0.45:      # dots are compact
            continue
        comps.append((xs.mean(), ys.mean(), len(xs), bw, bh))
    print(f"{name}: {len(comps)} compact blobs")
    for cx, cy, n, bw, bh in comps[:20]:
        print(f"   c=({cx:6.1f},{cy:6.1f})px=({IN(cx,cy)[0]:5.2f},{IN(cx,cy)[1]:5.2f})in n={n:4d} {bw}x{bh}px")

# saturated "core" colors (JPEG-washed dots still have a saturated core)
green = (g > 130) & (g > r + 30) & (g > b + 30)
blue = (b > 120) & (b > r + 30) & (b > g + 20)
orange = (r > 170) & (g > 80) & (g < r - 50) & (b < 120)

interior = np.zeros(r.shape, bool)
interior[PT:PB, PL:PR] = True
print("=== dot clusters inside plot ===")
dots(green & interior, "GREEN dots", 6, 400)
dots(blue & interior, "BLUE dots", 6, 400)
dots(orange & interior, "ORANGE ?", 10, 900)

# black text inside plot (axis lines are big; restrict to small blobs)
black = (mx < 90)
lbl, n = ndi.label(black)
print("\n=== small dark blobs inside plot (text: +ve, d1(x), d3(x), ?, C1..C3) ===")
res = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lbl == i)
    if not (10 <= len(xs) <= 900):
        continue
    if xs.min() < PL or xs.max() > PR or ys.min() < PT or ys.max() > PB:
        continue
    bw = xs.max() - xs.min() + 1
    bh = ys.max() - ys.min() + 1
    res.append((xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
res.sort(key=lambda t: (t[2], t[0]))
for x0, x1, y0, y1, n in res:
    print(f"   x[{x0},{x1}] y[{y0},{y1}] n={n:4d} center=({(x0+x1)//2},{(y0+y1)//2}) "
          f"in=({IN((x0+x1)/2,(y0+y1)/2)[0]:5.2f},{IN((x0+x1)/2,(y0+y1)/2)[1]:5.2f})")

print("\n=== Undefined box (mint, x<PL) ===")
mint = (g > r + 8) & (g > b + 5) & (g > 180) & (r > 160)
ys, xs = np.nonzero(mint & (np.arange(960)[None, :] < PL))
if len(xs):
    print(f"   x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(xs)} "
          f"in=({IN((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)[0]:5.2f},{IN((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)[1]:5.2f}) "
          f"size={(xs.max()-xs.min())*13.3333/960:.2f}x{(ys.max()-ys.min())*7.5/540:.2f}in")
else:
    print("   none")

print("=== New Class box (purple, x>PR) ===")
purple = (b > g + 12) & (r > g + 5) & (b > 170)
ys, xs = np.nonzero(purple & (np.arange(960)[None, :] > PR))
if len(xs):
    print(f"   x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(xs)} "
          f"in=({IN((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)[0]:5.2f},{IN((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)[1]:5.2f}) "
          f"size={(xs.max()-xs.min())*13.3333/960:.2f}x{(ys.max()-ys.min())*7.5/540:.2f}in")
else:
    print("   none")

print("=== bottom bar structure (rows 519-539) ===")
bar = a[519:540]
print("   row 525 unique-ish colors:", np.unique(bar[6].reshape(-1, 3), axis=0)[:6].tolist())
print("   col profile dark runs: ", [(x, int((bar[:, x].max(axis=1) < 60).sum())) for x in range(0, 960, 60)])
