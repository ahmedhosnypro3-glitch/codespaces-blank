#!/usr/bin/env python3
"""Adjudication probe v3 — addendum: TR z-axis at x646-648 (where orig's vline
actually is), tick-label strip left of it, stray-numeral zone, BR vline at
x731-738 over BR rows, red components in TR, fair BR-sliver red comparison."""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide025"

orig = np.asarray(Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
r15 = np.asarray(Image.open(f"{D}/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int32)
SC = 1125 / 540.0
OX, OY, CW, CH = 592, 160, 304, 208
r16 = np.zeros_like(orig)
r16[OY:OY + CH, OX:OX + CW] = np.asarray(
    Image.open(f"{D}/crop_dense_render_k16.png").convert("RGB").resize((CW, CH), Image.LANCZOS)).astype(np.int32)
VALID16 = np.zeros((540, 960), bool)
VALID16[OY:OY + CH, OX:OX + CW] = True

IMGS = [("orig", orig, None), ("render_k15b", r15, None), ("render_k16", r16, VALID16)]

TX0, TY0, TX1, TY1 = 616, 115, 880, 318
BX0, BY0, BX1, BY1 = 615, 344, 881, 532


def masks(A):
    r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    mx, mn = A.max(2), A.min(2)
    sat = mx - mn
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    red = (r > 140) & (r - g > 60) & (r - b > 60)
    dark = (lum < 110) & (sat < 90) & ~red
    gray = (lum > 120) & (lum < 215) & (sat < 24) & ~red
    return dict(red=red, dark=dark, gray=gray)


def longest_run(col):
    best = cur = 0
    for v in col:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


print("=== A: TR z-vline at x644-650, y120-315 (orig strongest col was x646-648) ===")
for nm, A, V in IMGS:
    M = masks(A)
    line = (M["dark"] | M["gray"])[120:316, 644:651]
    if V is not None:
        line &= V[120:316, 644:651]
    colc = line.sum(0)
    runs = [longest_run(line[:, c]) for c in range(7)]
    print(f"{nm}: x644-650 px={int(line.sum())} per-col={list(map(int, colc))} runs={runs}")

print("\n=== B: z-tick LABEL strip left of vline, x600-643 y120-315 (dark ink) ===")
for nm, A, V in IMGS:
    M = masks(A)
    strip = M["dark"][120:316, 600:644]
    if V is not None:
        strip &= V[120:316, 600:644]
    rows = strip.sum(1)
    on = rows >= 2
    clusters = []
    st = None
    for i, v in enumerate(on):
        if v and st is None:
            st = i
        elif not v and st is not None:
            if i - st >= 3:
                clusters.append((120 + st, 120 + i))
            st = None
    if st is not None:
        clusters.append((120 + st, 316))
    print(f"{nm}: dark px={int(strip.sum())} label-row clusters={len(clusters)} at y={clusters}")

print("\n=== C: stray-numeral zone upper-left of crop (slide x592-664 y160-200), dark ink ===")
for nm, A, V in IMGS:
    M = masks(A)
    sub = M["dark"][160:201, 592:665]
    if V is not None:
        sub &= V[160:201, 592:665]
    ys, xs = np.nonzero(sub)
    bbox = f"x{xs.min()+592}-{xs.max()+592} y{ys.min()+160}-{ys.max()+160}" if len(xs) else "none"
    print(f"{nm}: dark px={int(sub.sum())} bbox {bbox}")

print("\n=== D: BR z-vline at x731-738 over BR rows y350-525 ===")
for nm, A, V in IMGS:
    if nm == "render_k16":
        print(f"{nm}: BR rows y350-525 outside k16 crop (ends y368) — skip")
        continue
    M = masks(A)
    line = (M["dark"] | M["gray"])[350:526, 731:739]
    colc = line.sum(0)
    runs = [longest_run(line[:, c]) for c in range(8)]
    print(f"{nm}: x731-738 px={int(line.sum())} per-col={list(map(int, colc))} runs={runs}")
    # also scan whole BR box for strongest column
    line2 = (M["dark"] | M["gray"])[BY0 + 8:BY1 - 8, BX0 + 8:BX1 - 8]
    colc2 = line2.sum(0)
    order = np.argsort(-colc2)[:5]
    print(f"   BR-box top cols: {[(int(BX0 + 8 + c), int(colc2[c]), longest_run(line2[:, c])) for c in order if colc2[c] > 0]}")

print("\n=== E: red components in TR box x616-879 y115-317 (area>=15) ===")
for nm, A, V in IMGS:
    M = masks(A)
    red = M["red"][TY0:TY1, TX0:TX1].copy()
    if V is not None:
        red &= V[TY0:TY1, TX0:TX1]
    lab, n = ndimage.label(red, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 15:
            continue
        if len(xs) > 3 and xs.max() > xs.min():
            slope = np.polyfit(xs, ys, 1)[0]
        else:
            slope = float("inf")
        comps.append((len(xs), xs.min() + TX0, ys.min() + TY0, xs.max() + TX0, ys.max() + TY0, round(float(slope), 2)))
    comps.sort(key=lambda c: -c[0])
    print(f"{nm}: {len(comps)} comps (area, x0,y0,x1,y1, slope):")
    for c in comps[:10]:
        print(f"   area={c[0]} slide x{c[1]}..{c[3]} y{c[2]}..{c[4]} slope={c[5]}")

print("\n=== F: red in BR — full box (orig/k15b) vs fair sliver y344-368 (all) ===")
for nm, A, V in IMGS:
    M = masks(A)
    red_full = M["red"][BY0:BY1, BX0:BX1]
    red_sl = M["red"][BY0:369, BX0:BX1]
    if V is not None:
        red_full &= V[BY0:BY1, BX0:BX1]
        red_sl &= V[BY0:369, BX0:BX1]
    print(f"{nm}: red BR full={int(red_full.sum())}  red BR sliver y344-368={int(red_sl.sum())}")

print("\nPROBE3_DONE")
