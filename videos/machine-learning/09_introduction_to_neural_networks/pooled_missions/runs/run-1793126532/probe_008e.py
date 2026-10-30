#!/usr/bin/env python3
"""Precise map of the DIAGRAM region of slide_008.jpg (middle panel)."""
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
lum = a.mean(axis=2)
sat = a.max(axis=2) - a.min(axis=2)

def hx(p): return "#%02X%02X%02X" % (p[0], p[1], p[2])

# middle panel region (between maroon side panels)
MX0, MX1 = 168, 796
MY0, MY1 = 44, 517
mid = a[MY0:MY1, MX0:MX1]
mlum = lum[MY0:MY1, MX0:MX1]
msat = sat[MY0:MY1, MX0:MX1]
mh, mw = mlum.shape
print(f"middle region {MX0}..{MX1} x {MY0}..{MY1}  ({mw}x{mh})")

print("\n=== distinct colors in middle region (quantized, top 20) ===")
q = (mid // 16 * 16).reshape(-1, 3)
uniq, cnt = np.unique(q, axis=0, return_counts=True)
for i in np.argsort(-cnt)[:20]:
    print(f"   {hx(uniq[i])}  {cnt[i]*100.0/len(q):5.1f}%")

# --- axes: look for dark-ish long horizontal/vertical runs in middle
print("\n=== horizontal dark runs inside middle (rows with many pixels lum<200) ===")
dark = mlum < 200
rc = dark.sum(axis=1)
for y in range(mh):
    if rc[y] > 150:
        row = mid[y]
        print(f"   y={y+MY0:3d} n={rc[y]:4d}  colors at x=300,500,700: {hx(row[300-MX0])} {hx(row[500-MX0])} {hx(row[700-MX0])}")

print("\n=== vertical dark runs inside middle (cols with many pixels lum<200) ===")
cc = dark.sum(axis=0)
for x in range(mw):
    if cc[x] > 150:
        col = mid[:, x]
        print(f"   x={x+MX0:3d} n={cc[x]:4d}  colors at y=150,300,450: {hx(col[150-MY0])} {hx(col[300-MY0])} {hx(col[450-MY0])}")

# --- hatch tint classification map over middle, 16x10
print("\n=== hatch tint map over middle region (16 cols x 10 rows) ===")
print("   G=green B=blue P=pink(red) Y=yellow O=orange .=white K=dark")
for gy in range(10):
    y0, y1 = gy*mh//10, (gy+1)*mh//10
    row = ""
    for gx in range(16):
        x0, x1 = gx*mw//16, (gx+1)*mw//16
        blk = mid[y0:y1, x0:x1].reshape(-1,3).astype(float)
        r, g, b = blk[:,0].mean(), blk[:,1].mean(), blk[:,2].mean()
        if (r+g+b)/3 < 110: c = "K"
        elif r > 215 and g > 190 and b < 140: c = "Y"
        elif r > 190 and 100 < g < 175 and b < 90: c = "O"
        elif g - r > 4 and g - b > 4: c = "G"
        elif b - r > 6 and b - g > 6: c = "B"
        elif r - g > 6 and r - b > 4: c = "P"
        else: c = "."
        row += c
    print(f"   y[{gy*mh//10+MY0},{(gy+1)*mh//10+MY0}] {row}")

# --- strong saturated color blobs in middle
print("\n=== saturated pixel bboxes inside middle ===")
def blob(name, cond):
    ys, xs = np.where(cond)
    if not len(ys):
        print(f"   {name}: none"); return
    print(f"   {name}: n={len(ys)} x[{xs.min()+MX0},{xs.max()+MX0}] y[{ys.min()+MY0},{ys.max()+MY0}]")
    # split into rows of 30 to see line vs cluster
    hist = Counter(((ys)//30)*30)
    for k in sorted(hist):
        sel = ((ys)//30*30)==k
        print(f"      y[{k+MY0},{k+30+MY0}): n={sel.sum()} x[{xs[sel].min()+MX0},{xs[sel].max()+MX0}]")

blob("RED sat", (msat > 55) & (mid[:,:,0] > mid[:,:,1]+50) & (mid[:,:,0] > mid[:,:,2]+40))
blob("BLUE sat", (msat > 55) & (mid[:,:,2] > mid[:,:,0]+50) & (mid[:,:,2] > mid[:,:,1]+30))
blob("GREEN sat", (msat > 45) & (mid[:,:,1] > mid[:,:,0]+35) & (mid[:,:,1] > mid[:,:,2]+25))
blob("YELLOW sat", (msat > 60) & (mid[:,:,0] > mid[:,:,1]+60) & (mid[:,:,1] > mid[:,:,2]+50))
blob("ORANGE sat", (msat > 70) & (mid[:,:,0] > 190) & (mid[:,:,1] > 90) & (mid[:,:,1] < 175) & (mid[:,:,2] < 70))
blob("PURPLE sat", (msat > 25) & (mid[:,:,0] > 140) & (mid[:,:,2] > 140) & (mid[:,:,1] < mid[:,:,0]-20))

# --- vertical band check: where does the middle region start/end (maroon panels)?
print("\n=== row y=300 color scan across width ===")
for x in range(0, W, 20):
    print(f"   x={x:3d} {hx(a[300,x])}", end="")
    if (x//20) % 5 == 4: print()
print()
