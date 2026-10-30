#!/usr/bin/env python3
"""Cluster digit glyphs by bitmap shape; print one exemplar ASCII per cluster
with its member list, so table values can be read off unambiguously."""
import numpy as np
from PIL import Image

im = Image.open('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_050.jpg').convert('L')
A = np.asarray(im).astype(int)


def boxes(x0, x1, y0, y1, thr=190, minpix=8):
    ink = A[y0:y1, x0:x1] < thr
    covered = np.zeros_like(ink)
    out = []
    for yy in range(ink.shape[0]):
        for xx in range(ink.shape[1]):
            if ink[yy, xx] and not covered[yy, xx]:
                stack = [(yy, xx)]; covered[yy, xx] = True
                ys = [yy]; xs = [xx]
                while stack:
                    cy, cx = stack.pop()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < ink.shape[0] and 0 <= nx < ink.shape[1] and ink[ny, nx] and not covered[ny, nx]:
                                covered[ny, nx] = True; stack.append((ny, nx)); ys.append(ny); xs.append(nx)
                if len(ys) >= minpix:
                    out.append([x0+min(xs), y0+min(ys), x0+max(xs), y0+max(ys)])
    return out


def norm(b, H=12, W=8):
    x0, y0, x1, y1 = b
    g = A[y0:y1+1, x0:x1+1] < 190
    img = Image.fromarray((~g*255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    return (np.asarray(img) < 128).astype(int).flatten()


# --- top-left data table: digits in rows y78..107, cols x86..222
tbl = []
for (ya, yb) in [(78, 94), (96, 107)]:
    for b in boxes(86, 222, ya, yb):
        if (b[2]-b[0]) <= 10 and (b[3]-b[1]) <= 12:
            tbl.append((b, ya))

# --- vectors table: digits in rows y184..192, 199..207, 214..222
vec = []
for (ya, yb) in [(183, 194), (198, 209), (213, 224)]:
    for b in boxes(86, 222, ya, yb):
        if (b[2]-b[0]) <= 12 and (b[3]-b[1]) <= 12:
            vec.append((b, ya))

allg = tbl + vec
sigs = [norm(b) for b, _ in allg]
clusters = []
for i, s in enumerate(sigs):
    placed = False
    for c in clusters:
        if np.abs(c['sig'] - s).sum() <= 6:
            c['members'].append(i); placed = True; break
    if not placed:
        clusters.append({'sig': s, 'members': [i]})

for ci, c in enumerate(clusters):
    b, ya = allg[c['members'][0]]
    x0, y0, x1, y1 = b
    g = A[y0:y1+1, x0:x1+1] < 190
    print(f"--- cluster {ci}  members={[(allg[i][0], 'rowY'+str(allg[i][1])) for i in c['members']]}")
    for row in g:
        print('   ' + ''.join('#' if v else '.' for v in row))
