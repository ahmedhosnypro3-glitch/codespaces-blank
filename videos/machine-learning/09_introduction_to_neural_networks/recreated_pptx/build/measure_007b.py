#!/usr/bin/env python3
"""Detailed geometry of slide_007 plot: panel, axes, hatched regions, dots, labels."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def band(mask, gap=6, minlen=1):
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) == 0: return []
    out=[]; s=rows[0]; p=rows[0]
    for r in rows[1:]:
        if r-p>gap: out.append((s,p)); s=r
        p=r
    out.append((s,p)); return out

print("=== 1. WHITE PANEL (plot area) bbox ===")
# panel = big contiguous white region not background
white = (R>238)&(G>238)&(B>238)
# exclude the slide bg (E8E8E8) — panel is FFFFFF-ish
lab, n = ndimage.label(white)
sizes = ndimage.sum(white, lab, range(1, n+1))
big = [i+1 for i in range(n) if sizes[i] > 8000]
for i in big:
    yy, xx = np.where(lab==i)
    print(f"  comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} area={len(yy)}")

print("\n=== 2. RED pixels inside panel (axes + boundary lines) ===")
red = (R>110)&(R-G>45)&(R-B>45)
# restrict to panel-ish bbox later; first print row/col bands of red in mid area
sub = red.copy(); sub[:120,:] = False   # skip title
rows = np.where(sub.any(axis=1))[0]
print("  red rows present:", rows.min(), rows.max())
rb = band(sub, gap=10, minlen=None)
print("  red row bands (gap10):", [(int(s),int(e),int(sz)) for s,e,sz in [(x[0],x[1],int(red[x[0]:x[1]+1].sum())) for x in rb]])

# Vertical red lines: columns with many red pixels between y 400-520
for ylo,yhi,name in [(130,500,"plot")]:
    colsum = red[ylo:yhi,:].sum(axis=0)
    top = np.argsort(colsum)[::-1][:12]
    print(f"  red columns {name} (y{ylo}-{yhi}) top:",
          [(int(c), int(colsum[c])) for c in sorted(top.tolist()) if colsum[c] > 20])

rowsum = red[130:520,:].sum(axis=1)
topr = np.argsort(rowsum)[::-1][:12]
print("  red rows (x>100) top:",
      [(int(130+c), int(rowsum[c])) for c in sorted(topr.tolist()) if rowsum[c] > 20])

print("\n=== 3. HATCHED REGION FILLS (green/pink/blue tints) ===")
for name, cond in [
    ("greenish", (G>R+8)&(G>B+8)&(G>90)),
    ("pinkish",  (R>G+10)&(R>B+5)&(R>150)),
    ("blueish",  (B>R+10)&(B>G+10)&(B>120)),
]:
    yy, xx = np.where(cond)
    if len(yy)==0:
        print(f"  {name}: NONE"); continue
    print(f"  {name}: n={len(yy)} bbox x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()}")
    # per-band
    bands = band(cond, gap=8)
    for s,e in bands:
        sel = cond[s:e+1]
        yy2, xx2 = np.where(sel)
        print(f"      band y {s}-{e}: x {xx2.min()}-{xx2.max()} n={len(yy2)}")

print("\n=== 4. DOT CLUSTERS by color ===")
for name, cond in [
    ("pure red dots", (R>150)&(R-G>90)&(R-B>90)),
    ("pure green dots", (G>90)&(G-R>60)&(G-B>60)),
    ("pure blue dots", (B>120)&(B-R>80)&(B-G>70)),
]:
    yy, xx = np.where(cond)
    print(f"  {name}: n={len(yy)} bbox x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()}")
    lab2, n2 = ndimage.label(cond, structure=np.ones((3,3)))
    cents = ndimage.center_of_mass(cond, lab2, range(1, n2+1))
    bigc = [(int(round(c[1])), int(round(c[0])), int(sz)) for c, sz in
            zip(cents, ndimage.sum(cond, lab2, range(1, n2+1))) if sz >= 12]
    print(f"    dots>=12px: {len(bigc)}")
    for cx, cy, sz in sorted(bigc, key=lambda t: (t[1], t[0])):
        print(f"      dot at x={cx} y={cy} area={sz}")

print("\n=== 5. BLACK text in plot (labels C1.. d1(x)..) ===")
blk = (R<90)&(G<90)&(B<90)
sub = blk.copy(); sub[:110,:]=False
yy, xx = np.where(sub)
print("  black in plot bbox: x", xx.min(), xx.max(), " y", yy.min(), yy.max())

print("\n=== 6. Row band of black text in plot (label rows) ===")
rb = band(sub, gap=8)
for s,e in rb:
    yy2, xx2 = np.where(sub[s:e+1])
    print(f"    band y {s}-{e}: x {xx2.min()}-{xx2.max()} n={len(yy2)}")
