#!/usr/bin/env python3
"""Connected-component extraction of slide_008 diagram elements."""
from PIL import Image
import numpy as np
try:
    from scipy import ndimage
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False
print("scipy:", HAVE_SCIPY)

im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def hx(p): return "#%02X%02X%02X" % (p[0], p[1], p[2])

def components(name, cond, minpix=12):
    ys, xs = np.where(cond)
    if not len(ys):
        print(f"\n{name}: none"); return
    if not HAVE_SCIPY:
        print(f"\n{name}: n={len(ys)} (no scipy)"); return
    mask = np.zeros((H, W), bool)
    mask[ys, xs] = True
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    print(f"\n=== {name}: n={len(ys)} px, {n} components ===")
    out = []
    for i in range(1, n + 1):
        sel = lab == i
        cnt = sel.sum()
        if cnt < minpix: continue
        yy, xx = np.where(sel)
        out.append((cnt, xx.min(), xx.max(), yy.min(), yy.max(),
                    hx(a[yy[len(yy)//2], xx[len(xx)//2]])))
    out.sort(key=lambda t: -t[0])
    for cnt, x0, x1, y0, y1, col in out[:14]:
        print(f"   n={cnt:5d} x[{x0:3d},{x1:3d}] y[{y0:3d},{y1:3d}] c=({(x0+x1)//2:3d},{(y0+y1)//2:3d}) {col}")

r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
lum = a.mean(axis=2)
sat = a.max(axis=2) - a.min(axis=2)

components("RED sat (d1 line + C3 dots + red text)", (sat > 55) & (r > g + 55) & (r > b + 45))
components("BLUE sat (d2 line + C2 dots + blue text)", (sat > 55) & (b > r + 45) & (b > g + 30))
components("GREEN sat (d3 line + C1 dots)", (sat > 45) & (g > r + 40) & (g > b + 30))
components("YELLOW sat (C labels)", (sat > 70) & (r > 210) & (g > 200) & (b < 120))
components("ORANGE sat (? boxes)", (sat > 75) & (r > 200) & (g > 100) & (g < 180) & (b < 70))

# Axes: near-vertical dark-maroon line around x=309; horizontal around y=435
print("\n=== y-axis extent (col 309, dark) ===")
col = a[:, 305:314]
darkc = (col.mean(axis=2) < 190)
rows = np.where(darkc.sum(axis=1) >= 4)[0]
if len(rows):
    print(f"   dark rows {rows.min()}..{rows.max()}  sample color y=300 {hx(a[300,309])}")
print("   colors down col 309:", [(y, hx(a[y,309])) for y in [125,130,135,140,150,200,250,300,350,400,420,430,435,440,450]])

print("\n=== x-axis extent (row 435, dark) ===")
row = a[430:441]
darkr = (row.mean(axis=2) < 190)
cols = np.where(darkr.sum(axis=0) >= 4)[0]
if len(cols):
    print(f"   dark cols {cols.min()}..{cols.max()}")
print("   colors across row 435:", [(x, hx(a[435,x])) for x in [300,310,330,400,450,500,550,600,650,700,750,780,790]])

# plot panel border: scan for the thin top/bottom lines of the diagram panel
print("\n=== diagram panel border rows (full middle width) ===")
for y in range(115, 126):
    print(f"   y={y}: x=200 {hx(a[y,200])} x=400 {hx(a[y,400])} x=700 {hx(a[y,700])}")
for y in range(503, 520):
    print(f"   y={y}: x=200 {hx(a[y,200])} x=400 {hx(a[y,400])} x=700 {hx(a[y,700])}")

print("\n=== panel left/right edges ===")
for x in range(164, 174):
    print(f"   x={x}: y=200 {hx(a[200,x])} y=300 {hx(a[300,x])} y=450 {hx(a[450,x])}")
for x in range(790, 800):
    print(f"   x={x}: y=200 {hx(a[200,x])} y=300 {hx(a[300,x])} y=450 {hx(a[450,x])}")

print("\n=== title text rows (dark red) ===")
for y in range(50, 135, 4):
    row = a[y, 168:796]
    dk = (row.mean(axis=1) < 160).sum()
    print(f"   y={y}: dark={dk}")
