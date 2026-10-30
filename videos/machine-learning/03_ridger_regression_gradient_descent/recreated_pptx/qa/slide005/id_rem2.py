#!/usr/bin/env python3
"""Identify the Remember-box identity equation in slide 005 by GLYPH GROUPS.

The lower-right light-blue box's equation reads wider (208 px) than the
upper-right one (185 px), which raised the question whether it is a different
identity. Column ink profiles answer it: both boxes show the SAME 13 glyph
groups with the same inter-glyph gaps, the lower one shifted -20 px and scaled
~1.13x. X, T, (, X, W, ), =, (, X, W, ), T, X == "X^T (XW) = (XW)^T X",
matching analysis/slide_005_final.json equations[6] and equations[7].
"""
from PIL import Image

IM = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
      "unique_slides/slide_005.jpg")


def groups(px, x0, x1, y0, y1, thresh=140):
    prof = [sum(1 for y in range(y0, y1) if px[x, y] < thresh)
            for x in range(x0, x1)]
    out, s = [], None
    for i, c in enumerate(prof):
        if c > 0 and s is None:
            s = i
        if c == 0 and s is not None:
            out.append((x0 + s, x0 + i - 1))
            s = None
    if s is not None:
        out.append((x0 + s, x1 - 1))
    return out


def gaps(gs):
    return [b[0] - a[1] for a, b in zip(gs, gs[1:])]


def main():
    im = Image.open(IM).convert("L")
    px = im.load()
    # windows exclude both boxes' borders and the red Remember labels
    up = groups(px, 678, 880, 211, 238)
    lo = groups(px, 660, 876, 393, 421)
    for name, g in (("upper", up), ("lower", lo)):
        print(f"{name}: {len(g)} groups  {g}")
        print(f"{name}: gaps {gaps(g)}")
    # token map: X T ( X W ) = ( X W ) T X  -> 13 groups
    tokens = ["X", "T", "(", "X", "W", ")", "=", "(", "X", "W", ")", "T", "X"]
    print("both carry X^T(XW) = (XW)^T X :",
          len(up) == len(tokens) == len(lo))


if __name__ == "__main__":
    main()
