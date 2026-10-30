#!/usr/bin/env python3
"""STEP 2 readjudication: eq_stack FAIL's decisive claim, measured on the CURRENT
render (render_5) against the original frame.

Claim under test (crop_2_eq_stack_judge BLOCKER #1 + MAJOR #2/#3):
  "recreation does not preserve term order: W^T X_i => (W^T X_i) became
   (W^T X_i)(W=> X_i)"  i.e. missing second ^T / parens misplaced / reordered.
Method: ink-run census of the equation row in both images (frame space, thr<170),
plus a glyph-level read of the region between the two parens.
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_036.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide036/render_5.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
s = r.shape[0] / 540.0
print(f"scale s={s:.4f}")

def runs(img, x0, x1, y0, y1, thr=170, sc=1.0):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2)
    m = (lum < thr).any(axis=0)
    out, st = [], None
    for i, v in enumerate(m):
        if v and st is None: st = i
        elif not v and st is not None:
            out.append((round(x0 + st/sc, 1), round(x0 + (i-1)/sc, 1))); st = None
    if st is not None: out.append((round(x0 + st/sc, 1), round(x0 + (len(m)-1)/sc, 1)))
    return [t for t in out if t[1]-t[0] >= 1.5]

print("\n--- equation row, y372..397 (x250..530) ---")
print("ORIG :", runs(o, 250, 530, 372, 397))
print("REND :", runs(r, 250, 530, 372, 397, sc=s))

# superscript T presence: an ink run that sits ABOVE the main row for each W group
print("\n--- raised-T detection (ink in the band ABOVE the main row) ---")
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    for nm, (x0, x1) in (("group1", (328, 340)), ("group2", (478, 492))):
        a = img[int(366*sc):int(374*sc), int(x0*sc):int(x1*sc)]
        lum = a.mean(axis=2)
        n = int((lum < 190).sum())
        print(f"  {tag} {nm} superscript-band ink px: {n}")

# vertical extent of the arrow connector between the groups
print("\n--- connector (arrow) vertical extent, orig vs rend ---")
for tag, img, sc in (("orig", o, 1.0), ("rend", r, s)):
    a = img[int(376*sc):int(392*sc), int(390*sc):int(412*sc)]
    lum = a.mean(axis=2)
    rows = np.where((lum < 190).any(axis=1))[0]
    if len(rows):
        print(f"  {tag} arrow ink y {376+rows.min()/sc:.1f}..{376+rows.max()/sc:.1f}")
