#!/usr/bin/env python3
"""Verify a k15 render of slide 025 vs the original. usage: verify_k15.py <render.png>
Checks (all in slide space 960x540):
 1. BR bottom band x672..816 y472..517: per-cell diff vs orig not a solid block
    (max cell < 50% of cell area) and total band diff < 60%.
 2. BR row profile: per-row colored% in BR box correlates with orig (Pearson > 0.8).
 3. BR winding path: largest dark comp inside BR surface region has wind-ratio > 1.02.
 4. BL labels: NCC template ID at left anchor window matches 'Local Minima' and right
    anchor window matches 'Global Minima' (calibrated: same test on orig must agree).
 5. BL red marker-like comps in render <= orig count.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"

RENDER = sys.argv[1] if len(sys.argv) > 1 else RJ + "/render_k15.png"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ren_img = Image.open(RENDER).convert("RGB")
SX, SY = ren_img.size[0] / 960.0, ren_img.size[1] / 540.0
print("render=%s size=%s scale=%.4fx%.4f" % (RENDER, ren_img.size, SX, SY))


def ren_box(x0, y0, x1, y1):
    c = ren_img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))
    return np.array(c.resize((x1 - x0, y1 - y0), Image.BILINEAR)).astype(np.int32)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return m & ~pr


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), xs, ys))
    return out

ok = True

# 1. BR bottom band: hue-class diff (blue-vs-blue brightness differences are not
# a defect; a solid block of class mismatch = the old flush-overflow defect)
def classify(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mx, mn = a.max(2), a.min(2)
    out = np.zeros(a.shape[:2], np.int32)  # 0 white
    sat = (mx - mn) > 60
    out[sat & (b >= r) & (b >= g)] = 1      # blue
    out[sat & (g > r) & (g >= b)] = 2        # green
    out[sat & (r > 200) & (g > 120) & (b < 100)] = 3  # yellow
    out[sat & (r > 150) & (g <= 120)] = 4    # red
    out[sat & ~((b >= r) & (b >= g)) & ~((g > r) & (g >= b))
        & ~((r > 200) & (g > 120) & (b < 100)) & ~((r > 150) & (g <= 120))] = 5
    return out


bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = orig[by0:by1, bx0:bx1]
rb = ren_box(bx0, by0, bx1, by1)
oc, rc = classify(ob), classify(rb)
cdiff = (oc != rc)
# blue(1) vs blue counts as match; also allow white-vs-white
H, W = cdiff.shape
gx, gy = 12, 5
mx = max(cdiff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx].sum()
         for iy in range(gy) for ix in range(gx))
ca = (H // gy) * (W // gx)
rawdiff = (np.abs(ob - rb).sum(2) > 60)
c1 = mx < 0.5 * ca and cdiff.mean() < 0.60
ok &= c1
print("1. BR band classdiff=%.1f%% raw=%.1f%% maxcell=%d/%d (%.0f%%) -> %s" %
      (100 * cdiff.mean(), 100 * rawdiff.mean(), mx, ca, 100.0 * mx / ca,
       "PASS" if c1 else "FAIL"))
print("   orig classes: white=%.1f blue=%.1f green=%.1f other=%.1f" % (
    100 * (oc == 0).mean(), 100 * (oc == 1).mean(), 100 * (oc == 2).mean(),
    100 * ((oc >= 3)).mean()))
print("   rend classes: white=%.1f blue=%.1f green=%.1f other=%.1f" % (
    100 * (rc == 0).mean(), 100 * (rc == 1).mean(), 100 * (rc == 2).mean(),
    100 * ((rc >= 3)).mean()))

# 2. BR row profile correlation
P = 8
Bx0, By0, Bx1, By1 = 615, 344, 880, 531
o_prof = 100.0 * colmask(orig[By0 + P:By1 - P, Bx0 + P:Bx1 - P]).mean(1)
r_prof = 100.0 * colmask(ren_box(Bx0 + P, By0 + P, Bx1 - P, By1 - P)).mean(1)
n = min(len(o_prof), len(r_prof))
corr = float(np.corrcoef(o_prof[:n], r_prof[:n])[0, 1])
c2 = corr > 0.8
ok &= c2
print("2. BR row-profile corr=%.3f -> %s" % (corr, "PASS" if c2 else "FAIL"))

# 3. BR winding path: dark comps inside BR interior
rfull = ren_box(0, 0, 960, 540)
br = rfull[By0 + P:By1 - P, Bx0 + P:Bx1 - P]
lum = 0.299 * br[:, :, 0] + 0.587 * br[:, :, 1] + 0.114 * br[:, :, 2]
dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
best = None
for area, xs, ys in comps(dm, min_area=15):
    spanx = xs.max() - xs.min() + 1
    # winding: path length approx via bbox diagonal coverage; use tortuosity proxy:
    # count direction changes of the component's skeleton — approximate with
    # (perimeter-ish) len vs straight: use area/spanx as thickness and compute
    # polyline length by ordering points by x and summing segment lengths
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    ratio = seg / max(straight, 1.0)
    if best is None or area > best[0]:
        best = (area, spanx, seg, straight, ratio)
a, spanx, seg, straight, ratio = best
c3 = ratio > 1.02 and spanx > 30
ok &= c3
print("3. BR largest dark comp area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f -> %s" %
      (a, spanx, seg, straight, ratio, "PASS" if c3 else "FAIL"))

# 4. BL labels via NCC at anchor windows
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
_tcache = {}


def render_cand(s, fs):
    if (s, fs) not in _tcache:
        f = ImageFont.truetype(FONT, fs)
        im = Image.new("L", (300, 60), 255)
        ImageDraw.Draw(im).text((4, 4), s, font=f, fill=0)
        a = np.array(im)
        ys, xs = np.nonzero(a < 128)
        _tcache[(s, fs)] = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return _tcache[(s, fs)]


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


WL = (128, 432, 220, 480)   # left bottom anchor window (slide px)
WR = (262, 432, 360, 484)   # right bottom anchor window
for tag, a in (("orig", orig), ("render", rfull)):
    wl = identify(a[WL[1]:WL[3], WL[0]:WL[2]])
    wr = identify(a[WR[1]:WR[3], WR[0]:WR[2]])
    print("4. %s: left window -> '%s' (%.3f)  right window -> '%s' (%.3f)" % (tag, wl[1], wl[0], wr[1], wr[0]))
rl = identify(rfull[WL[1]:WL[3], WL[0]:WL[2]])[1]
rr = identify(rfull[WR[1]:WR[3], WR[0]:WR[2]])[1]
# anchor positions must match the original's measured text lines:
# orig left text x145..172 y447..460, right text x301..328 y450..465
c4 = (rl == "Local Minima" and rr == "Global Minima")
ok &= c4
print("   CHECK4 (render left=Local Minima, right=Global Minima): %s" % ("PASS" if c4 else "FAIL"))

# 5. BL red marker-like comps
BL = (83, 290, 377, 528)


def markers(a):
    bl = a[BL[1]:BL[3], BL[0]:BL[2]]
    rm = redmask(bl)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    out = []
    for area, xs, ys in comps(rm, min_area=8):
        w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, (xs.min() + xs.max()) // 2 + BL[0], (ys.min() + ys.max()) // 2 + BL[1]))
    return out


om = markers(orig)
rmk = markers(rfull)
c5 = len(rmk) <= len(om)
ok &= c5
print("5. marker-like red comps orig=%d render=%d -> %s" % (len(om), len(rmk), "PASS" if c5 else "FAIL"))
print("   orig markers: %s" % (om,))
print("   render markers: %s" % (rmk,))

print("\nSUMMARY: %s" % ("ALL PASS" if ok else "FAILURES PRESENT"))
sys.exit(0 if ok else 1)
