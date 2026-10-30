#!/usr/bin/env python3
"""Adjudicate crop_12_tl MAJORs against render_14 (TL x85..265 y115..288).
Correct per-image scales: orig 1.0x, render 2001/960.
Q1 contour rings on floor: cyan + green/yellow ring ink census.
Q2 left-edge third tick label: '2' vs '-2' (glyph run width).
Q3 bottom/front tick labels: ink column clusters."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{V}/recreated_pptx/qa/slide_025"
imgs = {
    "ORIG": (np.asarray(Image.open(f"{V}/unique_slides/slide_025.jpg").convert("RGB")).astype(int), 1.0),
    "REND14": (np.asarray(Image.open(f"{QA}/render_14.png").convert("RGB")).astype(int), 2001 / 960.0),
}


def zone(a, sc, x0, y0, x1, y1):
    return a[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]


TX0, TY0, TX1, TY1 = 85, 115, 265, 288

for tag, (a, sc) in imgs.items():
    print(f"=== {tag} TL x{TX0}..{TX1} y{TY0}..{TY1} (scale {sc:.5f}) ===")
    z = zone(a, sc, TX0, TY0, TX1, TY1)
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    # cyan ring ink: blue+green high, red low
    cyan = (b > 110) & (g > 100) & (b - r > 40) & (g - r > 25)
    # yellow ring ink
    yel = (r > 150) & (g > 120) & (b < 120) & (r - b > 60)
    # green ring ink
    grn = (g > 110) & (g - r > 35) & (g - b > 35)
    print(f"  floor-zone rings: cyan {int(cyan.sum())}  yellow {int(yel.sum())}  green {int(grn.sum())}")
    # Q2: left-edge tick labels (x band TX0..TX0+18), row clusters of dark ink
    lb = zone(a, sc, TX0 - 2, TY0, TX0 + 16, TY1)
    dl = (lb.sum(axis=2) < 420)
    rows = np.nonzero(dl.sum(axis=1) > 1)[0]
    if len(rows):
        runs, st = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] > rows[i - 1] + 3 * sc:
                runs.append((st, rows[i - 1])); st = rows[i]
        runs.append((st, rows[-1]))
        for a_, b_ in runs:
            sub = dl[a_:b_ + 1]
            cols = np.nonzero(sub.any(axis=0))[0]
            wid = (cols.max() - cols.min() + 1) / sc if len(cols) else 0
            print(f"  left-edge label y~{TY0 + (a_ + b_) / 2 / sc:.0f} h={(b_ - a_) / sc:.1f} w={wid:.1f}px")
    else:
        print("  left-edge labels: none")
    # Q3: bottom band labels (y TY1-20..TY1+8)
    bb = zone(a, sc, TX0 - 10, TY1 - 18, TX1 + 10, TY1 + 10)
    db = (bb.sum(axis=2) < 420)
    cols = np.nonzero(db.sum(axis=0) > 1)[0]
    if len(cols):
        runs, st = [], cols[0]
        for i in range(1, len(cols)):
            if cols[i] > cols[i - 1] + 4 * sc:
                runs.append((st, cols[i - 1])); st = cols[i]
        runs.append((st, cols[-1]))
        print("  bottom labels x-clusters: " + ", ".join(
            f"{TX0 - 10 + a_ / sc:.0f}..{TX0 - 10 + b_ / sc:.0f}(w{(b_ - a_) / sc:.0f})" for a_, b_ in runs))
    else:
        print("  bottom labels: none")
