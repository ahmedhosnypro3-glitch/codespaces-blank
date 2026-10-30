#!/usr/bin/env python3
r"""Verified colours + element geometry for slide 015 (deck 03, 2026-10-24).

MEASURED from unique_slides/slide_015.jpg (960x540, 1px=1pt):
  element        fill      border (core px)
  cream rect A   FBFDE5    C6CBC7  (x72/267/892, 1px line, lum 200)
  cream rect B   FBFDE5    C6CBC7  (x72/521, same)
  pink box       F7D0D3    B55964  (measured 142,61,84 @x73 - the C00000 family,
                                    JPEG-darkened; the deck's chrome red)
  peach box      F7DCBE    C29A8E  (measured 194,154,142)
  green box      CFFFE3    499243  (measured 73,146,67)
  title red      C00000    (measured 106,2,27)
  title blue     00008B    (measured 2,0,110)
  lambda green   1E7B1E    (census 1153/589/607 px)
  body ink       000000
Note: the analysis JSON's "white" for the red box fill and "green box border
439742" are corrected here - the frame's pink fill is #F7D0D3 and its border is
the C00000 family.
"""
import numpy as np
from PIL import Image

IMG = ("videos/machine-learning/03_ridger_regression_gradient_descent"
       "/unique_slides/slide_015.jpg")

# (label, fill_hex, border_hex, sample points)
ELEMENTS = [
    ("creamA", "FBFDE5", "C6CBC7", [(240, 72), (200, 267), (240, 892)]),
    ("creamB", "FBFDE5", "C6CBC7", [(430, 72), (200, 521), (510, 72)]),
    ("pink",   "F7D0D3", "B55964", [(300, 73), (300, 708), (276, 300)]),
    ("peach",  "F7DCBE", "C29A8E", [(300, 786), (300, 893), (278, 830)]),
    ("green",  "CFFFE3", "499243", [(494, 548), (494, 882), (474, 700)]),
]


def main():
    a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
    print(f"image {a.shape}")
    for label, fill, border, pts in ELEMENTS:
        print(f"{label:7s} fill #{fill} border #{border}")
        for y, x in pts:
            r, g, b = a[y, x]
            print(f"    ({x},{y}) -> #{r:02X}{g:02X}{b:02X}  "
                  f"hex-to-int err: {abs(int(fill[0:2],16)-r)+abs(int(fill[2:4],16)-g)+abs(int(fill[4:6],16)-b)}")
    # ink colours
    for label, pts in [("title_red", [(76, 300), (76, 700)]),
                       ("title_blue", [(76, 600), (76, 640)])]:
        for y, x in pts:
            r, g, b = a[y, x]
            print(f"{label:10s} ({x},{y}) -> #{r:02X}{g:02X}{b:02X}")


if __name__ == "__main__":
    main()
