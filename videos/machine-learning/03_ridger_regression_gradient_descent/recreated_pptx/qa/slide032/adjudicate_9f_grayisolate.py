#!/usr/bin/env python3
"""Adjudicate_9f — isolate the RIGHT point label by colour, not by bbox.

Build draws the point labels in LABEL_GRAY 666666 (lum ~102); the black chord and
its end dots are < 60 lum; gridlines are D9D9D9 (~217). A mid-luminance band
therefore isolates the label glyphs in BOTH images, including any "(" hidden
inside the dot, so the ORIGINAL's actual text can be read glyph by glyph.

Window: frame x716..766, y136..158 (label baseline band), both images normalised
to the same 1 char = 1 frame px grid.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

o = np.asarray(Image.open(V + "/unique_slides/slide_032.jpg").convert("L")).astype(float)
rim = Image.open(V + "/recreated_pptx/qa/slide032/render_9.png").convert("L")
S = rim.size[1] / 540.0
X0, Y0, X1, Y1 = 716, 136, 766, 158


def show(a, tag, lo, hi):
    print(f"--- {tag}: pixels with lum in [{lo},{hi}) ---")
    for ry in range(a.shape[0]):
        print(f"  {int(Y0) + ry:>3} " + "".join(
            "#" if lo <= v < hi else " " for v in a[ry, :]))
    print()


def clusters(a, lo, hi, gap=1, minpx=2):
    m = (a >= lo) & (a < hi)
    cols = m.sum(axis=0)
    nz = np.nonzero(cols)[0]
    if len(nz) == 0:
        return []
    runs, start = [], nz[0]
    for x, y in zip(nz, nz[1:]):
        if y - x > gap:
            runs.append((start, x)); start = y
    runs.append((start, nz[-1]))
    out = []
    for a0, b0 in runs:
        seg = m[:, a0:b0 + 1]
        rs = np.nonzero(seg.sum(axis=1))[0]
        n = int(seg.sum())
        if n >= minpx:
            out.append((X0 + a0, X0 + b0, int(Y0) + rs[0], int(Y0) + rs[-1], n))
    return out


# render window downsampled to 1 px per frame px for a like-for-like grid
rsub = rim.crop((int(X0 * S), int(Y0 * S), int(X1 * S), int(Y1 * S)))
rsub = rsub.resize((X1 - X0, Y1 - Y0), Image.LANCZOS)
r = np.asarray(rsub).astype(float)
osub = o[Y0:Y1, X0:X1]

for lo, hi in ((60, 200), (80, 170), (100, 200)):
    print("=" * 76)
    print(f"### luminance band {lo}..{hi}")
    print("\nORIGINAL clusters:")
    for c in clusters(osub, lo, hi):
        print(f"   x{c[0]}..{c[1]} y{c[2]}..{c[3]}  px={c[4]}")
    print("\nRENDER clusters:")
    for c in clusters(r, lo, hi):
        print(f"   x{c[0]}..{c[1]} y{c[2]}..{c[3]}  px={c[4]}")
    print()

print("=" * 76)
print("### the two label glyph groups side by side at 1 char = 1 frame px")
print("=" * 76)
show(osub[:, 10:24], "ORIG left half  x726..740", 60, 200)
show(r[:, 10:24], "REND left half  x726..740", 60, 200)
show(osub[:, 22:44], "ORIG right half x738..760", 60, 200)
show(r[:, 22:44], "REND right half x738..760", 60, 200)
