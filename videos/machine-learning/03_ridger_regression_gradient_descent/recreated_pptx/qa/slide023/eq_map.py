#!/usr/bin/env python3
"""eq_map.py — 1px/char class map of the slide_023 equation band so the original's
glyph structure (W, =, parens, superscript, colors) is read exactly rather than
guessed. Class: R=red-strong, r=red-loose, G=green, D=dark, .=fill. 960x540, 1px=1pt.
Author: worker w8-s023-20261020T2330 (resumption; banked from the prior bank's zoom dumps).
"""
import numpy as np
from PIL import Image

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

Y0, Y1, X0, X1 = 144, 194, 100, 440
red_s = (R > 120) & (R - G > 80) & (R - B > 80)
red_l = (R > 120) & (R - G > 45) & (R - B > 45)
green = (G > R + 40) & (G > B + 40) & (G > 90) & (G < 200)
dark = (R < 120) & (G < 120) & (B < 120)


def ch(y, x):
    if red_s[y, x]:
        return 'R'
    if green[y, x]:
        return 'G'
    if dark[y, x]:
        return 'D'
    if red_l[y, x]:
        return 'r'
    return '.'


print("== EQUATION BAND y%d..%d x%d..%d (1px/char) ==" % (Y0, Y1, X0, X1))
for cs in range(X0, X1, 65):
    ce = min(cs + 65, X1)
    print("--- x%d..%d ---" % (cs, ce - 1))
    print("      " + "".join(str((x // 10) % 10) for x in range(cs, ce)))
    print("      " + "".join(str(x % 10) for x in range(cs, ce)))
    for y in range(Y0, Y1 + 1):
        row = "".join(ch(y, x) for x in range(cs, ce))
        if row.strip('.'):
            print("y%4d %s" % (y, row))
        else:
            print("y%4d |%s|" % (y, "." * len(row)))

print()
print("== COLUMN GROUPS (gap>2, any ink) ==")
ink = red_s | red_l | green | dark
for label, xs0, xs1 in [("WHOLE", X0, X1)]:
    sub = ink[Y0:Y1 + 1, xs0:xs1 + 1]
    col = sub.any(axis=0)
    xs = np.where(col)[0]
    if not len(xs):
        continue
    groups = []
    g0 = p = xs[0]
    for x in xs[1:]:
        if x - p > 2:
            groups.append((int(g0), int(p))); g0 = x
        p = x
    groups.append((int(g0), int(p)))
    for (g0, g1) in groups:
        seg = ink[Y0:Y1 + 1, g0 + xs0:g1 + xs0 + 1]
        ys = np.where(seg.any(axis=1))[0]
        sr = red_s[Y0:Y1 + 1, g0 + xs0:g1 + xs0 + 1].sum()
        sg = green[Y0:Y1 + 1, g0 + xs0:g1 + xs0 + 1].sum()
        sd = dark[Y0:Y1 + 1, g0 + xs0:g1 + xs0 + 1].sum()
        slr = red_l[Y0:Y1 + 1, g0 + xs0:g1 + xs0 + 1].sum()
        print("  x%d..%d w=%d y%d..%d h=%d  D=%d G=%d R=%d r=%d"
              % (g0 + xs0, g1 + xs0, g1 - g0 + 1, ys[0] + Y0, ys[-1] + Y0,
                 ys[-1] - ys[0] + 1, sd, sg, sr, slr))

print()
print("== UNDERLINE scan (W underline) rows y176..190, x100..140 ==")
for y in range(176, 192):
    xs = np.where(ink[y, 100:150])[0]
    if len(xs):
        print("  y=%d x%d..%d n=%d" % (y, xs.min() + 100, xs.max() + 100, len(xs)))
