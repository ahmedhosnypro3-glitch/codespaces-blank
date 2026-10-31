#!/usr/bin/env python3
"""Adjudication probe v2 — slide 025 crop FAILs (k15b 06:40, k16 06:44).

Slide space 960x540. orig = unique_slides/slide_025.jpg.
render_k15b = slide025/render.png (06:21:24, md5 2ab860b7) resized 960x540 —
  the exact render whose crop (crop_dense_render.png md5 6784ca92) the k15b
  crop leg judged.
render_k16  = crop_dense_render_k16.png (md5 f02ee769) pasted back at slide
  (592,160) scale 1125/540; VALID ONLY inside x592-896 y160-368 (elsewhere the
  canvas is zero-fill). k16-only measurements are restricted to that window.
"""
import hashlib
import math
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
OX, OY, CW, CH = 592, 160, 304, 208
c16 = Image.open(f"{D}/crop_dense_render_k16.png").convert("RGB")
r16 = np.zeros_like(orig)
r16[OY:OY + CH, OX:OX + CW] = np.asarray(c16.resize((CW, CH), Image.LANCZOS)).astype(np.int32)
VALID16 = np.zeros((540, 960), bool)
VALID16[OY:OY + CH, OX:OX + CW] = True

# regenerate the k15b crop pair exactly as promote_k15b_025.sh did, verify md5
rc = Image.open(f"{D}/render.png").convert("RGB").crop(
    (int(592 * SC), int(160 * SC), int(math.ceil(896 * SC)), int(math.ceil(368 * SC))))
oc = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB").crop((592, 160, 896, 368)).resize(rc.size, Image.LANCZOS)
rc.save(f"{D}/crop_regen_render.png")
oc.save(f"{D}/crop_regen_orig.png")
print("regen render md5:", hashlib.md5(open(f"{D}/crop_regen_render.png", "rb").read()).hexdigest(),
      "(judged k15b:", hashlib.md5(open(f"{D}/crop_dense_render.png", "rb").read()).hexdigest() + ")")
print("regen orig   md5:", hashlib.md5(open(f"{D}/crop_regen_orig.png", "rb").read()).hexdigest(),
      "(judged k15b:", hashlib.md5(open(f"{D}/crop_dense_orig.png", "rb").read()).hexdigest() + ")")

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
    return dict(red=red, dark=dark, gray=gray, white=white, colored=colored)


IMGS = [("orig", orig, None), ("render_k15b", r15, None), ("render_k16", r16, VALID16)]

TX0, TY0, TX1, TY1 = 616, 115, 880, 318      # TR plot box
BX0, BY0, BX1, BY1 = 615, 344, 881, 532      # BR plot box


def longest_run(col):
    best = cur = 0
    for v in col:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


print("\n=== C1: z-axis vertical line in TR box — scan x616-879 y120-315 for the strongest column ===")
for nm, A, V in IMGS:
    M = masks(A)
    line = (M["dark"] | M["gray"])[TY0 + 5:TY1 - 2, TX0:TX1]
    if V is not None:
        line = line & V[TY0 + 5:TY1 - 2, TX0:TX1]
    colc = line.sum(0)
    order = np.argsort(-colc)[:6]
    det = [(int(TX0 + c), int(colc[c]), longest_run(line[:, c])) for c in order if colc[c] > 0]
    print(f"{nm}: top columns (slide x, px, longest run): {det}")

print("\n=== C1b: band x731-738 specifically, y120-315 ===")
for nm, A, V in IMGS:
    M = masks(A)
    line = (M["dark"] | M["gray"])[120:316, 731:739]
    if V is not None:
        line = line & V[120:316, 731:739]
    colc = line.sum(0)
    runs = [longest_run(line[:, c]) for c in range(8)]
    print(f"{nm}: x731-738 px={int(line.sum())} per-col={list(map(int, colc))} runs={runs}")

print("\n=== C2: z-tick label ink strips flanking x731-738 (dark ink), y120-315 ===")
for nm, A, V in IMGS:
    M = masks(A)
    for lbl, x0, x1 in (("left x700-730", 700, 731), ("right x739-770", 739, 771)):
        strip = M["dark"][120:316, x0:x1]
        if V is not None:
            strip = strip & V[120:316, x0:x1]
        rows = strip.sum(1)
        on = rows >= 2
        ncl = 0
        prev = False
        for v in on:
            if v and not prev:
                ncl += 1
            prev = v
        print(f"{nm}: {lbl}: dark px={int(strip.sum())} rows>=2px={int(on.sum())} clusters={ncl}")

