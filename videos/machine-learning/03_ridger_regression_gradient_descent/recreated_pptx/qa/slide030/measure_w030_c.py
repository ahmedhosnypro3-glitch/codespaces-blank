#!/usr/bin/env python3
"""Slide 030 focused PIL checks for the two crops whose colour-class masks are
contaminated by neighbouring fills (worker w030-finish-20261024c).

1. ARROW (frame px box 150..215 x 285..355): the red block arrow points down at
   the iteration table, but the table's pink fill bleeds into the same box. The
   arrow ink is isolated by (a) splitting saturated red strokes from pale pink
   fill and (b) dropping rows dominated by the fill.
2. CALLOUT (frame px box 320..585 x 280..332): purple band with a text line.
   Reports the colour census and locates the text pixels in each image.
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide030"

rend = Image.open(f"{Q}/render_6.png").convert("RGB")
orig = Image.open(f"{V}/unique_slides/slide_030.jpg").convert("RGB")
RW, RH = rend.size
SXR, SYR = RW / 960.0, RH / 540.0
rend_a = np.asarray(rend).astype(int)
orig_a = np.asarray(orig).astype(int)


def crop_px(box, sx, sy, W, H):
    x0, y0, x1, y1 = box
    return (int(round(x0 * sx)), int(round(y0 * sy)),
            min(int(round(x1 * sx)), W), min(int(round(y1 * sy)), H))


def redish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - g > 60) & (r - b > 40) & (r > 110)


def pinkish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 200) & (r - g > 18) & (r - b > 18) & (g > 150) & (b > 150)


print("== 1. ARROW (box 150..215 x 285..355 frame px) ==")
BOX = (150, 285, 215, 355)
for label, im, sx, sy, W, H in (("render", rend_a, SXR, SYR, RW, RH),
                               ("orig", orig_a, 1.0, 1.0, 960, 540)):
    X0, Y0, X1, Y1 = crop_px(BOX, sx, sy, W, H)
    sub = im[Y0:Y1, X0:X1]
    rm, pm = redish(sub), pinkish(sub)
    print(f"  -- {label}: box px {X0},{Y0}..{X1},{Y1}  red px={int(rm.sum())}  pink px={int(pm.sum())}")
    rows = []
    for i in range(sub.shape[0]):
        rows.append((round((Y0 + i) / sy, 1), int(rm[i].sum()), int(pm[i].sum())))
    # rows where pink dominates the row width -> table fill, excluded
    keep = [t for t in rows if t[2] < 0.25 * (X1 - X0)]
    dropped = [t for t in rows if t[2] >= 0.25 * (X1 - X0)]
    if dropped:
        print(f"     fill-dominated rows dropped: y={dropped[0][0]}..{dropped[-1][0]} "
              f"({len(dropped)} rows)")
    if keep:
        ys = [t[0] for t in keep]
        print(f"     arrow rows kept: y={ys[0]}..{ys[-1]}")
    # arrow ink bbox from kept rows only
    mask = rm.copy()
    for i, t in enumerate(rows):
        if t[2] >= 0.25 * (X1 - X0):
            mask[i, :] = False
    ys_i, xs_i = np.where(mask)
    if len(xs_i):
        bx = (round((xs_i.min() + X0) / sx, 1), round((ys_i.min() + Y0) / sy, 1),
              round((xs_i.max() + X0) / sx, 1), round((ys_i.max() + Y0) / sy, 1))
        area = len(xs_i) / (sx * sy)
        # principal axis (tilt) of the arrow ink
        cx, cy = xs_i.mean(), ys_i.mean()
        cov = np.cov(np.vstack([xs_i - cx, ys_i - cy]))
        w_, v_ = np.linalg.eigh(cov)
        vec = v_[:, np.argmax(w_)]
        ang = np.degrees(np.arctan2(vec[1], vec[0]))
        if ang < 0:
            ang += 180
        print(f"     arrow ink bbox(frame px)={bx}  area={area:.1f} px  centroid="
              f"({(cx+X0)/sx:.1f},{(cy+Y0)/sy:.1f})  major-axis angle={ang:.1f} deg")
        # width profile: ink width per row
        prof = []
        for i in range(sub.shape[0]):
            n = int(mask[i].sum())
            if n:
                prof.append((round((Y0 + i) / sy, 1), round(n / sx, 1)))
        print("     width profile (frame y: width px): " +
              " ".join(f"{y}:{w}" for y, w in prof))

print("\n== 2. CALLOUT (box 320..585 x 280..332 frame px) ==")
BOX2 = (320, 280, 585, 332)
for label, im, sx, sy, W, H in (("render", rend_a, SXR, SYR, RW, RH),
                                ("orig", orig_a, 1.0, 1.0, 960, 540)):
    X0, Y0, X1, Y1 = crop_px(BOX2, sx, sy, W, H)
    sub = im[Y0:Y1, X0:X1]
    flat = sub.reshape(-1, 3)
    print(f"  -- {label}: {sub.shape[1]}x{sub.shape[0]} px")
    # 4-bit-per-channel colour census
    q = (flat // 32)
    keys, counts = np.unique(q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2], return_counts=True)
    order = np.argsort(-counts)[:8]
    for k in order:
        r = (k // 64) * 32, ((k // 8) % 8) * 32, (k % 8) * 32
        print(f"     bin rgb~{r}  n={counts[k]}")
    # purple band detection
    r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    purple = (r - g > 25) & (b - g > 25) & (b > 120)
    rows = np.where(purple.sum(axis=1) > 0.5 * sub.shape[1])[0]
    if len(rows):
        y_lo, y_hi = (Y0 + rows.min()) / sy, (Y0 + rows.max()) / sy
        band = purple[Y0 and 0 or 0:]
        print(f"     purple band rows frame y={y_lo:.1f}..{y_hi:.1f} "
              f"(height {y_hi-y_lo:.1f} frame px)")
        bandmask = np.zeros_like(purple)
        bandmask[rows.min():rows.max() + 1, :] = True
        inside = purple & bandmask
        # text pixels: inside the band rows, NOT purple, and not background gray
        bg = (np.abs(r - 233) < 8) & (np.abs(g - 233) < 8) & (np.abs(b - 231) < 8)
        text = bandmask & ~purple & ~bg
        ys_i, xs_i = np.where(text)
        if len(xs_i):
            tb = (round((xs_i.min() + X0) / sx, 1), round((ys_i.min() + Y0) / sy, 1),
                  round((xs_i.max() + X0) / sx, 1), round((ys_i.max() + Y0) / sy, 1))
            med = np.median(sub[text], axis=0)
            print(f"     text-like pixels inside band: n={len(xs_i)} bbox={tb} "
                  f"median rgb={med.astype(int)}")
        else:
            print("     text-like pixels inside band: none")
    else:
        print("     no purple band rows >50% width")

print("\nFOCUSED CHECKS DONE")
