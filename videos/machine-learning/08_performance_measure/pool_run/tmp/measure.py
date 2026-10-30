import sys
from PIL import Image
import numpy as np

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

blue = (B - R > 40) & (R < 160)
black = (R < 110) & (G < 110) & (B < 140) & ~blue
red = (R - G > 50) & (R - B > 50)

def bands(mask, name, y0=0, y1=None):
    if y1 is None:
        y1 = H
    rows = mask[y0:y1].any(axis=1)
    out = []
    inb = False
    start = 0
    for i, v in enumerate(rows):
        if v and not inb:
            start = i
            inb = True
        elif not v and inb:
            out.append((start + y0, i - 1 + y0))
            inb = False
    if inb:
        out.append((start + y0, y1 - 1))
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] <= 4:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b) if False else (b[0], b[1]))
    merged = [list(m) for m in merged]
    print(f"--- {name} ---")
    for (s, e) in merged:
        sub = mask[s:e + 1]
        cols = sub.any(axis=0)
        idx = np.where(cols)[0]
        print(f"  y={s}-{e} (h={e-s+1}) x={idx.min()}-{idx.max()} (w={idx.max()-idx.min()+1})")
    return merged

bands(blue, "BLUE", 100, 540)
bands(black, "BLACK", 100, 540)
bands(red, "RED", 0, 540)
