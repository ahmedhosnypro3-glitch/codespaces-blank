#!/usr/bin/env python3
"""k17g analysis: inspect k15 assets, composite on 960x540, gather patch data."""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
K15 = RJ + "/assets_k15"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
print("orig", orig.shape)

# addImage rects from build/slide_025.js
PANELS = {
    "tl": (85, 115, 180, 173),
    "tr": (616, 115, 263, 202),
    "bl": (83, 290, 293, 237),
    "br": (615, 344, 265, 187),
}
imgs = {}
canvas = np.full((540, 960, 3), 255, np.uint8)
for k, (x0, y0, w, h) in PANELS.items():
    im = Image.open(f"{K15}/plot_025_{k}.png").convert("RGB")
    imgs[k] = im
    sx, sy = im.size[0] / w, im.size[1] / h
    print(k, "png size", im.size, "scale %.4f x %.4f" % (sx, sy))
    canvas[y0:y0 + h, x0:x0 + w] = np.array(im.resize((w, h), Image.BILINEAR))

comp = canvas.astype(np.int32)

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)

# ── TR red along diag (652,189)->(667,165) ──
def redhit(a, p0, p1, n=200, rad=2):
    hits = 0
    for i in range(n):
        t = i / (n - 1)
        x, y = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
        xi, yi = int(round(x)), int(round(y))
        x0, x1 = max(0, xi - rad), min(a.shape[1], xi + rad + 1)
        y0, y1 = max(0, yi - rad), min(a.shape[0], yi + rad + 1)
        hits += int(redmask(a[y0:y1, x0:x1]).any())
    return hits

print("\n== TR diag red-hit ==")
print("orig     (652,189)->(667,165):", redhit(orig, (652, 189), (667, 165)), "/200")
print("k15 comp (652,189)->(667,165):", redhit(comp, (652, 189), (667, 165)), "/200")

# sample orig red color + thickness along segment
cols = []
thick = []
p0, p1 = (652, 189), (667, 165)
for i in range(200):
    t = i / 199
    x, y = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
    xi, yi = int(round(x)), int(round(y))
    win = orig[max(0, yi - 4):yi + 5, max(0, xi - 4):xi + 5]
    rm = redmask(win)
    if rm.any():
        cols.append(win[rm].mean(0))
        # thickness: red run in the column xi near yi
        col = redmask(orig[max(0, yi - 6):yi + 7, xi:xi + 1])[:, 0]
        thick.append(int(col.sum()))
print("orig red color median:", np.median(np.array(cols), 0) if cols else None)
print("orig red thickness runs (col): median", np.median(thick) if thick else None,
      "vals", sorted(set(thick)))

# ── BR band diff ──
bx0, by0, bx1, by1 = 672, 472, 816, 528
ob = orig[by0:by1, bx0:bx1]
cb = comp[by0:by1, bx0:bx1]
diff = (np.abs(ob - cb).sum(2) > 60)
print("\n== BR band x672..816 y472..528 ==")
print("k15 comp diff px=%d of %d (%.1f%%)" % (diff.sum(), diff.size, 100 * diff.mean()))
# orig band row colors (mean per row)
for y in range(by0, by1, 4):
    row = orig[y, bx0:bx1]
    print("  orig row y=%d mean RGB" % y, row.mean(0).round(1), " min", row.min(0), " max", row.max(0))

# ── BL dark-ink comps orig vs comp ──
print("\n== BL dark comps (slide coords) ==")
BL = (83, 290, 377, 528)
def darkcomps(a):
    x0, y0, x1, y1 = BL
    bl = a[y0:y1, x0:x1]
    dm = darkmask(bl)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    dm[413 - y0:423 - y0, :] = False
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 12:
            out.append((len(xs), int(xs.min() + x0), int(ys.min() + y0),
                        int(xs.max() + x0), int(ys.max() + y0)))
    return sorted(out, reverse=True)[:25]
print("orig:")
for c in darkcomps(orig):
    print("  area=%d x%d..%d y%d..%d" % c)
print("k15 comp:")
for c in darkcomps(comp):
    print("  area=%d x%d..%d y%d..%d" % c)

# label ink color in orig at anchors
anchors = {
    "top":    (236, 302, 278, 322, "Global Minima"),
    "right-m": (325, 388, 350, 401, "Local Minima"),
    "low-L":  (138, 438, 205, 470, "Local Minima"),
    "low-R":  (300, 448, 346, 470, "Global Minima"),
}
print("\n== orig label ink color / bbox at anchors ==")
for k, (x0, y0, x1, y1, s) in anchors.items():
    win = orig[y0:y1 + 1, x0:x1 + 1]
    dm = darkmask(win)
    if dm.any():
        ys, xs = np.nonzero(dm)
        print("  %s '%s': ink bbox x%d..%d y%d..%d (w%d h%d) color med %s" % (
            k, s, xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0,
            xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, np.median(win[dm], 0)))
    else:
        print("  %s '%s': no dark ink" % (k, s))

# ── BL red markers at (199,445),(270,482) ──
print("\n== red presence near markers ==")
for (mx, my) in [(199, 445), (270, 482)]:
    for name, a in (("orig", orig), ("k15comp", comp)):
        win = redmask(a[my - 6:my + 7, mx - 6:mx + 7])
        print("  %s (%d,%d): red px=%d" % (name, mx, my, win.sum()))

# ── winding: BR largest dark comp ──
print("\n== BR winding ==")
BR = (615, 344, 881, 532)
def winding(a):
    x0, y0, x1, y1 = BR
    bl = a[y0:y1, x0:x1]
    dm = darkmask(bl, thr=120, sat=60)
    dm[:4, :] = False; dm[-4:, :] = False; dm[:, :4] = False; dm[:, -4:] = False
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 100 and (best is None or len(xs) > best[0]):
            best = (len(xs), xs.min(), ys.min(), xs.max(), ys.max())
    if best is None:
        return None
    area, bx0_, by0_, bx1_, by1_ = best
    straight = np.hypot(bx1_ - bx0_, by1_ - by0_)
    return area, straight, area / straight if straight else 0
print("orig BR:", winding(orig))
print("k15comp BR:", winding(comp))
