#!/usr/bin/env python3
"""crop-legs-016b: adjudicate the last_bullet MAJOR (underline placement) against
BOTH images — PIL-first, frame space 960x540, 1px = 1pt.

crop_5_last_bullet_judge.txt claims (MAJOR/high): the original underlines
"Small number of samples" and "Large vector" but NOT "Length", while the
recreation underlines only "Length".

Banked counter-evidence (selfcheck_attempt_4.txt): dark underline under
'Length (d)' at y518..531 measured in BOTH images; LEG A verdict lists the
underline under "Length" as present in both.

Method: find every long horizontal dark stroke in the last-bullet region
(y470..540, x80..830) in each image — contiguous ink runs >= 25 frame px wide
whose column band is dark (luma < 120) — then report y and x-extent in frame px,
plus the word each extent sits under (glyph rows of the two text lines).
"""
import numpy as np
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")

oa = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
na = np.asarray(Image.open(f"{QA}/render_5.png").convert("RGB")).astype(int)
S = na.shape[0] / oa.shape[0]
print(f"orig {oa.shape[1]}x{oa.shape[0]}  render {na.shape[1]}x{na.shape[0]}  S={S:.4f}")

X0, X1, Y0, Y1 = 80, 830, 470, 540


def strokes(a, s):
    """Long horizontal dark strokes inside the region, in frame px."""
    seg = a[int(Y0 * s):int(Y1 * s), int(X0 * s):int(X1 * s)]
    luma = seg.mean(axis=2)
    dark = luma < 120
    out = []
    for r in range(dark.shape[0]):
        row = dark[r]
        run, st = None, None
        for i, v in enumerate(row):
            if v and st is None:
                st = i
            elif not v and st is not None:
                if i - st >= 25 * s:            # >= 25 frame px wide
                    out.append((r / s + Y0, st / s + X0, (i - 1) / s + X0))
                st = None
        if st is not None and len(row) - st >= 25 * s:
            out.append((r / s + Y0, st / s + X0, (len(row) - 1) / s + X0))
    return out


print("\n=== dark horizontal strokes >=25 frame px, region x80..830 y470..540 ===")
for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
    st = strokes(a, s)
    # merge contiguous rows that produce the same stroke (a 1-2 frame-px tall rule)
    merged = []
    for y, x0, x1 in st:
        if merged and abs(merged[-1][0] - y) <= 1.5 and abs(merged[-1][2] - x0) < 6:
            m = merged[-1]
            merged[-1] = ((m[0] + y) / 2, min(m[1], x0), max(m[2], x1))
        else:
            merged.append((y, x0, x1))
    print(f"  {lbl}: {len(merged)} stroke band(s)")
    for y, x0, x1 in merged:
        print(f"    y{y:6.1f}  x{x0:6.1f}..{x1:6.1f}  width {x1-x0:6.1f} frame px")

print("\n=== glyph rows per text line (ink rows), BOTH ===")
for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
    seg = a[int(Y0 * s):int(Y1 * s), int(X0 * s):int(X1 * s)]
    dark = seg.mean(axis=2) < 160
    rows = dark.any(axis=1)
    bands, st = [], None
    for i, v in enumerate(rows):
        if v and st is None:
            st = i
        elif not v and st is not None:
            if i - st >= 3:
                bands.append((st / s + Y0, (i - 1) / s + Y0))
            st = None
    if st is not None:
        bands.append((st / s + Y0, (len(rows) - 1) / s + Y0))
    print(f"  {lbl}: text/ink bands " + ", ".join(
        f"y{p:.0f}..{q:.0f}" for p, q in bands))

print("\n=== word extents on the last-bullet lines (frame px), BOTH ===")
# b5a "Small number of samples" line, b5b "Large vector Length (d)" line
for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
    for tag, y0, y1 in (("b5a", 484, 502), ("b5b", 508, 528)):
        seg = a[int(y0 * s):int(y1 * s), int(X0 * s):int(X1 * s)]
        colhas = (seg.mean(axis=2) < 160).any(axis=0)
        runs, st = [], None
        for i, v in enumerate(colhas):
            if v and st is None:
                st = i
            elif not v and st is not None:
                if i - st >= 2:
                    runs.append((st / s + X0, (i - 1) / s + X0))
                st = None
        if st is not None:
            runs.append((st / s + X0, (len(colhas) - 1) / s + X0))
        # group words: gaps >= 4 frame px separate words
        words, cur = [], [runs[0]]
        for r0, r1 in runs[1:]:
            if r0 - cur[-1][1] - 1 >= 4:
                words.append((cur[0][0], cur[-1][1]))
                cur = [r0, r1] if False else [(r0, r1)]
            else:
                cur.append((r0, r1))
        if cur:
            words.append((cur[0][0], cur[-1][1]))
        print(f"  {lbl} {tag}: words " + " ".join(
            f"[{p:.0f}-{q:.0f}]" for p, q in words))
print("\nDONE")
