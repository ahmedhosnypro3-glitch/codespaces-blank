#!/usr/bin/env python3
"""slide_001 v4: precise per-line ink boxes for original AND render_v4, mapped to inches."""
import os
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = os.path.join(V, "unique_slides/slide_001.jpg")
REND = os.path.join(V, "recreated_pptx/build/slide_001_rendered_v4-1.png")
OUT = os.path.join(V, "recreated_pptx/build/measure_001_v4.txt")

def load(path):
    im = Image.open(path).convert("RGB")
    return np.asarray(im).astype(np.float64)

def lines(a, exclude_rules=True, minink=2, gapmerge=8, box=None):
    L = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    H, W = L.shape
    ink = L < 170
    if exclude_rules:
        ink[:, :8] = False; ink[:, W-8:] = False
        ink[:8, :] = False
        ink[H-30:, :] = False
    if box:
        x0, y0, x1, y1 = box
        m = np.zeros_like(ink)
        m[y0:y1+1, x0:x1+1] = ink[y0:y1+1, x0:x1+1]
        ink = m
    r = ink.sum(axis=1)
    bands = []
    inb = False
    for y in range(H):
        if r[y] > minink and not inb:
            st = y; inb = True
        elif r[y] <= minink and inb:
            bands.append([st, y-1]); inb = False
    if inb: bands.append([st, H-1])
    m = []
    for b in bands:
        if m and b[0] - m[-1][1] <= gapmerge: m[-1][1] = b[1]
        else: m.append(b)
    res = []
    for (y0, y1) in m:
        sub = ink[y0:y1+1]
        if sub.sum() < 20: continue
        xs = np.nonzero(sub.sum(axis=0) > 0)[0]
        cols = a[y0:y1+1][sub]
        med = np.median(cols, axis=0).astype(int)
        res.append((y0, y1, int(xs.min()), int(xs.max()), int(sub.sum()), med.tolist()))
    return res

def hexs(c):
    return "#%02X%02X%02X" % tuple(c)

out = []
def p(*x):
    s = " ".join(str(v) for v in x); out.append(s); print(s)

o = load(ORIG); r = load(REND)
PO = 72.0   # original px per inch
PR = o.shape[1] / 13.3333 if abs(o.shape[1]/o.shape[0] - 13.3333/7.5) < 0.05 else 72.0
PR = r.shape[0] / 7.5
p("orig px/in %.3f  render px/in %.3f" % (o.shape[1]/13.3333, PR))
p("")
p("=== ORIGINAL ink lines (px, and inches = px/%.1f) ===" % PO)
ol = lines(o, exclude_rules=False, box=(62, 46, 899, 515))
for (y0, y1, x0, x1, npx, med) in ol:
    p("y %4d-%4d (h%3d) x %4d-%4d (w%4d) px%5d  %s   |  y %.3f-%.3f in  x %.3f-%.3f in" %
      (y0, y1, y1-y0+1, x0, x1, x1-x0+1, npx, hexs(med), y0/PO, (y1+1)/PO, x0/PO, (x1+1)/PO))

p("")
p("=== RENDER v4 ink lines (px, inches = px/%.1f) ===" % PR)
rl = lines(r, exclude_rules=True, box=(30, 15, 1970, 1090))
for (y0, y1, x0, x1, npx, med) in rl:
    p("y %4d-%4d (h%3d) x %4d-%4d (w%4d) px%5d  %s   |  y %.3f-%.3f in  x %.3f-%.3f in" %
      (y0, y1, y1-y0+1, x0, x1, x1-x0+1, npx, hexs(med), y0/PR, (y1+1)/PR, x0/PR, (x1+1)/PR))

with open(OUT, "w") as f:
    f.write("\n".join(out))
p(""); p("wrote", OUT)
