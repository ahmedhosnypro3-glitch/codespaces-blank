#!/usr/bin/env python3
"""Build-time ink measurement of the equation line: W = (X^T X + λI)^(-1) X^T Y
in slide_023.jpg. 960x540 frame, 1px=1pt. Prints detailed ink bbox per glyph."""
import numpy as np
from PIL import Image
from collections import Counter

a = np.array(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# any non-fill ink inside green box region: fill is (206,255,226)
fill = np.array([206, 255, 226])
d = np.abs(a - fill).sum(axis=2)
ink = d > 120          # tolerant: catches dark ink, red ink, green ink
red = (R > 120) & (R - G > 80) & (R - B > 80)
green = (G > R + 40) & (G > B + 40) & (G > 90) & (G < 200)   # green ink (λ and I)

def runs(idx, gap=3):
    out = []
    i = 0
    n = len(idx)
    while i < n:
        if idx[i]:
            s = i
            while i < n and idx[i]:
                i += 1
            out.append([int(s), int(i - 1)])
        else:
            i += 1
    # merge small gaps
    m = []
    for r in out:
        if m and r[0] - m[-1][1] - 1 <= gap:
            m[-1][1] = r[1]
        else:
            m.append(r)
    return m

print("== EQUATION INK GROUPS (y146..190, x95..445, ink=nonfill) ==")
sub = ink[146:191, 95:446]
col = sub.any(axis=0)
for s, e in runs(col, gap=4):
    seg = ink[146:191, s + 95:e + 96]
    ys = np.where(seg.any(axis=1))[0]
    segred = red[146:191, s + 95:e + 96]
    seggreen = green[146:191, s + 95:e + 96]
    # also all-ink rows for dark
    print(f"  x{s+95}..{e+95} w={e-s+1} y{ys[0]+146}..{ys[-1]+146} hh={ys[-1]-ys[0]+1} red={int(segred.sum())} green={int(seggreen.sum())}")

print()
print("== rows of ( and ) strokes ==")
for y in range(146, 192):
    line = ink[y, 95:445]
    xs = np.where(line)[0]
    if len(xs):
        # report only the paren columns & superscript
        pass
for (label, xs0, xs1) in [("open_paren", 179, 186), ("close_paren", 334, 342), ("sup_minus", 358, 365), ("sup_one", 366, 373)]:
    seg = ink[146:192, xs0:xs1 + 1]
    ys = np.where(seg.any(axis=1))[0]
    print(f"  {label}: y{ys[0]+146}..{ys[-1]+146}  n={int(seg.sum())}")

print()
print("== GREEN ink (lambda, I) exact bbox ==")
gg = green[146:192, 95:446]
ys, xs = np.where(gg)
print("  green bbox:", (int(xs.min() + 95), int(ys.min() + 146), int(xs.max() + 95), int(ys.max() + 146)) if len(xs) else None)
colg = gg.any(axis=0)
for s, e in runs(colg, gap=4):
    seg = gg[146:192, s + 95:e + 96]
    ys2 = np.where(seg.any(axis=1))[0]
    print(f"  green x{s+95}..{e+95} y{ys2[0]+146}..{ys2[-1]+146}")

print()
print("== UNDERLINE under W (y186..196) ==")
for y in range(183, 197):
    xs = np.where(ink[y, 95:180])[0]
    if len(xs):
        print(f"  y={y}: x{xs.min()+95}..{xs.max()+95} n={len(xs)}")

print()
print("== W ink detail (x100..132) ==")
for y in range(150, 190):
    xs = np.where(ink[y, 100:132])[0]
    if len(xs):
        print(f"  y={y}: x{xs.min()+100}..{xs.max()+100} n={len(xs)}")
