#!/usr/bin/env python3
"""Whole-frame red clusters + left-middle box borders."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
X0, X1, Y0, Y1 = 62, 899, 46, 536

print("=== ALL red clusters inside panel ===")
sub = satred[Y0:Y1, X0:X1 + 1]
cc = sub.sum(axis=0)
xs = np.where(cc > 0)[0]
if len(xs):
    runs = []; s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 4:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        ys = np.where(sub[:, a:b + 1].any(axis=1))[0]
        px = np.where(sub[ys.min():ys.max() + 1, a:b + 1])
        rgb = IM[ys.min() + Y0 + px[0], a + X0 + px[1]]
        col = rgb.mean(axis=0).astype(int)
        print(f"  x{X0+a}..{X0+b} w{b-a+1} y{Y0+ys.min()}..{Y0+ys.max()} "
              f"px={int(sub[:, a:b+1].sum())} avg #{col[0]:02X}{col[1]:02X}{col[2]:02X}")

print("\n=== BLUE clusters inside panel ===")
sub = satblue[Y0:Y1, X0:X1 + 1]
cc = sub.sum(axis=0)
xs = np.where(cc > 0)[0]
if len(xs):
    runs = []; s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 4:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        ys = np.where(sub[:, a:b + 1].any(axis=1))[0]
        print(f"  x{X0+a}..{X0+b} w{b-a+1} y{Y0+ys.min()}..{Y0+ys.max()} px={int(sub[:, a:b+1].sum())}")

print("\n=== left-middle box borders (dark, y130..260, x60..250) ===")
sub = ((LUM < 200) & ~satred & ~satblue)[130:261, 60:251]
cc = sub.sum(axis=0)
xs = np.where(cc > 40)[0]
if len(xs):
    runs = []; s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 3:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        ys = np.where(sub[:, a:b + 1].any(axis=1))[0]
        print(f"  vertical x{60+a}..{60+b} (w{b-a+1}) y{130+ys.min()}..{130+ys.max()}")
rows = np.where(sub.sum(axis=1) > 40)[0]
if len(rows):
    out = []; s = rows[0]
    for i in range(1, len(rows)):
        if rows[i] - rows[i - 1] > 3:
            out.append((s, rows[i - 1])); s = rows[i]
    out.append((s, rows[-1]))
    for a, b in out:
        xs2 = np.where(sub[a:b + 1].any(axis=0))[0]
        print(f"  horizontal y{130+a}..{130+b} (h{b-a+1}) x{60+xs2.min()}..{60+xs2.max()}")
