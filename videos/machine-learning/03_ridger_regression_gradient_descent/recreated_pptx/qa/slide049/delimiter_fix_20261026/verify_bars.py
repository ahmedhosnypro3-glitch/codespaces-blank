#!/usr/bin/env python3
"""PIL verification of slide 049 straight delimiter bars + re-laid digit cells.
Expected geometry from locked measurements (frame px, render scale 2.0833 @150dpi).
Bar check = longest consecutive ink run in the column window. Digit checks compare
ink centroids (mask per color) against the locked original-frame centroids.
Exits 1 on any FAIL."""
import sys
from PIL import Image

NEW = sys.argv[1] if len(sys.argv) > 1 else "scratch/tmp/delimchk/r049_new.png"
SWEEP = sys.argv[2] if len(sys.argv) > 2 else ""
S = 2.0833
TOL = 5.0
B = [140, 206, 272, 338, 404, 470]
DY = [[145, 192], [214, 260], [277, 324], [347, 392], [410, 456], [475, 522]]

BARS = []
for x in [89.81, 111.95, 133.86, 156.28, 179.34, 202.25]: BARS.append((x, 77, 31, "top2"))
for x in [101.37, 123.59, 146.15, 169.01, 191.46, 213.61]: BARS.append((x, 77, 31, "top2"))
for x in [640.96, 664.10, 686.30]: BARS.append((x, 86, 33, "z"))
for x in [654.65, 676.56, 699.07]: BARS.append((x, 86, 33, "z"))
for x in [93.59, 115.28, 137.43, 160.65, 182.66, 205.64]: BARS.append((x, 180, 46, "aug"))
for x in [105.84, 127.15, 149.74, 172.35, 195.05, 217.20]: BARS.append((x, 180, 46, "aug"))
BARS += [(330.28, 57, 49, "iw"), (351.72, 57, 49, "iw")]
for i in range(6):
    b = B[i]; y0, y1 = DY[i]; h = y1 - y0 + 1
    BARS += [(329.0, b + 7, 13, f"trip{i}"), (375.0, b + 8, 12, f"trip{i}")]
    BARS += [(378.5, y0, h, f"dx{i}"), (401.0, y0, h, f"dx{i}")]
    wL, wR = (733.8, 755.4) if i >= 3 else (722.3, 744.0)
    BARS += [(wL, y0, h, f"W{i}"), (wR, y0, h, f"W{i}")]

im = Image.open(NEW).convert("RGB")
W, H = im.size
pix = im.load()
lum = lambda p: (p[0] + p[1] + p[2]) / 3

def longest_run(x0, x1, y0, y1, thresh=210):
    runs, cur = [], None
    for y in range(max(0, int(y0)), min(H, int(y1) + 1)):
        ink = any(lum(pix[x, y]) < thresh for x in range(int(x0), int(x1) + 1))
        if ink:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur:
            runs.append(cur); cur = None
    if cur: runs.append(cur)
    return max(runs, key=lambda r: r[1] - r[0]) if runs else None

def centroid(x0, x1, y0, y1, mask):
    pts = [(x, y) for y in range(max(0, int(y0)), min(H, int(y1) + 1))
           for x in range(max(0, int(x0)), min(W, int(x1) + 1)) if mask(pix[x, y])]
    if not pts: return None
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n, n)

GREENM = lambda p: p[1] > p[0] + 30 and p[1] > p[2] + 30 and lum(p) < 230
BLACKM = lambda p: lum(p) < 100
REDM = lambda p: p[0] > p[1] + 50 and p[0] > p[2] + 50 and lum(p) < 230
INKM = lambda p: p[2] > p[0] + 40 and p[2] > p[1] + 40 and lum(p) < 230

fails = 0
for (x, y0, h, tag) in BARS:
    m = longest_run((x - 1.2) * S, (x + 2.2) * S, (y0 - 3) * S, (y0 + h + 3) * S)
    exp_c = (y0 + h / 2.0) * S
    if m is None:
        print(f"FAIL {tag} x={x}: NO INK"); fails += 1
    else:
        mc = (m[0] + m[1]) / 2.0
        ok = abs(mc - exp_c) <= TOL
        print(f"{'PASS' if ok else 'FAIL'} {tag} x={x}: run c {mc:.1f} vs {exp_c:.1f}")
        fails += 0 if ok else 1

