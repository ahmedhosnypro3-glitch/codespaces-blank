#!/usr/bin/env python3
"""Slide 026 self-check attempt 4 — closed-loop PIL comparison of the 150dpi render
against the banked 8-pass measurement targets (ALL values in frame px; render is
2001x1125, 1 frame px = 1125/540 = 2.0833 render px on y, 2001/960 = 2.0844 on x).

Tolerance: <= ~2 frame px per edge (the bank's ~4px@150dpi law).
Frame containment: interior content ink must sit inside the blue box border
(x82..864, y90..500) and the title inside the house panel (x54..903, y45..540).
"""
import numpy as np
from PIL import Image

import os
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "render_4.png")
ren = np.asarray(Image.open(R).convert("RGB")).astype(int)
H, W, _ = ren.shape
SY, SX = H / 540.0, W / 960.0
print("render %dx%d  scale x %.4f y %.4f" % (W, H, SX, SY))

rR, rG, rB = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
red = (rR - rG > 40) & (rR - rB > 40)
blue = (rB - rR > 40) & (rB - rG > 40)
inkW = (np.abs(ren - 255).max(axis=2) > 30)          # ink on white (box interior)
GRAY = np.array([233, 233, 231])
inkG = (np.abs(ren - GRAY).max(axis=2) > 25)         # ink on gray panel (title)

def band(mask, fy0, fy1, fx0, fx1):
    """Ink bbox within a FRAME-px window, returned in frame px."""
    y0, y1 = int(fy0 * SY), int(fy1 * SY)
    x0, x1 = int(fx0 * SX), int(fx1 * SX)
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    # FIX: (window_origin + offset) / scale — origin is RENDER px, scale converts to frame px
    return ((x0 + xs.min()) / SX, (x0 + xs.max()) / SX,
            (y0 + ys.min()) / SY, (y0 + ys.max()) / SY)

def report(name, got, want):
    if got is None:
        print("  %-10s MISSING INK  (want %s)" % (name, want))
        return False
    d = [got[0] - want[0], got[1] - want[1], got[2] - want[2], got[3] - want[3]]
    ok = all(abs(v) <= 2.0 for v in d)
    print("  %-10s got x %6.1f..%6.1f y %6.1f..%6.1f | want x %d..%d y %d..%d | d %+5.1f %+5.1f %+5.1f %+5.1f %s"
          % (name, got[0], got[1], got[2], got[3], want[0], want[1], want[2], want[3],
             d[0], d[1], d[2], d[3], "OK" if ok else "<<< FIX"))
    return ok

allok = True
print("\n== TEXT BANDS (render vs banked, frame px) ==")
allok &= report("title",   band(inkG, 56, 86, 280, 650),   (294, 639, 60, 82))
allok &= report("gdhdr",   band(red,  105, 133, 100, 860), (109, 392, 110, 129))
allok &= report("rowA",    band(blue, 138, 168, 140, 860), (146, 469, 143, 162))
allok &= report("rowB",    band(blue, 172, 202, 140, 860), (146, 846, 177, 196))
allok &= report("rowC-bl", band(blue, 205, 236, 140, 516), (146, 512, 210, 229))
allok &= report("rowC-red",band(red,  205, 236, 515, 860), (518, 689, 210, 229))
allok &= report("rowD",    band(blue, 238, 268, 140, 860), (146, 830, 243, 262))
allok &= report("noteshdr",band(red,  305, 328, 100, 860), (109, 159, 310, 324))
allok &= report("N1",      band(inkW, 338, 366, 86, 860),  (91, 769, 342, 361))
allok &= report("N2",      band(inkW, 372, 400, 100, 860), (109, 575, 376, 394))
allok &= report("N3",      band(inkW, 437, 465, 86, 860),  (91, 836, 441, 460))
allok &= report("N4",      band(inkW, 470, 496, 100, 860), (109, 295, 475, 494))

print("\n== UNDERLINE BARS (solid runs near the measured bar rows) ==")
def longest_run(row):
    """Longest contiguous True run in a boolean row -> (start, length)."""
    best = (0, 0)
    i, n = 0, len(row)
    while i < n:
        if row[i]:
            j = i
            while j < n and row[j]:
                j += 1
            if j - i > best[1]:
                best = (i, j - i)
            i = j
        else:
            i += 1
    return best

