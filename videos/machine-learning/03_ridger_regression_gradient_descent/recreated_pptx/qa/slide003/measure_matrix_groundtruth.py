#!/usr/bin/env python3
"""PIL ground-truth measurement: bottom-left design matrix + weight vector.

Adjudicate judge_attempt_16 finding #1 (middle white row ellipsis count) and
finding #2 (weight-vector case/ellipsis) against the ORIGINAL frame, and compare
against render_17 (the current build). Frame px, 1px=1pt; render downscaled 72/150.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"

orig = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
ren = Image.open(QA + "/render_17.png").convert("RGB").resize((960, 540), Image.LANCZOS)
a = np.asarray(orig).astype(int)
r = np.asarray(ren).astype(int)


def ink_mask(im):
    s = im.sum(axis=2)
    return s < 300  # very dark (text/lines/dots).


def detect_row_bands(im, x_probe=385):
    """Row bands by fill color down a text-free vertical of the matrix."""
    fills = {"yellow": (255, 255, 153), "cyan": (204, 255, 255),
             "white": (255, 255, 255), "pink": (255, 192, 203)}
    col = im[:, x_probe, :]
    out, cur, start = [], None, None
    for y in range(350, 500):
        pxv = col[y]
        lab = None
        for name, ref in fills.items():
            if all(abs(pxv[i] - ref[i]) < 26 for i in range(3)):
                lab = name
                break
        if lab != cur:
            if cur is not None and start is not None and y - start >= 6:
                out.append((cur, start, y - 1))
            cur, start = lab, y
    if cur is not None and 499 - start >= 6:
        out.append((cur, start, 499))
    return out


def ink_runs(im, y0, y1, x0, x1, gap=9):
    """Connected dark-ink x-runs within a y-band -> glyph groups (cells)."""
    m = ink_mask(im)[y0:y1, x0:x1]
    if m.sum() == 0:
        return []
    colsum = m.sum(axis=0)
    present = colsum > 0
    runs, s = [], None
    for i, p in enumerate(present):
        if p and s is None:
            s = i
        elif not p and s is not None:
            runs.append((s + x0, i - 1 + x0))
            s = None
    if s is not None:
        runs.append((s + x0, len(present) - 1 + x0))
    merged = []
    for rn in runs:
        if merged and rn[0] - merged[-1][1] < gap:
            merged[-1] = (merged[-1][0], rn[1])
        else:
            merged.append((rn[0], rn[1]))
    return merged


print("=== ORIGINAL bottom-left matrix: row bands (fill) + ink glyph-runs per row ===")
bands_o = detect_row_bands(a)
for (name, y0, y1) in bands_o:
    runs = ink_runs(a, y0, y1, 150, 432, gap=11)
    print(f"  row {name:6s} y{y0}..{y1}  ({y1-y0+1}px)  glyph-run count={len(runs)}")
    for (rx0, rx1) in runs:
        print(f"      ink x {rx0}..{rx1}  (center {(rx0+rx1)//2}, w {rx1-rx0+1})")

print("\n=== render_17 bottom-left matrix: row bands (fill) + ink glyph-runs per row ===")
bands_r = detect_row_bands(r)
for (name, y0, y1) in bands_r:
    runs = ink_runs(r, y0, y1, 150, 432, gap=11)
    print(f"  row {name:6s} y{y0}..{y1}  ({y1-y0+1}px)  glyph-run count={len(runs)}")
    for (rx0, rx1) in runs:
        print(f"      ink x {rx0}..{rx1}  (center {(rx0+rx1)//2}, w {rx1-rx0+1})")

print("\n=== WEIGHT VECTOR (right of matrix, x452..530) per-row ink ===")


def wv_rows(im):
    col = im[:, 505, :]
    white = (col[:, 0] > 240) & (col[:, 1] > 240) & (col[:, 2] > 240)
    rows, s = [], None
    for y in range(325, 490):
        if white[y] and s is None:
            s = y
        elif not white[y] and s is not None:
            if y - s >= 8:
                rows.append((s, y - 1))
            s = None
    return rows


for tag, im in (("ORIG", a), ("REND", r)):
    print(f"  {tag}: w-vector entry rows:")
    for (ry0, ry1) in wv_rows(im):
        runs = ink_runs(im, ry0, ry1, 452, 526, gap=9)
        s = f"    y{ry0}..{ry1}: runs={len(runs)} "
        for (rx0, rx1) in runs:
            s += f"[x{rx0}..{rx1} w{rx1-rx0+1}] "
        print(s)
