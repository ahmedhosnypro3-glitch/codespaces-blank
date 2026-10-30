#!/usr/bin/env python3
"""Precise x-run analysis of specific text bands in slide_023.jpg."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

red = (R > 120) & (R - G > 80) & (R - B > 80)
yellow = (R > 240) & (G > 200) & (B < 215) & (G > B + 15)
dark = (R < 130) & (G < 130) & (B < 130)

def runs(mask_1d):
    """x-intervals where mask_1d is True."""
    out = []
    x = 0
    while x < len(mask_1d):
        if mask_1d[x]:
            x0 = x
            while x < len(mask_1d) and mask_1d[x]:
                x += 1
            out.append((x0, x - 1))
        else:
            x += 1
    return out

def band_report(y0, y1, x0, x1, label):
    print(f"\n== {label} (y{y0}..{y1}, x{x0}..{x1})")
    for name, m in [('RED', red), ('YEL', yellow), ('DARK', dark)]:
        sub = m[y0:y1+1, x0:x1+1]
        # union across rows
        colhit = sub.any(axis=0)
        rr = runs(colhit)
        if rr:
            s = ", ".join(f"{a0+x0}-{a1+x0}" for a0, a1 in rr[:40])
            print(f"  {name} x-runs (union): {s}")
        else:
            print(f"  {name}: none")

# green box text bands
band_report(112, 145, 95, 780, "green box line 1 (Recall:)")
band_report(146, 190, 95, 780, "green box line 2 (equation)")
band_report(191, 216, 95, 780, "green box line 3 (dimension note)")

# exact green box edges: scan columns where green fill present at mid-height
gm = (G > 245) & (G > R + 20) & (np.abs(G - B) < 40) & (R > 150)
mid = gm[165, :]
print("\ngreen fill at y=165, x-runs:", runs(mid))
gm2 = gm[:, 160]
print("green fill rows at x=160, y-runs:", runs(gm2))

# blue box: borders. Find the violet border color runs
violet = (np.abs(R - 186) < 45) & (np.abs(G - 180) < 45) & (B > R + 20) & (B > 200)
# row 228-232
for y in [227, 228, 229, 230, 231, 232, 233]:
    print(f"violet runs y={y}:", runs(violet[y, :])[:10])
# vertical borders: scan columns 70..100 and 870..900 for violet
colv = violet[240:420, :].any(axis=0)
print("violet column union y240..420:", runs(colv)[:10])

# solution box: measure its fill + edges
# pale yellow-green fill
pg = (R > 235) & (G > 240) & (B < 240) & (G - B > 15) & (R - B > 10)
mid2 = pg[480, :]
print("\nsolution fill at y=480, x-runs:", runs(mid2)[:10])
pg2 = pg[:, 500]
print("solution fill rows at x=500, y-runs:", runs(pg2)[:10])
# yellow line at y437-439: sample colors
for y in [434, 435, 436, 437, 438, 439, 440]:
    row = a[y, 300:500]
    from collections import Counter
    print(f"y={y} colors x300..500:", Counter(tuple(p) for p in row).most_common(3))
# bottom: y526..535
for y in [526, 527, 528, 529, 530, 531, 532, 533]:
    row = a[y, 300:500]
    from collections import Counter
    print(f"y={y} colors x300..500:", Counter(tuple(p) for p in row).most_common(3))
