#!/usr/bin/env python3
"""Fine-grained measurement of slide_028: element bounding boxes in 960x540 px (=pt)."""
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_028.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

def bbox(mask):
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) == 0: return None
    cols = np.where(mask.any(axis=0))[0]
    return (int(rows[0]), int(rows[-1]), int(cols[0]), int(cols[-1]))

def runs(mask, min_h=2):
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) == 0: return []
    out = []
    start = None
    for ri in range(int(rows[0]), int(rows[-1]) + 2):
        on = ri < mask.shape[0] and mask[ri].any()
        if on and start is None:
            start = ri
        elif not on and start is not None:
            if ri - start >= min_h:
                out.append((start, ri - 1))
            start = None
    res = []
    for (r0, r1) in out:
        c = mask[r0:r1+1]
        cc = np.where(c.any(axis=0))[0]
        if len(cc):
            res.append((r0, r1, int(cc[0]), int(cc[-1])))
    return res

r = a[:,:,0]; g = a[:,:,1]; b = a[:,:,2]

# --- RED text/lines (formula box border, red calc text, arrow) ---
red = (r > 150) & (r - g > 50) & (r - b > 50)
print(f"\nRED: total={red.sum()}")
print("RED runs:")
for (r0, r1, c0, c1) in runs(red, 2):
    print(f"  rows {r0}-{r1} h={r1-r0+1} cols {c0}-{c1} w={c1-c0+1}")

# --- BLUE text ---
blue = (b > 130) & (b - r > 40) & (b - g > 20)
print(f"\nBLUE: total={blue.sum()}")
print("BLUE runs:")
for (r0, r1, c0, c1) in runs(blue, 2):
    print(f"  rows {r0}-{r1} h={r1-r0+1} cols {c0}-{c1} w={c1-c0+1}")

# --- ORANGE nodes (ff6600) ---
orange = (r > 200) & (g > 80) & (g < 160) & (b < 100)
print(f"\nORANGE: total={orange.sum()}")
for (r0, r1, c0, c1) in runs(orange, 3):
    print(f"  rows {r0}-{r1} h={r1-r0+1} cols {c0}-{c1} w={c1-c0+1}")

# --- GRAY O-value boxes (c0c0c0 fill, distinct from e6e6e6 bg) ---
gray = (abs(r-g) < 12) & (abs(g-b) < 12) & (abs(r - 192) < 25)
print(f"\nGRAY(~192): total={gray.sum()}")
for (r0, r1, c0, c1) in runs(gray, 3):
    print(f"  rows {r0}-{r1} h={r1-r0+1} cols {c0}-{c1} w={c1-c0+1}")

# --- DARK ink ---
dark = (r+g+b)/3 < 90
print(f"\nDARK: total={dark.sum()}")
for (r0, r1, c0, c1) in runs(dark, 2):
    print(f"  rows {r0}-{r1} h={r1-r0+1} cols {c0}-{c1} w={c1-c0+1}")

# --- sample specific pixel colors to locate boxes ---
print("\n=== pixel samples (y, x) -> rgb ===")
for (yy, xx, tag) in [(60,890,"badge?"), (100,300,"red box border?"), (150,600,"net diagram"),
                      (200,700,"gray box?"), (430,880,"gray box?"), (300,450,"center")]:
    print(f"  ({yy},{xx}) {tag}: {tuple(a[yy,xx])}")