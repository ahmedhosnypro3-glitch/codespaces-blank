#!/usr/bin/env python3
"""Adjudicate_9g — hue-coded map of the RIGHT point label in the ORIGINAL.

Graph analysis record: red dot at (2,10) labelled in red, green dot at (5,1)
labelled in green. If the right label is also coloured, a gray-band test splits it
wrongly. This prints a hue-classified map so colour AND glyph shape are visible at
once, plus a census of which colour family each ink pixel belongs to.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

im = Image.open(V + "/unique_slides/slide_032.jpg").convert("RGB")
a = np.asarray(im).astype(int)
X0, Y0, X1, Y1 = 626, 138, 764, 158


def cls(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    sat = mx - mn
    if mx > 235 and sat < 25:
        return " "
    if sat < 22:
        return "." if mx < 200 else (" " if mx > 225 else ",")
    if r > g + 40 and r > b + 40:
        return "R"
    if g > r + 25 and g > b + 25:
        return "G"
    if r > 120 and b > 120 and g < r - 30:
        return "M"
    return "o"


sub = a[Y0:Y1, X0:X1]
print(f"hue-coded map, frame x{X0}..{X1} y{Y0}..{Y1}")
print("   R=red G=green M=magenta o=other-chromatic .=light-gray ,=mid-gray #=dark")
for ry in range(sub.shape[0]):
    row = "".join(cls(sub[ry, cx]) for cx in range(sub.shape[1]))
    print(f"  {Y0 + ry:>3} {row}")

print("\ncolour census over the LEFT label '(2, 10)' region (x620..660, y144..162):")
sub2 = a[144:162, 620:660]
from collections import Counter
c = Counter(cls(sub2[ry, cx]) for ry in range(sub2.shape[0]) for cx in range(sub2.shape[1]))
print("  ", dict(c))
print("colour census over the VERTEX label '(5, 1)' region (x686..726, y239..258):")
sub3 = a[239:258, 686:726]
c = Counter(cls(sub3[ry, cx]) for ry in range(sub3.shape[0]) for cx in range(sub3.shape[1]))
print("  ", dict(c))
print("colour census over the RIGHT label region (x730..758, y140..154):")
sub4 = a[140:154, 730:758]
c = Counter(cls(sub4[ry, cx]) for ry in range(sub4.shape[0]) for cx in range(sub4.shape[1]))
print("  ", dict(c))
print("colour census over the chord+dot (x716..730, y140..156):")
sub5 = a[140:156, 716:730]
c = Counter(cls(sub5[ry, cx]) for ry in range(sub5.shape[0]) for cx in range(sub5.shape[1]))
print("  ", dict(c))

print("\nrepresentative RGB samples in the right-label region:")
for (x, y) in [(733, 145), (735, 146), (737, 147), (744, 145), (746, 147), (748, 149),
               (730, 143), (732, 144), (734, 148), (740, 148), (745, 150)]:
    print(f"   ({x},{y}) -> {a[y, x].tolist()}")
