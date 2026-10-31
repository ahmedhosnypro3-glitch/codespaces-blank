#!/usr/bin/env python3
"""Per-claim PIL adjudication of slide025/judge_full_fresh2.txt (06:38:32Z FAIL) vs the
current deliverable render (render.png 06:21:24, from slide_025_recreated.pptx md5
736036754a8d built 06:20:52) and unique_slides/slide_025.jpg. Read-only."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide025"
R = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)          # 1125x2001
Oimg = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")              # 540x960
O = np.asarray(Oimg.resize((R.shape[1], R.shape[0]), Image.LANCZOS)).astype(int)
S = R.shape[1] / 960.0  # slide-px -> render-px scale (~2.0844)

def slide_box(x0, y0, x1, y1):
    return (slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S)))

def masks(A):
    r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    mx = A.max(axis=2); mn = A.min(axis=2); sat = mx - mn
    dark = A.sum(axis=2) < 330
    white = (r > 240) & (g > 240) & (b > 240)
    gray = (sat < 24) & (mx > 120) & (mx < 235)
    red = (r > 120) & (g < 110) & (b < 110) & (sat > 60)
    colored = (sat > 45) & ~red & ~dark & ~(white)
    return dict(dark=dark, white=white, gray=gray, red=red, colored=colored)

MR, MO = masks(R), masks(O)

def stat(name, box):
    sr, so = slide_box(*box)
    print(f"--- {name} slide-box {box} ---")
    for k in ("dark", "gray", "red", "colored", "white"):
        print(f"  {k}: render={int(MR[k][sr, so].sum())} orig={int(MO[k][sr, so].sum())}")

# D1: TR z-axis scale strip, upper-left of TR axes box (slide ~x585-660, y120-210)
stat("D1 TR z-label strip (x585-665,y120-215)", (585, 120, 665, 215))
# TR z-axis vertical line presence: column dark-ink runs in x600-625, y120-320
for nm, M in (("render", MR), ("orig", MO)):
    strip = M["dark"][slide_box(600, 120, 626, 320)]
    colsum = strip.sum(axis=0)
    best = int(colsum.max()); bx = int(colsum.argmax())
    rows = strip[:, bx].sum() if strip.size else 0
    print(f"  D1 z-vline {nm}: strip x600-626 best col slide-x={600+bx} darkpx={best} of {strip.shape[0]} rows")

# D3: TR frame top/bottom via red horizontal edges within x578-820
for nm, M in (("render", MR), ("orig", MO)):
    band = M["red"][slide_box(578, 100, 822, 340)]
    rows = band.sum(axis=1)
    ys = [int(i + 100) for i, v in enumerate(rows) if v > 60]
    print(f"  D3 TR red-edge rows(>60px) {nm}: y={ys[:6]}...{ys[-6:] if ys else []}")

# D4: BL gray 3D box/grid ink + surface extent in BL plot interior
stat("D4 BL plot interior (x70-450,y300-530)", (70, 300, 450, 530))
for nm, M in (("render", MR), ("orig", MO)):
    box = M["colored"][slide_box(70, 300, 450, 530)]
    cols = box.sum(axis=0); rows = box.sum(axis=1)
    cx = [int(70 + i) for i, v in enumerate(cols) if v > 10]
    print(f"  D4 BL colored cols {nm}: x{cx[0] if cx else '-'}..{cx[-1] if cx else '-'} (orig expectation to ~340)")

# D6: BR containment — colored ink in bottom band of BR frame interior
stat("D6 BR bottom band (x480-890,y505-537)", (480, 505, 890, 537))
stat("D6 BR right band (x860-895,y300-530)", (860, 300, 895, 530))
for nm, M in (("render", MR), ("orig", MO)):
    band = M["colored"][slide_box(480, 505, 890, 537)]
    rows = band.sum(axis=1)
    print(f"  D6 BR bottom-band colored per slide-row {nm}: " +
          " ".join(f"y{505+i}:{int(v)}" for i, v in enumerate(rows)))

# D7: TL gray axes-box ink
stat("D7 TL plot interior (x70-450,y105-290)", (70, 105, 450, 290))

# D9: title red bbox (slide y55-95, x200-760)
for nm, M in (("render", MR), ("orig", MO)):
    band = M["red"][slide_box(200, 55, 760, 95)]
    ys, xs = np.where(band)
    if len(xs):
        print(f"  D9 title red bbox {nm}: x{200+xs.min()/S:.0f}-{200+xs.max()/S:.0f} "
              f"y{55+ys.min()/S:.1f}-{55+ys.max()/S:.1f} px={len(xs)}")
    else:
        print(f"  D9 title red bbox {nm}: none")

# D5: BL callout label dark-ink centroids in four sub-boxes (slide coords from fresh2 D5)
for lbl, box in (("GlobalMaxima", (200, 290, 260, 315)), ("LocalMaxima", (240, 325, 300, 350)),
                 ("LocalMinima", (110, 435, 175, 465)), ("GlobalMinima", (150, 455, 230, 485))):
    for nm, M in (("render", MR), ("orig", MO)):
        sub = M["dark"][slide_box(*box)]
        ys, xs = np.where(sub)
        if len(xs):
            cx = box[0] + xs.mean() / S; cy = box[1] + ys.mean() / S
            print(f"  D5 {lbl} {nm}: centroid slide=({cx:.0f},{cy:.0f}) ink={len(xs)}")
        else:
            print(f"  D5 {lbl} {nm}: no ink in box {box}")

# D8: TL left tick strip ink presence (values not OCR-able at 960px; presence only)
stat("D8 TL left tick strip (x60-110,y110-280)", (60, 110, 110, 280))

# D10/D2 supplement: TR surface extent (colored) rows/cols in TR plot
for nm, M in (("render", MR), ("orig", MO)):
    box = M["colored"][slide_box(585, 115, 825, 330)]
    rows = box.sum(axis=1); cols = box.sum(axis=0)
    ry = [int(115 + i) for i, v in enumerate(rows) if v > 10]
    cx = [int(585 + i) for i, v in enumerate(cols) if v > 10]
    print(f"  TR colored extent {nm}: y{ry[0] if ry else '-'}..{ry[-1] if ry else '-'} "
          f"x{cx[0] if cx else '-'}..{cx[-1] if cx else '-'} total={int(box.sum())}")
