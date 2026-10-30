#!/usr/bin/env python3
r"""Adjudicate slide 015 attempt 3's two census flags.

redbox_eq: render ink 548 vs original 323 (render 1.7x heavier) and 125pt wide
           vs the frame's 97pt.
solution : render ink 1028 vs original 1654 (render 0.62x as much ink).

Prints the original's ink column profile inside the pink box (so the equation
block can be separated from the sentence) and the green box, plus the render's
equivalent, so the exact block bboxes are known before any build change.
"""
import itertools

import numpy as np
from PIL import Image

D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"


def blocks(cols, xoff):
    """Blank-column runs -> content block boundaries."""
    blanks = [xoff + i for i, c in enumerate(cols) if c == 0]
    runs, out = [], []
    for k, g in itertools.groupby(enumerate(blanks), key=lambda t: t[1] - t[0]):
        gl = list(g)
        runs.append((gl[0][1], gl[-1][1]))
    prev = xoff
    for a, b in runs:
        if b - a >= 6:  # a real gutter
            out.append((prev, a))
            prev = b + 1
    out.append((prev, xoff + len(cols) - 1))
    return [t for t in out if t[1] >= t[0]]


def scan(name, img, L, F, y0, y1, x0, x1, thr=150):
    """Window is given in FRAME px.  For the original (F=1) the slice is direct;
    for the render (F=2.0844) the same frame-px window is scaled into render px
    and the measured bbox is mapped back to frame px."""
    if abs(F - 1.0) < 1e-9:
        sub = L[y0:y1 + 1, x0:x1 + 1] < thr
        rf = 1.0
    else:
        ry0, ry1 = int(y0 * F), int(y1 * F) + 1
        rx0, rx1 = int(x0 * F), int(x1 * F) + 1
        sub = L[ry0:ry1, rx0:rx1] < thr
        rf = F
    ys, xs = np.where(sub)
    if not len(ys):
        print(f"{name}: NO INK in window")
        return
    ix0, ix1 = int(x0 + xs.min() / rf), int(x0 + xs.max() / rf)
    iy0, iy1 = int(y0 + ys.min() / rf), int(y0 + ys.max() / rf)
    print(f"{name}: frame ink x{ix0}..{ix1} y{iy0}..{iy1} "
          f"w={ix1 - ix0 + 1} h={iy1 - iy0 + 1} px@frame = "
          f"{(ix1 - ix0 + 1)}x{(iy1 - iy0 + 1)}pt  density={sub.mean():.3f}")
    cols = sub.sum(axis=0)
    fr = blocks(cols, x0)
    print(f"{name}: content blocks (frame x0..x1): {fr}")
    for bx0, bx1 in fr:
        b = sub[:, max(0, bx0 - x0):bx1 - x0 + 1]
        bys, bxs = np.where(b)
        if len(bys):
            print(f"    block x{bx0}..{bx1} y{y0 + int(bys.min())}..{y0 + int(bys.max())} "
                  f"w={bx1 - bx0 + 1} inkpx={int(b.sum())}")


def main():
    o = np.asarray(Image.open(f"{D}/unique_slides/slide_015.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{D}/recreated_pptx/qa/slide_015/render_3.png").convert("RGB")).astype(int)
    oL, rL = o.mean(axis=2), r.mean(axis=2)
    F = r.shape[1] / 960.0

    print("=== PINK BOX interior (frame x72..711, y274..336) ===")
    print("--- ORIGINAL ---")
    scan("orig pink", o, oL, 1.0, 274, 336, 72, 711)
    print("--- RENDER (measured in FRAME px) ---")
    scan("rend pink", r, rL, F, 274, 336, 72, 711)

    print("\n=== GREEN BOX (frame x547..885, y472..516) ===")
    print("--- ORIGINAL ---")
    scan("orig green", o, oL, 1.0, 472, 516, 547, 885)
    print("--- RENDER ---")
    scan("rend green", r, rL, F, 472, 516, 547, 885)

    print("\n=== NORMAL (left of green, frame x225..545, y468..520) ===")
    print("--- ORIGINAL ---")
    scan("orig normal", o, oL, 1.0, 468, 520, 225, 545)
    print("--- RENDER ---")
    scan("rend normal", r, rL, F, 468, 520, 225, 545)


if __name__ == "__main__":
    main()