print("\n=== C3: BR surface (x615-880 y344-531, pad-8 GT method) — orig & k15b only (k16 crop covers y<=368) ===")
for nm, A, V in IMGS:
    if nm == "render_k16":
        print(f"{nm}: BR surface NOT covered by k16 crop (crop ends y368); skipping")
        continue
    p = A[BY0 + 8:BY0 + 179, BX0 + 8:BX0 + 257]
    mx, mn = p.max(2), p.min(2)
    red = (p[:, :, 0] > 170) & (p[:, :, 1] < 90) & (p[:, :, 2] < 90)
    cm = ((mx - mn) > 60) & (mx > 90) & ~red
    ys, xs = np.nonzero(cm)
    t = jet_t(p[ys, xs])
    hist, _ = np.histogram(t, bins=16, range=(0, 1))
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
    print(f"{nm}: colored%={100.0*cm.mean():.1f} hist16={list(map(int, hist))} "
          f"diag mean={np.nanmean(td):.3f} std={np.nanstd(td):.3f}")

print("\n=== C3b: TR surface (the crop content) x616-879 y115-317 ===")
for nm, A, V in IMGS:
    M = masks(A)
    sub = M["colored"][TY0:TY1, TX0:TX1]
    if V is not None:
        sub = sub & V[TY0:TY1, TX0:TX1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        print(f"{nm}: no colored px in TR"); continue
    t = jet_t(A[TY0:TY1, TX0:TX1][ys, xs])
    hist, _ = np.histogram(t, bins=16, range=(0, 1))
    bx0, bx1, by0, by1 = xs.min() + TX0, xs.max() + TX0, ys.min() + TY0, ys.max() + TY0
    print(f"{nm}: TR colored%={100.0*sub.mean():.1f} surf bbox x{bx0}..{bx1} y{by0}..{by1} (w={bx1-bx0+1} h={by1-by0+1}) hist16={list(map(int, hist))}")

print("\n=== C4: grid/wall gray ink ===")
for nm, A, V in IMGS:
    M = masks(A)
    tr = M["gray"][TY0:TY1, TX0:TX1]
    cr = M["gray"][160:369, 592:897]
    if V is not None:
        tr = tr & V[TY0:TY1, TX0:TX1]
        cr = cr & V[160:369, 592:897]
    br = M["gray"][BY0:BY1, BX0:BX1]
    if V is not None:
        br = br & V[BY0:BY1, BX0:BX1]
    print(f"{nm}: gray px TR={int(tr.sum())} crop-region={int(cr.sum())} BR={int(br.sum())}")

print("\n=== C5: red diagonal (652,189)->(667,165) in TR + red totals ===")
x1, y1, x2, y2 = 652.0, 189.0, 667.0, 165.0
L2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
for tol in (2.0, 3.0):
    print(f"-- tolerance {tol}px --")
    for nm, A, V in IMGS:
        M = masks(A)
        yy, xx = np.mgrid[TY0:TY1, TX0:TX1]
        t = np.clip(((xx - x1) * (x2 - x1) + (yy - y1) * (y2 - y1)) / L2, 0, 1)
        dist = np.hypot(xx - (x1 + t * (x2 - x1)), yy - (y1 + t * (y2 - y1)))
        near = dist <= tol
        red_tr = M["red"][TY0:TY1, TX0:TX1]
        if V is not None:
            red_tr = red_tr & V[TY0:TY1, TX0:TX1]
            near = near & V[TY0:TY1, TX0:TX1]
        n_diag = int((red_tr & near).sum())
        print(f"{nm}: red within {tol}px of segment = {n_diag}; total red TR={int(red_tr.sum())}", end="")
        red_br = M["red"][BY0:BY1, BX0:BX1]
        if V is not None:
            red_br = red_br & V[BY0:BY1, BX0:BX1]
        print(f"; red BR={int(red_br.sum())}")

print("\n=== C6: TR white-above-surface (3D box leaves bg above silhouette) ===")
for nm, A, V in IMGS:
    M = masks(A)
    col = M["colored"][TY0:TY1, TX0:TX1]
    if V is not None:
        col = col & V[TY0:TY1, TX0:TX1]
    ys, xs = np.nonzero(col)
    by0 = ys.min()
    top = M["white"][TY0:TY0 + max(1, by0), TX0:TX1]
    if V is not None:
        top = top & V[TY0:TY0 + max(1, by0), TX0:TX1]
    print(f"{nm}: TR surf top y={by0 + TY0}, white px above top in box={int(top.sum())}, white in whole box={int((M['white'][TY0:TY1, TX0:TX1] & (V[TY0:TY1, TX0:TX1] if V is not None else True)).sum())}")

print("\nPROBE2_DONE")
