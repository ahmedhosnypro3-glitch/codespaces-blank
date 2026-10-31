#!/usr/bin/env python3
"""Standard composite probe for slide 025 k17 asset sets.
Composites a 4-PNG asset set onto a 960x540 canvas (white + gray panel
E9E9E7 x54..903 y45..540) at the build/slide_025.js addImage rects, then
checks vs unique_slides/slide_025.jpg:
  md5:  each PNG differs from assets_k15
  CHECK1: BR band slide x672..816 y472..517 diff-vs-orig total % (target <50%)
  CHECK2: BL labels at anchors via NCC template ID
           x138..205 y438..470 'Local Minima' | x300..346 y448..470 'Global Minima'
           x325..350 y388..401 'Local Minima' | x236..278 y302..322 'Global Minima'
  CHECK3: TR red segment (652,189)->(667,165) red-hit % within 2px (orig ~54%, target >=20%)
  CHECK4: BR winding (largest dark comp wind-ratio, target ~6.02)
  CHECK5: BL markers exactly 2 at (199,445),(270,482), area 60-67
usage: pil_k17_probe.py <assets_dir> <label>
"""
import os
import sys
import hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ASSETS = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(ASSETS)

ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

# build/slide_025.js addImage placements: (name, x, y, w, h) in slide px
PLACEMENTS = [
    ("tl", 85, 115, 180, 173),
    ("tr", 616, 115, 263, 202),
    ("bl", 83, 290, 293, 237),
    ("br", 615, 344, 265, 187),
]

canvas = np.full((540, 960, 3), 255, np.int32)
canvas[45:540, 54:904] = np.array([233, 233, 231], np.int32)  # E9E9E7 panel
md5s = []
for name, x, y, w, h in PLACEMENTS:
    p = os.path.join(ASSETS, "plot_025_%s.png" % name)
    md5s.append((name, hashlib.md5(open(p, "rb").read()).hexdigest(), os.path.getsize(p)))
    im = Image.open(p).convert("RGB").resize((w, h), Image.BILINEAR)
    canvas[y:y + h, x:x + w] = np.asarray(im).astype(np.int32)
REN = canvas

print("== probe label: %s  assets: %s ==" % (LABEL, ASSETS))
print("== assets md5 ==")
for n, m, s in md5s:
    print("  plot_025_%s.png  md5=%s  size=%d" % (n, m, s))
k15 = os.path.join(RJ, "assets_k15")
print("== md5 vs assets_k15 ==")
alldiff = True
for name, x, y, w, h in PLACEMENTS:
    p = os.path.join(k15, "plot_025_%s.png" % name)
    m15 = hashlib.md5(open(p, "rb").read()).hexdigest()
    m17 = dict((n, m) for n, m, s in md5s)[name]
    diff = m15 != m17
    alldiff &= diff
    print("  plot_025_%s.png  k15=%s %s=%s  DIFFERENT=%s" % (name, m15, LABEL, m17, diff))
print("  ALL_MD5_DIFFERENT_FROM_K15: %s" % alldiff)


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~pr


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), xs, ys))
    return out


# ── CHECK1: BR bottom band ──────────────────────────────────────────────────
print("\n== CHECK1: BR band slide x672..816 y472..517 diff vs orig ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = ORIG[by0:by1, bx0:bx1]
rb = REN[by0:by1, bx0:bx1]
diff = (np.abs(ob - rb).sum(2) > 60)
H, W = diff.shape
gx, gy = 12, 5
cells = [[int(diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx].sum())
          for ix in range(gx)] for iy in range(gy)]
mx = max(max(r) for r in cells)
ca = (H // gy) * (W // gx)
band_pct = 100.0 * diff.mean()
print("  band %dx%d total diff px=%d (%.1f%%)  maxcell=%d/%d (%.1f%%)" % (W, H, diff.sum(), band_pct, mx, ca, 100.0 * mx / ca))
for r in cells:
    print("  cell row:", r)
c1 = band_pct < 50.0
print("  CHECK1 (band diff < 50%%): %s" % ("PASS" if c1 else "FAIL"))
print("  per-row colored%% (x615..880) orig vs render, y466..530:")
oprof = 100.0 * colmask(ORIG[344:531, 615:880]).mean(1)
rprof = 100.0 * colmask(REN[344:531, 615:880]).mean(1)
for i in range(122, 187, 3):
    print("    y%d orig=%3.0f render=%3.0f" % (344 + i, oprof[i], rprof[i]))
prof_corr = float(np.corrcoef(oprof, rprof)[0, 1])
print("  row-profile corr=%.3f" % prof_corr)

# ── CHECK2: BL labels at anchors ────────────────────────────────────────────
print("\n== CHECK2: BL labels at orig anchors (NCC template ID) ==")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
_tc = {}


def render_cand(s, fs):
    if (s, fs) not in _tc:
        f = ImageFont.truetype(FONT, fs)
        im = Image.new("L", (300, 60), 255)
        ImageDraw.Draw(im).text((4, 4), s, font=f, fill=0)
        a = np.array(im)
        ys, xs = np.nonzero(a < 128)
        _tc[(s, fs)] = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return _tc[(s, fs)]


def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den > 0 else -1.0


def lum(a):
    return (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])


