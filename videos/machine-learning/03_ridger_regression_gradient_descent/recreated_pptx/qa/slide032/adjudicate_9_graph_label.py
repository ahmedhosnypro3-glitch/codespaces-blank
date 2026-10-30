#!/usr/bin/env python3
"""Adjudicate the attempt-9 graph-crop FAIL finding #1:

  judge: IMG1 (render) prints "(7, 7)" by the right-end black dot; IMG2 (original)
  prints "(?, ?)" at the same spot.

Build draws the label at build/slide_032.js:200  gLabel("(7, 7)", 724, 140, 30, 13)
because an earlier probe recorded "(7, 7)" off the frame.

This script dumps a PIXEL ink map of BOTH images over the label window
(frame x716..760, y134..156) so the glyphs can be read shape-by-shape.
Frame is 960x540 (1px = 1pt); render_9 is 2001x1125 (2.0833 px/frame px).
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = V + "/unique_slides/slide_032.jpg"
REND = V + "/recreated_pptx/qa/slide032/render_9.png"

o = np.asarray(Image.open(ORIG).convert("L")).astype(int)
r = np.asarray(Image.open(REND).convert("L")).astype(int)
S = r.shape[0] / 540.0
print(f"ORIG {o.shape[1]}x{o.shape[0]}   REND {r.shape[1]}x{r.shape[0]}  S={S:.4f}\n")


def window(im, x0, y0, x1, y1):
    """frame-px bbox -> pixel subarray (scales with the image's own resolution)"""
    s = im.shape[0] / 540.0
    return im[int(round(y0 * s)):int(round(y1 * s)), int(round(x0 * s)):int(round(x1 * s))]


def lum_map(sub, x0, y0, s, step=1):
    """ASCII luminance map: every pixel row/col shown (1 char = 1 source pixel)."""
    print(f"--- luminance map, frame x{x0}..{x0 + sub.shape[1] / s:.0f} "
          f"y{y0}..{y0 + sub.shape[0] / s:.0f} ---")
    hdr = "     " + "".join(str(int((x0 + c / s) // 10 % 10)) if (int(x0 + c / s) % 10 == 0) else " "
                           for c in range(sub.shape[1]))
    print(hdr)
    for ry in range(sub.shape[0]):
        ROW = "".join(
            "#" if v < 120 else ("+" if v < 175 else ("." if v < 225 else " "))
            for v in sub[ry, :])
        print(f"  {int(y0 + ry / s):>3} {ROW}")


def ink_census(sub, x0, y0, s, thr=235):
    m = sub < thr
    cols = m.sum(axis=0)
    rn = np.nonzero(m.sum(axis=1))[0]
    cn = np.nonzero(cols)[0]
    print(f"  ink px {int(m.sum())}  ink rows y{y0 + rn[0] / s:.0f}..{y0 + rn[-1] / s:.0f}"
          f"  ink cols x{x0 + cn[0] / s:.0f}..{x0 + cn[-1] / s:.0f}")
    # column clusters (gap > 2 px)
    runs, start = [], cn[0]
    for a, b in zip(cn, cn[1:]):
        if b - a > 2:
            runs.append((start, a)); start = b
    runs.append((start, cn[-1]))
    print("  col clusters (frame px): " + ", ".join(
        f"{x0 + a / s:.0f}..{x0 + b / s:.0f}" for a, b in runs))


for tag, im in (("ORIG", o), ("REND9", r)):
    print("=" * 70)
    print(f"### {tag} — right-dot label window  x716..762  y134..156")
    sub = window(im, 716, 134, 762, 156)
    ink_census(sub, 716, 134, im.shape[0] / 540.0)
    lum_map(sub, 716, 134, im.shape[0] / 540.0)

# ---- the reference: the SAME glyph set as the ORIGINAL's own "(2, 10)" label,
#      which the build reproduces as "(2, 10)" at x619..659 (build line 199).
print("\n" + "=" * 70)
print("### REFERENCE — left label '(2, 10)' in BOTH images (x612..664, y144..162)")
for tag, im in (("ORIG", o), ("REND9", r)):
    sub = window(im, 612, 144, 664, 162)
    ink_census(sub, 612, 144, im.shape[0] / 540.0)
    lum_map(sub, 612, 144, im.shape[0] / 540.0)

# ---- global: any '?' shaped glyph anywhere near the right dot? sweep the
#      wider plot interior for tiny dark clusters at label height y134..156.
print("\n" + "=" * 70)
print("### wide sweep — dark-ish clusters (lum<200, >=3 px) at frame y134..156, x574..810")
for tag, im in (("ORIG", o), ("REND9", r)):
    s = im.shape[0] / 540.0
    band = window(im, 574, 134, 810, 156)
    m = band < 200
    cols = m.sum(axis=0)
    nz = np.nonzero(cols)[0]
    runs, start = [], nz[0]
    for a, b in zip(nz, nz[1:]):
        if b - a > 2:
            runs.append((start, a)); start = b
    runs.append((start, nz[-1]))
    tot = int(m.sum())
    print(f"  {tag}: dark px {tot}; clusters: " + ", ".join(
        f"x{574 + a / s:.0f}..{574 + b / s:.0f} (n={int(cols[a:b + 1].sum())})" for a, b in runs))
