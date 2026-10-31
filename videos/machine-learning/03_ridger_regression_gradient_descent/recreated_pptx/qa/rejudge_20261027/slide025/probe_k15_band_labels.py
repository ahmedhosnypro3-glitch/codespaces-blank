#!/usr/bin/env python3
"""Deeper probe: BR bottom band rows + BL bottom label ink map, orig vs k14 render vs k15 render."""
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
r14 = Image.open(RJ + "/slide025/render.png").convert("RGB")
r15 = Image.open(RJ + "/slide025/render_k15.png").convert("RGB")
SX, SY = r15.size[0] / 960.0, r15.size[1] / 540.0

def ren_box(img, x0, y0, x1, y1):
    c = img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))
    return np.array(c.resize((x1 - x0, y1 - y0), Image.BILINEAR)).astype(np.int32)

def colored(a, thr=50):
    return (a.max(2) - a.min(2)) > thr

def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)

# ── BR band x672..816 y472..517: per-row colored% + mean RGB, orig/k14/k15 ──
print("== BR bottom band x672..816 y472..517 per-row colored%% and diff-vs-orig ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = orig[by0:by1, bx0:bx1]
r14b = ren_box(r14, bx0, by0, bx1, by1)
r15b = ren_box(r15, bx0, by0, bx1, by1)
for yy in range(0, by1 - by0):
    sy = by0 + yy
    co = 100.0 * colored(ob[yy][None, :, :])[0].mean()
    c14 = 100.0 * colored(r14b[yy][None, :, :])[0].mean()
    c15 = 100.0 * colored(r15b[yy][None, :, :])[0].mean()
    d14 = int((np.abs(ob[yy] - r14b[yy]).sum(1) > 60).sum())
    d15 = int((np.abs(ob[yy] - r15b[yy]).sum(1) > 60).sum())
    print("  y=%d orig_col=%5.1f k14_col=%5.1f k15_col=%5.1f | diff k14=%3d k15=%3d | origRGB=%s k15RGB=%s"
          % (sy, co, c14, c15, d14, d15, tuple(ob[yy, 20]), tuple(r15b[yy, 20])))

# also full BR panel bottom rows y455..540 colored%
print("\n== BR panel rows y455..540 colored%% (cols x615..880) ==")
for name, a in (("orig", orig), ("k14", ren_box(r14, 0, 0, 960, 540)), ("k15", ren_box(r15, 0, 0, 960, 540))):
    rows = [100.0 * colored(a[yy, 615:881][None, :, :])[0].mean() for yy in range(455, 540)]
    print("  %s: %s" % (name, " ".join("%d:%.0f" % (455 + i, v) for i, v in enumerate(rows))))

# ── BL bottom region ink map (orig) y430..530 x83..377, downsampled ASCII ──
print("\n== BL bottom ink map orig y425..530 x83..377 (2px cells, #=dark) ==")
x0, y0, x1, y1 = 83, 425, 377, 530
for name, a in (("orig", orig), ("k14", ren_box(r14, 0, 0, 960, 540)), ("k15", ren_box(r15, 0, 0, 960, 540))):
    print("  --- %s ---" % name)
    dm = darkmask(a[y0:y1, x0:x1])
    H, W = dm.shape
    for yy in range(0, H, 3):
        line = ""
        for xx in range(0, W, 3):
            blk = dm[yy:yy + 3, xx:xx + 3]
            line += "#" if blk.sum() >= 2 else ("." if blk.sum() == 1 else " ")
        print("  y%d %s" % (y0 + yy, line))

# ── BL bottom label components (orig vs k15), no template matching ──
print("\n== BL bottom dark comps (y>=430) orig vs k15 ==")
for name, a in (("orig", orig), ("k14", ren_box(r14, 0, 0, 960, 540)), ("k15", ren_box(r15, 0, 0, 960, 540))):
    bl = a[290:528, 83:377]
    dm = darkmask(bl)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    dm[413 - 290:423 - 290, :] = False
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 5 and ys.min() + 290 >= 430:
            boxes.append((len(xs), xs.min() + 83, ys.min() + 290, xs.max() + 83, ys.max() + 290))
    # merge into lines
    boxes.sort(key=lambda b: b[2])
    lines = []
    for b in boxes:
        hit = None
        for L in lines:
            if abs((b[2] + b[4]) / 2 - (L[2] + L[4]) / 2) < 7 and (b[1] - L[3] < 10 or L[1] - b[3] < 10):
                hit = L
                break
        if hit:
            hit[1] = min(hit[1], b[1]); hit[2] = min(hit[2], b[2])
            hit[3] = max(hit[3], b[3]); hit[4] = max(hit[4], b[4]); hit[0] += b[0]
        else:
            lines.append(list(b))
    print("  %s:" % name)
    for L in sorted(lines, key=lambda l: l[2]):
        print("    area=%d slide x%d..%d y%d..%d w=%d h=%d" % (L[0], L[1], L[3], L[2], L[4], L[3] - L[1] + 1, L[4] - L[2] + 1))

# ── BL red comps full panel orig vs k14 vs k15 ──
print("\n== BL red comps (all) orig vs k14 vs k15 ==")
def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)
for name, a in (("orig", orig), ("k14", ren_box(r14, 0, 0, 960, 540)), ("k15", ren_box(r15, 0, 0, 960, 540))):
    bl = a[290:528, 83:377]
    rm = redmask(bl)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - 290:423 - 290, :] = False
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    cs = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 8:
            cs.append((len(xs), xs.min() + 83, ys.min() + 290, xs.max() + 83, ys.max() + 290))
    cs.sort(key=lambda c: -c[0])
    print("  %s: %s" % (name, cs[:10]))
print("\nPROBE_DONE")
