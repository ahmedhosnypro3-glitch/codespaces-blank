#!/usr/bin/env python3
"""Consolidated precise measurement of slide_023.jpg for the build.
Measures: title bbox/size, each box bbox + fill + border colors, every text
line's y-extent/x-extent/pitch, equation ink bbox + baseline, centering.
960x540 frame, 1px = 1pt = 1/72in."""
import numpy as np
from PIL import Image
from collections import Counter

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]


def bbox(mask, y0, y1, x0, x1):
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    if not sub.any():
        return None
    ys, xs = np.where(sub)
    return (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0))


def modal(arr, mask, n=3):
    px = arr[mask]
    if len(px) == 0:
        return None
    return Counter(map(tuple, px.tolist())).most_common(n)


red = (R > 120) & (R - G > 80) & (R - B > 80)
navy = (B > R + 40) & (B > 90) & (G < 120)      # dark blue #1F3864 family
blk = (R < 110) & (G < 110) & (B < 110)
darkink = blk | (navy & (R < 190))

print("=" * 70)
print("TITLE (red, y70..110)")
print(" bbox:", bbox(red, 70, 110, 0, W - 1))
rows = [y for y in range(70, 112) if red[y, 100:800].sum() > 0]
print(" red rows with ink:", rows[0], "..", rows[-1] if rows else None, " cap-height=",
      (rows[-1] - rows[0] + 1) if rows else 0)

print("=" * 70)
print("BOX GEOMETRY (row/col scans for fill + border)")

# --- scan each box's vertical extent via column x=400 (through a text-free strip) ---
def col_scan(x, y0, y1):
    return [(y, tuple(a[y, x])) for y in range(y0, y1 + 1)]

# green box: find top/bottom border by looking for saturated green border color
gborder = (G > R + 40) & (G > B + 40) & (G > 90) & (G < 190)
print(" green border rows at x=600:", [y for y in range(90, 240) if gborder[y, 600]])
print(" green border cols at y=210:", [x for x in range(80, 800) if gborder[210, x]])
_gstrip = a[160, 200:700]
_gm = (gborder[160, 200:700]) | (_gstrip[:, 1] > 245)
print(" green fill modal (y160, x200..700):", Counter(map(tuple, _gstrip[_gm].tolist())).most_common(3))

# fill colors (interior, text-free)
print(" GREEN fill cores:", Counter(map(tuple, a[160:200, 600:740].reshape(-1, 3).tolist())).most_common(2))
print(" GREEN border core:", Counter(map(tuple, a[111, 300:600].tolist())).most_common(2),
      Counter(map(tuple, a[112, 300:600].tolist())).most_common(2))
print(" GREEN left border:", Counter(map(tuple, a[160:180, 98:100].reshape(-1, 3).tolist())).most_common(2))
print(" GREEN right border:", Counter(map(tuple, a[160:180, 753:756].reshape(-1, 3).tolist())).most_common(2))

