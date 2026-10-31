#!/usr/bin/env python3
"""PIL check of a k15 render of slide 025 vs the original frame.
usage: pil_k15_render_check.py <render.png>
Checks:
  1. BR bottom band slide x672..816 y472..517: per-cell diff vs orig must not be
     a solid ~2350px/cell diff block (k14 defect).
  2. BL labels: bottom two text lines must be 'Local Minima' (upper) then
     'Global Minima' (lower), positioned lower-left like the original.
  3. BL red marker-like comps (x-shaped maxima markers): count in render must
     not exceed orig (extra markers absent in original must be removed).
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"

RENDER = sys.argv[1] if len(sys.argv) > 1 else RJ + "/slide025/render.png"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ren_img = Image.open(RENDER).convert("RGB")
SX, SY = ren_img.size[0] / 960.0, ren_img.size[1] / 540.0
print("render=%s size=%s scale=%.4fx%.4f" % (RENDER, ren_img.size, SX, SY))

def ren_box(x0, y0, x1, y1):
    c = ren_img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))
    return np.array(c.resize((x1 - x0, y1 - y0), Image.BILINEAR)).astype(np.int32)

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)

def lum(a):
    return (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])

def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append([len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), i])
    return out

# ── 1. BR bottom band x672..816 y472..517: per-cell diff grid ────────────────
print("\n== 1. BR bottom band slide x672..816 y472..517 diff-vs-orig grid ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = orig[by0:by1, bx0:bx1]
rb = ren_box(bx0, by0, bx1, by1)
diff = (np.abs(ob - rb).sum(2) > 60)
H, W = diff.shape
gx, gy = 12, 5  # 12x5 cells
print("  band %dx%d, total diff px=%d (%.1f%%)" % (W, H, diff.sum(), 100.0 * diff.mean()))
cells = []
for iy in range(gy):
    row = []
    for ix in range(gx):
        c = diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx]
        row.append(int(c.sum()))
    cells.append(row)
for r in cells:
    print("  cell row:", r)
mx = max(max(r) for r in cells)
cell_area = (H // gy) * (W // gx)
print("  max cell diff=%d of cell area %d (%.1f%% solid); k14 defect was ~2350px/cell solid"
      % (mx, cell_area, 100.0 * mx / cell_area))
ok1 = mx < 0.5 * cell_area  # not a solid block
print("  CHECK1 (band no longer solid diff block): %s" % ("PASS" if ok1 else "FAIL"))

# ── 2. BL bottom labels via NCC template ID ──────────────────────────────────
print("\n== 2. BL panel bottom labels (orig vs render) ==")
BL = (83, 290, 377, 528)
x0, y0, x1, y1 = BL
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]

def render_cand(s, fs):
    f = ImageFont.truetype(FONT, fs)
    im = Image.new("L", (300, 60), 255)
    ImageDraw.Draw(im).text((4, 4), s, font=f, fill=0)
    a = np.array(im)
    ys, xs = np.nonzero(a < 128)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den > 0 else -1.0

def find_labels(a):
    bl = a[y0:y1, x0:x1]
    dm = darkmask(bl)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    dm[413 - y0:423 - y0, :] = False
    words = []
    for area, wx0, wy0, wx1, wy1, _ in comps(dm, min_area=5):
        w, h = wx1 - wx0 + 1, wy1 - wy0 + 1
        if w > 25 and h <= 9:
            continue
        if w > 40 and h < 3 * w // 4:
            continue
        words.append([wx0, wy0, wx1, wy1])
    # cluster into lines by y-center proximity
    lines = []
    for b in sorted(words, key=lambda b: (b[1], b[0])):
        hit = None
        for L in lines:
            if abs((b[1] + b[3]) / 2 - (L[1] + L[3]) / 2) < 6 and (b[0] - L[2] < 14 or L[0] - b[2] < 14):
                hit = L
                break
        if hit:
            hit[0] = min(hit[0], b[0]); hit[1] = min(hit[1], b[1])
            hit[2] = max(hit[2], b[2]); hit[3] = max(hit[3], b[3])
        else:
            lines.append(list(b))
    out = []
    for L in sorted(lines, key=lambda l: l[1]):
        w, h = L[2] - L[0] + 1, L[3] - L[1] + 1
        if w < 40 or h < 5:
            continue
        crop = lum(bl[L[1]:L[3] + 1, L[0]:L[2] + 1]).astype(np.float32)
        best = (-2, "?")
        for s in CANDS:
            for fs in range(7, 16):
                c = render_cand(s, fs)
                cr = np.array(Image.fromarray(c.astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32)
                v = ncc(crop, cr)
                if v > best[0]:
                    best = (v, s)
        out.append((L[0] + x0, L[1] + y0, L[2] + x0, L[3] + y0, best[1], round(best[0], 3)))
    return out

print("  orig labels:")
for t in find_labels(orig):
    print("    slide x%d..%d y%d..%d -> '%s' ncc=%.3f" % t)
print("  render labels:")
rlab = find_labels(ren_box(0, 0, 960, 540))
for t in rlab:
    print("    slide x%d..%d y%d..%d -> '%s' ncc=%.3f" % t)
bottom2 = rlab[-2:] if len(rlab) >= 2 else []
ok2 = False
if len(bottom2) == 2:
    upper, lower = bottom2[0], bottom2[1]
    ok2 = (upper[4] == "Local Minima" and lower[4] == "Global Minima"
           and upper[1] < 470 and lower[1] >= 450 and upper[0] < 350 and lower[0] < 350)
print("  CHECK2 (BL bottom lines: Local Minima upper, Global Minima lower, lower-left): %s"
      % ("PASS" if ok2 else "FAIL"))

# ── 3. BL red marker-like comps ──────────────────────────────────────────────
print("\n== 3. BL red marker-like comps (x maxima markers) ==")
def markers(a):
    bl = a[y0:y1, x0:x1]
    rm = redmask(bl)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - y0:423 - y0, :] = False
    out = []
    for area, rx0, ry0, rx1, ry1, _ in comps(rm, min_area=8):
        w, h = rx1 - rx0 + 1, ry1 - ry0 + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, (rx0 + rx1) // 2 + x0, (ry0 + ry1) // 2 + y0))
    return out

om = markers(orig)
rm_ = markers(ren_box(0, 0, 960, 540))
print("  orig marker-like: %s" % (om,))
print("  render marker-like: %s" % (rm_,))
ok3 = len(rm_) <= len(om)
print("  CHECK3 (no extra red x markers vs orig): %s" % ("PASS" if ok3 else "FAIL"))

print("\nSUMMARY: CHECK1=%s CHECK2=%s CHECK3=%s" % ("PASS" if ok1 else "FAIL", "PASS" if ok2 else "FAIL", "PASS" if ok3 else "FAIL"))
