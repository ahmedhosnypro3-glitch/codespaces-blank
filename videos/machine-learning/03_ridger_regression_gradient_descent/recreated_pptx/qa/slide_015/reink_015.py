#!/usr/bin/env python3
r"""Re-measure slide 015's equation ink bboxes from the original frame.

unique_slides/slide_015.jpg is 960x540 and 1px == 1pt == 1/72in.  Threshold is
luma<150 (ink).  Every equation is measured inside a window that EXCLUDES the
element borders (cream rects x74..890, pink box x73..709, peach x786..895,
green box x547..885) so the rect edge is not mistaken for glyph ink.

VERIFIED OUTPUT (banked 2026-10-24, used by build_eq_015.py MAX_EXTENT/BAND):
  tag        x0..x1   y0..y1   w    h
  eq1_l1     97..791  108..150 695  43
  eq1_l2     97..760  167..209 664  43
  eq1_l3     97..652  220..262 556  43
  deriv_l1   79..652  352..402 574  51
  deriv_l2   79..499  417..466 421  50
  normal     229..501 484..508 273  25
  solution   553..884 477..509 332  33
  redbox_eq  81..210  279..301 130  23
  redbox_sent 209..702 296..315 494 20
  peach_eq   791..890 295..329 100  35
  peach_remem 792..856 279..290 65  12
"""
import numpy as np
from PIL import Image

IMG = ("videos/machine-learning/03_ridger_regression_gradient_descent"
       "/unique_slides/slide_015.jpg")

# (label, y0, y1, x0, x1) -> tight ink bbox; windows exclude element borders
WINDOWS = [
    ("eq1_l1", 108, 151, 97, 795), ("eq1_l2", 167, 210, 97, 765),
    ("eq1_l3", 220, 263, 97, 656),
    ("redbox_eq", 279, 301, 78, 210), ("redbox_sent", 296, 315, 208, 706),
    ("peach_remem", 277, 292, 788, 900), ("peach_eq", 294, 332, 786, 900),
    ("deriv_l1", 351, 403, 76, 660), ("deriv_l2", 417, 467, 76, 520),
    ("normal", 483, 509, 225, 545), ("solution", 477, 509, 552, 890),
]


def main():
    a = np.asarray(Image.open(IMG).convert("L"))
    print(f"image {a.shape}")
    for label, y0, y1, x0, x1 in WINDOWS:
        m = a[y0:y1 + 1, x0:x1 + 1] < 150
        ys, xs = np.where(m)
        if not len(ys):
            print(f"{label:12s} NO INK in window")
            continue
        ax0, ax1 = x0 + int(xs.min()), x0 + int(xs.max())
        ay0, ay1 = y0 + int(ys.min()), y0 + int(ys.max())
        print(f"{label:12s} x{ax0}..{ax1} y{ay0}..{ay1} "
              f"w={ax1 - ax0 + 1} h={ay1 - ay0 + 1} density={m.mean():.3f}")


if __name__ == "__main__":
    main()
