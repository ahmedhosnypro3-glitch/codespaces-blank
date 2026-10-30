#!/usr/bin/env python3
"""Logo structure + residual-ink scan + bold/regular stroke probes for slide_001.jpg."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

print("=== LOGO full structure (x560..960, y430..545) ===")
x0, x1, y0, y1 = 560, 960, 430, 545
seg = IM[y0:y1, x0:x1]
sr, sg, sb = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
# non-panel ink
bgd = np.minimum(np.abs(seg - np.array([231, 233, 230])).sum(axis=2),
                 np.abs(seg - np.array([254, 255, 253])).sum(axis=2))
ink = bgd > 60
ys, xs = np.where(ink)
print(f"logo-region ink bbox: x {x0+xs.min()}..{x0+xs.max()}, y {y0+ys.min()}..{y0+ys.max()}")
# class masks
teal = (sg > 120) & (sb > 120) & (sr < 110) & (abs(sg - sb) < 60)
white = (sr > 248) & (sg > 248) & (sb > 248)
dark = (sr < 90) & (sg < 90) & (sb < 90)
pink = (sr > 140) & (sr < 230) & (sg > 80) & (sg < 180) & (sb > 110) & (sb < 200) & (sr > sb)
for nm, m in [("teal", teal), ("white", white), ("dark", dark), ("pink", pink)]:
    ys, xs = np.where(m)
    if len(ys):
        print(f"{nm}: n={len(ys)}, bbox x {x0+xs.min()}..{x0+xs.max()}, y {y0+ys.min()}..{y0+ys.max()}")
    else:
        print(f"{nm}: none")

# White right panel: exclude text pixels — take white-only columns/rows coverage
print("\nwhite panel extent (rows/cols with >50% white):")
wc = white.sum(axis=0)
wr = white.sum(axis=1)
onx = np.where(wc > (y1 - y0) * 0.4)[0]
ony = np.where(wr > (x1 - x0) * 0.4)[0]
if len(onx):
    print(f"  white cols {x0+onx.min()}..{x0+onx.max()}; rows {y0+ony.min()}..{y0+ony.max()}" if len(ony) else f"  white cols {x0+onx.min()}..{x0+onx.max()}, no majority rows")

# teal panel: text-free rows for extent
tc = teal.sum(axis=0)
trx = teal.sum(axis=1)
onx2 = np.where(tc > 5)[0]
ony2 = np.where(trx > 5)[0]
print(f"teal panel cols {x0+onx2.min()}..{x0+onx2.max()}, rows {y0+ony2.min()}..{y0+ony2.max()}")

# white text inside teal panel (ZEWAIL CITY)
treg = teal | (white & np.zeros_like(teal))
inside = IM[y0:y1, x0:x1]
wt = (inside[:, :, 0] > 240) & (inside[:, :, 1] > 240) & (inside[:, :, 2] > 240)
# white pixels within teal bbox
tb0, tb1 = ony2.min(), ony2.max()
tbc0, tbc1 = onx2.min(), onx2.max()
sub_wt = wt[tb0:tb1 + 1, tbc0:tbc1 + 1]
ys, xs = np.where(sub_wt)
if len(ys):
    print(f"WHITE text/px inside teal: n={len(ys)}, bbox x {x0+tbc0+xs.min()}..{x0+tbc0+xs.max()}, y {y0+tb0+ys.min()}..{y0+tb0+ys.max()}")
    rows = np.where(sub_wt.any(axis=1))[0]
    if len(rows):
        bands = []
        s = p = rows[0]
        for yy in rows[1:]:
            if yy - p > 2:
                bands.append((s, p)); s = yy
            p = yy
        bands.append((s, p))
        print(f"  white bands (y+offset {y0+tb0}): {[(y0+tb0+a, y0+tb0+z) for a, z in bands]}")

# dark text in right panel: line structure x from teal right edge to white extent
print("\ndark text lines in right panel (x676..900):")
dreg = dark[:, :]
sub_d = dreg[:, 676 - x0:900 - x0]
rows = np.where(sub_d.any(axis=1))[0]
if len(rows):
    bands = []
    s = p = rows[0]
    for yy in rows[1:]:
        if yy - p > 2:
            bands.append((s, p)); s = yy
        p = yy
    bands.append((s, p))
    for a, z in bands:
        xs2 = np.where(sub_d[a:z + 1].any(axis=0))[0]
        pxs = seg[a:z + 1][:, 676 - x0:900 - x0][sub_d[a:z + 1]]
        cnt = Counter(map(tuple, pxs // 24 * 24))
        print(f"  dark line y {y0+a}..{y0+z} (h={z-a+1}), x {676+xs2.min()}..{676+xs2.max()}: {cnt.most_common(3)}")

# pink pixels: where?
ys, xs = np.where(pink)
if len(ys):
    cnt = Counter(map(tuple, seg[pink] // 24 * 24))
    print(f"\npink colors: {cnt.most_common(5)}")
    # pink rows bands
    rows = np.where(pink.any(axis=1))[0]
    bands = []
    s = p = rows[0]
    for yy in rows[1:]:
        if yy - p > 3:
            bands.append((s, p)); s = yy
        p = yy
    bands.append((s, p))
    for a, z in bands:
        xs3 = np.where(pink[a:z + 1].any(axis=0))[0]
        print(f"  pink band y {y0+a}..{y0+z}, x {x0+xs3.min()}..{x0+xs3.max()}, n={pink[a:z+1].sum()}")

print("\n=== RESIDUAL INK SCAN (unattributed regions) ===")
bgdF = np.minimum(np.abs(IM - np.array([231, 233, 230])).sum(axis=2),
                  np.abs(IM - np.array([254, 255, 253])).sum(axis=2))
inkF = bgdF > 90
# attributed regions (generous): chrome strokes x54..65,895..910 + bottom rows>533
# + badge x850..900 y50..100 + title x270..680 y120..280 + subtitle x340..610 y310..340
# + prepared x430..550 y350..375 + name x345..635 y375..402 + email x380..600 y402..420
# + instr x80..390 y418..536 + logo x580..900 y440..540
mask = np.zeros_like(inkF)
mask[:, :70] = True
mask[:, 890:] = True
mask[530:, :] = True
mask[40:110, 845:910] = True
mask[115:285, 265:690] = True
mask[305:345, 335:615] = True
mask[348:378, 425:555] = True
mask[372:405, 340:640] = True
mask[398:422, 375:605] = True
mask[415:540, 75:400] = True
mask[435:545, 575:905] = True
resid = inkF & ~mask
ys, xs = np.where(resid)
print(f"residual ink px: {len(ys)}")
if len(ys):
    # cluster residuals coarsely
    from collections import defaultdict
    clusters = defaultdict(list)
    for y, x in zip(ys, xs):
        clusters[(y // 30, x // 60)].append((y, x))
    for k in sorted(clusters):
        pts = clusters[k]
        ys2 = [p[0] for p in pts]; xs2 = [p[1] for p in pts]
        print(f"  cluster ~y{min(ys2)}..{max(ys2)} x{min(xs2)}..{max(xs2)}: n={len(pts)}")
        cnt = Counter(map(tuple, IM[min(ys2):max(ys2)+1, min(xs2):max(xs2)+1].reshape(-1, 3)[::max(1, len(pts)//50)]))
        print(f"    sample colors: {cnt.most_common(3)}")

print("\n=== stroke-width probes (bold vs regular) ===")
def stem_width(y_top, y_bot, x_left, x_right, label):
    sub = IM[y_top:y_bot, x_left:x_right]
    s = np.minimum(np.abs(sub - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub - np.array([254, 255, 253])).sum(axis=2)) > 90
    mid = s[len(s) // 2]
    # find runs
    idx = np.where(mid)[0]
    runs = []
    if len(idx):
        st = p = idx[0]
        for i in idx[1:]:
            if i - p > 1:
                runs.append((st, p)); st = i
            p = i
        runs.append((st, p))
    print(f"{label}: mid-row runs {[ (x_left+a, x_left+z, z-a+1) for a,z in runs ]}")

# 'l' stem in Khaled (center name, bold per spec): 'Khaled' approx x390..455 (from slice: 390-455)
stem_width(383, 392, 388, 460, "center name midrow (y383..392)")
# same text in instructors block: 'Dr.' at x124..~152, midrow
stem_width(453, 462, 122, 380, "instr name1 midrow (y453..462)")
# subtitle (bold per spec) midrow for comparison
stem_width(318, 330, 345, 605, "subtitle midrow (y318..330)")
# email (regular per spec)
stem_width(407, 414, 382, 596, "center email midrow (y407..414)")
# instr email1 midrow
stem_width(476, 483, 123, 325, "instr email1 midrow (y476..483)")
# instr name2 midrow
stem_width(498, 506, 122, 345, "instr name2 midrow (y498..506)")
# instr email2 midrow
stem_width(520, 527, 122, 318, "instr email2 midrow (y520..527)")

print("\n=== instructors header left edge + first blue line left edge (precise) ===")
for (label, ya, yb, xa, xb) in [
    ("hdr 'Instructors:'", 422, 438, 70, 230),
    ("name1 line", 449, 469, 110, 400),
    ("email1 line", 472, 487, 110, 340),
    ("name2 line", 494, 510, 110, 360),
    ("email2 line", 516, 532, 110, 330),
]:
    sub = IM[ya:yb, xa:xb]
    s = np.minimum(np.abs(sub - np.array([231, 233, 230])).sum(axis=2),
                   np.abs(sub - np.array([254, 255, 253])).sum(axis=2)) > 90
    cols = np.where(s.any(axis=0))[0]
    rows = np.where(s.any(axis=1))[0]
    print(f"{label}: x {xa+cols.min()}..{xa+cols.max()}, y {ya+rows.min()}..{ya+rows.max()}")
