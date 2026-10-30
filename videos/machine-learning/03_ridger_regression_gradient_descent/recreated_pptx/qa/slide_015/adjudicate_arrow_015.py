#!/usr/bin/env python3
r"""Decide whether slide 015 has a right-pointing ARROW between the normal
equation and the green box, or whether the ink there is part of the equation.

Adjudication is pixel-first: the original's ink in the gap window is compared
against the render's ink in the SAME frame-px window, and the original's ink is
also compared against the normal equation's own rendered ink (so that equation
glyphs are not miscounted as a separate arrow).

No file is written.
"""
import numpy as np
from PIL import Image

D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

ORIG = f"{D}/unique_slides/slide_015.jpg"
REND = f"{D}/recreated_pptx/qa/slide_015/render_3.png"


def masks(img, F, y0, y1, x0, x1, thr):
    L = np.asarray(Image.open(img).convert("L")).astype(int)
    sub = L[int(y0 * F):int(y1 * F) + 1, int(x0 * F):int(x1 * F) + 1] < thr
    return sub, F


def bbox(sub, x0, y0, F):
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (round(x0 + xs.min() / F), round(x0 + xs.max() / F),
            round(y0 + ys.min() / F), round(y0 + ys.max() / F), int(sub.sum()))


def main():
    o = np.asarray(Image.open(ORIG).convert("L")).astype(int)
    r = np.asarray(Image.open(REND).convert("L")).astype(int)
    F = r.shape[1] / 960.0

    # full normal-equation band as the build intends it (image x229..229+266)
    print("=== normal equation band (frame x225..545, y466..520) ===")
    om = o[466:521, 225:546] < 200
    rm = r[int(466 * F):int(520 * F) + 1, int(225 * F):int(545 * F) + 1] < 200
    print("orig ink px", int(om.sum()), "bbox", bbox(om, 225, 466, 1.0))
    print("rend ink px", int(rm.sum()), "bbox(frame px)",
          bbox(rm, 225, 466, F))

    # the gap strictly BETWEEN the render's equation end and the green box
    print("\n=== gap: x489..546 (right of the render's eq ink, left of green box) ===")
    om = o[466:521, 489:547] < 200
    rm = r[int(466 * F):int(521 * F), int(489 * F):int(546 * F)] < 200
    print("orig ink px", int(om.sum()), "bbox", bbox(om, 489, 466, 1.0))
    print("rend ink px", int(rm.sum()), "bbox", bbox(rm, 489, 466, F))

    # the ORIGINAL's own gap measured from ITS equation's right edge (x510)
    print("\n=== original gap: x511..546 ===")
    om = o[466:521, 511:547] < 200
    print("orig ink px", int(om.sum()), "bbox", bbox(om, 511, 466, 1.0))

    # narrow the original's tail glyph: is there a TALL thin stroke (a paren) or
    # a broad blob (an arrowhead)?
    print("\n=== original tail glyph, per-column ink (x496..515, y480..512, thr 205) ===")
    om = o[480:513, 496:516] < 205
    for cx in range(496, 516):
        ys = np.where(om[:, cx - 496])[0]
        print(f"  x={cx}: n={len(ys)}"
              + (f" y{480 + ys.min()}..{480 + ys.max()}" if len(ys) else ""))


if __name__ == "__main__":
    main()
