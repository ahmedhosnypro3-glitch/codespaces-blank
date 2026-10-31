#!/usr/bin/env python3
"""k17h PIL verification: composite assets_k17h at the four slide-025 plot boxes
onto a 960x540 canvas, compare vs unique_slides/slide_025.jpg.

Writes pil_k17h_out.txt with:
  CHECK1: BR bottom band x672..816 y472..517 per-cell diff grid vs orig
          (defect = solid diff block; also row colored% profile y455..525)
  CHECK2: BL label windows (the four PIL-measured anchors) - dark ink present
          and NCC template id where possible
  CHECK3: BL red marker-like comps == orig {(199,445),(270,482)} count/pos
  winding: BR largest dark comp wind-ratio (target 6.02)
  TR seg: red-hit along slide (652,189)->(667,165) (orig 54%)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
A = os.path.join(RJ, "assets_k17h")

BOXES = {
    "tl": (85, 115, 180, 173),
    "tr": (616, 115, 263, 202),
    "bl": (83, 290, 293, 237),
    "br": (615, 344, 265, 187),
}

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
canvas_img = Image.fromarray(orig.astype(np.uint8)).copy()
for name, (x0, y0, w, h) in BOXES.items():
    im = Image.open(os.path.join(A, "plot_025_%s.png" % name)).convert("RGB")
    canvas_img.paste(im.resize((w, h), Image.BILINEAR), (x0, y0))
ren = np.array(canvas_img).astype(np.int32)

L = []
def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    L.append(s)


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
            out.append([len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())])
    return out


def colmask(a, border=0):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    m = ((mx - mn) > 60) & (mx > 90) & ~red
    if border:
        m[:border, :] = False; m[-border:, :] = False
        m[:, :border] = False; m[:, -border:] = False
    return m


p("composite = assets_k17h at boxes tl(85,115,180,173) tr(616,115,263,202) bl(83,290,293,237) br(615,344,265,187)")

# ── 1. BR bottom band ────────────────────────────────────────────────────────
p("")
p("== 1. BR bottom band slide x672..816 y472..517 diff-vs-orig grid ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = orig[by0:by1, bx0:bx1]
rb = ren[by0:by1, bx0:bx1]
diff = (np.abs(ob - rb).sum(2) > 60)
H, W = diff.shape
gx, gy = 12, 5
p("  band %dx%d, total diff px=%d (%.1f%%)" % (W, H, diff.sum(), 100.0 * diff.mean()))
for iy in range(gy):
    row = [int(diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx].sum())
           for ix in range(gx)]
    p("  cell row: %s" % row)
mx = max(max(int(diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx].sum())
             for ix in range(gx)) for iy in range(gy))
cell_area = (H // gy) * (W // gx)
p("  max cell diff=%d of cell area %d (%.1f%% solid); k14 defect was ~2350px/cell solid"
  % (mx, cell_area, 100.0 * mx / cell_area))
ok1 = mx < 0.5 * cell_area
p("  CHECK1 (band no longer solid diff block): %s" % ("PASS" if ok1 else "FAIL"))

p("")
p("== 1b. BR row colored%% y455..525 (cols x615..880), orig vs k17h ==")
ORIG_PROF = [82,82,82,82,82,83,83,85,85,85,82,81,79,76,76,76,76,75,74,74,
             73,73,72,72,71,70,66,56,55,50,46,46,46,45,45,45,44,44,44,43,46,
             46,45,45,42,41,41,41,43,44,41,41,41,39,37,36,36,30,26,22,18,17,
             16,18,16,12,10,12,9,2,2]
om = colmask(orig[344:531, 615:880])
rm = colmask(ren[344:531, 615:880])
oprof = 100.0 * om[455 - 344:526 - 344].mean(1)
rprof = 100.0 * rm[455 - 344:526 - 344].mean(1)
p("  orig: " + " ".join("%.0f" % v for v in oprof))
p("  k17h: " + " ".join("%.0f" % v for v in rprof))
p("  prof mean|diff| = %.2f" % np.abs(oprof - rprof).mean())

# ── 2. BL labels at the four anchors ─────────────────────────────────────────
p("")
p("== 2. BL label anchor windows (orig ink vs k17h ink, NCC id) ==")
BL = (83, 290, 377, 528)
x0, y0, x1, y1 = BL
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
ANCHORS = [
    ("top",   "Global Minima", (236, 302, 278, 322)),
    ("right-m", "Local Minima", (325, 388, 350, 401)),
    ("low-L", "Local Minima", (138, 438, 205, 470)),
    ("low-R", "Global Minima", (300, 448, 346, 470)),
]


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


ok2 = True
for name, want, (ax0, ay0, ax1, ay1) in ANCHORS:
    for tag, img in (("orig", orig), ("k17h", ren)):
        crop = lum(img[ay0:ay1, ax0:ax1]).astype(np.float32)
        ink = int((crop < 145).sum())
        best = (-2, "?")
        h, w = crop.shape
        for s in CANDS:
            for fs in range(6, 14):
                c = render_cand(s, fs)
                cr = np.array(Image.fromarray(c.astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32)
                v = ncc(crop, cr)
                if v > best[0]:
                    best = (v, s)
        p("  %-7s %-4s x%d..%d y%d..%d ink=%d -> best '%s' ncc=%.3f (want '%s')"
          % (name, tag, ax0, ax1, ay0, ay1, ink, best[1], best[0], want))
    # k17h window must contain dark ink (label actually drawn there)
    crop = lum(ren[ay0:ay1, ax0:ax1])
    if (crop < 145).sum() < 20:
        ok2 = False
p("  CHECK2 (BL labels present at all four anchors): %s" % ("PASS" if ok2 else "FAIL"))

# ── 3. BL red marker-like comps ──────────────────────────────────────────────
p("")
p("== 3. BL red marker-like comps ==")


def markers(a):
    bl = a[y0:y1, x0:x1]
    rm = redmask(bl)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - y0:423 - y0, :] = False
    out = []
    for area, rx0, ry0, rx1, ry1 in comps(rm, min_area=8):
        w, h = rx1 - rx0 + 1, ry1 - ry0 + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, (rx0 + rx1) // 2 + x0, (ry0 + ry1) // 2 + y0))
    return out


om = markers(orig)
rmk = markers(ren)
p("  orig marker-like: %s" % (om,))
p("  k17h marker-like: %s" % (rmk,))
ok3 = len(rmk) == len(om) and all(
    any(abs(a[1] - b[1]) <= 6 and abs(a[2] - b[2]) <= 6 for b in om) for a in rmk)
p("  CHECK3 (markers match orig (199,445),(270,482)): %s" % ("PASS" if ok3 else "FAIL"))

# ── 4. BR winding ────────────────────────────────────────────────────────────
p("")
p("== 4. BR black path winding (lum<100, low-sat, frame excluded) ==")
br = ren[344:531, 615:880]
dm = (br.max(2) < 100) & ((br.max(2) - br.min(2)) < 80)
dm[:8] = False; dm[-8:] = False; dm[:, :8] = False; dm[:, -8:] = False
lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
best = None
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 20:
        continue
    area = len(xs)
    if best is None or area > best[0]:
        best = (area, xs, ys)
if best:
    area, xs, ys = best
    # winding: total turning angle / pi along the ordered path skeleton
    pts = sorted(zip(xs, ys), key=lambda q: (q[1], q[0]))
    # order by nearest-neighbor chain
    rem = list(zip(xs, ys))
    chain = [rem.pop(0)]
    while rem:
        c = chain[-1]
        j = min(range(len(rem)), key=lambda i: (rem[i][0] - c[0]) ** 2 + (rem[i][1] - c[1]) ** 2)
        chain.append(rem.pop(j))
    spanx = xs.max() - xs.min()
    length = sum(np.hypot(chain[i+1][0]-chain[i][0], chain[i+1][1]-chain[i][1]) for i in range(len(chain)-1))
    straight = np.hypot(xs.max() - xs.min(), ys.max() - ys.min())
    winding = length / max(straight, 1e-9)  # wind-ratio = len/straight (k16 metric)
    p("  largest: area=%d slide-x %d..%d slide-y %d..%d | x-span=%d len=%.1f straight=%.1f wind-ratio=%.3f"
      % (area, 615 + xs.min(), 615 + xs.max(), 344 + ys.min(), 344 + ys.max(),
         spanx, length, straight, winding))
    p("  WIND-ratio len/straight (k15-view path, k16 measured 6.020): %.3f" % winding)
else:
    p("  no dark comp found -> FAIL")

# ── 5. TR red diagonal segment ───────────────────────────────────────────────
p("")
p("== 5. TR red diagonal slide (652,189)->(667,165) ==")


def seg_hit(img, x0, y0, x1, y1, n=60):
    hits = 0
    for i in range(n + 1):
        t = i / n
        x = int(round(x0 + (x1 - x0) * t))
        y = int(round(y0 + (y1 - y0) * t))
        nb = img[max(0, y - 1):y + 2, max(0, x - 1):x + 2]
        if redmask(nb).any():
            hits += 1
    return hits / (n + 1)


oh = seg_hit(orig, 652, 189, 667, 165)
rh = seg_hit(ren, 652, 189, 667, 165)
p("  orig red-hit=%.3f  k17h red-hit=%.3f  (target ~0.54) -> %s"
  % (oh, rh, "PASS" if rh >= 0.4 else "FAIL"))

p("")
p("SUMMARY: CHECK1=%s CHECK2=%s CHECK3=%s winding~6.02 TRseg=%.2f"
  % ("PASS" if ok1 else "FAIL", "PASS" if ok2 else "FAIL", "PASS" if ok3 else "FAIL", rh))

with open(os.path.join(RJ, "pil_k17h_out.txt"), "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote pil_k17h_out.txt")
