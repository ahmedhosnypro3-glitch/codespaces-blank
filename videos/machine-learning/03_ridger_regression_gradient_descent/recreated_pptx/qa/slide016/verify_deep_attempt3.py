#!/usr/bin/env python3
"""Deep-dive on the two residual verification questions (worker-016-fix-2):

Q1 DEFECT A follow-up: are the two blue key-term runs ("L2 regularization" on
   original b3b and "L1 regularization" on b4b) actually BLUE in the current
   render? My first pass used a strict blue test (b-r>40 & b<200) that thin
   18pt text fails after LANCZOS downscale with white. Re-measure both at
   native render resolution (2001x1125) and with a saturation-only test.

Q2 DEFECT B follow-up: the banked overrun in render_1 sat at y~505 (not in the
   y518-530 band I first scanned). Scan the full y495..531 band for ink beyond
   the inner box's right edge (x833) on ALL banked renders + the original.
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
RENDERS = [
    ("render_1", f"{QA}/render_1.png"),
    ("render_2", f"{QA}/render_2.png"),
    ("render_3", f"{QA}/render_3.png"),
]
o = Image.open(ORIG).convert("RGB")
oa = np.asarray(o).astype(int)

print("## Q1 — blue key-term runs (L2/L1 regularization)")
print("   Original's blue-run bboxes (frame px): b3b x254..390 y357..374;")
print("   b4b x254..390 y434..447 (from the banked line inventory).")
regions = [("b3b 'L2 regularization'", 254, 390, 357, 374),
           ("b4b 'L1 regularization'", 254, 390, 434, 447)]

for label, path in RENDERS:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    s = a.shape[0] / 540
    for name, x0, x1, y0, y1 in regions:
        reg = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
        r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
        sat = b - r
        m = (sat > 25)
        if m.any():
            ys, xs = np.where(m)
            cols = np.unique(xs)
            print(f"  {label:9s} {name:26s} blue px={int(m.sum()):6d} "
                  f"(of {m.size})  x={cols.min()+int(x0*s)}..{cols.max()+int(x0*s)} "
                  f"(frame px)  mean RGB of blue px="
                  f"({reg[...,0][m].mean():.0f},{reg[...,1][m].mean():.0f},{reg[...,2][m].mean():.0f})")
        else:
            print(f"  {label:9s} {name:26s} blue px=0")
for name, x0, x1, y0, y1 in regions:
    reg = oa[y0:y1, x0:x1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    m = (b - r) > 25
    print(f"  {'ORIGINAL':9s} {name:26s} blue px={int(m.sum()):6d} (of {m.size}) "
          f"x={np.where(m.any(axis=0))[0].min()+x0}..{np.where(m.any(axis=0))[0].max()+x0}")

print("\n## Q2 — ink beyond the inner box right edge x833, band y495..531")
print("   (render_1's banked overrun: black underline x675..877 at y~505 crossing x830)")
for label, path in RENDERS:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    s = a.shape[0] / 540
    reg = a[int(495 * s):int(531 * s), int(834 * s):int(899 * s)]
    m = a[int(495 * s):int(531 * s), int(834 * s):int(899 * s)].min(axis=2) < 160
    print(f"  {label:9s} ink px in x834..898, y495..530 = {int(m.sum())}")
    if m.any():
        rows = np.where(m.any(axis=1))[0]
        cols = np.where(m.any(axis=0))[0]
        print(f"            bbox y={rows.min()+495}..{rows.max()+495} "
              f"x={cols.min()+834}..{cols.max()+834} (frame px)")
oreg = oa[495:531, 834:899]
mreg = oreg.min(axis=2) < 160
print(f"  {'ORIGINAL':9s} ink px in x834..898, y495..530 = {int(mreg.sum())}")

print("\n   wide dark runs in the same band, full width (which element crosses x833?):")
for label, path in RENDERS:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    s = a.shape[0] / 540
    band = a[int(495 * s):int(531 * s)].min(axis=2) < 160
    cols = np.where(band.any(axis=0))[0]
    runs, start, prev = [], cols[0], cols[0]
    for c in cols[1:]:
        if c != prev + 1:
            if prev - start + 1 >= 40:
                runs.append((start / s, prev / s))
            start = c
        prev = c
    if prev - start + 1 >= 40:
        runs.append((start / s, prev / s))
    print(f"  {label:9s} " + ", ".join(f"x{a_:.0f}..{b_:.0f}" for a_, b_ in runs))
band = oa[495:531].min(axis=2) < 160
cols = np.where(band.any(axis=0))[0]
runs, start, prev = [], cols[0], cols[0]
for c in cols[1:]:
    if c != prev + 1:
        if prev - start + 1 >= 40:
            runs.append((start, prev))
        start = c
    prev = c
if prev - start + 1 >= 40:
    runs.append((start, prev))
print(f"  {'ORIGINAL':9s} " + ", ".join(f"x{a_:.0f}..{b_:.0f}" for a_, b_ in runs))
