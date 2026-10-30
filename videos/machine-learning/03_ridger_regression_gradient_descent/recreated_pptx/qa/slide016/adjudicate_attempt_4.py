#!/usr/bin/env python3
"""PIL-first adjudication of judge_attempt_4's single MAJOR finding.

The judge claims two wording deltas in bullet 2 of the ORIGINAL vs the render:
  (A) render has "model generalization" where the original has just "generalization"
  (B) render has "the regularization term" where the original has "the
      generalization term"

Fidelity law: the FRAME wins for recreation; the validated analysis JSON is the
corroborating record. This script measures the disputed zone in BOTH images at
1px=1pt and reconstructs the word geometry, so each claim can be settled from
pixels before any build change.
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")

o = Image.open(ORIG).convert("RGB")
oa = np.asarray(o).astype(int)
f = Image.open(f"{QA}/render_4.png").convert("RGB")
fa = np.asarray(f).astype(int)
S = fa.shape[0] / 540
# native-res render sliced into frame px for each band below


def frame_slice(arr, y0, y1, x0, x1):
    """Native-resolution slice mapped to frame bbox."""
    return arr[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)], S


def ink(a):
    return a.min(axis=2) < 160


def word_clusters(mask, ss):
    """Group ink columns into glyph clusters, then merge clusters separated by
    <2px into words. Returns (word_start, word_end) in frame px."""
    cols = np.where(mask.any(axis=0))[0]
    if not len(cols):
        return []
    glyphs = []
    start = prev = cols[0]
    for c in cols[1:]:
        if c != prev + 1:
            glyphs.append((start, prev))
            start = c
        prev = c
    glyphs.append((start, prev))
    words = [list(glyphs[0])]
    for g in glyphs[1:]:
        if g[0] - words[-1][1] - 1 <= 2:
            words[-1][1] = g[1]
        else:
            words.append([g[0], g[1]])
    return [((w[0] / ss), (w[1] / ss)) for w in words]


print("=" * 78)
print("Bullet-2 line geometry (frame px, 1px=1pt)")
print("Original b2a: y230..248   b2b: y256..273")
print("Render b2a:   y~231..249  b2b: y~257..275 (from the line table)")
print()
for tag, (y0, y1) in [("b2a", (228, 250)), ("b2b", (254, 276))]:
    om = ink(oa[y0:y1, 82:840])
    rm, _ = frame_slice(fa, y0, y1, 82, 840)
    rm = ink(rm)
    print(f"--- {tag}  y{y0}..{y1} ---")
    print(f"  original ink px = {int(om.sum()):5d}  render ink px = {int(rm.sum()):5d}")
    oc = np.where(om.any(axis=0))[0] + 82
    rc = np.where(rm.any(axis=0))[0] / S + 82
    print(f"  original x extent {oc.min()}..{oc.max()} (w={oc.max()-oc.min()})")
    print(f"  render   x extent {rc.min():.0f}..{rc.max():.0f} "
          f"(w={rc.max()-rc.min():.0f})")
    ow = word_clusters(om, 1.0)
    rw = word_clusters(rm, S)
    print(f"  original words: {len(ow)}  render words: {len(rw)}")
    for i, (a_, b_) in enumerate(ow):
        print(f"    O{i + 1:2d}  x{a_:4.0f}-{b_:4.0f}  w={b_ - a_ + 1:4.0f}")
    for i, (a_, b_) in enumerate(rw):
        print(f"    R{i + 1:2d}  x{a_:4.0f}-{b_:4.0f}  w={b_ - a_ + 1:4.0f}")
