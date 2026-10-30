#!/usr/bin/env python3
"""Adjudicate attempt-30 crop findings (title_bar, noreg_rows) vs the original.

Q1 italic shear: per-glyph ink-column shear between header top/bottom halves.
Q2 header blue modal color (orig vs render 0000FF).
Q3 Outlier-header panel fill (cream tint in orig?).
Q4 y-row digit colors per test column (red/green/red vs all-green).
Q5 W-paren ink bbox + stroke weight.
"""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q19 = f"{V}/recreated_pptx/qa/slide019"
S = 2001 / 960.0

orig = np.asarray(Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(f"{Q19}/render_28.png").convert("RGB")).astype(int)


def zone(a, x0, y0, x1, y1, sc=1.0):
    return a[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]


def ink_mask(z):
    # dark/blue text ink (not the pale yellow band)
    return z.sum(axis=2) < 460


print("=" * 76)
print("Q1/Q2: NO-REG header glyph shear + color  (x138..372 y178..200)")
print("=" * 76)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND28", rend, S)):
    z = zone(a, 138, 176, 372, 202, sc)
    m = ink_mask(z)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    blue = m & (b - r > 30)
    redm = m & (r - b > 40) & (r - g > 30)
    print(f"--- {tag} ---")
    print(f"  ink px={int(m.sum())}  blue px={int(blue.sum())}  red px={int(redm.sum())}")
    if int(blue.sum()) > 50:
        ys, xs = np.nonzero(blue)
        modal = np.median(z[ys, xs], axis=0)
        print(f"  blue modal rgb = {modal.round(1)}  bbox x {138 + xs.min()/sc:.1f}..{138 + xs.max()/sc:.1f}  y {176 + ys.min()/sc:.1f}..{176 + ys.max()/sc:.1f}")
    # shear: split ink rows into top/bottom halves, mean x per half over 12px-wide
    # glyph windows sampled every 24 px
    ys, xs = np.nonzero(m)
    if len(xs) < 100:
        print("  too little ink"); continue
    y0i, y1i = ys.min(), ys.max()
    mid = (y0i + y1i) / 2
    top, bot = ys <= mid, ys > mid
    print(f"  ink row span {176 + y0i/sc:.0f}..{176 + y1i/sc:.0f}; glyph-window shear (topX - botX, px):")
    W = int(12 * sc)
    for gx in range(0, int((372 - 138) * sc) - W, int(24 * sc)):
        tmask = top & (xs >= gx) & (xs < gx + W)
        bmask = bot & (xs >= gx) & (xs < gx + W)
        if tmask.sum() > 12 and bmask.sum() > 12:
            tx, bx = np.median(xs[tmask]), np.median(xs[bmask])
            print(f"    win x~{138 + gx/sc:5.1f}: top {tx/sc:6.1f}  bot {bx/sc:6.1f}  shear {(tx - bx)/sc:+5.2f}")

print()
print("=" * 76)
print("Q3: Outlier header panel fill (x68..116 y172..200) modal bg")
print("=" * 76)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND28", rend, S)):
    z = zone(a, 70, 174, 114, 198, sc)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    m = ink_mask(z)
    bg = ~m
    if bg.sum() > 30:
        modal = np.median(z[bg], axis=0)
        print(f"{tag}: bg modal rgb = {modal.round(1)}  (n={int(bg.sum())})")

print()
print("=" * 76)
print("Q4: y-row digit colors per test column (NO REG g1: y~272..286)")
print("=" * 76)
# NO REG test grid: gx0=206, v0=266, colW=38; y-row gy+69=274 (g1 gy=205)
# RIDGE3: gx0=466, v0=526, colW=38; RIDGE10: gx0=726, v0=786
COLS = [("NOREG", 266), ("RIDGE3", 526), ("RIDGE10", 786)]
GROUPY = [(274, 290), (379, 395), (489, 505)]  # y-row bands per group (gy+69..+85)
for gname, (gy0, gy1) in enumerate(GROUPY):
    print(f"--- group {gname + 1} y-row band y{gy0}..{gy1} ---")
    for cname, vx in COLS:
        for tag, a, sc in (("ORIG", orig, 1.0), ("REND28", rend, S)):
            z = zone(a, vx, gy0, vx + 114, gy1, sc)
            r, g, b = z[..., 0], z[..., 1], z[..., 2]
            m = z.sum(axis=2) < 500
            # exclude the yellow band bg; digit ink: green-ish or red-ish
            grn = m & (g - r > 30) & (g - b > 20)
            red = m & (r - g > 40) & (r - b > 40)
            blk = m & (abs(r - g) < 40) & (abs(g - b) < 40)
            tot = int(grn.sum() + red.sum() + blk.sum())
            if tot:
                print(f"  {cname:7s} {tag:7s}: green {int(grn.sum()):3d}  red {int(red.sum()):3d}  blackish {int(blk.sum()):3d}")

print()
print("=" * 76)
print("Q5: W paren ink bbox/weight (NO REG g1: W box x129..206, y200..297)")
print("=" * 76)
for tag, a, sc in (("ORIG", orig, 1.0), ("REND28", rend, S)):
    # left paren column ~x0+37..x0+45 => 161..170; right paren ~x0+67..x0+75 => 191..199
    for nm, x0, x1 in (("left paren", 158, 172), ("right paren", 188, 202)):
        z = zone(a, x0, 202, x1, 300, sc)
        m = z.sum(axis=2) < 420
        ys, xs = np.nonzero(m)
        if len(ys) < 10:
            print(f"{tag:7s} {nm}: no ink")
            continue
        # stroke weight: mean run length of horizontal ink runs
        runs = []
        for row in m:
            c = 0
            for v in row:
                if v:
                    c += 1
                elif c:
                    runs.append(c); c = 0
            if c:
                runs.append(c)
        w = np.mean(runs) if runs else 0
        print(f"{tag:7s} {nm}: ink {int(m.sum()):4d}  y {202 + ys.min()/sc:.0f}..{202 + ys.max()/sc:.0f}  "
              f"h={(ys.max()-ys.min()+1)/sc:.0f}  mean-hor-run {w/sc:.1f}px")
