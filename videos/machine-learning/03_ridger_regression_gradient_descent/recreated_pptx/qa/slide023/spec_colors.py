#!/usr/bin/env python3
"""Final geometry+color spec for slide_023 build. 960x540 frame, 1px=1pt.
Reports box bboxes, exact fill + border colors, and per-word bbox/color for
every text line (yellow solution box, blue box, example lines, dim note)."""
import numpy as np
from PIL import Image
from collections import Counter

a = np.array(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def hist(y0, y1, x0, x1, n=4, label=""):
    reg = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    c = Counter(map(tuple, reg.tolist())).most_common(n)
    tot = region_total = reg.shape[0]
    print(f" {label}: ", [(tuple(int(v) for v in k), v) for k, v in c], f" ({100*max(v for _, v in c)/max(tot,1):.0f}% top)")


print("=" * 74)
print("BOX FILLS (text-free strips)")
hist(128, 145, 600, 740, 3, "GREEN fill")
hist(235, 240, 500, 860, 3, "BLUE fill (top strip)")
hist(240, 250, 500, 620, 3, "BLUE fill (right of L1)")
hist(345, 357, 700, 860, 3, "BLUE fill (below L3)")
hist(455, 462, 600, 860, 3, "SOL fill (top strip)")
hist(482, 492, 730, 860, 3, "SOL fill (right interior)")
hist(524, 528, 700, 860, 3, "SOL fill (bottom strip)")
hist(60, 68, 300, 500, 2, "gray panel above green box")
hist(424, 432, 300, 600, 2, "gray between blue box and example")
hist(392, 398, 300, 600, 2, "gray between example lines")
hist(432, 437, 300, 500, 3, "gap above solution box")

print("=" * 74)
print("BOX BORDERS")
print(" GREEN  top  y109-111 x300..600:", Counter(map(tuple, a[109:112, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" GREEN  bot  y218-219 x300..600:", Counter(map(tuple, a[218:220, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" GREEN  left x98-99  y160..190:", Counter(map(tuple, a[160:190, 98:100].reshape(-1, 3).tolist())).most_common(2))
print(" GREEN  right x753-755 y160..190:", Counter(map(tuple, a[160:190, 753:756].reshape(-1, 3).tolist())).most_common(2))
print(" BLUE   top  y228-229 x300..600:", Counter(map(tuple, a[228:230, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" BLUE   bot  y425-426 x300..600:", Counter(map(tuple, a[425:427, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" BLUE   left x88-89  y300..400:", Counter(map(tuple, a[300:400, 88:90].reshape(-1, 3).tolist())).most_common(2))
print(" BLUE   right x867-869 y300..400:", Counter(map(tuple, a[300:400, 867:870].reshape(-1, 3).tolist())).most_common(2))
print(" SOL    top  y435-436 x300..600:", Counter(map(tuple, a[435:437, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" SOL    bot  y529-531 x300..600:", Counter(map(tuple, a[529:532, 300:600].reshape(-1, 3).tolist())).most_common(2))
print(" SOL    left x86-87  y470..500:", Counter(map(tuple, a[470:500, 86:88].reshape(-1, 3).tolist())).most_common(2))
print(" SOL    right x873-875 y470..500:", Counter(map(tuple, a[470:500, 873:876].reshape(-1, 3).tolist())).most_common(2))

print("=" * 74)
print("BADGE")
hist(66, 70, 870, 884, 3, "badge fill")

print("=" * 74)
print("PER-WORD TEXT (words split on >=5px whitespace; dominant core color)")

red = (R > 120) & (R - G > 80) & (R - B > 80)
navy = (B > R + 40) & (B > 90) & (G < 120)
blk = (R < 110) & (G < 110) & (B < 110)
ALL = red | navy | blk


def clsc(px):
    r, g, b = px
    if r > 120 and r - g > 80 and r - b > 80:
        return "RED"
    if b > r + 40 and b > 90 and g < 120:
        return "NAVY"
    if r < 110 and g < 110 and b < 110:
        return "BLK"
    return "other"


def words(y0, y1, x0, x1, label):
    sub = ALL[y0:y1 + 1, x0:x1 + 1]
    col = sub.any(axis=0)
    xs = np.where(col)[0]
    if not len(xs):
        print(f" {label}: no ink")
        return
    grp = []
    g0 = p = xs[0]
    for x in xs[1:]:
        if x - p > 4:
            grp.append((int(g0), int(p)))
            g0 = x
        p = x
    grp.append((int(g0), int(p)))
    print(f" {label}:")
    for (s, e) in grp:
        seg = a[y0:y1 + 1, s + x0:e + x0 + 1]
        cls = Counter(clsc(p) for p in seg.reshape(-1, 3) if clsc(p) != "other")
        om = np.where(ALL[y0:y1 + 1, s + x0:e + x0 + 1])
        ys = om[0] if len(om) else [0]
        top = ys.min() + y0 if len(ys) else None
        bot = ys.max() + y0 if len(ys) else None
        best = cls.most_common(1)
        colname = best[0][0] if best else "?"
        print(f"   x{s+x0}..{e+x0} w={e-s+1} y{top}..{bot} -> {colname} ({best[0][1] if best else 0})")


# SOLUTION box: label + 2 centered lines
words(444, 470, 90, 880, "SOL label")
words(470, 502, 90, 880, "SOL L1")
words(500, 530, 90, 880, "SOL L2")
# BLUE box 3 lines
words(238, 268, 90, 870, "BLUE L1")
words(270, 300, 90, 870, "BLUE L2")
words(302, 336, 90, 870, "BLUE L3")
# EXAMPLE 2 lines
words(356, 390, 90, 870, "EX L1")
words(394, 424, 90, 870, "EX L2")
# DIM NOTE line
words(191, 220, 95, 780, "DIM NOTE")
# EQUATION (nonfill ink)
print(" EQUATION: ink x104..429 y151..186, underline y180-181 x104..129")
print("   lambda+1 are GREEN; superscript (-1) is RED")
