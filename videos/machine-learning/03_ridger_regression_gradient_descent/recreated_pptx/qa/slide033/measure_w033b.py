#!/usr/bin/env python3
"""Focused PIL follow-up for slide 033: curve colour/shape, panel colour,
text-ink census, and the (500,60) anomaly."""
import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(f"{DECK}/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide033/render_8.png").convert("RGB")).astype(int)
SX, SY = 2001 / 960, 1125 / 540


def rm_(y0, y1, x0, x1):
    return rend[int(y0 * SY):int(y1 * SY), int(x0 * SX):int(x1 * SX)]


print("=" * 72)
print("PANEL COLOUR SAMPLES (ORIG vs REND) — house panel expected E9E9E7=(233,233,231)")
print("=" * 72)
for (y, x, what) in [(100, 930, "panel right of plot"), (200, 70, "panel left col"),
                     (500, 60, "panel below table-left"), (520, 500, "panel bottom centre"),
                     (470, 890, "panel right-bottom"), (60, 500, "panel top of plot"),
                     (318, 500, "above table"), (340, 700, "in band1"), (480, 700, "next-x band")]:
    o, r = orig[y, x], rm_(y, y + 1, x, x + 1)[0, 0]
    print(f"  ({y:3d},{x:3d}) {what:24s} ORIG {tuple(o)}  REND {tuple(r)}")

print()
print("=" * 72)
print("ORIGINAL PLOT: what colours live inside the plot box x608..843 y62..311?")
print("=" * 72)
pb = orig[63:311, 610:842].reshape(-1, 3)
q = np.percentile(pb, list(range(0, 101, 10)), axis=0)
print("decile-min/max per channel (R):", [int(v) for v in q[0]], "...", [int(v) for v in q[-1]])
# the curve is the most-saturated teal-ish ink: find its colour by mode of "not gray/white/black"
mx, mn = pb.max(axis=1), pb.min(axis=1)
sat = mx - mn
sel = pb[(sat > 30) & (mx > 60) & (mx < 250)]
if len(sel):
    print(f"saturated pixels in plot box: {len(sel)}; their median RGB {tuple(int(v) for v in np.median(sel,axis=0))}")
    # cluster by rounded colour
    rnd = (sel // 16 * 16)
    vals, counts = np.unique(rnd, axis=0, return_counts=True)
    order = np.argsort(-counts)[:8]
    for i in order:
        print(f"   colour ~{tuple(vals[i])}  count {counts[i]}")

print()
print("=" * 72)
print("CURVE EXTRACTION — ORIG (frame) vs RENDER (frame-mapped)")
print("=" * 72)


def curve_cols(img, x0, x1, y0, y1, mask_fn, yscale=1.0, xscale=1.0):
    sub = img[int(y0 * yscale):int(y1 * yscale), int(x0 * xscale):int(x1 * xscale)]
    m = mask_fn(sub)
    cols, rows = [], []
    for j in range(sub.shape[1]):
        idx = np.flatnonzero(m[:, j])
        if len(idx):
            cols.append(j / xscale + x0)
            rows.append(idx.mean() / yscale + y0)
    return np.array(cols, float), np.array(rows, float)


def teal_mask(sub):
    """teal: G,B high and close, R clearly lower, strongly saturated."""
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    return (G > 110) & (B > 110) & (R < G - 45) & (abs(G - B) < 70)


cxo, cyo = curve_cols(orig, 610, 843, 62, 311, teal_mask, 1.0, 1.0)
cxr, cyr = curve_cols(rend, 610, 843, 62, 311, teal_mask, SY, SX)
print(f"ORIG teal columns: {len(cxo)}  x-range {cxo.min():.0f}..{cxo.max():.0f}" if len(cxo) else "ORIG: none")
print(f"REND teal columns: {len(cxr)}  x-range {cxr.min():.0f}..{cxr.max():.0f}" if len(cxr) else "REND: none")


def ripple(cx, cy, name):
    if len(cx) < 12:
        print(f"{name}: too few columns")
        return
    # restrict to contiguous span
    d2 = cy[2:] - 2 * cy[1:-1] + cy[:-2]
    print(f"{name}: cols {len(cx)}, gaps>3px={int(np.sum(np.diff(cx) > 3))}, "
          f"ripple std(d2)={d2.std():.3f} frame-px, max|d2|={np.abs(d2).max():.2f}")
    tp = [(round(cx[i], 1), round(cy[i], 1)) for i in range(1, len(cy) - 1)
          if (cy[i] - cy[i - 1]) * (cy[i + 1] - cy[i]) < 0]
    # compress near-duplicate turning points
    comp = []
    for t in tp:
        if comp and abs(t[0] - comp[-1][0]) < 3:
            comp[-1] = (t[0], min(comp[-1][1], t[1]))
        else:
            comp.append(t)
    print(f"   turning points (x,y): {comp}")


if len(cxo):
    ripple(cxo, cyo, "ORIG")
if len(cxr):
    ripple(cxr, cyr, "REND")
if len(cxo) and len(cxr):
    lo, hi = max(cxo.min(), cxr.min()), min(cxo.max(), cxr.max())
    if hi - lo > 20:
        go = np.interp(np.arange(lo, hi, 1), cxo, cyo)
        gr = np.interp(np.arange(lo, hi, 1), cxr, cyr)
        res = go - gr
        print(f"residual ORIG-vs-REND over x{lo:.0f}..{hi:.0f}: median {np.median(res):+.2f}px, "
              f"std {res.std():.2f}px, max|.| {np.abs(res).max():.2f}px")

print()
print("=" * 72)
print("TEXT INK CENSUS (red / blue / dark masks, frame px)")
print("=" * 72)


def ink(img, y0, y1, x0, x1, mask, ysc=1.0, xsc=1.0):
    s = img[int(y0 * ysc):int(y1 * ysc), int(x0 * xsc):int(x1 * xsc)]
    return int(mask(s).sum())


RED = lambda s: (s[:, :, 0] > 150) & (s[:, :, 1] < 100) & (s[:, :, 2] < 100)
BLUE = lambda s: (s[:, :, 2] > 120) & (s[:, :, 2] > s[:, :, 0] + 40) & (s[:, :, 1] < 120)
DARK = lambda s: s.max(axis=2) < 120
regions = {
    "title x100-530 y60-90": (60, 90, 100, 530),
    "sub1 x110-530 y92-112": (92, 112, 110, 530),
    "sub2 x180-470 y115-140": (115, 140, 180, 470),
    "eq x449-585 y182-230": (182, 230, 449, 585),
    "annot x246-597 y254-299": (254, 299, 246, 597),
    "table x86-869 y320-519": (320, 519, 86, 869),
}
for n, (y0, y1, x0, x1) in regions.items():
    print(f"{n}")
    for mnn, m in (("RED", RED), ("BLUE", BLUE), ("DARK", DARK)):
        o = ink(orig, y0, y1, x0, x1, m)
        r = ink(rend, y0, y1, x0, x1, m, SY, SX)
        print(f"   {mnn:5s} orig {o:7d}  rend {r:7d}  ratio {r/max(o,1):5.2f}")