def identify(win):
    w, h = win.shape[1], win.shape[0]
    best = (-2, "?")
    for s in CANDS:
        for fs in range(7, 16):
            c = render_cand(s, fs)
            cr = np.array(Image.fromarray(c.astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32)
            v = ncc(lum(win).astype(np.float32), cr)
            if v > best[0]:
                best = (v, s)
    return best


ANCHORS = [
    ("top",     236, 302, 278, 322, "Global Minima"),
    ("right-m", 325, 388, 350, 401, "Local Minima"),
    ("low-L",   138, 438, 205, 470, "Local Minima"),
    ("low-R",   300, 448, 346, 470, "Global Minima"),
]
c2 = True
for tag, ax0, ay0, ax1, ay1, want in ANCHORS:
    ow = identify(ORIG[ay0:ay1, ax0:ax1])
    rw = identify(REN[ay0:ay1, ax0:ax1])
    dm = (REN[ay0:ay1, ax0:ax1].max(2) < 145) & ((REN[ay0:ay1, ax0:ax1].max(2) - REN[ay0:ay1, ax0:ax1].min(2)) < 80)
    ok = rw[1] == want and dm.sum() > 30
    c2 &= ok
    print("  %-7s anchor x%d..%d y%d..%d want='%s' | orig='%s'(%.2f) render='%s'(%.2f) ink=%d -> %s" %
          (tag, ax0, ax1, ay0, ay1, want, ow[1], ow[0], rw[1], rw[0], dm.sum(), "OK" if ok else "MISS"))
print("  CHECK2 (labels at anchors): %s" % ("PASS" if c2 else "FAIL"))

# ── CHECK3: TR red diagonal segment (652,189)->(667,165) ────────────────────
print("\n== CHECK3: TR red segment (652,189)->(667,165) red-hit within 2px ==")


def redhit(a, x0, y0, x1, y1, n=200):
    rm = redmask(a)
    hit = 0
    for i in range(n):
        t = i / (n - 1.0)
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        xi, yi = int(round(x)), int(round(y))
        win = rm[max(0, yi - 2):yi + 3, max(0, xi - 2):xi + 3]
        if win.any():
            hit += 1
    return 100.0 * hit / n


for tag, a in (("orig", ORIG), ("render", REN)):
    h = redhit(a, 652, 189, 667, 165)
    print("  %s (652,189)->(667,165): red-hit %.0f%%" % (tag, h))
h_r = redhit(REN, 652, 189, 667, 165)
c3 = h_r >= 20.0
print("  CHECK3 (render red-hit >= 20%%, orig was 54%%): %s" % ("PASS" if c3 else "FAIL"))

# ── CHECK4: winding (verify_k15 metric on BR box) ───────────────────────────
print("\n== CHECK4: BR winding path (largest dark comp, verify_k15 metric) ==")
Bx0, By0, Bx1, By1 = 615, 344, 880, 531
P = 8
br = REN[By0 + P:By1 - P, Bx0 + P:Bx1 - P]
dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
best = None
for area, xs, ys in comps(dm, min_area=15):
    spanx = xs.max() - xs.min() + 1
    if best is None or area > best[0]:
        best = (area, spanx, xs, ys)
if best:
    a, spanx, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    ratio = seg / max(straight, 1.0)
    print("  area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f (target ~6.02)" % (a, spanx, seg, straight, ratio))
else:
    ratio = 0.0
    print("  no dark comp found")
cw = ratio > 1.02 and spanx > 30
print("  CHECK4 (winding ~6.02, ratio>1.02 & spanx>30): %s" % ("PASS" if cw else "FAIL"))

# ── CHECK5: markers ─────────────────────────────────────────────────────────
print("\n== CHECK5: BL red marker-like comps ==")
BL = (83, 290, 377, 528)
x0, y0, x1, y1 = BL


def markers(a):
    bl = a[y0:y1, x0:x1]
    rm = redmask(bl)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - y0:423 - y0, :] = False
    out = []
    for area, xs, ys in comps(rm, min_area=8):
        w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, (xs.min() + xs.max()) // 2 + x0, (ys.min() + ys.max()) // 2 + y0))
    return out


om = markers(ORIG)
rmk = markers(REN)
print("  orig markers: %s" % (om,))
print("  render markers: %s" % (rmk,))
targets = [(199, 445), (270, 482)]
matched = []
for tx, ty in targets:
    hit = any(abs(m[1] - tx) <= 6 and abs(m[2] - ty) <= 6 for m in rmk)
    matched.append(hit)
areas_ok = all(60 <= m[0] <= 67 for m in rmk) if len(rmk) == 2 else False
cm = len(rmk) == 2 and all(matched) and areas_ok
print("  marker areas in 60-67: %s" % areas_ok)
print("  CHECK5 markers: exactly 2 at (199,445),(270,482) area 60-67: %s" % ("PASS" if cm else "FAIL"))

overall = all([alldiff, c1, c2, c3, cw, cm])
print("\nSUMMARY: md5_all_diff=%s CHECK1=%s (%.1f%%) CHECK2=%s CHECK3=%s (%.0f%%) CHECK4 winding=%.3f %s CHECK5 markers=%s" %
      (alldiff, "PASS" if c1 else "FAIL", band_pct, "PASS" if c2 else "FAIL",
       "PASS" if c3 else "FAIL", h_r, ratio, "PASS" if cw else "FAIL", "PASS" if cm else "FAIL"))
print("OVERALL %s: %s" % (LABEL, "PASS" if overall else "FAIL"))