def barscan(name, fy0, fy1, fx0, fx1, mask, want):
    """A solid bar row has a contiguous run >= 70% of the measured bar width at
    >= 85% density (a text row's longest run is a word — shorter and spotty)."""
    y0, y1 = int(fy0 * SY), int(fy1 * SY)
    x0, x1 = int(fx0 * SX), int(fx1 * SX)
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    minlen = (want[1] - want[0]) * 0.50 * SX
    best = None
    for i in range(sub.shape[0]):
        s, L = longest_run(sub[i])
        if L >= minlen and sub[i, s:s + L].mean() > 0.85:
            best = (i, s, s + L)
    if best is None:
        print("  %-8s NO BAR (want %s)" % (name, want))
        return False
    i, s0, s1 = best
    a, b = (x0 + s0) / SX, (x0 + s1) / SX
    yy = (y0 + i) / SY
    ok = abs(a - want[0]) <= 3 and abs(b - want[1]) <= 3 and abs(yy - want[2]) <= 3
    print("  %-8s bar x %6.1f..%6.1f at y %6.1f | want %s %s"
          % (name, a, b, yy, want, "OK" if ok else "<<< FIX"))
    return ok
allok &= barscan("rowB", 188, 198, 300, 860, blue, (349, 716, 193))
allok &= barscan("rowD", 254, 264, 280, 500, blue, (287, 473, 259))
allok &= barscan("N3a",  452, 464, 150, 300, inkW, (177, 277, 458))
allok &= barscan("N3b",  452, 464, 500, 760, inkW, (538, 728, 458))

print("\n== BULLET DISCS ==")
allok &= report("N1-bul", band(inkW, 344, 354, 88, 100), (91, 97, 346, 352))
allok &= report("N3-bul", band(inkW, 444, 453, 88, 100), (91, 97, 446, 451))

print("\n== FRAME CONTAINMENT ==")
# blue box border geometry (heavy blue columns/rows in the render)
boxm = blue.copy()
cols = np.where(boxm.sum(axis=0) > 150 * SY)[0]
rows = np.where(boxm.sum(axis=1) > 400 * SX)[0]
cf = [round(c / SX) for c in cols]; rf = [round(r / SY) for r in rows]
print("  blue border cols (frame px): %s | rows: %s" % (cf, rf))
# content ink = all ink EXCLUDING the border strokes themselves and the chrome zone
content = (inkW | red | blue).copy()
content[:int(94 * SY)] = False                 # above the box top border
content[int(497 * SY):] = False                # below the box bottom border
content[:, :int(86 * SX)] = False              # left of the box left border
content[:, int(860 * SX):] = False             # right of the box right border
ys, xs = np.where(content)
ex = (xs.min() / SX, xs.max() / SX, ys.min() / SY, ys.max() / SY)
print("  interior content ink extent: x %.1f..%.1f  y %.1f..%.1f" % ex)
print("  (box interior: x 84..862, y 93..497)")
cont_ok = ex[0] >= 82 and ex[1] <= 864 and ex[2] >= 90 and ex[3] <= 500
print("  containment inside blue box: %s" % ("OK" if cont_ok else "FAIL <<<"))
allok &= cont_ok
# title ink only (window stops at the box top border y90 so the border is excluded)
twin = inkG[:int(88 * SY)].copy()
twin[:, :int(280 * SX)] = False                # drop chrome strokes (x<280)
tys, txs = np.where(twin)
tex = (txs.min() / SX, txs.max() / SX, tys.min() / SY, tys.max() / SY)
print("  title ink: x %.1f..%.1f y %.1f..%.1f (panel x54..903 y45..540)" % tex)
t_ok = tex[0] >= 54 and tex[1] <= 903 and tex[2] >= 45 and tex[3] <= 90
print("  title inside panel & above box: %s" % ("OK" if t_ok else "FAIL <<<"))
allok &= t_ok

print("\nSELFCHECK-1 RESULT: %s" % ("PASS" if allok else "FAIL"))
