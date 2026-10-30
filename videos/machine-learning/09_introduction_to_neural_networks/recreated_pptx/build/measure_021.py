"""PIL measurements of original slide_021.jpg (960x540) -> fractions of frame + inches."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
FW, FH = W, H           # frame px
IN = 13.3333            # slide inches wide
ppf = IN / FW           # inches per frame px


def ink_mask(sub, thresh=25):
    """relative-ink mask vs local background (median of the sub-image)"""
    bg = np.median(sub.reshape(-1, 3), axis=0)
    return (np.abs(sub - bg).max(axis=2) > thresh)


def bbox_frac(sub, mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (xs.min(), ys.min(), xs.max(), ys.max())


# ---- 1. red frame (thin red rectangle) ----
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110) & (r - g > 50) & (r - b > 50)
# exclude the bottom black bar rows and plot red lines inside boxes:
# find long horizontal red runs per row (frame stroke)
rowcount = red.sum(axis=1)
colcount = red.sum(axis=0)
print("=== RED FRAME ===")
for y in range(H):
    if rowcount[y] > 300:
        xs = np.where(red[y])[0]
        print(f"  row y={y} n={rowcount[y]} x=[{xs.min()},{xs.max()}]")
print("  cols with >200 red px:")
for x in range(W):
    if colcount[x] > 200:
        ys = np.where(red[:, x])[0]
        print(f"  col x={x} n={colcount[x]} y=[{ys.min()},{ys.max()}]")

# ---- 2. blue/indigo graph borders ----
blue = (b > 110) & (b - r > 45) & (b - g > 25)
print("\n=== BLUE BORDERS ===")
bcols = blue.sum(axis=0)
brows = blue.sum(axis=1)
print("  rows with >250 blue px:", [ (y,int(brows[y])) for y in range(H) if brows[y] > 250 ][:40])
print("  cols with >250 blue px:", [ (x,int(bcols[x])) for x in range(W) if bcols[x] > 250 ][:40])

# ---- 3. pink formula boxes ----
pink = (r > 235) & (g > 200) & (g < 245) & (b > 200) & (b < 250) & (r - g > 8) & (r - b > 8)
print("\n=== PINK BOXES ===")
prows = pink.sum(axis=1)
pcols = pink.sum(axis=1)
runs = []
inrun = False
for y in range(H):
    if prows[y] > 120 and not inrun:
        start = y; inrun = True
    elif prows[y] <= 120 and inrun:
        runs.append((start, y)); inrun = False
if inrun: runs.append((start, H))
print("  y-bands:", runs)
for (y0, y1) in runs:
    band = a[y0:y1]
    m = (band[:, :, 0] > 235) & (band[:, :, 1] > 200) & (band[:, :, 0] - band[:, :, 1] > 8)
    xs = np.where(m.sum(axis=0) > (y1 - y0) * 0.4)[0]
    if len(xs):
        print(f"   band y {y0}-{y1}: x [{xs.min()},{xs.max()}] "
              f"-> frac x {xs.min()/FW:.3f}-{xs.max()/FW:.3f}, y {y0/FH:.3f}-{y1/FH:.3f}, "
              f"in x {xs.min()*ppf:.2f}-{xs.max()*ppf:.2f}, y {y0*ppf:.2f}-{y1*ppf:.2f}")

# ---- 4. black bottom bar ----
print("\n=== BLACK BAR ===")
dark = (r < 60) & (g < 60) & (b < 60)
drows = dark.sum(axis=1)
for y in range(H):
    if drows[y] > 400:
        print(f"  row y={y} n={drows[y]}")

# ---- 5. yellow badge ----
print("\n=== YELLOW BADGE ===")
yel = (r > 225) & (g > 215) & (b < 200) & (r - b > 60)
ys_, xs_ = np.where(yel)
if len(xs_):
    # cluster top-right
    m = (xs_ > 700) & (ys_ < 120)
    if m.sum():
        print(f"  badge x [{xs_[m].min()},{xs_[m].max()}] y [{ys_[m].min()},{ys_[m].max()}] "
              f"-> frac ({xs_[m].min()/FW:.3f},{ys_[m].min()/FH:.3f})-({xs_[m].max()/FW:.3f},{ys_[m].max()/FH:.3f}) "
              f"in ({xs_[m].min()*ppf:.2f},{ys_[m].min()*ppf:.2f})-({xs_[m].max()*ppf:.2f},{ys_[m].max()*ppf:.2f})")

# ---- 6. distinct colors census ----
print("\n=== COLOR CENSUS (quantized) ===")
q = (a // 32 * 32).reshape(-1, 3)
from collections import Counter
cnt = Counter(map(tuple, q))
for col, n in cnt.most_common(14):
    print(f"  {col}  n={n}")