# dx digits: GREEN, '5'@392, '-1'@393.5, cys b+12/b+29/b+45.5
for i in range(6):
    b = B[i]
    for t, cx, cy in (("5", 392, b + 12), ("m1", 393.5, b + 29), ("m1", 393.5, b + 45.5)):
        c = centroid((cx - 9) * S, (cx + 9) * S, (cy - 9) * S, (cy + 9) * S, GREENM)
        if c is None: print(f"FAIL dx{i} {t}@{cy}: NO GREEN"); fails += 1
        else:
            ok = abs(c[0] - cx * S) <= TOL and abs(c[1] - cy * S) <= TOL
            print(f"{'PASS' if ok else 'FAIL'} dx{i} {t}: ({c[0]:.1f},{c[1]:.1f}) n={c[2]}")
            fails += 0 if ok else 1
# W digits: BLACK, r1-3 5@733.5/m1@736; r4-6 5@745.5/m1@748; same cys
for i in range(6):
    b = B[i]
    w5, wm1 = (745.5, 748) if i >= 3 else (733.5, 736)
    for t, cx, cy in (("5", w5, b + 12), ("m1", wm1, b + 29), ("m1", wm1, b + 45.5)):
        c = centroid((cx - 9) * S, (cx + 9) * S, (cy - 9) * S, (cy + 9) * S, BLACKM)
        if c is None: print(f"FAIL W{i} {t}@{cy}: NO BLACK"); fails += 1
        else:
            ok = abs(c[0] - cx * S) <= TOL and abs(c[1] - cy * S) <= TOL
            print(f"{'PASS' if ok else 'FAIL'} W{i} {t}: ({c[0]:.1f},{c[1]:.1f}) n={c[2]}")
            fails += 0 if ok else 1
# initial-W digits: BLACK 13pt, 4@341.5, -2@344.5 x2, cys 66.5/82.5/97.5
for t, cx, cy in (("4", 341.5, 66.5), ("m2", 344.5, 82.5), ("m2", 344.5, 97.5)):
    c = centroid((cx - 9) * S, (cx + 9) * S, (cy - 9) * S, (cy + 9) * S, BLACKM)
    if c is None: print(f"FAIL iw {t}@{cy}: NO BLACK"); fails += 1
    else:
        ok = abs(c[0] - cx * S) <= TOL and abs(c[1] - cy * S) <= TOL
        print(f"{'PASS' if ok else 'FAIL'} iw {t}: ({c[0]:.1f},{c[1]:.1f}) n={c[2]}")
        fails += 0 if ok else 1
# untouched certified triplet digits still present: centres 335/353/371, ink ~b+15
for i in range(6):
    b = B[i]
    mask = REDM if i < 3 else INKM
    for k, cx in enumerate([335, 353, 371]):
        c = centroid((cx - 6) * S, (cx + 6) * S, (b + 6) * S, (b + 24) * S, mask)
        if c is None: print(f"FAIL trip{i} d{k}: NO {'RED' if i<3 else 'INK'}"); fails += 1
        else:
            ok = abs(c[1] - (b + 15) * S) <= 7.0
            print(f"{'PASS' if ok else 'FAIL'} trip{i} d{k}: ({c[0]:.1f},{c[1]:.1f}) n={c[2]}")
            fails += 0 if ok else 1

# zone-confined diff vs the HEAD build render (my edit base); chrome hairline
# jitter bands excluded
if SWEEP:
    import numpy as np
    ZONES = [(86.5, 74, 217.5, 111), (638, 83, 702, 122), (91, 177.5, 220, 229),
             (324, 54, 358, 110), (326, 144, 405, 528), (693, 144, 760, 528)]
    def in_zones(fx_, fy_):
        return any(a <= fx_ <= c and bb <= fy_ <= d for (a, bb, c, d) in ZONES)
    def in_jitter(rx, ry):
        return (117 <= rx <= 127 or 1873 <= rx <= 1884 or 1117 <= ry <= 1126
                or (1788 <= rx <= 1860 and 114 <= ry <= 190))
    a = np.asarray(Image.open(SWEEP).convert("RGB")).astype(int)
    b2 = np.asarray(im).astype(int)
    d = np.abs(a - b2).max(axis=2)
    bad = [(x, y) for y, x in zip(*np.nonzero(d > 8))
           if not in_zones(x / S, y / S) and not in_jitter(x, y)]
    print(f"diff-vs-sweep>8: {(d > 8).sum()} px; outside zones+jitter: {len(bad)}")
    for x, y in bad[:12]:
        print(f"  STRAY ({x},{y}) frame=({x/S:.1f},{y/S:.1f}) d={d[y,x]}")
    fails += len(bad)
print("EXIT " + ("FAIL" if fails else "PASS") + f" ({fails} failures)")
sys.exit(1 if fails else 0)
