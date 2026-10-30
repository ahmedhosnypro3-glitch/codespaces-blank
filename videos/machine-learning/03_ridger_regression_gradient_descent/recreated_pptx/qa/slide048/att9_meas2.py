#!/usr/bin/env python3
"""att9 measurement pass 2: precise bboxes for the 048 rebuild."""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)

def runs(mask, start):
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None: s = i
        elif not v and s is not None: out.append((start + s, start + i - 1)); s = None
    if s is not None: out.append((start + s, start + len(mask) - 1))
    return out

def col_bands(a, x0, x1, y0, y1, thr=185):
    z = a[y0:y1, x0:x1]
    m = z.sum(axis=2) < thr * 3
    res = []
    for (cx0, cx1) in runs(m.any(axis=0), x0):
        sub = m[:, cx0 - x0:cx1 - x0 + 1]
        yb = runs(sub.any(axis=1), y0)
        px = a[y0:y1, cx0:cx1 + 1][sub]
        res.append((cx0, cx1, yb, px.mean(axis=0).round().astype(int), len(px)))
    return res

print("===== 1. 048 row-1 LEFT side, rule excluded (x274..600, y143..196) =====")
for b in col_bands(O48, 274, 600, 143, 196):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} mean={tuple(b[3])} npx={b[4]}")

print("===== 2. 049 row-2 W-column ink bbox in orig (x715..760, y207..262) =====")
z = O49[207:262, 715:760]; m = z.sum(axis=2) < 185 * 3
ys, xs = np.where(m)
print(f"  ink x{715+xs.min()}..{715+xs.max()} y{207+ys.min()}..{207+ys.max()} npx={m.sum()}")

print("===== 3. wcol asset ink bbox =====")
im = np.array(Image.open(f"{DECK}/recreated_pptx/build/assets/slide_049_wcol_paren_1.png").convert("RGBA"))
alpha = im[:, :, 3]; dark = (im[:, :, :3].sum(axis=2) < 600) & (alpha > 40)
ys, xs = np.where(dark)
print(f"  asset {im.shape[1]}x{im.shape[0]}px ink x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} "
      f"-> frame {xs.min()*0.12:.1f}..{xs.max()*0.12:.1f} x {ys.min()*0.12:.1f}..{ys.max()*0.12:.1f} pt")
# per-row digit bands inside asset
rows = dark.any(axis=1)
print(f"  y-runs(pt): {[(round(a*0.12,1), round(b*0.12,1)) for a, b in runs(rows, 0)]}")
iw = np.array(Image.open(f"{DECK}/recreated_pptx/build/assets/eq_initial_w_col_paren.png").convert("RGBA"))
al = iw[:, :, 3]; dk = (iw[:, :, :3].sum(axis=2) < 600) & (al > 40)
ys, xs = np.where(dk)
print(f"  iw asset {iw.shape[1]}x{iw.shape[0]}px ink x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} "
      f"-> frame {xs.min()*0.12:.1f}..{xs.max()*0.12:.1f} x {ys.min()*0.12:.1f}..{ys.max()*0.12:.1f} pt")
rows = dk.any(axis=1)
print(f"  iw y-runs(pt): {[(round(a*0.12,1), round(b*0.12,1)) for a, b in runs(rows, 0)]}")

print("===== 4. green calibration: 048 legend Zero vs row-1 result =====")
z = O48[108:126, 390:430]; m = z.sum(axis=2) < 650
g = m & (z[:, :, 1] > z[:, :, 0] + 15) & (z[:, :, 1] > z[:, :, 2] + 15)
if g.sum():
    px = z[g]
    print(f"  legend Zero: npx={g.sum()} mean={px.mean(axis=0).round().astype(int)} "
          f"darkest={px[px.sum(axis=1).argmin()]}")
z = O48[148:196, 736:770]; m = z.sum(axis=2) < 650
g = m & (z[:, :, 1] > z[:, :, 0] + 15) & (z[:, :, 1] > z[:, :, 2] + 15)
px = z[g]
print(f"  row-1 result: npx={g.sum()} mean={px.mean(axis=0).round().astype(int)} "
      f"darkest={px[px.sum(axis=1).argmin()]}")
# per-x sub-columns of the green column (paren vs digit zones)
cols = g.any(axis=0)
print(f"  green x-runs: {runs(cols, 736)}")
for (a, b) in runs(cols, 736):
    sub = g[:, a - 736:b - 736 + 1]
    yy = runs(sub.any(axis=1), 148)
    px = O48[148:196, a:b + 1][sub]
    print(f"    x{a}..{b} yr={yy} npx={sub.sum()} mean={px.mean(axis=0).round().astype(int)} "
          f"darkest={px[px.sum(axis=1).argmin()]}")

print("===== 5. rows 2-6 LEFT side diff 048 vs 049 (x276..598) =====")
for name, (ya, yb) in [("r2", (199, 271)), ("r3", (274, 329)), ("r4", (332, 394)),
                       ("r5", (406, 460)), ("r6", (463, 527))]:
    d = np.abs(O48[ya:yb, 276:598] - O49[ya:yb, 276:598]).sum(axis=2)
    print(f"  {name} y{ya}..{yb}: max|d|={d.max()} npx>60={(d > 60).sum()}")

print("===== 6. z_zone diff localization (x530..715, y60..130) =====")
d = np.abs(O48[60:130, 530:715] - O49[60:130, 530:715]).sum(axis=2)
ys, xs = np.where(d > 60)
if len(xs):
    print(f"  diff bbox x{530+xs.min()}..{530+xs.max()} y{60+ys.min()}..{60+ys.max()} npx={len(xs)}")
    import collections
    cc = collections.Counter((530 + x) // 20 * 20 for x in xs)
    print(f"  x-hist: {sorted(cc.items())}")

print("===== 7. 048 panel horizontal rules (x300..840, thr sum<620) =====")
z = O48[135:535, 300:840]
m = z.sum(axis=2) < 620
rc = m.sum(axis=1)
for i, c in enumerate(rc):
    if c > 400: print(f"  rule y={135+i} npx={c}")
# left vertical
z2 = O48[145:520, 270:280]; m2 = z2.sum(axis=2) < 620
cc = m2.sum(axis=0)
print(f"  left-vertical x-census (x270..280): {[(270+i, int(c)) for i, c in enumerate(cc) if c > 100]}")

print("===== 8. legend diff localization (x235..512, y106..126) =====")
d = np.abs(O48[106:126, 235:512] - O49[106:126, 235:512]).sum(axis=2)
ys, xs = np.where(d > 60)
if len(xs):
    print(f"  diff bbox x{235+xs.min()}..{235+xs.max()} y{106+ys.min()}..{106+ys.max()} npx={len(xs)}")

print("===== 9. row-1 left column (4;-2;-2) precise (x370..412, y143..196) =====")
for b in col_bands(O48, 370, 412, 143, 196):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} mean={tuple(b[3])} npx={b[4]}")

print("===== 10. 048 rows 2-6 left-side anatomy sample (r2 x274..600, y199..271) =====")
for b in col_bands(O48, 274, 600, 199, 271):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} mean={tuple(b[3])} npx={b[4]}")
