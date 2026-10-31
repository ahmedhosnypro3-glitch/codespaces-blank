#!/usr/bin/env python3
"""Claim-targeted PIL probe for crop_dense_judge_k15b.txt (06:40 FAIL) vs the
on-disk crop pair (md5-verified == the k15b leg pair).

Crop pair: crop_dense_render.png / crop_dense_orig.png, 634x434, cut from
slide-space region x592-896 y160-368 at render scale 2001/960 = 2.0844.
Inverse map: slide_x = crop_x/2.0844 + 592 ; slide_y = crop_y/2.0844 + 160.
Region = TR (Convex) plot box, slide-space x616-879 y115-317 (per probe_fresh025_k15claims.py).
"""
import numpy as np
from PIL import Image
import hashlib

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide025"
SC = 2001 / 960.0
OX, OY = 592, 160

def load(f):
    p = f"{D}/{f}"
    return p, hashlib.md5(open(p, "rb").read()).hexdigest(), np.asarray(Image.open(p).convert("RGB")).astype(int)

pr, mr, R = load("crop_dense_render.png")
po, mo, O = load("crop_dense_orig.png")
print(f"crop_dense_render.png md5={mr}  crop_dense_orig.png md5={mo}")
H, W = R.shape[:2]
print(f"crop size {W}x{H}, scale {SC:.4f}, origin slide ({OX},{OY})")

def slide2crop(x, y):
    return (x - OX) * SC, (y - OY) * SC

# TR plot box in slide space -> crop space
bx0, by0 = slide2crop(616, 115)
bx1, by1 = slide2crop(879, 317)
print(f"TR box in crop coords: x{max(0,bx0):.0f}-{min(W,bx1):.0f} y{max(0,by0):.0f}-{min(H,by1):.0f}")

def masks(A):
    r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    mx = A.max(axis=2); mn = A.min(axis=2)
    sat = mx - mn
    dark = A.sum(axis=2) < 330
    white = (r > 240) & (g > 240) & (b > 240)
    gray = (sat < 24) & (mx > 120) & (mx < 235)          # mesh/grid/panel gray
    red = (r > 120) & (g < 110) & (b < 110) & (sat > 60)
    colored = (sat > 45) & ~red & ~dark                    # surface fill
    return dict(dark=dark, white=white, gray=gray, red=red, colored=colored, sat=sat, mx=mx)

MR, MO = masks(R), masks(O)

# locate plot content bbox (non-white, non-panel-bg) per image
def content_bbox(A, M):
    bg = (np.abs(A[:,:,0]-233)<14)&(np.abs(A[:,:,1]-233)<14)&(np.abs(A[:,:,2]-231)<14)
    m = ~M["white"] & ~bg
    ys, xs = np.where(m)
    return xs.min(), ys.min(), xs.max(), ys.max(), int(m.sum())

for nm, A, M in (("render", R, MR), ("orig", O, MO)):
    x0, y0, x1, y1, n = content_bbox(A, M)
    print(f"content bbox {nm}: x{x0}-{x1} y{y0}-{y1} px={n} "
          f"(slide x{x0/SC+OX:.0f}-{x1/SC+OX:.0f} y{y0/SC+OY:.0f}-{y1/SC+OY:.0f})")

# plot interior = TR box clipped to crop
ix0, iy0 = int(max(0, bx0)), int(max(0, by0))
ix1, iy1 = int(min(W, bx1)), int(min(H, by1))
interior = (slice(iy0, iy1), slice(ix0, ix1))
print(f"interior slice x{ix0}-{ix1} y{iy0}-{iy1}")

print("\n=== C1/C4: surface fill share + hue histogram of colored px in interior ===")
def hue_bins(A, m):
    A = A[interior]
    r, g, b = A[:, :, 0][m], A[:, :, 1][m], A[:, :, 2][m]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    sat = mx - mn
    out = {}
    red = (mx == r) & (sat > 60)
    yel = (mx == r) & (g > b + 30) & (sat > 60)
    grn = (g >= r) & (g >= b) & (sat > 60)
    cyn = (g > r + 20) & (b > r + 20) & (sat > 60)
    blu = (b > r + 30) & (b > g + 10)
    for nm2, mm in (("red", red), ("yellow/orange", yel), ("green", grn), ("cyan", cyn), ("blue", blu)):
        out[nm2] = int(mm.sum())
    out["total_colored"] = int(m.sum())
    return out

for nm, M in (("render", MR), ("orig", MO)):
    tot = int((~M["white"])[interior].sum())
    col = M["colored"][interior]
    hb = hue_bins(R if nm == "render" else O, col)
    print(f"{nm}: colored% of interior = {100.0*hb['total_colored']/tot:.1f}%  hue: " +
          " ".join(f"{k}={v} ({100.0*v/max(1,hb['total_colored']):.0f}%)" for k, v in hb.items()))

