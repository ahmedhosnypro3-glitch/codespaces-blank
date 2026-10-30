#!/usr/bin/env python3
"""Deep measurement of slide_028.jpg — connected components, color census,
curve tracing, dot detection. Companion to measure_original.py."""
import numpy as np
from PIL import Image
from scipy import ndimage

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# ---------- color census of the title band ----------
print("== TITLE BAND COLOR CENSUS (y 60..100, x 150..750) ==")
band = IM[60:100, 150:750]
flat = band.reshape(-1, 3)
nonbg = flat[(flat.sum(axis=1) < 720) & (flat.sum(axis=1) > 60)]  # non-white
if len(nonbg):
    from collections import Counter
    cnt = Counter(map(tuple, np.round(nonbg / 24) * 24))
    for col, n in cnt.most_common(8):
        print(f"  ~{col} n={n}")

# ---------- tighter red masks ----------
# title red band y 77-91 from previous pass: expand mask, get full bbox
red_ink = (r > 120) & ((r - g) > 40) & ((r - b) > 40)
# exclude house strokes columns 55..62 and 898..905
red_content = red_ink.copy()
red_content[:, :65] = False
red_content[:, 895:] = False
red_content[530:, :] = False  # exclude bottom stroke
lbl, n = ndimage.label(red_content)
print(f"\n== RED CONTENT COMPONENTS (excl. house strokes): {n} ==")
comps = []
for i in range(1, n + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) < 4:
        continue
    comps.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max(), i))
comps.sort(reverse=True)
for c in comps[:20]:
    size, x0, x1, y0, y1, i = c
    ys, xs = np.where(lbl == i)
    print(f"  n={size} x {x0}-{x1} y {y0}-{y1} w={x1-x0+1} h={y1-y0+1} "
          f"cx={(x0+x1)/2:.0f} cy={(y0+y1)/2:.0f}")

# ---------- black-ish text components ----------
print("\n== NEAR-BLACK COMPONENTS (r,g,b<120, val<360) ==")
dark = (r < 120) & (g < 120) & (b < 120)
# exclude badge numeral region for the listing clarity but keep note
lblb, nb = ndimage.label(dark)
boxes = []
for i in range(1, nb + 1):
    ys, xs = np.where(lblb == i)
    if len(ys) < 3:
        continue
    boxes.append((xs.min(), xs.max(), ys.min(), ys.max(), len(ys)))
boxes.sort(key=lambda t: (t[2], t[0]))
for x0, x1, y0, y1, npx in boxes:
    print(f"  n={npx} x {x0}-{x1} y {y0}-{y1} w={x1-x0+1} h={y1-y0+1}")

# ---------- blue components (curve + dots + segments), exclude border ----------
# curve blue 2E75B6=(46,117,182): high blue, mid green; border 1F4E79=(31,78,121)
curveblue = (b > 150) & (b - r > 80) & (g > 70) & (g < 190) & (r < 120)
lblc, nc = ndimage.label(curveblue)
print(f"\n== CURVE-BLUE COMPONENTS: {nc} ==")
cboxes = []
for i in range(1, nc + 1):
    ys, xs = np.where(lblc == i)
    if len(ys) < 3:
        continue
    cboxes.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max(), i))
cboxes.sort(reverse=True)
for size, x0, x1, y0, y1, i in cboxes[:25]:
    # fill ratio distinguishes dots (blobby) from strokes (thin)
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    fr = size / (w_ * h_)
    print(f"  n={size} x {x0}-{x1} y {y0}-{y1} w={w_} h={h_} fillratio={fr:.2f} "
          f"cx={(x0+x1)/2:.0f} cy={(y0+y1)/2:.0f}")

# ---------- border-only mask (dark blue, exclude lighter curve blue) ----------
border = (b > 90) & (b < 150) & (b - r > 40) & (b - g > 25) & (r < 80)
lblbd, nbd = ndimage.label(border)
print(f"\n== BORDER COMPONENTS: {nbd} ==")
bboxes = []
for i in range(1, nbd + 1):
    ys, xs = np.where(lblbd == i)
    if len(ys) < 3:
        continue
    bboxes.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
bboxes.sort(reverse=True)
for size, x0, x1, y0, y1 in bboxes[:12]:
    print(f"  n={size} x {x0}-{x1} y {y0}-{y1} w={x1-x0+1} h={y1-y0+1}")

# ---------- purple ring tight (badge only) ----------
print("\n== BADGE RING (tight) ==")
pur = (b > 160) & (b - g > 60) & (r > 60) & (r < 160) & (g < 130)
ys, xs = np.where(pur)
sel = (xs > 840) & (xs < 915)
ys2, xs2 = ys[sel], xs[sel]
if len(ys2):
    print(f"  ring: x {xs2.min()}-{xs2.max()} y {ys2.min()}-{ys2.max()} n={len(ys2)}")
