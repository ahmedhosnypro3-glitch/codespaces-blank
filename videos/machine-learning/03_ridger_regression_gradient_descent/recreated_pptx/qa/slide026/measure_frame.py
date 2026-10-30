#!/usr/bin/env python3
"""PIL broad census of unique_slides/slide_026.jpg (960x540, 1px=1pt).
Slide: title 'Gradient Descent Solution', badge 26, blue-bordered white content
box, red section headers, blue algorithm steps [1..3], black Notes bullets.
Pass 1: color-class census + band clustering per class.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
print("size:", W, "x", H)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
# blue: strong blue dominance (0000FF family, JPEG-darkened ok)
blue = (b > 90) & ((b - r) > 40) & ((b - g) > 40)
yel = (r > 200) & (g > 200) & (b < 190)
dark = (r < 100) & (g < 100) & (b < 100)
white = (r > 245) & (g > 245) & (b > 245)
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
pur = (b > 150) & (r > 70) & (r < 180) & (g < 130)

for name, m in [("red", red), ("blue", blue), ("yellow", yel), ("dark", dark),
                ("purple", pur), ("white", white), ("gray", gray)]:
    ys, xs = np.where(m)
    if len(ys):
        print(f"{name}: {m.sum()} px  bbox x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}")
    else:
        print(f"{name}: 0 px")

def bands(mask, label, min_gap=3, min_px=4):
    """cluster rows of a mask into contiguous bands; report per-band bbox+px"""
    rows = np.where(mask.sum(axis=1) > 0)[0]
    print(f"\n== {label} row bands ==")
    if not len(rows):
        print("  none")
        return []
    out = []
    start = prev = rows[0]
    for y in rows[1:]:
        if y > prev + min_gap:
            out.append((start, prev)); start = y
        prev = y
    out.append((start, prev))
    for (y0, y1) in out:
        band = mask[y0:y1 + 1]
        cols = np.where(band.any(axis=0))[0]
        if band.sum() < min_px:
            continue
        print(f"  band y {y0}-{y1} h={y1-y0+1}  x {cols.min()}-{cols.max()} (w={cols.max()-cols.min()+1})  px={int(band.sum())}")
    return out

# RED: title + section headers; exclude chrome strokes (cols<64, cols>894, rows>533)
tr = red.copy()
tr[:, :64] = False; tr[:, 895:] = False; tr[534:, :] = False; tr[:40, :] = False
bands(tr, "RED ink (excl chrome strokes)")

# YELLOW: badge
ys, xs = np.where(yel)
if len(ys):
    print(f"\nyellow badge bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} center ({(xs.min()+xs.max())/2},{(ys.min()+ys.max())/2}) d={xs.max()-xs.min()+1}")

# BLUE: border box + text. First find long vertical/horizontal runs (border).
print("\n== BLUE structure ==")
colprof = blue.sum(axis=0)  # per-column count
# candidate border verticals: columns with >100 blue px
vcands = [x for x in range(W) if colprof[x] > 100]
print("blue-heavy columns (px>100):", vcands[:20], "..." if len(vcands) > 20 else "")
rowprof = blue.sum(axis=1)
hcands = [y for y in range(H) if rowprof[y] > 100]
print("blue-heavy rows (px>100):", hcands[:20], "..." if len(hcands) > 20 else "")

# Long horizontal runs per row (border top/bottom edges are ~700px runs)
print("\nrows with a blue run >= 300 px:")
for y in range(H):
    xs_b = np.where(blue[y])[0]
    if len(xs_b) == 0:
        continue
    # longest contiguous run
    runs = []
    s = xs_b[0]; p = xs_b[0]
    for x in xs_b[1:]:
        if x > p + 2:
            runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    longest = max(runs, key=lambda rr: rr[1] - rr[0])
    if longest[1] - longest[0] >= 300:
        print(f"  row {y}: run x {longest[0]}..{longest[1]} (len {longest[1]-longest[0]+1})")

print("\ncolumns with a blue run >= 200 px:")
for x in range(W):
    ys_b = np.where(blue[:, x])[0]
    if len(ys_b) == 0:
        continue
    runs = []
    s = ys_b[0]; p = ys_b[0]
    for y in ys_b[1:]:
        if y > p + 2:
            runs.append((s, p)); s = y
        p = y
    runs.append((s, p))
    longest = max(runs, key=lambda rr: rr[1] - rr[0])
    if longest[1] - longest[0] >= 200:
        print(f"  col {x}: run y {longest[0]}..{longest[1]} (len {longest[1]-longest[0]+1})")

# BLUE text bands: exclude the border columns/rows region -> mask inside-box text
# (will fill exact box bounds in pass 2; for now exclude heavy border cols/rows)
bt = blue.copy()
for x in vcands:
    bt[:, x] = False
for y in hcands:
    bt[y, :] = False
bands(bt, "BLUE ink (excl heavy border rows/cols)")

# DARK ink: notes text; exclude badge window (badge center 876,73 d~35)
dk = dark.copy()
dk[50:100, 855:900] = False  # badge numeral zone
bands(dk, "DARK ink (excl badge)")

# WHITE regions: content box fill is white on gray panel — find large white area
print("\n== WHITE area census (rows with >400 white px inside panel x64..894) ==")
wcount = white[:, 64:895].sum(axis=1)
wrows = np.where(wcount > 400)[0]
if len(wrows):
    # contiguous clusters
    start = prev = wrows[0]; cl = []
    for y in wrows[1:]:
        if y > prev + 3:
            cl.append((start, prev)); start = y
        prev = y
    cl.append((start, prev))
    for (y0, y1) in cl:
        band = white[y0:y1 + 1, 64:895]
        cols = np.where(band.any(axis=0))[0] + 64
        print(f"  white band y {y0}-{y1} (h={y1-y0+1}) x {cols.min()}-{cols.max()}")
else:
    print("  none >400")
