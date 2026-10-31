#!/usr/bin/env python3
"""Pixel-first adjudication probe for crop_dense_judge_k15b.txt (06:40 FAIL) and
crop_dense_judge_k16.txt (06:44 FAIL), slide 025.

Render side uses the exact render the k15b legs judged: slide025/render.png
(mtime 2026-10-31 06:21:24, md5 2ab860b7..., promoted k15b render; the crop leg
judged crop_dense_render.png md5 6784ca92 cut from it at region 592,160,896,368).
k16 leg judged crop_dense_render_k16.png (md5 f02ee769), reconstructed to slide
space via its cut geometry (origin 592,160, scale 1125/540).

All measurements in slide space 960x540. Read-only wrt existing evidence.
"""
import hashlib
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide025"

orig = np.asarray(Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
r15 = np.asarray(Image.open(f"{D}/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int32)

SC = 1125 / 540.0
OX, OY = 592, 160
c16 = Image.open(f"{D}/crop_dense_render_k16.png").convert("RGB")
cw, ch = 304, 208  # slide-space crop size 896-592 x 368-160
r16 = np.zeros_like(orig)
paste = c16.resize((cw, ch), Image.LANCZOS)
r16[OY:OY + ch, OX:OX + cw] = np.asarray(paste).astype(np.int32)

print("render.png md5:", hashlib.md5(open(f"{D}/render.png", "rb").read()).hexdigest())
print("crop_dense_render.png md5:", hashlib.md5(open(f"{D}/crop_dense_render.png", "rb").read()).hexdigest())
print("crop_dense_render_k16.png md5:", hashlib.md5(open(f"{D}/crop_dense_render_k16.png", "rb").read()).hexdigest())

IMGS = [("orig", orig), ("render_k15b(render.png 06:21)", r15), ("render_k16(crop_k16->slide)", r16)]

JET = plt.get_cmap("jet")
JET_LUT = (JET(np.linspace(0, 1, 256))[:, :3] * 255.0)
_JET_SQ = (JET_LUT ** 2).sum(1)


def jet_t(px):
    p = px.astype(np.float64)
    d = _JET_SQ[None, :] - 2.0 * (p @ JET_LUT.T) + (p * p).sum(1)[:, None]
    return d.argmin(1) / 255.0


def masks(A):
    r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    mx, mn = A.max(2), A.min(2)
    sat = mx - mn
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    red = (r > 140) & (r - g > 60) & (r - b > 60)
    dark = (lum < 110) & (sat < 90) & ~red
    gray = (lum > 120) & (lum < 215) & (sat < 24) & ~red
    white = (r > 245) & (g > 245) & (b > 245)
    colored = (sat > 60) & (mx > 90) & ~red
    return dict(red=red, dark=dark, gray=gray, white=white, colored=colored, sat=sat, lum=lum)


# ---- BR box (slide x615..880, y344..531) ----
BX0, BY0, BX1, BY1 = 615, 344, 881, 532

# ---- TR box (slide x616..879, y115..317) ----
TX0, TY0, TX1, TY1 = 616, 115, 880, 318

print("\n=== C1: BR z-axis vertical line, band x731-738, y350-525 ===")
for nm, A in IMGS:
    M = masks(A)
    line = M["dark"] | M["gray"]
    band = line[350:526, 731:739]
    colc = band.sum(0)
    # longest vertical run per column
    runs = []
    for c in range(band.shape[1]):
        col = band[:, c]
        best = cur = 0
        for v in col:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        runs.append(best)
    print(f"{nm}: dark+gray px in x731-738 y350-525 = {int(band.sum())}; "
          f"per-col counts x731..738 = {list(map(int, colc))}; longest runs = {runs}")

print("\n=== C2: z-tick label ink strips flanking the vline (dark ink) ===")
for nm, A in IMGS:
    M = masks(A)
    for lbl, x0, x1 in (("left strip x703-730", 703, 731), ("right strip x739-768", 739, 769)):
        strip = M["dark"][350:526, x0:x1]
        rows = strip.sum(1)
        cl = int((rows >= 2).sum())
        # cluster count
        on = rows >= 2
        ncl = 0
        prev = False
        for v in on:
            if v and not prev:
                ncl += 1
            prev = v
        print(f"{nm}: {lbl}: dark px={int(strip.sum())} rows-with-ink={cl} clusters={ncl}")

print("\n=== C3: BR surface colored% + jet-t hist/16 + main-diag stats (box pad 8, GT method) ===")
for nm, A in IMGS:
    p = A[BY0 + 8:BY0 + 187 - 8, BX0 + 8:BX0 + 265 - 8]
    mx, mn = p.max(2), p.min(2)
    red = (p[:, :, 0] > 170) & (p[:, :, 1] < 90) & (p[:, :, 2] < 90)
    cm = ((mx - mn) > 60) & (mx > 90) & ~red
    colored_pct = 100.0 * cm.mean()
    ys, xs = np.nonzero(cm)
    t = jet_t(p[ys, xs])
    hist, _ = np.histogram(t, bins=16, range=(0, 1))
    # diag over full box with border=2
    box = A[BY0:BY0 + 187, BX0:BX0 + 265]
    mx2, mn2 = box.max(2), box.min(2)
    red2 = (box[:, :, 0] > 170) & (box[:, :, 1] < 90) & (box[:, :, 2] < 90)
    m2 = ((mx2 - mn2) > 60) & (mx2 > 90) & ~red2
    m2[:2] = False; m2[-2:] = False; m2[:, :2] = False; m2[:, -2:] = False
    ys2, xs2 = np.nonzero(m2)
    t2 = jet_t(box[ys2, xs2])
    x0, y0 = xs2.min(), ys2.min()
    diag = np.abs((xs2 - x0) - (ys2 - y0)) <= 2
    td = t2[diag] if diag.sum() > 10 else np.array([np.nan])
    sb = (xs2.min() + BX0, ys2.min() + BY0, xs2.max() + BX0, ys2.max() + BY0)
    print(f"{nm}: colored%={colored_pct:.1f} surf-bbox slide x{sb[0]}..{sb[2]} y{sb[1]}..{sb[3]} "
          f"hist16={list(map(int, hist))} diag mean={np.nanmean(td):.3f} std={np.nanstd(td):.3f}")

print("\n=== C4: grid/wall gray ink ===")
for nm, A in IMGS:
    M = masks(A)
    br = M["gray"][BY0:BY1, BX0:BX1]
    tr = M["gray"][TY0:TY1, TX0:TX1]
    # crop region (what the judge saw): x592-896 y160-368
    cr = M["gray"][160:369, 592:897]
    print(f"{nm}: gray px BR={int(br.sum())} TR={int(tr.sum())} crop-region={int(cr.sum())}")

print("\n=== C5: red diagonal along (652,189)->(667,165) in TR (dist<=2 px to segment) + red in BR ===")
import math
x1, y1, x2, y2 = 652.0, 189.0, 667.0, 165.0
L = math.hypot(x2 - x1, y2 - y1)
for nm, A in IMGS:
    M = masks(A)
    yy, xx = np.mgrid[115:318, 616:880]
    # distance to segment
    t = ((xx - x1) * (x2 - x1) + (yy - y1) * (y2 - y1)) / (L * L)
    t = np.clip(t, 0, 1)
    px = x1 + t * (x2 - x1)
    py = y1 + t * (y2 - y1)
    dist = np.hypot(xx - px, yy - py)
    near = dist <= 2.0
    red_tr = M["red"][115:318, 616:880]
    n_diag = int((red_tr & near).sum())
    n_red_tr = int(red_tr.sum())
    red_br = M["red"][BY0:BY1, BX0:BX1]
    print(f"{nm}: red px within 2px of (652,189)->(667,165) = {n_diag}; total red in TR box = {n_red_tr}; "
          f"red in BR box = {int(red_br.sum())}")

print("\n=== C6: TR surface 3D-ness proxies (TR box x616-879 y115-317) ===")
for nm, A in IMGS:
    M = masks(A)
    sub = A[TY0:TY1, TX0:TX1]
    Msub = {k: v[TY0:TY1, TX0:TX1] for k, v in M.items()}
    ys, xs = np.nonzero(Msub["colored"])
    if len(xs) == 0:
        print(f"{nm}: no colored px"); continue
    bx0, bx1, by0, by1 = xs.min() + TX0, xs.max() + TX0, ys.min() + TY0, ys.max() + TY0
    # white above surface top (3D box leaves background above silhouette)
    top_white = int(Msub["white"][:max(1, by0 - TY0), :].sum())
    gray_in = int(Msub["gray"].sum())
    white_in = int(Msub["white"].sum())
    print(f"{nm}: TR colored surf bbox slide x{bx0}..{bx1} y{by0}..{by1} (w={bx1-bx0+1} h={by1-by0+1}) "
          f"colored%={100.0*Msub['colored'].mean():.1f} white-above-top={top_white} gray-in-box={gray_in} white-in-box={white_in}")

print("\nPROBE_DONE")
