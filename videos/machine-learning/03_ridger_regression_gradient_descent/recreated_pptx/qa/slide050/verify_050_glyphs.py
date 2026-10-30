#!/usr/bin/env python3
"""Extract + cluster every digit glyph in the top-left region of slide 050
(table x66..246 y54..250). Clusters identical bitmap shapes so values can be read."""
import numpy as np
from PIL import Image

im = Image.open('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_050.jpg').convert('L')
a = np.asarray(im).astype(int)

# region of interest: the two tables
X0, X1, Y0, Y1 = 66, 246, 54, 250
sub = a[Y0:Y1, X0:X1]
ink = sub < 190

# column profile of ink to find glyph columns
colprof = ink.sum(axis=0)
# connected components on columns
def runs(mask):
    out = []
    start = None
    for i, v in enumerate(mask):
        if v and start is None: start = i
        elif not v and start is not None:
            out.append((start, i)); start = None
    if start is not None: out.append((start, len(mask)))
    return out

# glyph boxes: use a simple flood-fill-ish on ink cols/rows via projections
glyphs = []
covered = np.zeros_like(ink)
for y in range(ink.shape[0]):
    for x in range(ink.shape[1]):
        if ink[y, x] and not covered[y, x]:
            # BFS
            stack = [(y, x)]; covered[y, x] = True
            ys = [y]; xs = [x]
            pix = []
            while stack:
                cy, cx = stack.pop(); pix.append((cy, cx))
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < ink.shape[0] and 0 <= nx < ink.shape[1] and ink[ny,nx] and not covered[ny,nx]:
                            covered[ny,nx] = True; stack.append((ny,nx)); ys.append(ny); xs.append(nx)
            if len(pix) >= 8:
                glyphs.append((min(xs), min(ys), max(xs), max(ys), len(pix)))

glyphs.sort(key=lambda g: (g[1], g[0]))
print("glyph count", len(glyphs))
for g in glyphs:
    gx0, gy0, gx1, gy1, n = g
    print(f"abs({X0+gx0},{Y0+gy0})-({X0+gx1},{Y0+gy1}) n={n} w={gx1-gx0+1} h={gy1-gy0+1}")
