#!/usr/bin/env python3
"""w2 (worker w8-s023b) — fresh fine measurement of slide_023.jpg.

Copy-then-modify of the banked forensics approach (build_spec.py / other_lines.py):
classify every ink pixel by colour family and report word-level segments with
their y-extent, so the build can place verbatim text + coloured spans exactly.
960x540 frame, 1px = 1pt = 1/72 in.  READ-ONLY: never writes to the frame.
"""
import numpy as np
from PIL import Image
from collections import Counter

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]
print("frame", W, "x", H)


def fam(y, x):
    r, g, b = a[y, x]
    if r > 120 and r - g > 60 and r - b > 60:
        return 'RED'
    if b > r + 30 and b > 90 and g < 140:
        return 'NAVY'
    if r < 115 and g < 115 and b < 115:
        return 'BLK'
    if g > 110 and g - r > 40 and g - b > 40:
        return 'GRN'
    return 'other'


def segments(y0, y1, x0, x1, bg, thr=120, gap=4, show='all'):
    """bg = background colour of the box interior; ink = |px-bg|.sum > thr."""
    d = np.abs(a[y0:y1 + 1, x0:x1 + 1] - np.array(bg)).sum(axis=2)
    m = d > thr
    cols = m.any(axis=0)
    xi = np.where(cols)[0]
    if not len(xi):
        print(f"  region y{y0}..{y1} x{x0}..{x1}: NO INK")
        return
    groups = []
    s = p = int(xi[0])
    for x in xi[1:]:
        if x - p > gap:
            groups.append((s, p))
            s = int(x)
        p = int(x)
    groups.append((s, p))
    print(f"  region y{y0}..{y1} x{x0}..{x1} (bg {bg}) ink x{groups[0][0]+x0}..{groups[-1][1]+x0}")
    for (g0, g1) in groups:
        sub = m[:, g0:g1 + 1]
        ys = np.where(sub.any(axis=1))[0]
        ty, by = int(ys.min()) + y0, int(ys.max()) + y0
        px = a[y0:y1 + 1, g0 + x0:g1 + x0 + 1][sub]
        cc = Counter(fam(y, x) for y, x in zip(*np.where(sub)))
        fams = [(k, v) for k, v in cc.most_common(3) if v > 4]
        # darkest core colour
        lum = px.sum(axis=1)
        core = tuple(int(v) for v in px[np.argsort(lum)[:max(3, len(px) // 20)]].mean(axis=0))
        print(f"    x{g0+x0}..{g1+x0} w={g1-g0+1} y{ty}..{by} h={by-ty+1} "
              f"fams={fams} core={core}")


PANEL = [233, 233, 231]
GREEN = [207, 255, 227]
BLUE = [250, 253, 255]
YELL = [250, 253, 226]

print("\n== TITLE (panel bg) ==")
segments(72, 108, 60, 900, PANEL, gap=6)
print("\n== RECALL: text vs underline (green bg) ==")
segments(112, 148, 90, 400, GREEN, gap=3)
print("   row-profile of the underline band y130..148 x95..185:")
for y in range(126, 150):
    row = np.abs(a[y, 95:190] - np.array(GREEN)).sum(axis=1) > 120
    if row.any():
        xs = np.where(row)[0]
        print(f"     y{y}: x{xs.min()+95}..{xs.max()+95} n={row.sum()}")
print("\n== DIMNOTE (green bg) ==")
segments(189, 216, 90, 790, GREEN, gap=5)
print("\n== EQUATION band (green bg) ==")
segments(146, 192, 95, 440, GREEN, gap=4)
print("\n== BLUE L1 ==")
segments(238, 270, 90, 870, BLUE, gap=4)
print("\n== BLUE L2 ==")
segments(270, 304, 90, 870, BLUE, gap=4)
print("\n== BLUE L3 ==")
segments(302, 340, 90, 870, BLUE, gap=4)
print("\n== EX L1 (panel bg) ==")
segments(356, 392, 90, 870, PANEL, gap=4)
print("\n== EX L2 (panel bg) ==")
segments(392, 428, 90, 870, PANEL, gap=4)
print("\n== SOL label ==")
segments(444, 470, 90, 420, YELL, gap=3)
print("\n== SOL L1 ==")
segments(470, 502, 230, 800, YELL, gap=4)
print("\n== SOL L2 ==")
segments(502, 534, 280, 760, YELL, gap=4)

print("\n== BOX BORDERS (saturated edge scan) ==")


def edge_rows(mask, x, y0, y1):
    return [y for y in range(y0, y1) if mask[y, x]]


gb = (G > R + 40) & (G > B + 40) & (G > 90) & (G < 195)
print(" GREEN  top rows x=600:", edge_rows(gb, 600, 95, 245),
      " bottom rows x=600:", edge_rows(gb, 600, 195, 245))
print(" GREEN  left cols y=200:", [x for x in range(80, 120) if gb[200, x]],
      " right cols y=200:", [x for x in range(730, 790) if gb[200, x]])
# green box outer fill extent (rows where fill spans widely)
gf = (G > R + 6) & (G > B + 6) & (G > 200) & (R > 180) & (G < 252)
rows = [y for y in range(95, 245) if gf[y, 200:750].sum() > 300]
print(" GREEN  fill wide rows:", rows[0] if rows else None, "..", rows[-1] if rows else None)
cols = [x for x in range(85, 870) if gf[210, x - 85:x].sum() > 140]
print(" GREEN  fill wide cols y=210:", cols[0] if cols else None, "..", cols[-1] if cols else None)

# blue box: pale blue fill + violet-ish border
bf = (B > R + 4) & (B > 235) & (R > 235) & (G > 240) & (B > G)
rows = [y for y in range(220, 440) if bf[y, 200:750].sum() > 300]
print(" BLUE   fill wide rows:", rows[0] if rows else None, "..", rows[-1] if rows else None)
vb = (B > R + 25) & (B > 150) & (R < 225)
print(" BLUE   violet rows x=600:", edge_rows(vb, 600, 220, 440))
print(" BLUE   violet cols y=320:", [x for x in range(80, 100) if vb[320, x]],
      [x for x in range(855, 880) if vb[320, x]])
cols = [x for x in range(80, 880) if bf[320, x - 80:x].sum() > 500]
print(" BLUE   fill wide cols y=320:", cols[0] if cols else None, "..", cols[-1] if cols else None)

yf = (R > 245) & (G > 245) & (B > 205) & (B < 242)
rows = [y for y in range(425, min(545, H)) if yf[y, 200:750].sum() > 300]
print(" YELLOW fill wide rows:", rows[0] if rows else None, "..", rows[-1] if rows else None)
cols = [x for x in range(80, 880) if yf[500, x - 80:x].sum() > 500]
print(" YELLOW fill wide cols y=500:", cols[0] if cols else None, "..", cols[-1] if cols else None)
print(" YELLOW violet/brown top rows x=600:", edge_rows(vb, 600, 425, min(545, H)))
print(" YELLOW border cols y=500:", [x for x in range(80, 100) if vb[500, x]],
      [x for x in range(860, 880) if vb[500, x]])

print("\n== BADGE ==")
sub = a[40:110, 840:915]
ys, xs = np.where(np.abs(sub - np.array([255, 255, 166])).sum(axis=2) < 200)
print("  badge-ish bbox x", xs.min() + 840, "..", xs.max() + 840, " y",
      ys.min() + 40, "..", ys.max() + 40)
for r in [70, 73, 76]:
    xs = np.where(np.abs(a[r, 845:910] - np.array([109, 90, 205])).sum(axis=1) < 260)[0]
    print(f"  ring row y={r}: x {xs.min()+845 if len(xs) else None}..{xs.max()+845 if len(xs) else None} n={len(xs)}")
xs = np.where(np.abs(a[73, 845:910] - np.array([109, 90, 205])).sum(axis=1) < 260)[0]
print("  ring cols y=73:", [int(v + 845) for v in xs])
ys = np.where(np.abs(a[45:105, 876] - np.array([109, 90, 205])).sum(axis=1) < 260)[0]
print("  ring rows x=876:", [int(v + 45) for v in ys])
