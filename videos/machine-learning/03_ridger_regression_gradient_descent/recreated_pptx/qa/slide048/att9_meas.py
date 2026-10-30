#!/usr/bin/env python3
"""att9 pre-build PIL measurements for slide 048 (carrier-s7a-048-fc1).

Settles, from bytes only:
  A. row-1 right-side anatomy + colors (green result-vector claim, red +1, red <=)
  B. row-1 left-side anatomy (bracket columns, triplet, label, =0)
  C. rows 2-6 right side vs 049 orig (pixel-identity claim)
  D. top band / legend / Z zone vs 049 orig (pixel-identity claims)
  E. aug box vs 049 orig + title ink color + extent (caption fix #4)
  F. calc-panel rule lines + left-bottom emptiness census
"""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
H, W = O48.shape[:2]
print(f"orig size {W}x{H}")

def ink(a, thr=170):
    return a.sum(axis=2) < thr * 3

def runs(mask, axis_vals):
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((axis_vals[s], axis_vals[i - 1])); s = None
    if s is not None:
        out.append((axis_vals[s], axis_vals[-1]))
    return out

def classify(px):
    r, g, b = px
    if r < 170 and g < 170 and b < 170:
        if r > g + 40 and r > b + 40: return "RED"
        if g > r + 25 and g > b + 25: return "GREEN"
        if b > r + 30 and b > g + 10: return "BLUE"
        return "INK"
    return f"({r},{g},{b})"

def col_bands(a, x0, x1, y0, y1, thr=170):
    """per-column ink presence -> column runs; for each run, y-bands + mean color"""
    z = a[y0:y1, x0:x1]
    m = ink(z, thr)
    cols = m.any(axis=0)
    res = []
    for (cx0, cx1) in runs(cols, range(x0, x1)):
        sub = m[:, cx0 - x0:cx1 - x0 + 1]
        ys = sub.any(axis=1)
        yb = runs(ys, range(y0, y1))
        px = a[y0:y1, cx0:cx1 + 1][sub]
        mean = px.mean(axis=0).round().astype(int)
        res.append((cx0, cx1, yb, classify(mean), len(px)))
    return res

print("\n===== A. ROW-1 RIGHT SIDE (x600..812, y139..197) =====")
for b in col_bands(O48, 600, 812, 139, 197):
    print(f"  x{b[0]}..{b[1]} ybands={b[2]} color={b[3]} npx={b[4]}")

print("\n===== B. ROW-1 LEFT SIDE (x274..600, y139..197) =====")
for b in col_bands(O48, 274, 600, 139, 197):
    print(f"  x{b[0]}..{b[1]} ybands={b[2]} color={b[3]} npx={b[4]}")

print("\n===== C. rows 2-6 right side: 048 vs 049 (x600..811) =====")
for name, (ya, yb) in [("r2", (199, 271)), ("r3", (274, 329)), ("r4", (332, 394)),
                       ("r5", (406, 460)), ("r6", (463, 527))]:
    d = np.abs(O48[ya:yb, 600:812] - O49[ya:yb, 600:812]).sum(axis=2)
    print(f"  {name} y{ya}..{yb}: max|d|={d.max()} npx>60={(d > 60).sum()}")

print("\n===== C2. 049 rows right side bands for mapping (x600..811) =====")
for name, (ya, yb) in [("049r1", (142, 205)), ("049r2", (208, 271)), ("049r3", (274, 337)),
                       ("049r4", (340, 403)), ("049r5", (406, 469)), ("049r6", (472, 527))]:
    d = np.abs(O48[ya:yb, 600:812] - O49[ya:yb, 600:812]).sum(axis=2)
    print(f"  {name} y{ya}..{yb}: max|d|={d.max()} npx>60={(d > 60).sum()}")

