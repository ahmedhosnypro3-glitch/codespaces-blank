#!/usr/bin/env python3
"""Color-categorized ASCII map of the original's table region + rule color sampling.

Category per block (dominant inked color class):
  '.' background panel   'B' blue   'R' red   'G' green   'K' black
  'g' bluish-gray rule   'y' yellow   '?' other
"""
import numpy as np
from PIL import Image

VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(f"{VID}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
H, W, _ = orig.shape

X0, X1, Y0, Y1 = 54, 903, 165, 530


def classify(px):
    r, g, b = px
    if abs(r - 233) < 24 and abs(g - 233) < 24 and abs(b - 227) < 24:
        return "."
    mx, mn = max(r, g, b), min(r, g, b)
    if r > 150 and g < 110 and b < 110:
        return "R"
    if b > 150 and r < 130 and g < 130:
        return "B"
    if g > 110 and r < 130 and b < 130:
        return "G"
    if mx < 90:
        return "K"
    if b > r + 8 and b > g + 8:
        return "g"   # bluish gray
    if r > 180 and g > 180 and b < 140:
        return "y"
    if mx - mn < 25:
        return "K" if mx < 150 else "."
    return "?"


# ── rule color sampling at detected stroke positions ───────────────────────────
print("=== ORIGINAL rule pixel colors (sampled at stroke positions, y 200..520) ===")
verts = [(57, 59), (64, 66), (116, 118), (123, 125), (129, 131), (205, 206), (236, 236),
         (269, 269), (303, 303), (336, 336), (369, 369), (377, 379), (383, 385), (390, 390),
         (465, 466), (496, 496), (529, 529), (562, 562), (595, 595), (629, 629),
         (637, 639), (642, 644), (648, 649), (724, 725), (754, 755), (787, 788), (821, 821),
         (854, 854), (887, 887), (893, 894), (900, 902)]
for xa, xb in verts:
    sub = orig[200:520, xa:xb + 1].reshape(-1, 3)
    inked = sub[(np.abs(sub.astype(int) - np.array([233, 233, 227])).sum(axis=1) > 60)]
    if len(inked) == 0:
        print(f"  x{xa}..{xb}: no ink"); continue
    q = (inked // 16) * 16
    keys, counts = np.unique(q, axis=0, return_counts=True)
    o = np.argsort(-counts)[:3]
    s = " ".join(f"{tuple(int(v) for v in keys[i])}:{counts[i]}" for i in o)
    print(f"  x{xa:3d}..{xb:3d}  n={len(inked):5d}  {s}")

horz = [(169, 171), (186, 193), (201, 201), (249, 249), (272, 272), (297, 297),
        (301, 302), (308, 309), (333, 333), (357, 357), (379, 379), (405, 405),
        (409, 409), (417, 417), (441, 441), (465, 465), (486, 486), (514, 515), (523, 525)]
print("=== ORIGINAL horizontal rule colors (x 60..900) ===")
for ya, yb in horz:
    sub = orig[ya:yb + 1, 60:900].reshape(-1, 3)
    inked = sub[(np.abs(sub.astype(int) - np.array([233, 233, 227])).sum(axis=1) > 60)]
    xs = np.where((np.abs(orig[ya:yb + 1, 60:900].astype(int) - np.array([233, 233, 227])).sum(axis=2) > 60).any(axis=0))[0]
    if len(inked) == 0:
        print(f"  y{ya}..{yb}: no ink"); continue
    q = (inked // 16) * 16
    keys, counts = np.unique(q, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    s = " ".join(f"{tuple(int(v) for v in keys[i])}:{counts[i]}" for i in o)
    print(f"  y{ya:4d}..{yb:4d}  n={len(inked):5d}  x{60+xs.min()}..{60+xs.max()}  {s}")

# ── ASCII map, 4px per char, plus a column ruler ───────────────────────────────
step = 4
print("\n=== ORIGINAL structure map (4px/char) x54..903 y165..530 ===")
hdr = "".join(str((X0 + i * step) // 100 % 10) if (X0 + i * step) % 20 < step else " "
              for i in range((X1 - X0) // step))
print("     " + hdr)
for yy in range(Y0, Y1, step):
    row = []
    for xx in range(X0, X1, step):
        blk = orig[yy:yy + step, xx:xx + step].reshape(-1, 3)
        cnt = {}
        for p in blk:
            c = classify(p)
            cnt[c] = cnt.get(c, 0) + 1
        if "." in cnt and cnt["."] >= 12:
            row.append(".")
        else:
            best = max((k for k in cnt if k != "."), key=lambda k: cnt[k], default=".")
            row.append(best if best != "." else ".")
    print(f"{yy:4d} " + "".join(row))
