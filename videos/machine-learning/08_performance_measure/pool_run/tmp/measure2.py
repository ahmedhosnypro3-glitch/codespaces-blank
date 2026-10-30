import sys
from PIL import Image
import numpy as np

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
blue = (B - R > 40) & (R < 170)
dark = (R < 130) & (G < 130) & (B < 130)

def lines(mask, y0, y1, x0, x1, label, minpix=3, gap=5):
    sub = np.zeros_like(mask)
    sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    cnt = sub.sum(axis=1)
    rows = cnt >= minpix
    raw = []
    inb = False
    for i, v in enumerate(rows):
        if v and not inb:
            st = i
            inb = True
        elif not v and inb:
            raw.append((st, i - 1))
            inb = False
    if inb:
        raw.append((st, len(rows) - 1))
    merged = []
    for b in raw:
        if merged and b[0] - merged[-1][1] <= gap:
            merged[-1][1] = b[1]
        else:
            merged.append([b[0], b[1]])
    print(f"--- {label} (y {y0}-{y1}, x {x0}-{x1}) ---")
    for (s, e) in merged:
        band = sub[s:e + 1]
        cols = band.any(axis=0)
        idx = np.where(cols)[0]
        print(f"  y={s}-{e} (h={e-s+1}) x={idx.min()}-{idx.max()} (w={idx.max()-idx.min()+1})  rowmax={band.sum(axis=1).max()}")

# Blue text lines in content area
lines(blue, 95, 500, 60, 900, "BLUE content")
# Dark text inside the two definition boxes (they are white-filled boxes with dark text)
# box regions to be refined; first scan dark ink rows with density profile in whole content area
lines(dark, 95, 500, 60, 900, "DARK content", gap=6)
# row density profiles for regions of interest
for (y0, y1, lab) in [(108, 200, "para region"), (220, 260, "tpr def"), (330, 450, "fpr def")]:
    cnt = blue[y0:y1, 60:900].sum(axis=1)
    print(f"--- profile {lab} (blue) ---")
    for i, c in enumerate(cnt):
        print(f"  y={y0+i}: {c}")
