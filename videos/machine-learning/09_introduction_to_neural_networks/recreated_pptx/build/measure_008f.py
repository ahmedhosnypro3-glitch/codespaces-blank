#!/usr/bin/env python3
"""Connected-component ground truth of the ORIGINAL slide_008 in-plot elements."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(ORIG).convert("RGB").resize((960, 540), Image.LANCZOS)
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

# plot interior (measured border x=166..800, y=122..508); inset 6px to skip border
PL = 172; PR = 794; PT = 128; PB = 502

def components(name, mask, minsize=20, maxsize=100000):
    lbl, n = ndi.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lbl == i)
        if len(xs) < minsize or len(xs) > maxsize:
            continue
        out.append((xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
    out.sort(key=lambda t: -t[4])
    print(f"{name}: {len(out)} components (top 14 by size)")
    for x0, x1, y0, y1, n in out[:14]:
        print(f"   px x[{x0},{x1}] y[{y0},{y1}] n={n}  center=({(x0+x1)//2},{(y0+y1)//2})")
        print(f"        in = ({(x0+x1)/2*13.33/960:.2f}, {(y0+y1)/2*7.5/540:.2f})in size={(x1-x0)*13.33/960:.2f}x{(y1-y0)*7.5/540:.2f}in")
    return out

interior = np.zeros_like(r, dtype=bool)
interior[PT:PB, PL:PR] = True

# green dots: distinct green where g is max and clearly above r,b
green = (g > 150) & (g > r + 20) & (g > b + 20) & interior
blue = (b > 130) & (b > r + 15) & (b > g + 15) & interior
red = (r > 140) & (r > g + 25) & (r > b + 25) & interior
yellow = (r > 180) & (g > 160) & (b < g - 60) & interior
orange = (r > 170) & (g > 90) & (g < r - 45) & (b < g - 25) & interior

print(f"plot interior px: x[{PL},{PR}] y[{PT},{PB}]")
components("GREEN (C1 dots + d3 line)", green, minsize=15)
components("BLUE (C2 dots + d2 line)", blue, minsize=15)
components("RED (C3 dots + d1 line)", red, minsize=15)
components("YELLOW boxes", yellow, minsize=25)
components("ORANGE ? boxes", orange, minsize=12)
