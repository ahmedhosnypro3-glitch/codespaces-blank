#!/usr/bin/env python3
"""Slide 003 — precise regional analysis of the ORIGINAL frame.

For each content region: exact coloured-band extents (fill colour matched),
dark-ink extents, red/blue/gray-ink extents, and a compact row/col profile so the
render can be compared element by element.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
ORIG = B + "/unique_slides/slide_003.jpg"
a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
R, G, Bc = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def mask_colour(hexs, tol=26):
    c = np.array([int(hexs[i:i + 2], 16) for i in (0, 2, 4)])
    return ((abs(R - c[0]) < tol) & (abs(G - c[1]) < tol) &
            (abs(Bc - c[2]) < tol))


def bbox(m, win):
    x0, y0, x1, y1 = win
    b = m[y0:y1, x0:x1]
    if b.sum() == 0:
        return None
    ys, xs = np.where(b)
    return (int(xs.min() + x0), int(ys.min() + y0),
            int(xs.max() + x0), int(ys.max() + y0), int(b.sum()))


DARK = (a.sum(axis=2) < 430)
RED = (R > 150) & (G < 110) & (Bc < 110)
BLUE = (Bc > 150) & (R < 110) & (G < 130)
GRAY = (abs(R - G) < 22) & (abs(G - Bc) < 22) & (R > 90) & (R < 200)


def show(name, win):
    print(f"\n--- {name}  win={win}")
    for nm, m in (("dark", DARK), ("red", RED), ("blue", BLUE), ("gray", GRAY)):
        b = bbox(m, win)
        print(f"    {nm:5s} {b}")

    # row profile of dark+colour ink
    x0, y0, x1, y1 = win
    rows = []
    for y in range(y0, y1):
        n = DARK[y, x0:x1].sum() + RED[y, x0:x1].sum() + BLUE[y, x0:x1].sum()
        rows.append((y, int(n)))
    nz = [(y, n) for y, n in rows if n > 0]
    if nz:
        # group contiguous rows into bands
        bands, cur = [], [nz[0]]
        for y, n in nz[1:]:
            if y - cur[-1][0] <= 2:
                cur.append((y, n))
            else:
                bands.append(cur)
                cur = [(y, n)]
        bands.append(cur)
        for bnd in bands:
            print(f"    rows {bnd[0][0]}..{bnd[-1][0]}  max_ink={max(n for _, n in bnd)}")

    # column profile
    cols = []
    for x in range(x0, x1):
        n = DARK[y0:y1, x].sum() + RED[y0:y1, x].sum() + BLUE[y0:y1, x].sum()
        cols.append((x, int(n)))
    nzc = [(x, n) for x, n in cols if n > 0]
    if nzc:
        cb, cur = [], [nzc[0]]
        for x, n in nzc[1:]:
            if x - cur[-1][0] <= 3:
                cur.append((x, n))
            else:
                cb.append(cur)
                cur = [(x, n)]
        cb.append(cur)
        segs = [f"{b[0][0]}..{b[-1][0]}" for b in cb]
        print("    col groups: " + " ".join(segs[:14]))


show("TITLE", (70, 60, 845, 100))
show("N Training Samples", (70, 160, 290, 215))
show("TOP MATRIX BOX", (265, 100, 600, 310))
show("REMEMBER BOX", (640, 145, 885, 230))
show("IN GENERAL BOX", (650, 258, 860, 302))
show("BOTTOM-LEFT BOX", (72, 318, 545, 522))
show("BOTTOM-RIGHT BOX", (560, 318, 765, 522))
show("ARROW", (525, 375, 585, 410))
show("BADGE", (835, 48, 915, 98))
