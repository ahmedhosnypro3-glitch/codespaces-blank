#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_028.jpg (960x540, 1px = 1pt = 1/72in).

Masks (from analysis/slide_028_final.json + deck chrome):
  title/axes red  FF0000 | curve/dots blue 2E75B6 | border 1F4E79
  black text 000000 | gray panel E9E9E7 | badge FDFD96 / ring 6A5ACD
  house strokes C00000 (JPEG-darkened maroon cores per house_chrome.js notes)

Dumps per-element ink bboxes + stats to guide the build. Nothing is edited here.
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
print(f"size {W}x{H}")
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]


def bbox_of(mask, label, limit=None):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{label}: NONE")
        return None
    if limit is not None:
        ys, xs = ys[ys < limit[0]], xs[ys < limit[0]] if False else (ys, xs)
    print(f"{label}: x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}  n={len(ys)} "
          f"cx={(xs.min()+xs.max())/2:.1f} cy={(ys.min()+ys.max())/2:.1f}")
    return xs.min(), xs.max(), ys.min(), ys.max()


# ---- pure red (title + axis arrows), excluding house stroke C00000-ish ----
# pure FF0000 has g,b near 0 and r>200; house C00000 core is r~110-130 on JPEG
pure_red = (r > 200) & (g < 90) & (b < 90)
print("== PURE RED (FF0000-family) ==")
tr = bbox_of(pure_red, "all pure red")
# per-row profile of pure red to separate title band vs arrows
rows = np.where(pure_red.any(axis=1))[0]
if len(rows):
    # find contiguous row bands
    bands = []
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y > p + 4:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for (y0, y1) in bands:
        m = pure_red[y0:y1 + 1]
        xs = np.where(m.any(axis=0))[0]
        n = m.sum()
        print(f"  red band y {y0}-{y1}: x {xs.min()}-{xs.max()} n={n}")

# ---- dark blue border 1F4E79 (thin frame around both panels) ----
print("== DARK BLUE 1F4E79-family border ==")
darkblue = (b > 90) & (b - r > 50) & (b - g > 30) & (r < 90)
db = bbox_of(darkblue, "all darkblue")

# ---- curve blue 2E75B6 ----
print("== CURVE BLUE 2E75B6-family ==")
curveblue = (b > 130) & (r < 110) & (b - r > 70) & (g > 60) & (g < 180)
cb = bbox_of(curveblue, "all curveblue")
if cb:
    # per-column profile split by panel halves
    for name, x0, x1 in [("LEFT", 0, W // 2), ("RIGHT", W // 2, W)]:
        sub = curveblue[:, x0:x1]
        ys, xs = np.where(sub)
        if len(ys):
            print(f"  {name} panel blue: x {x0+xs.min()}-{x0+xs.max()} y {ys.min()}-{ys.max()} n={len(ys)}")

# ---- black text (title is red; headings/labels black) ----
print("== BLACK TEXT ==")
black = (r < 80) & (g < 80) & (b < 80)
bl = bbox_of(black, "all black")
if bl:
    rows = np.where(black.any(axis=1))[0]
    bands = []
    s = rows[0]; p = rows[0]
    for y in rows[1:]:
        if y > p + 4:
            bands.append((s, p)); s = y
        p = y
    bands.append((s, p))
    for (y0, y1) in bands:
        m = black[y0:y1 + 1]
        xs = np.where(m.any(axis=0))[0]
        print(f"  black band y {y0}-{y1}: x {xs.min()}-{xs.max()} n={int(m.sum())}")

# ---- badge ----
print("== BADGE (FDFD96 + ring 6A5ACD) ==")
yel = (r > 220) & (g > 220) & (b < 200) & (b > 150)
bb = bbox_of(yel, "badge yellow")
pur = (b > 150) & (r > 70) & (r < 180) & (g < 130)
pb = bbox_of(pur, "badge ring purple")

# ---- house chrome sanity on this frame ----
print("== HOUSE CHROME (this frame) ==")
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
gr = bbox_of(gray, "gray panel")
stroke_red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
sr = bbox_of(stroke_red, "house stroke red (incl. C00000)")
# exclude content pure red zone (left column check)
mid = stroke_red[250:300, :]
xs = np.where(mid.any(axis=0))[0]
print(f"  strokes at mid-height cols: {xs.min()}-{xs.max()}" if len(xs) else "  none")
