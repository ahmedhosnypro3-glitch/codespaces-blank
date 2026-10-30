#!/usr/bin/env python3
r"""Frame-containment check for slide 015.

Every content element must sit fully INSIDE its enclosing element.  Compares
the render's ink bbox against the frame-px box that encloses it, in both the
original and the render, so an element that spills in the original is not
counted as a defect in the render.

The ink windows sit strictly INSIDE each element's border so the element's own
stroke is never measured as content ink (that is what produced a phantom 1px
"spill" on the solution box: its right border is drawn at x886 and the window
reached x890).

Elements (measured from unique_slides/slide_015.jpg):
  cream rect A   x72..892  y104..266   (eq1 l1..l3)
  pink box       x73..709  y275..334   (redbox_eq + sentence)
  peach box      x786..895 y275..332   (Remember + peach_eq)
  cream rect B   x72..892  y344..521   (deriv l1..l2 + normal)
  green box      x547..885 y472..516   (solution)

Usage: containment_015.py [render_path]
"""
import sys

import numpy as np
from PIL import Image

D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

# (label, box x0,x1,y0,y1, ink window x0,x1,y0,y1) - windows exclude borders
CHECKS = [
    ("eq1_l1",     72, 892, 104, 266,   97, 796, 106, 158),
    ("eq1_l2",     72, 892, 104, 266,   97, 766, 163, 214),
    ("eq1_l3",     72, 892, 104, 266,   97, 657, 216, 264),
    ("redbox_eq",  73, 709, 275, 334,   80, 207, 279, 302),
    ("redbox_sent", 73, 709, 275, 334, 208, 706, 294, 317),
    ("peach_eq",  786, 895, 275, 332,  790, 893, 298, 330),
    ("deriv_l1",   72, 892, 344, 521,   76, 660, 349, 405),
    ("deriv_l2",   72, 892, 344, 521,   76, 520, 414, 468),
    ("normal",     72, 892, 344, 521,  225, 545, 468, 519),
    ("solution",  547, 885, 472, 516,  552, 883, 474, 514),
]


def ink_bbox(L, F, y0, y1, x0, x1, thr=200):
    sub = L[int(y0 * F):int(y1 * F) + 1, int(x0 * F):int(x1 * F) + 1] < thr
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (round(x0 + xs.min() / F), round(x0 + xs.max() / F),
            round(y0 + ys.min() / F), round(y0 + ys.max() / F))


def main():
    rend = (sys.argv[1] if len(sys.argv) > 1
            else f"{D}/recreated_pptx/qa/slide_015/render_4.png")
    o = np.asarray(Image.open(f"{D}/unique_slides/slide_015.jpg").convert("L")).astype(int)
    r = np.asarray(Image.open(rend).convert("L")).astype(int)
    F = r.shape[1] / 960.0
    spills = 0
    for label, bx0, bx1, by0, by1, ix0, ix1, iy0, iy1 in CHECKS:
        print(f"{label:12s} box x{bx0}..{bx1} y{by0}..{by1}")
        for name, L_, F_ in (("orig", o, 1.0), ("rend", r, F)):
            b = ink_bbox(L_, F_, iy0, iy1, ix0, ix1)
            if b is None:
                print(f"{'':12s}   {name}: NO INK in window")
                continue
            ox0, ox1, oy0, oy1 = b
            dl, dr, dt, db = bx0 - ox0, ox1 - bx1, by0 - oy0, oy1 - by1
            worst = max(dl, dr, dt, db)
            tag = "  <-- SPILL" if worst > 0 else ""
            if name == "rend" and worst > 0:
                spills += 1
            print(f"{'':12s}   {name}: x{ox0}..{ox1} y{oy0}..{oy1}"
                  f" out L{dl:+d} R{dr:+d} T{dt:+d} B{db:+d}{tag}")
    print(f"\nrender spills: {spills}")


if __name__ == "__main__":
    main()
