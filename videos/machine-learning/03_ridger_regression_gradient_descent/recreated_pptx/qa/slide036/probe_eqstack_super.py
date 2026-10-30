#!/usr/bin/env python3
"""Decisive eq-stack readjudication on the CURRENT render (render_5).

Tests the eq_stack FAIL's decisive claims against both images:
  (a) second W lost its ^T  -> count raised-T ink clusters in the superscript band
  (b) arrow moved inside parens / term reordering -> compare main-row run structure
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_036.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide036/render_5.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
s = r.shape[0] / 540.0

def runs(img, x0, x1, y0, y1, thr=175, sc=1.0, minw=1.0):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2)
    m = (lum < thr).any(axis=0)
    out, st = [], None
    for i, v in enumerate(m):
        if v and st is None: st = i
        elif not v and st is not None:
            out.append((round(x0+st/sc,1), round(x0+(i-1)/sc,1))); st=None
    if st is not None: out.append((round(x0+st/sc,1), round(x0+(len(m)-1)/sc,1)))
    return [t for t in out if t[1]-t[0] >= minw]

def yext(img, x0, x1, y0, y1, thr=175, sc=1.0):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2)
    rows = np.where((lum < thr).any(axis=1))[0]
    return (round(y0+rows.min()/sc,1), round(y0+rows.max()/sc,1)) if len(rows) else None

print("=" * 76)
print("SUPERSCRIPT BAND (y360..375) — where the raised T's live")
print("=" * 76)
for tag, img, sc in (("ORIG", o, 1.0), ("REND", r, s)):
    rr = runs(img, 250, 540, 360, 375, sc=sc, minw=1.0)
    print(f"{tag}: {len(rr)} run(s): {rr}")

print()
print("=" * 76)
print("MAIN ROW (y376..397) — term structure")
print("=" * 76)
for tag, img, sc in (("ORIG", o, 1.0), ("REND", r, s)):
    rr = runs(img, 250, 540, 376, 397, sc=sc, minw=1.0)
    print(f"{tag}: {len(rr)} run(s): {rr}")

print()
print("=" * 76)
print("PER-GROUP vertical extents (a raised T shows ink ABOVE the main row)")
print("=" * 76)
# group1 paren/W region and group2 paren/W region, generous windows
for nm, (x0, x1) in (("group1 term", (300, 375)), ("group2 term", (440, 515))):
    for tag, img, sc in (("ORIG", o, 1.0), ("REND", r, s)):
        e = yext(img, x0, x1, 355, 400, sc=sc)
        print(f"  {nm:12s} {tag}: ink y-extent {e}")

print()
print("ARROW CONNECTOR between the groups (x375..420)")
for tag, img, sc in (("ORIG", o, 1.0), ("REND", r, s)):
    rr = runs(img, 375, 420, 376, 397, sc=sc, minw=2.0)
    e = yext(img, 375, 420, 372, 400, sc=sc)
    print(f"  {tag}: runs {rr}  y-extent {e}")
