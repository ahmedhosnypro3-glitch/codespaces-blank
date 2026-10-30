#!/usr/bin/env python3
"""Region map of the original frame: dominant non-background color per grid cell."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
H, W = o.shape[:2]

# classify each pixel
r, g, b = o[:, :, 0].astype(int), o[:, :, 1].astype(int), o[:, :, 2].astype(int)
mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
sat = mx - mn

def classify(pp):
    R, G, B = pp
    s = max(R, G, B) - min(R, G, B)
    if s < 25:
        if max(R, G, B) > 240: return '.'   # white
        if abs(R - 233) < 18 and abs(G - 233) < 18: return ','  # panel gray
        if max(R, G, B) < 120: return '#'     # dark/black
        return '-'                            # other gray
    if R == max(R, G, B):
        if G > 150 and B < 120: return 'Y'    # yellow
        if G > 100 and B > 130: return 'P'    # pink/magenta
        return 'R'
    if G == max(R, G, B):
        if B > 150: return 'C'                # cyan
        return 'G'
    # B dominant
    if R > 150: return 'P'                    # purple/pink (blue-ish with red)
    return 'B'

# 24x54 cell grid: each cell 40x10 px
cs_h, cs_w = 10, 20
print("Region map (char per 20x10px cell). Rows are y, cols are x.")
hdr = "     " + "".join(str((c * cs_w // 100) % 10) for c in range(W // cs_w))
print(hdr)
for cy in range(H // cs_h):
    row = ""
    for cx in range(W // cs_w):
        cell = o[cy*cs_h:(cy+1)*cs_h, cx*cs_w:(cx+1)*cs_w].reshape(-1, 3)
        cnt = Counter(classify(tuple(p)) for p in cell)
        # drop background chars
        fg = [(k, v) for k, v in cnt.most_common() if k not in '.,']
        if not fg:
            bg = cnt.most_common(1)[0][0]
            row += bg if bg in ',' else ' '
        else:
            # prefer saturated family with most px, but '#' dark text counts too
            row += fg[0][0]
    print(f"{cy*cs_h:>4} {row}")

print()
print("Legend: R=red G=green C=cyan Y=yellow P=purple/pink B=blue #=dark/gray -=gray .=white ,=panel-gray")
