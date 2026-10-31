#!/usr/bin/env python3
"""Inspect k15 BL PNG at full res: red comps + dark comps mapped to slide coords."""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

X0, Y0, W, H = 83, 290, 293, 237
im = Image.open(RJ + "/assets_k15/plot_025_bl.png").convert("RGB")
a = np.array(im).astype(np.int32)
sx, sy = im.size[0] / W, im.size[1] / H
print("bl png", im.size, "scale %.4f %.4f" % (sx, sy))

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)

def slide_bbox(x0, y0, x1, y1):
    return (X0 + x0 / sx, Y0 + y0 / sy, X0 + x1 / sx, Y0 + y1 / sy)

print("\n== k15 BL PNG red comps area>=20 (slide bbox) ==")
rm = redmask(a)
lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) >= 20:
        s = slide_bbox(xs.min(), ys.min(), xs.max(), ys.max())
        print("  area=%d slide x%.0f..%.0f y%.0f..%.0f" % (len(xs), s[0], s[2], s[1], s[3]))

print("\n== red px near slide markers (199,445),(270,482) in PNG ==")
for (mx, my) in [(199, 445), (270, 482)]:
    lx, ly = (mx - X0) * sx, (my - Y0) * sy
    win = rm[max(0, int(ly - 25)):int(ly + 25), max(0, int(lx - 25)):int(lx + 25)]
    print("  (%d,%d): red px in +-6slide window = %d" % (mx, my, win.sum()))

print("\n== k15 BL PNG dark comps area>=40 (slide bbox) ==")
dm = darkmask(a)
lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) >= 40:
        s = slide_bbox(xs.min(), ys.min(), xs.max(), ys.max())
        print("  area=%d slide x%.0f..%.0f y%.0f..%.0f" % (len(xs), s[0], s[2], s[1], s[3]))

# what does the region around the 4 anchors look like in k15 png (dark ink)?
anchors = {
    "top":    (236, 302, 278, 322),
    "right-m": (325, 388, 350, 401),
    "low-L":  (138, 438, 205, 470),
    "low-R":  (300, 448, 346, 470),
}
print("\n== dark ink inside anchor boxes in k15 PNG ==")
for k, (x0, y0, x1, y1) in anchors.items():
    lx0, ly0 = (x0 - X0) * sx, (y0 - Y0) * sy
    lx1, ly1 = (x1 - X0) * sx, (y1 - Y0) * sy
    win = dm[int(ly0):int(ly1) + 1, int(lx0):int(lx1) + 1]
    print("  %s: dark px=%d of %d" % (k, win.sum(), win.size))

# background color around labels in k15 png (sample ring outside anchor boxes)
print("\n== k15 PNG bg sample around anchors (median of non-dark px in 2x box) ==")
for k, (x0, y0, x1, y1) in anchors.items():
    lx0, ly0 = int((x0 - X0) * sx), int((y0 - Y0) * sy)
    lx1, ly1 = int((x1 - X0) * sx), int((y1 - Y0) * sy)
    pad = int(6 * sx)
    win = a[max(0, ly0 - pad):ly1 + pad, max(0, lx0 - pad):lx1 + pad]
    wdm = darkmask(win)
    bg = win[~wdm]
    print("  %s: bg median %s (n=%d)" % (k, np.median(bg, 0) if len(bg) else None, len(bg)))
