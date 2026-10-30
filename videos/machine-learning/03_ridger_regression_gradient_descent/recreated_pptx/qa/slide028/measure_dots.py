#!/usr/bin/env python3
"""Measure axes colour/extent + dot trajectory in the original, excluding frame borders."""
import numpy as np
from collections import Counter
from PIL import Image

o = np.asarray(Image.open(
    '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
).convert('RGB')).astype(int)

def bg_mask(a, bg=(254, 255, 253), tol=30):
    return np.all(np.abs(a - np.array(bg)) < tol, axis=2)

white = (o[:, :, 0] > 235) & (o[:, :, 1] > 235) & (o[:, :, 2] > 235)
gray = (np.abs(o[:, :, 0] - 233) < 14) & (np.abs(o[:, :, 1] - 233) < 14) & (np.abs(o[:, :, 2] - 231) < 16)
ink = ~white & ~gray

# interior only: exclude the 1F4E79 frame rectangle x90..858 y127..509 (2px halo)
inner = np.zeros_like(ink)
inner[132:505, 96:853] = True
chart_ink = ink & inner

print("=== AXIS STROKES inside chart interior (x96..853, y132..505) ===")
colsum = chart_ink.sum(axis=0)
print("cols with >=40 ink px:")
for x in np.where(colsum >= 40)[0]:
    sel = chart_ink[:, x]
    c = Counter(tuple(p) for p in o[:, x][sel])
    print(f"  x={x}: n={int(colsum[x])} top={c.most_common(2)}")
rowsum = chart_ink.sum(axis=1)
print("rows with >=40 ink px:")
for y in np.where(rowsum >= 40)[0]:
    sel = chart_ink[y]
    c = Counter(tuple(p) for p in o[y][sel])
    print(f"  y={y}: n={int(rowsum[y])} top={c.most_common(2)}")

# ---------- DOT TRAJECTORY ----------
print("\n=== DOT / CURVE TRAJECTORY (blue family, interior) ===")
blue = (np.abs(o[:, :, 0] - 46) < 100) & (np.abs(o[:, :, 1] - 117) < 100) & (np.abs(o[:, :, 2] - 182) < 100)
blue[:, :100] = False; blue[:, 850:] = False
blue[:135, :] = False; blue[503:, :] = False

# split panels at the divider.  find the divider x
div = None
for x in range(400, 550):
    col = blue[:, x]
    if col.sum() > 200:
        div = x
        break
print("panel divider candidate x:", div)

for side, (x0, x1) in [('LEFT', (100, 473)), ('RIGHT', (476, 850))]:
    b = blue.copy(); b[:, :x0] = False; b[:, x1:] = False
    print(f"\n--- {side} panel x{x0}..{x1} ---")
    print("  x  ytop ybot  n   (column ink extent)")
    rows = []
    for x in range(x0, x1, 8):
        col = np.where(b[:, x])[0]
        if len(col):
            rows.append((x, int(col.min()), int(col.max()), len(col)))
    for t in rows:
        print("   ", t)
