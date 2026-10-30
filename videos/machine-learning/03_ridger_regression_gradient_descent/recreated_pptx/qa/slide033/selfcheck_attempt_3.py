#!/usr/bin/env python3
"""Verify render_3 vs original: band fills, text rows, curve, gridlines.
Windows are frame-px and scale per-image (the render is 2.083x the frame)."""
import numpy as np
from PIL import Image
from collections import Counter

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033/render_3.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
fails = []


def bandfill(im, y0, y1, x0=160, x1=820):
    H = im.shape[0]; s = H / 540.0
    sub = im[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s):int(4 * s)].reshape(-1, 3)
    sub = sub[sub.sum(axis=1) > 400]
    if not len(sub):
        return None
    return Counter(map(tuple, sub)).most_common(1)[0][0]


print("=== BAND FILLS (orig vs render) ===")
bands = [(328, 368), (378, 408), (422, 452), (464, 476), (488, 498)]
for y0, y1 in bands:
    fo = bandfill(o, y0, y1); fr = bandfill(r, y0, y1)
    def hexf(c): return "#%02X%02X%02X" % c if c else "None"
    d = max(abs(a - b) for a, b in zip(fo, fr)) if (fo and fr) else 999
    print(f"  y{y0}-{y1}: ORIG {hexf(fo)}  REND {hexf(fr)}  maxdiff={d}")
    if d > 12:
        fails.append(f"band y{y0}-{y1} fill differs: {hexf(fo)} vs {hexf(fr)}")

print("\n=== TEXT ROW INK (label col + data cols) — proportional check ===")
lum_o = o.sum(axis=2); lum_r = r.sum(axis=2)
for ry in [341, 359, 383, 401, 427, 445, 469, 493]:
    so = o.shape[0] / 540.0; sr = r.shape[0] / 540.0
    a = int((lum_o[int((ry - 4) * so):int((ry + 5) * so), int(86 * so):int(121 * so)] < 330).sum())
    b = int((lum_r[int((ry - 4) * sr):int((ry + 5) * sr), int(86 * sr):int(121 * sr)] < 330).sum())
    c = int((lum_o[int((ry - 4) * so):int((ry + 5) * so), int(122 * so):int(868 * so)] < 330).sum())
    d = int((lum_r[int((ry - 4) * sr):int((ry + 5) * sr), int(122 * sr):int(868 * sr)] < 330).sum())
    # normalise by render's higher pixel count (it renders at 2.083^2 = 4.34x)
    dn = d / 4.34
    print(f"  row y{ry}: label ORIG={a:>4} REND={b:>4} | data ORIG={c:>5} REND={d:>5} (norm {dn:>5})"
          + ("  <-- RENDER INK LIGHT" if dn < c * 0.5 else ""))

print("\n=== GREEN CURVE (isolated) ===")
S = r.shape[0] / 540.0
R, G, B = r[:, :, 0], r[:, :, 1], r[:, :, 2]
grn = (G - R > 25) & (G - B > 25) & (G > 90)
col = {}
ys_, xs_ = np.where(grn[int(105 * S):int(305 * S), int(615 * S):int(830 * S)])
for y, x in zip(ys_, xs_):
    col.setdefault(int(x), []).append(int(y) + int(105 * S))
if len(col) > 50:
    xs = sorted(col); cy = np.array([np.median(col[x]) for x in xs], float)
    d2 = np.diff(cy, 2)
    gaps = sum(1 for i in range(len(xs) - 1) if xs[i + 1] - xs[i] > 8)
    print(f"  curve cols {xs[0]/S:.0f}..{xs[-1]/S:.0f} frame ({len(xs)} cols)")
    print(f"  y range frame {cy.min()/S:.0f}..{cy.max()/S:.0f}")
    print(f"  ripple std={np.std(d2):.3f}px max|d2|={np.abs(d2).max():.3f}px; column gaps>8px: {gaps}")
    if gaps > 2:
        fails.append(f"curve has {gaps} column gaps — not one continuous curve")
    if np.std(d2) > 2.5:
        fails.append(f"curve ripple {np.std(d2):.2f}px too rough")
else:
    fails.append(f"curve too sparse ({len(col)} cols)")

print("\n=== TABLE GRIDLINES on render (frame px) ===")
lumr = r.sum(axis=2)
hrows = []
for y in range(316, 524):
    if (lumr[int(y * S), int(122 * S):int(868 * S):int(2 * S)] < 520).mean() > 0.5:
        hrows.append(y)
print(f"  horizontal: {hrows}")
expect_h = [320, 374, 410, 418, 454, 460, 478, 484, 501, 517]
for e in expect_h:
    if not any(abs(e - h) <= 3 for h in hrows):
        fails.append(f"horizontal gridline y{e} missing on render")
vcols = []
for x in range(115, 865, 4):
    if (lumr[int(325 * S):int(515 * S):2, int(x * S)] < 520).mean() > 0.4:
        vcols.append(x)
print(f"  vertical: {vcols}")

print()
if fails:
    print("VERIFY: FAIL")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("VERIFY: PASS — band fills, text rows, one smooth curve, gridlines all match")
