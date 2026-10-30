#!/usr/bin/env python3
"""Fit the table column grid and verify against all text rows."""
import numpy as np
from PIL import Image

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
lum = o.sum(axis=2)

# Row 356-368 strong tokens: 135,203,243,284,324,364,404,445,485,525,565,606,646,772,807,847
# diffs from 135: 0,68,108,149,189,229,269,310,350,390,430,471,511,637,672,712
# pitch ~40.1
# Hypothesis: grid centres = 121 + k*40.0 for k=0..?  -> 121,161,201,241,281,321,361,401,441,481,521,561,601,641,681,721,761,801,841
obs = [135, 203, 243, 284, 324, 364, 404, 445, 485, 525, 565, 606, 646, 772, 807, 847]
print("Hypothesis grid 121+k*40:", [121 + k * 40 for k in range(19)])
print("observed strong tokens:", obs)
print()
# check residuals
for g in [121 + k * 40 for k in range(19)]:
    near = [v for v in obs if abs(v - g) < 22]
    mark = "OK " if near else "?? "
    print(f"  grid {g:>4}: {mark} nearest {near}")

print()
print("=== Check: 121+40k matches ALL rows' token centroids? ===")
rows = [(356, 368), (380, 387), (396, 407), (423, 431), (442, 451), (462, 477)]
for y0, y1 in rows:
    dark = lum[y0:y1, 118:870] < 330
    cols = np.where(dark.any(axis=0))[0] + 118
    toks = []
    cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] >= 5:
            toks.append((cur[0] + cur[-1]) // 2)
            cur = [c]
        else:
            cur.append(c)
    toks.append((cur[0] + cur[-1]) // 2)
    grid = [121 + k * 40 for k in range(19)]
    assigned = []
    for t in toks:
        g = min(grid, key=lambda g: abs(g - t))
        assigned.append(g if abs(g - t) < 20 else f"?{t}")
    print(f"  rows {y0}-{y1}: -> {[str(a) for a in assigned]}")

print()
print("=== Label column: x 86-121. Text rows in label col ===")
for y0, y1 in [(356, 368), (380, 387), (396, 407), (423, 431), (442, 451), (462, 477)]:
    dark = lum[y0:y1, 86:121] < 330
    ys_, xs_ = np.where(dark)
    if len(ys_):
        print(f"  rows {y0}-{y1}: label ink rows {y0+ys_.min()}-{y0+ys_.max()} cols {86+xs_.min()}-{86+xs_.max()}")

print()
print("=== EXACT row-band (fill) boundaries — dominant fill per band ===")
bands = [(334, 368), (376, 410), (420, 455), (458, 479), (482, 504)]
for y0, y1 in bands:
    mid = (y0 + y1) // 2
    # dominant fill over x 130-860
    from collections import Counter
    cnt = Counter(tuple(o[mid, x]) for x in range(130, 860, 4))
    print(f"  band y{y0}-{y1}: dominant {cnt.most_common(1)[0]}")

print()
print("=== Row band vertical extents exactly (using col 500 which is data col 9) ===")
prev = None; start = None
for y in range(318, 524):
    c = tuple(o[y, 500])
    if c != prev:
        if prev is not None and y - start >= 3:
            print(f"  y {start}-{y-1} (h={y-start}): {prev}")
        prev = c; start = y
print(f"  y {start}-523: {prev}")