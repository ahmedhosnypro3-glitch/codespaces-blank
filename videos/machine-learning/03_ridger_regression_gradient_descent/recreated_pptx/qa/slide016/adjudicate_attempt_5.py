#!/usr/bin/env python3
"""PIL-first adjudication of judge_attempt_5's two MINOR findings (worker-016-finish).

F1: original h2 line — is "(model parameters)" blue, or only "Penalize large values of W"?
F2: bottom gap — last line band mid-y and box bottom border, render vs original.
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{QA}/render_5.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int)

def blue_mask(a):
    return (a[:, :, 2].astype(int) - a[:, :, 0].astype(int) > 60) & (a[:, :, 2] > 110)

print("=== F1: h2 band y128..148 — blue extent ===")
for tag, a in [("original", o), ("render_5", r)]:
    m = blue_mask(a)
    band = m[128:148, 100:540]
    cols = np.where(band.any(axis=0))[0] + 100
    if len(cols):
        print(f"  {tag}: blue x{cols.min()}..{cols.max()} (px {int(band.sum())})")
    else:
        print(f"  {tag}: no blue px")
    # what colors are "(model parameters)" (x355..515)?
    sub = a[128:148, 355:515]
    ink = sub.min(axis=2) < 160
    if ink.sum():
        px = sub[ink]
        print(f"    '(model parameters)' region: ink {int(ink.sum())} px, "
              f"mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}), "
              f"blue-ish px (b-r>60 & b>110): {int((blue_mask(sub)).sum())}")

print("\n=== F1b: h2 ink extent both ===")
for tag, a in [("original", o), ("render_5", r)]:
    m = (a.min(axis=2) < 160)
    band = m[128:148, 100:540]
    cols = np.where(band.any(axis=0))[0] + 100
    print(f"  {tag}: h2 ink x{cols.min()}..{cols.max()}")

print("\n=== F2: last line + box bottom ===")
for tag, a in [("original", o), ("render_5", r)]:
    m = (a.min(axis=2) < 160)
    # b5b band
    band = m[505:530, 95:400]
    rows = np.where(band.any(axis=1))[0] + 505
    cols = np.where(band.any(axis=0))[0] + 95
    print(f"  {tag}: b5b ink rows {rows.min()}..{rows.max()} cols {cols.min()}..{cols.max()} "
          f"mid-y {int((rows.min()+rows.max())/2)}")
    # box bottom border
    for y in range(528, 537):
        row = m[y, 100:825]
        if row.sum() > 600:
            print(f"  {tag}: box bottom border at y={y} (ink {int(row.sum())})")
            break
    # dark underline
    d = (a.min(axis=2) < 100)
    for y in range(510, 535):
        cs = d[y, 100:300]
        if cs.sum() > 30:
            print(f"  {tag}: dark underline y={y} (ink {int(cs.sum())})")
    # vertical gaps
    ink_rows = np.where(m[128:536, 100:820].any(axis=1))[0] + 128
    print(f"  {tag}: first content row {ink_rows.min()} last content row {ink_rows.max()}")
