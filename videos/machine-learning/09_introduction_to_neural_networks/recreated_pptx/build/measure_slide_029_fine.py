#!/usr/bin/env python3
"""Fine scan: red-ish frame lines, key boxes, text bands."""
from PIL import Image
import numpy as np

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_029.jpg").convert("RGB")
W, H = img.size
a = np.asarray(img).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# red-dominant: R notably > G and R > B
redmask = (R > 120) & (R - G > 55) & (R - B > 55)
print("red-dominant px:", redmask.sum())

# column histogram of red-dominant
colsum = redmask.sum(axis=0)
rowsum = redmask.sum(axis=1)

# find long horizontal red runs (frame top/bottom edges) -> rows with many red px
print("\nrows with >200 red px (frame edges):")
for y in range(H):
    if rowsum[y] > 200:
        xs = np.where(redmask[y])[0]
        print(f"  y={y} pct={y/H*100:.1f} n={rowsum[y]} xspan={xs.min()}-{xs.max()} pct={xs.min()/W*100:.1f}-{xs.max()/W*100:.1f}")

print("\ncols with >100 red px (frame left/right edges + error bar):")
for x in range(W):
    if colsum[x] > 100:
        ys = np.where(redmask[:,x])[0]
        print(f"  x={x} pct={x/W*100:.1f} n={colsum[x]} yspan={ys.min()}-{ys.max()} pct={ys.min()/H*100:.1f}-{ys.max()/H*100:.1f}")

# magenta-ish: R,B high, G lower
magmask = (R > 150) & (B > 150) & (G < R - 40)
print("\nmagenta px:", magmask.sum())
cols = np.where(magmask.sum(axis=0) > 30)[0]
rows = np.where(magmask.sum(axis=1) > 30)[0]
if len(cols): print("  magenta cols:", cols.min(), cols.max())
if len(rows): print("  magenta rows:", rows.min(), rows.max())
# find the two magenta boxes: cluster columns
mcols = magmask.sum(axis=0)
runs=[]; inr=False
for x in range(W):
    if mcols[x]>30:
        if not inr: st=x; inr=True
    else:
        if inr: runs.append((st,x-1)); inr=False
if inr: runs.append((st,W-1))
print("  magenta col runs:", [(r[0],r[1],round(r[0]/W*100,1),round(r[1]/W*100,1)) for r in runs])
mrows = magmask.sum(axis=1)
runs=[]; inr=False
for y in range(H):
    if mrows[y]>30:
        if not inr: st=y; inr=True
    else:
        if inr: runs.append((st,y-1)); inr=False
if inr: runs.append((st,H-1))
print("  magenta row runs:", [(r[0],r[1],round(r[0]/H*100,1),round(r[1]/H*100,1)) for r in runs])

# green-dominant
gmask = (G > 110) & (G - R > 40) & (G - B > 25)
print("\ngreen px:", gmask.sum())
gcols = gmask.sum(axis=0)
runs=[]; inr=False
for x in range(W):
    if gcols[x]>25:
        if not inr: st=x; inr=True
    else:
        if inr: runs.append((st,x-1)); inr=False
if inr: runs.append((st,W-1))
print("  green col runs:", [(r[0],r[1],round(r[0]/W*100,1),round(r[1]/W*100,1)) for r in runs])

# near-black text density per band (find text rows)
dark = (R<90)&(G<90)&(B<90)
rowsum_d = dark.sum(axis=1)
print("\nrow-band text density (every 10 rows):")
for y in range(0, H, 10):
    n = dark[y:y+10].sum()
    print(f"  y={y:3d}-{y+10:3d} pct={y/H*100:4.1f} darkpx={n}")

# bottom black letterbox bar
print("\nbottom 30 rows mean luminance:")
lum = a.mean(axis=2)
for y in range(H-30, H, 5):
    print(f"  y={y}: mean={lum[y].mean():.0f}")
