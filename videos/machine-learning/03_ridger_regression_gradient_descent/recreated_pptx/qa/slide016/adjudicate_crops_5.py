#!/usr/bin/env python3
"""crop-legs-016 PIL adjudication of slide 016 attempt-5 crop-leg MINORs
(vs render_5.png == current pptx, md5 e50fd50d429ca880793c05b94e0c6487).

Frame space 960x540; 150dpi render 2001x1125 -> S = 1125/540 = 2.0833 render px
per frame px (1px = 1pt). Every finding is measured against BOTH images before
any build change is proposed (PIL-first adjudication).

Findings adjudicated (from crop_5_missing_band_judge.txt and
crop_5_bullet2_judge.txt):
  mb#1  stray space before ')' in "Ridge Regularization )"   (MINOR/high)
  mb#2  two spaces before "(also know as" in the original    (MINOR/medium)
  mb#3  red runs darker in IMG1                              (MINOR/low)
  b2#1  yellow highlight absent behind "customized weigh factor" (MINOR/medium)
  b2#2  phrase text tint vs body ("if it is actually red text") (MINOR/low)
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
ink = lambda a: a.min(axis=2) < 200


def band(a, x0, x1, y0, y1, s):
    return a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]


def runs(m, lo, s):
    out, st = [], None
    for i, v in enumerate(m):
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st / s + lo, (i - 1) / s + lo)); st = None
    if st is not None:
        out.append((st / s + lo, (len(m) - 1) / s + lo))
    return out


print("\n=== F1: yellow-fill (r>190,g>190,b<160) per band, BOTH ===")
for name, y0, y1 in [("better-generalization line", 170, 200),
                     ("bullet2 L1/L2", 222, 285),
                     ("L3 'customized weigh factor'", 285, 300),
                     ("missing_band L7-L10", 325, 455),
                     ("last-bullet cluster", 470, 533)]:
    for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
        seg = band(a, 80, 830, y0, y1, s)
        y = ((seg[:, :, 0] > 190) & (seg[:, :, 1] > 190) & (seg[:, :, 2] < 160)).sum()
        print(f"  {name:32s} {lbl:6s} yellow px {int(y):7d}")

print("\n=== F2: red underline under 'customized weigh factor' (y293..300) ===")
for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
    b = band(a, 80, 830, 293, 300, s)
    r = ((b[:, :, 0] > 120) & (b[:, :, 1] < 90) & (b[:, :, 2] < 90)).sum()
    print(f"  {lbl:6s} red px {int(r):6d}")

print("\n=== G1: ink RGB vs known red/blue runs (is L3 red text?) ===")
for name, x0, x1, y0, y1 in [("RED 'Squared Norm'", 385, 667, 333, 349),
                             ("RED '(N)'", 647, 670, 486, 501),
                             ("BLUE 'L2 regularization'", 254, 390, 357, 374),
                             ("L3 'customized weigh factor'", 108, 360, 282, 293),
                             ("BODY b2a L1", 108, 400, 228, 250)]:
    for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
        seg = band(a, x0, x1, y0, y1, s)
        m = ink(seg); px = seg[m]
        if not len(px):
            print(f"  {name:30s} {lbl:6s} (no ink)"); continue
        r, g, b = px[:, 0], px[:, 1], px[:, 2]
        sr = int(((r > 140) & (g < 90) & (b < 90)).sum())
        print(f"  {name:30s} {lbl:6s} ink {len(px):6d} mean "
              f"({r.mean():3.0f},{g.mean():3.0f},{b.mean():3.0f}) strong-red "
              f"{sr:5d} ({100*sr/len(px):5.1f}%)")

print("\n=== G2/G3: b3b line word-gap profile (y357..376) ===")
for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
    seg = band(a, 250, 640, 357, 376, s)
    fr = runs(ink(seg).any(axis=0), 250, s)
    gaps = [fr[i + 1][0] - fr[i][1] - 1 for i in range(len(fr) - 1)]
    print(f"  {lbl}: {len(fr)} clusters; gaps: " + " ".join(f"{g:.0f}" for g in gaps))
    print(f"    clusters x360..440: " +
          " ".join(f"{p:.0f}-{q:.0f}" for p, q in fr if 350 < p < 450))

print("\n=== F5: gap last letter -> ')' (L8 tail, x400..620) ===")
for lbl, a, s in (("orig", oa, 1.0), ("render", na, S)):
    fr = runs(ink(band(a, 400, 620, 355, 376, s)).any(axis=0), 400, s)
    tail = [r for r in fr if r[1] >= (fr[-1][1] - 20)]
    print(f"  {lbl}: tail clusters " + ", ".join(f"{p:.0f}..{q:.0f}" for p, q in tail) +
          f"  | gap->')' {(tail[-1][0]-tail[-2][1]-1):.0f} frame px" if len(tail) >= 2 else "")
print("\nDONE")
