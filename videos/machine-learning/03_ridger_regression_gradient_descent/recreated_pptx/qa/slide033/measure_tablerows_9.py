#!/usr/bin/env python3
"""Table-row ink-run comparison for slide 033, render_9 vs unique_slides/slide_033.jpg.

Adjudication kit for a judge finding about the table's right-hand columns /
missing rows. Per row band, extracts dark-ink column runs in BOTH images and
reports any run present in the original with no overlapping render run
(potential MISSING ink) and vice versa (potential EXTRA ink).

Phantom trap law: runs narrower than 3 px are dropped.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide033/render_9.png").convert("RGB")).astype(int)
SR = ren.shape[0] / 540.0

ROW_BANDS = [(336, 349), (353, 366), (378, 391), (396, 409),
             (422, 435), (440, 453), (464, 477), (488, 501)]


def runs(img, scale, y0, y1, thr=150, minw=3):
    r0, r1 = int(round(y0 * scale)), int(round(y1 * scale))
    sub = img[r0:r1]
    dark = (sub.max(axis=2) < thr)
    n = dark.shape[0]
    col = dark.sum(axis=0)
    runs_, open_ = [], False
    for j in range(len(col)):
        fc = int(j / scale)
        if col[j] >= n * 0.9:                     # full-height column: gridline/edge
            if open_:
                runs_.append([st, prev]); open_ = False
            continue
        if col[j] > 0:
            if not open_:
                st, prev, open_ = fc, fc, True
            else:
                prev = fc
        elif open_:
            runs_.append([st, prev]); open_ = False
    if open_:
        runs_.append([st, prev])
    merged = []
    for a, b in runs_:
        if merged and a - merged[-1][1] <= 2:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [(a, b) for a, b in merged if b - a + 1 >= minw]


def overlap(a, b, lo, hi):
    return not (hi < a or lo > b)


for ri, (y0, y1) in enumerate(ROW_BANDS):
    o = runs(orig, 1.0, y0, y1)
    r = runs(ren, SR, y0, y1)
    miss = [(a, b) for a, b in o if not any(overlap(a, b, c, d) for c, d in r)]
    extra = [(a, b) for a, b in r if not any(overlap(a, b, c, d) for c, d in o)]
    print(f"row{ri} y{y0}-{y1}: ORIG {len(o)} runs / RENDER {len(r)} runs")
    if miss:
        print(f"   ORIG-only (MISSING-ink candidates): {miss}")
    if extra:
        print(f"   RENDER-only (EXTRA-ink candidates):  {extra}")
print()
print("Verdict key: ORIG-only runs at cell level = potential BLOCKER (ink the")
print("original has and the render lacks); RENDER-only runs = content the")
print("original does not show, which the judge may flag as wrong/stray data.")