print("\n=== C1b: 3D-ness proxies in interior ===")
for nm, A, M in (("render", R, MR), ("orig", O, MO)):
    col = M["colored"][interior]
    lum = (0.299*A[:,:,0] + 0.587*A[:,:,1] + 0.114*A[:,:,2])[interior]
    # vertical brightness profile of colored px per row (shading => large row-to-row delta)
    prof = []
    sub = lum.copy(); sub[~col] = np.nan
    for i in range(sub.shape[0]):
        v = sub[i][~np.isnan(sub[i])]
        prof.append(np.nanmean(v) if len(v) else np.nan)
    prof = np.array(prof)
    d = np.abs(np.diff(prof))
    d = d[~np.isnan(d)]
    top_band = (slice(iy0, iy0 + max(1, (iy1 - iy0) // 3)), slice(ix0, ix1))
    white_above = int(M["white"][top_band].sum())
    gray_in = int(M["gray"][interior].sum())
    print(f"{nm}: colored-row lum mean={np.nanmean(prof):.1f} row-delta mean={np.nanmean(d):.2f} max={np.nanmax(d):.1f} "
          f"white-in-top-third={white_above} graymesh-in-interior={gray_in}")

print("\n=== C2: z-axis vertical line + tick/label ink at left of TR box ===")
# left strip: crop x from ix0 to ix0+70 (slide x616-650), full interior height
for nm, M in (("render", MR), ("orig", MO)):
    strip = M["dark"][iy0:iy1, ix0:ix0+70]
    rows = strip.sum(axis=1)
    # tick rows: rows with >=3 dark px
    ticks = np.where(rows >= 3)[0] + iy0
    # cluster tick rows
    cl = []
    for t in ticks:
        if cl and t - cl[-1][-1] <= 2: cl[-1].append(t)
        else: cl.append([t])
    print(f"{nm}: z-strip dark px={int(strip.sum())} tick-rows clusters={len(cl)} at y={[ (c[0],c[-1]) for c in cl ][:12]}")
    # vertical axis line: column with most dark px
    cols = strip.sum(axis=0)
    if cols.max() > 0:
        c = int(cols.argmax())
        print(f"   strongest vertical line at strip-x {c} (slide x{(ix0+c)/SC+OX:.1f}) with {int(cols.max())} dark px of {iy1-iy0} rows")

print("\n=== C3: bottom axis-label strip (slide y295-317 -> crop) ===")
cy0, cy1 = slide2crop(590, 295)[1], slide2crop(590, 320)[1]
for nm, M in (("render", MR), ("orig", MO)):
    strip = M["dark"][int(max(0,cy0)):int(min(H,cy1)), ix0:ix1]
    cols = strip.sum(axis=0)
    # text clusters along x
    on = cols >= 2
    cl = []
    st = None
    for i, v in enumerate(on):
        if v and st is None: st = i
        elif not v and st is not None:
            if i - st >= 2: cl.append((st + ix0, i + ix0))
            st = None
    if st is not None: cl.append((st + ix0, len(on) + ix0))
    print(f"{nm}: bottom-strip dark px={int(strip.sum())} label clusters={len(cl)} at x={[(a,b) for a,b in cl][:12]}")

print("\n=== C5: grid/wall gray ink (whole crop + above-surface band) ===")
for nm, M in (("render", MR), ("orig", MO)):
    g = M["gray"]
    print(f"{nm}: gray px whole crop={int(g.sum())} ({100.0*g.sum()/(W*H):.1f}%) interior={int(g[interior].sum())} "
          f"top band y0-{iy0+40}={int(g[:max(1,iy0+40), :].sum())}")

print("\n=== C6: red stroke pixels + orientation ===")
for nm, M in (("render", MR), ("orig", MO)):
    red = M["red"]
    ys, xs = np.where(red)
    n = len(xs)
    print(f"{nm}: red px={n} ({100.0*n/(W*H):.2f}%)", end="")
    if n > 20:
        P = np.stack([xs, ys], 1).astype(float)
        P -= P.mean(0)
        cov = np.cov(P.T)
        w, v = np.linalg.eigh(cov)
        ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
        elong = np.sqrt(w[1] / max(1e-9, w[0]))
        print(f" principal angle={ang:.1f}deg elongation={elong:.1f} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}")
        # diagonal test: fraction of red px far from horizontal lines (row-wise spread)
        rows = np.bincount(ys, minlength=H)
        print(f"   rows containing red: {int((rows>0).sum())} of {H}; max red in one row={int(rows.max())}")
    else:
        print()

print("\n=== C2b: stray numeral check — dark ink in upper-left of crop (slide x592-660, y160-200) ===")
for nm, M in (("render", MR), ("orig", MO)):
    sub = M["dark"][0:83, 0:150]  # crop y0-83 = slide y160-200, x0-150 = slide x592-664
    ys, xs = np.where(sub)
    print(f"{nm}: upper-left dark px={int(sub.sum())}", end="")
    if len(xs):
        print(f" bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} (slide x{xs.min()/SC+OX:.0f}-{xs.max()/SC+OX:.0f} y{ys.min()/SC+OY:.0f}-{ys.max()/SC+OY:.0f})")
    else:
        print()
