#!/usr/bin/env python3
"""Final precise table text-row + column extraction."""
import numpy as np
from PIL import Image

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
lum = o.sum(axis=2)

print("=== Clean extraction: rows 355-370, find number tokens & centres ===")
y0, y1 = 356, 368
dark = lum[y0:y1, 86:870] < 330
cols = np.where(dark.any(axis=0))[0] + 86
toks = []
cur = [cols[0]]
for c in cols[1:]:
    if c - cur[-1] >= 5:
        toks.append(((cur[0] + cur[-1]) // 2, cur[0], cur[-1]))
        cur = [c]
    else:
        cur.append(c)
toks.append(((cur[0] + cur[-1]) // 2, cur[0], cur[-1]))
print(f"rows {y0}-{y1}: {len(toks)} tokens")
for t in toks:
    print(f"   centre={t[0]:>4} span={t[1]}-{t[2]}")

# expected centres for label col + 16 data cols (x from spec)
spec_x = [-11, -10.9, -10.8, -10.7, -10.6, -10.5, -10.4, -10.3, -10.2, -10.1, -10, -9.9, -9.8, -9.7, -9.6, -9.5]
print("\nspec x-row values:", spec_x)

print("\n=== same for rows 380-386 (line 2) ===")
for (y0, y1) in [(380, 387), (396, 407), (423, 431), (432, 441), (442, 451), (462, 477), (484, 501)]:
    dark = lum[y0:y1, 86:870] < 330
    cols = np.where(dark.any(axis=0))[0] + 86
    if not len(cols):
        print(f"rows {y0}-{y1}: no ink")
        continue
    toks = []
    cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] >= 5:
            toks.append((cur[0] + cur[-1]) // 2)
            cur = [c]
        else:
            cur.append(c)
    toks.append((cur[0] + cur[-1]) // 2)
    print(f"rows {y0}-{y1}: {len(toks)} tokens at centres {toks}")

print("\n=== Determine column grid: fit centres from rows 356-368 ===")
# derive from the 356-368 row's strong tokens
strong = [128, 156, 195, 235, 276, 316, 356, 396, 437, 477, 517, 557, 598, 638, 679, 721, 769, 799, 839]
d = np.diff(strong)
print("diffs:", d, "mean", d.mean(), "std", d.std())