print("\n===== D. top band / legend / Z zone diffs 048 vs 049 =====")
for name, (x0, x1, ya, yb) in [
    ("top_band", (66, 734, 48, 132)), ("legend", (235, 512, 106, 126)),
    ("z_zone", (530, 715, 60, 130)), ("table_zone", (80, 225, 58, 130)),
    ("initialw", (325, 535, 55, 105))]:
    d = np.abs(O48[ya:yb, x0:x1] - O49[ya:yb, x0:x1]).sum(axis=2)
    print(f"  {name} x{x0}..{x1} y{ya}..{yb}: max|d|={d.max()} npx>60={(d > 60).sum()}")

print("\n===== E. aug box: diff + title color =====")
d = np.abs(O48[136:260, 66:250] - O49[136:260, 66:250]).sum(axis=2)
print(f"  aug box x66..250 y136..260: max|d|={d.max()} npx>60={(d > 60).sum()}")
t = O48[140:165, 70:248]
tm = ink(t, 170)
ys, xs = np.where(tm)
if len(xs):
    print(f"  048 title ink bbox x{70+xs.min()}..{70+xs.max()} y{140+ys.min()}..{140+ys.max()} npx={len(xs)}")
    px = t[tm]
    print(f"  048 title ink mean={px.mean(axis=0).round().astype(int)} "
          f"darkest={px[px.sum(axis=1).argmin()]}")
    # red/violet pixel count
    r_ink = ((px[:, 0] > px[:, 1] + 30) & (px[:, 0] > px[:, 2] + 30)).sum()
    v_ink = ((px[:, 2] > px[:, 0] + 20) & (px[:, 2] > px[:, 1] + 20)).sum()
    print(f"  048 title: red-ish px={r_ink} violet/blue-ish px={v_ink}")
t49 = O49[140:165, 70:248]
tm49 = ink(t49, 170)
ys49, xs49 = np.where(tm49)
if len(xs49):
    px49 = t49[tm49]
    print(f"  049 title ink bbox x{70+xs49.min()}..{70+xs49.max()} y{140+ys49.min()}..{140+ys49.max()} "
          f"mean={px49.mean(axis=0).round().astype(int)}")

print("\n===== F. calc rules + left-bottom census =====")
z = O48[135:535, 280:850]
m = ink(z, 175)
rows_ink = m.sum(axis=1)
for i, c in enumerate(rows_ink):
    if c > 300:
        print(f"  rule row y={135+i} npx={c}")
below = O48[310:538, 66:262]
bm = ink(below, 175)
print(f"  below-iteration-box zone x66..262 y310..538: ink px={bm.sum()}")

print("\n===== G. row-1 result-vector green check (x738..768, y148..194) =====")
z = O48[148:194, 736:770]
g = (z[:, :, 1] > z[:, :, 0] + 20) & (z[:, :, 1] > z[:, :, 2] + 20) & (z.sum(axis=2) < 600)
print(f"  green px={g.sum()}")
if g.sum():
    ys, xs = np.where(g)
    print(f"  green bbox x{736+xs.min()}..{736+xs.max()} y{148+ys.min()}..{148+ys.max()}")
    px = z[g]
    print(f"  green mean={px.mean(axis=0).round().astype(int)} darkest={px[px.sum(axis=1).argmin()]}")
# same check on 049's row W-columns for reference
z9 = O49[213:260, 718:750]
g9 = (z9[:, :, 1] > z9[:, :, 0] + 20) & (z9[:, :, 1] > z9[:, :, 2] + 20) & (z9.sum(axis=2) < 600)
print(f"  049 W-col zone green px={g9.sum()}")

print("\n===== H. row-1 right side: red px census (x670..812, y139..197) =====")
z = O48[139:197, 670:812]
r = (z[:, :, 0] > z[:, :, 1] + 40) & (z[:, :, 0] > z[:, :, 2] + 40) & (z.sum(axis=2) < 600)
print(f"  red px={r.sum()}")
if r.sum():
    ys, xs = np.where(r)
    print(f"  red bbox x{670+xs.min()}..{670+xs.max()} y{139+ys.min()}..{139+ys.max()}")
    # cluster by x
    cols = r.any(axis=0)
    print(f"  red x-runs: {[(670+a, 670+b) for a, b in runs(cols, range(0, 142))]}")
