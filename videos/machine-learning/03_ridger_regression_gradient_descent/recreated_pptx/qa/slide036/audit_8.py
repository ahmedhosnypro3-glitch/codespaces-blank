#!/usr/bin/env python3
"""PIL audit for slide 036 attempt 8 (render_8.png vs slide_036.jpg).

Measured numbers used by the attempt-8 judge transcripts:
  1. per-line text ink spans (font-substitution width ratios)
  2. box4/box2 line ink-run gaps around the implication arrows and the equation
     phrase gap (collision audit)
  3. equation piece bboxes (Error=, Sigma, limit, term1, arrow, term2, phrase)
  4. term2 delimiter spans vs enclosed glyph extent
  5. red-part color check of the summation limit
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.array(Image.open(f"{V}/unique_slides/slide_036.jpg").convert("RGB")).astype(int)
r = np.array(Image.open(f"{V}/recreated_pptx/qa/slide036/render_8.png").convert("RGB")).astype(int)
S = r.shape[0] / 540.0

print(f"render {r.shape[1]}x{r.shape[0]}  scale {S:.6f} render px / frame px")
print(f"original {o.shape[1]}x{o.shape[0]}")


def bbox(a, x0, y0, x1, y1, thr=175, scale=1.0):
    X0, X1, Y0, Y1 = [int(round(v * scale)) for v in (x0, x1, y0, y1)]
    sub = a[Y0:Y1, X0:X1]
    lum = sub.mean(axis=2)
    m = lum < thr
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (round((X0 + xs.min()) / scale, 1), round((Y0 + ys.min()) / scale, 1),
            round((X0 + xs.max()) / scale, 1), round((Y0 + ys.max()) / scale, 1))


def runs(a, x0, y0, x1, y1, thr=175, scale=1.0, gap=3):
    X0, X1, Y0, Y1 = [int(round(v * scale)) for v in (x0, x1, y0, y1)]
    sub = a[Y0:Y1, X0:X1]
    lum = sub.mean(axis=2)
    cols = (lum < thr).any(axis=0)
    out, i = [], 0
    while i < len(cols):
        if cols[i]:
            j = i
            while j + 1 < len(cols) and cols[j + 1]:
                j += 1
            out.append([round((X0 + i) / scale), round((X0 + j) / scale)])
            i = j + 1
        else:
            i += 1
    merged = []
    for r0 in out:
        if merged and r0[0] - merged[-1][1] <= gap:
            merged[-1][1] = r0[1]
        else:
            merged.append(r0)
    return merged


print("\n== 1. per-line ink spans (text only, border columns excluded) ==")
LINES = {
    "b1L1": (79, 100, 866, 120), "b1L2": (79, 125, 866, 152),
    "b1L3": (79, 155, 866, 181), "b1L4": (79, 185, 866, 212),
    "b2L1": (79, 230, 866, 254), "b2L2": (79, 257, 866, 285),
    "b2L3": (79, 287, 866, 315),
    "b3head": (79, 336, 866, 362),
    "b4L1": (79, 444, 866, 466), "b4L2": (79, 470, 866, 495),
    "b4L3": (79, 498, 866, 523),
}
ratios = []
for nm, (x0, y0, x1, y1) in LINES.items():
    a = bbox(o, x0, y0, x1, y1, 150)
    b = bbox(r, x0, y0, x1, y1, 150, S)
    if a and b:
        wa, wb = a[2] - a[0], b[2] - b[0]
        ratios.append(wb / wa)
        print(f"  {nm:7s} orig x{a[0]:5.1f}..{a[2]:5.1f} (w{wa:5.1f})   "
              f"rend x{b[0]:5.1f}..{b[2]:5.1f} (w{wb:5.1f})   ratio {wb/wa:.3f}")
print(f"  width-ratio range {min(ratios):.3f}..{max(ratios):.3f} "
      f"(Arial vs the source's serif face; deck-standard substitution)")

print("\n== 2. collision audit: box4 lines + equation phrase gap ==")
for nm, (x0, y0, x1, y1) in {"b4L1": (79, 444, 866, 466), "b4L2": (79, 470, 866, 495),
                             "b4L3": (79, 498, 866, 523)}.items():
    ra = runs(o, x0, y0, x1, y1, 150, 1.0, gap=4)
    rb = runs(r, x0, y0, x1, y1, 150, S, gap=4)
    print(f"  {nm} orig run count {len(ra)}  gaps"
          f" {[round(ra[i+1][0]-ra[i][1]) for i in range(len(ra)-1)][:24]}")
    print(f"  {nm} rend run count {len(rb)}  gaps"
          f" {[round(rb[i+1][0]-rb[i][1]) for i in range(len(rb)-1)][:24]}")

print("\n== 3. equation pieces (frame px bbox) ==")
PIECES = {"Error=": (80, 365, 160, 400), "Sigma": (212, 360, 246, 400),
          "limit": (150, 398, 345, 420), "term1": (295, 362, 375, 400),
          "arrow": (390, 368, 415, 398), "term2": (435, 362, 505, 400),
          "phrase": (503, 370, 740, 400)}
for nm, box in PIECES.items():
    print(f"  {nm:7s} orig {bbox(o, *box)}   rend {bbox(r, *box, scale=S)}")

print("\n== 4. term2 delimiter spans vs enclosed glyphs ==")
for nm, (x0, x1) in {"term2 (": (442, 450), "term2 )": (492, 502)}.items():
    for tag, img, sc in (("orig", o, 1.0), ("rend", r, S)):
        X0, X1 = int(x0 * sc), int(x1 * sc)
        col = img[int(370 * sc):int(398 * sc), X0:X1].mean(axis=2)
        ys = np.where((col < 175).any(axis=1))[0]
        if len(ys):
            print(f"  {nm} {tag}: stroke y {370+ys.min()/sc:.1f}..{370+ys.max()/sc:.1f}")
g = bbox(o, 451, 366, 494, 400)
gr = bbox(r, 451, 366, 494, 400, S)
print(f"  enclosed glyphs (W..i) orig y{g[1]}..{g[3]}  rend y{gr[1]}..{gr[3]}")

print("\n== 5. summation-limit color (red parts) ==")
for tag, img, sc in (("orig", o, 1.0), ("rend", r, S)):
    X0, X1 = int(155 * sc), int(310 * sc)
    Y0, Y1 = int(400 * sc), int(416 * sc)
    sub = img[Y0:Y1, X0:X1]
    red = (sub[:, :, 0] > 120) & (sub[:, :, 1] < 90) & (sub[:, :, 2] < 90)
    ys, xs = np.where(red)
    if len(xs):
        print(f"  {tag}: {int(red.sum())} red px, x "
              f"{155+xs.min()/sc:.0f}..{155+xs.max()/sc:.0f}")
    else:
        print(f"  {tag}: NO red px in the limit band")

print("\n== 6. frame containment of the equation asset ==")
eq = bbox(r, 80, 360, 760, 420, 150, S)
print(f"  equation ink {eq} inside box3 (x69..869, y328..421): "
      f"{eq[0] >= 69 and eq[2] <= 869 and eq[1] >= 328 and eq[3] <= 421}")
print(f"  gap to red X mark: X ink {bbox(r, 750, 360, 800, 400, 120, S)}")
