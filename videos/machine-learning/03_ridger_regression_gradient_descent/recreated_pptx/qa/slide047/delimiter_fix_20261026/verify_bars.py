#!/usr/bin/env python3
"""PIL verification of slide 047 straight delimiter bars + re-laid digits.
Expected geometry from locked measurements (frame px, render scale 2.0833 @150dpi).
Bar check = longest consecutive ink run in the column window (robust to neighbor ink).
Exits 1 on any FAIL."""
import sys
from PIL import Image

NEW = sys.argv[1] if len(sys.argv) > 1 else "scratch/tmp/delimchk/r047_new.png"
OLD = sys.argv[2] if len(sys.argv) > 2 else "scratch/tmp/delimchk/r047-1.png"
S = 2.0833
TOL = 5.0

TL2_L = [89.81, 111.45, 133.54, 156.30, 178.75, 201.69]
TL2_R = [100.50, 122.84, 145.10, 168.06, 189.78, 212.36]
Z_L = [598.06, 621.45, 643.03]
Z_R = [609.92, 632.78, 654.45]
AUG_L = [93.27, 114.66, 137.11, 159.49, 182.17, 204.63]
AUG_R = [105.67, 126.09, 149.00, 171.29, 193.88, 215.93]
# (x, y0, h, tag)
BARS = []
for x in TL2_L: BARS.append((x, 77, 31, "tl2"))
for x in TL2_R: BARS.append((x, 77, 31, "tl2"))
for x in Z_L:   BARS.append((x, 80, 32, "z"))
for x in Z_R:   BARS.append((x, 80, 32, "z"))
for x in AUG_L: BARS.append((x, 180, 46, "aug"))
for x in AUG_R: BARS.append((x, 180, 46, "aug"))
BARS += [(330.5, 57, 50, "W"), (352.0, 57, 50, "W")]
for dy, h in ((0, 48), (69, 48), (135, 47)):
    BARS += [(330.0, 147 + dy, 13, f"trip{dy}"), (378.0, 148 + dy, 12, f"trip{dy}"),
             (380.9, 145 + dy, h, f"stack{dy}"), (403.95, 145 + dy, h, f"stack{dy}")]

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

BLUE = lambda p: p[2] > p[0] + 30 and p[2] > p[1] + 30 and lum(p) < 230
GREEN = lambda p: p[1] > p[0] + 30 and p[1] > p[2] + 30 and lum(p) < 230

fails = 0
for (x, y0, h, tag) in BARS:
    m = longest_run((x - 1.2) * S, (x + 2.2) * S, (y0 - 3) * S, (y0 + h + 3) * S)
    exp_c = (y0 + h / 2.0) * S
    if m is None:
        print(f"FAIL {tag} x={x}: NO INK"); fails += 1
    else:
        mc = (m[0] + m[1]) / 2.0
        ok = abs(mc - exp_c) <= TOL
        print(f"{'PASS' if ok else 'FAIL'} {tag} x={x}: run y {m[0]}..{m[1]} c {mc:.1f} vs {exp_c:.1f}")
        fails += 0 if ok else 1

for dy in (0, 69, 135):
    for k, cx in enumerate([336, 353.5, 369.5]):
        c = centroid((cx - 7) * S, (cx + 7) * S, (153.5 + dy - 9) * S, (153.5 + dy + 9) * S, BLUE)
        if c is None: print(f"FAIL rowvec dy={dy} d{k}: NO BLUE"); fails += 1
        else:
            ok = abs(c[0] - cx * S) <= TOL and abs(c[1] - (153.5 + dy) * S) <= TOL
            print(f"{'PASS' if ok else 'FAIL'} rowvec dy={dy} d{k}: ({c[0]:.1f},{c[1]:.1f}) n={c[2]}")
            fails += 0 if ok else 1
    for cy in (153.5, 167, 184):
        c = centroid((395 - 9) * S, (395 + 9) * S, (cy + dy - 8) * S, (cy + dy + 8) * S, GREEN)
        if c is None: print(f"FAIL stack dy={dy} cy={cy}: NO GREEN"); fails += 1
        else:
            ok = abs(c[0] - 395 * S) <= TOL and abs(c[1] - (cy + dy) * S) <= TOL
            print(f"{'PASS' if ok else 'FAIL'} stack dy={dy} cy={cy}: ({c[0]:.1f},{c[1]:.1f}) n={c[2]}")
            fails += 0 if ok else 1

# zone-confined diff vs before render (frame px boxes, padded)
ZONES = [(86.5, 74, 217.5, 110), (595, 77, 659, 114.5), (91, 177.5, 218.5, 229),
         (324, 54.5, 358, 109.5)]
for dy in (0, 69, 135):
    ZONES.append((327.5, 144 + dy, 381.5, 162 + dy))
    ZONES.append((378.5, 142.5 + dy, 407.5, 196.5 + dy))
def in_zones(fx, fy):
    return any(a <= fx <= c and b <= fy <= d for (a, b, c, d) in ZONES)
def in_jitter(rx, ry):
    return (117 <= rx <= 127 or 1873 <= rx <= 1884 or 1117 <= ry <= 1126
            or (1788 <= rx <= 1860 and 114 <= ry <= 190))
import numpy as np
a = np.asarray(Image.open(OLD).convert("RGB")).astype(int)
b = np.asarray(im).astype(int)
d = np.abs(a - b).max(axis=2)
bad = [(x, y) for y, x in zip(*np.nonzero(d > 8))
       if not in_zones(x / S, y / S) and not in_jitter(x, y)]
print(f"diff>8 total: {(d > 8).sum()} px; outside zones+jitter: {len(bad)}")
for x, y in bad[:12]:
    print(f"  STRAY ({x},{y}) frame=({x/S:.1f},{y/S:.1f}) d={d[y,x]}")
fails += len(bad)
print("EXIT " + ("FAIL" if fails else "PASS") + f" ({fails} failures)")
sys.exit(1 if fails else 0)
