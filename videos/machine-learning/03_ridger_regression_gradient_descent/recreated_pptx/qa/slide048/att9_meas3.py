#!/usr/bin/env python3
"""att9 measurement pass 3: z_zone anatomy, rule zones, asset digit anchors."""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
A = f"{DECK}/recreated_pptx/build/assets"

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

print("===== 1. rule-zone diffs 048 vs 049 =====")
for name, (ya, yb) in [("197/206", (193, 210)), ("263/272", (259, 276)),
                       ("329/338", (325, 342)), ("395/404", (391, 408)),
                       ("461/470", (457, 474)), ("528", (524, 532))]:
    d = np.abs(O48[ya:yb, 300:840] - O49[ya:yb, 300:840]).sum(axis=2)
    print(f"  {name}: max|d|={d.max()} npx>60={(d > 60).sum()}")

print("===== 2. x274 left vertical y-extent (both) =====")
for nm, O in [("048", O48), ("049", O49)]:
    z = O[140:535, 272:277]; m = z.sum(axis=2) < 620
    rr = m.sum(axis=1)
    ys = [140 + i for i, c in enumerate(rr) if c >= 2]
    print(f"  {nm}: vertical ink rows {min(ys)}..{max(ys)} count={len(ys)}")

print("===== 3. 049 r2 W-col digit bands (x724..744, y207..262) =====")
for b in col_bands(O49, 724, 746, 207, 262):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} npx={b[4]}")

print("===== 4. asset internal digit bands =====")
for nm, f in [("wcol", "slide_049_wcol_paren_1.png"), ("iw", "eq_initial_w_col_paren.png")]:
    im = np.array(Image.open(f"{A}/{f}").convert("RGBA"))
    dark = (im[:, :, :3].sum(axis=2) < 600) & (im[:, :, 3] > 128)
    # digits zone: exclude 3px-wide paren edges
    inner = dark[:, 30:180]
    rr = runs(inner.any(axis=1), 0)
    print(f"  {nm}: y-runs(px600)={rr} -> pt {[(round(a*.12,1), round(b*.12,1)) for a,b in rr]}")
    cc = runs(dark.any(axis=0), 0)
    print(f"  {nm}: x-runs(px600)={cc[:6]}{'...' if len(cc)>6 else ''} -> pt {[(round(a*.12,1), round(b*.12,1)) for a,b in cc[:6]]}")

print("===== 5. row-1 right col colors precise =====")
for nm, (x0, x1) in [("col1 digits", (648, 662)), ("col1 lp", (641, 645)),
                     ("col2 digits", (712, 717)), ("col2 lp", (705, 709)),
                     ("col3 digits", (748, 759))]:
    z = O48[150:194, x0:x1 + 1]; m = z.sum(axis=2) < 650
    if m.sum():
        px = z[m]
        print(f"  {nm}: npx={m.sum()} mean={px.mean(axis=0).round().astype(int)} "
              f"darkest={px[px.sum(axis=1).argmin()]}")

print("===== 6. z_zone anatomy: 048 vs 049 (x530..715, y60..130) =====")
for nm, O in [("048", O48), ("049", O49)]:
    print(f"  --- {nm} ---")
    for b in col_bands(O, 530, 715, 60, 130):
        print(f"    x{b[0]}..{b[1]} yb={b[2]} npx={b[4]}")