print(" BLUE fill cores:", Counter(map(tuple, a[250:270, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" BLUE border top core:", Counter(map(tuple, a[229, 300:600].tolist())).most_common(2))
print(" BLUE border left core:", Counter(map(tuple, a[300:400, 88:90].reshape(-1, 3).tolist())).most_common(2))
print(" BLUE border right core:", Counter(map(tuple, a[300:400, 867:870].reshape(-1, 3).tolist())).most_common(2))

print(" SOLUTION fill cores:", Counter(map(tuple, a[250:270, 300:600].reshape(-1, 3).tolist())).most_common(1))
print(" SOLUTION fill cores2 (y455..465 x500..860):", Counter(map(tuple, a[455:465, 500:860].reshape(-1, 3).tolist())).most_common(2))
print(" SOLUTION border top core y436:", Counter(map(tuple, a[436, 300:600].tolist())).most_common(2))
print(" SOLUTION border left core x87:", Counter(map(tuple, a[470:500, 87:88].reshape(-1, 3).tolist())).most_common(2))
print(" SOLUTION border right core x874:", Counter(map(tuple, a[470:500, 874:875].reshape(-1, 3).tolist())).most_common(2))
print(" SOLUTION border bottom y530:", Counter(map(tuple, a[530, 300:600].tolist())).most_common(2))

print("=" * 70)
print("BOX ROW/COL EXTENT (full scans)")


def full_extent(mask, minpx=20):
    rows = np.where(mask.sum(axis=1) > minpx)[0]
    return (int(rows[0]), int(rows[-1])) if len(rows) else None


greenfill = (G > R + 6) & (G > B + 10) & (G > 200) & (R > 180) & (G < 250)
print(" green fill rows (x95..770):", full_extent(greenfill[:, 95:770]))

print("=" * 70)
print("TEXT LINES — bbox + cap-height per line (for font size)")
lines = [
    ("title",      red,                70, 110, 150, 800),
    ("recall",     darkink,           110, 145,  90, 700),
    ("equation",   darkink | red,     146, 190,  95, 760),
    ("dimnote",    darkink | red,     191, 218,  95, 780),
    ("blueL1",     navy | red,        238, 268,  90, 870),
    ("blueL2",     navy | red,        270, 300,  90, 870),
    ("blueL3",     navy | red,        302, 336,  90, 870),
    ("exL1",       blk | red,         356, 390,  90, 870),
    ("exL2",       blk | red,         392, 424,  90, 870),
    ("solL1",      navy,              470, 500, 240, 730),
    ("solL2",      navy,              500, 528, 300, 670),
]
for name, m, y0, y1, x0, x1 in lines:
    b = bbox(m, y0, y1, x0, x1)
    print(f" {name:9s} bbox={b}")
    if b:
        h = b[3] - b[1] + 1
        print(f"           height={h}  est_Arial_pt(cap 0.72)={h/0.72:.1f}  (x-h 0.52)={h/0.52:.1f}")

print("=" * 70)
print("BLUE box line pitch (navy row bands, x100..860)")
nb = navy[:, 100:860]
rows = np.where(nb.sum(axis=1) > 2)[0]
bands = []
s = p = rows[0]
for r in rows[1:]:
    if r > p + 2:
        bands.append((s, p)); s = r
    p = r
bands.append((s, p))
for b in bands:
    print("   navy band y%d..%d" % b)
print(" pitch between band tops:", [bands[i + 1][0] - bands[i][0] for i in range(len(bands) - 1)])

print("=" * 70)
print("EQUATION detail (x100..440, y146..192)")
ink = darkink | red
sub = ink[146:193, 100:440]
colhit = sub.any(axis=0)
xs = np.where(colhit)[0]
groups = []
g0 = xs[0]
prev = xs[0]
for x in xs[1:]:
    if x - prev > 2:
        groups.append((int(g0 + 100), int(prev + 100)))
        g0 = x
    prev = x
groups.append((int(g0 + 100), int(prev + 100)))
for (g0, g1) in groups:
    seg = ink[146:193, g0:g1 + 1]
    ys = np.where(seg.any(axis=1))[0]
    segred = red[146:193, g0:g1 + 1]
    print(f"  x{g0}..{g1} w={g1-g0+1} y{ys[0]+146}..{ys[-1]+146} h={ys[-1]-ys[0]+1} redpx={int(segred.sum())}")

print("=" * 70)
print("DIM NOTE line: separate words/segments x100..780 y191..218")
dn = darkink | red
sub = dn[191:219, 100:780]
colhit = sub.any(axis=0)
xs = np.where(colhit)[0]
groups = []
g0 = xs[0]; prev = xs[0]
for x in xs[1:]:
    if x - prev > 3:
        groups.append((int(g0 + 100), int(prev + 100))); g0 = x
    prev = x
groups.append((int(g0 + 100), int(prev + 100)))
for (g0, g1) in groups:
    seg = dn[191:219, g0:g1 + 1]
    ys = np.where(seg.any(axis=1))[0]
    sr = red[191:219, g0:g1 + 1]
    print(f"  x{g0}..{g1} w={g1-g0+1} y{ys[0]+191}..{ys[-1]+191} redpx={int(sr.sum())} inkpx={int(seg.sum())}")

print("=" * 70)
print("CENTERING CHECK")
print(" panel x54..903 center =", (54 + 903) / 2)
print(" green box x-range; sol box x-range")