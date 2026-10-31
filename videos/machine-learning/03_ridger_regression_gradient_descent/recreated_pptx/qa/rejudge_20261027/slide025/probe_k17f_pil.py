#!/usr/bin/env python3
"""PIL probe for slide 025 k17f assets vs the original frame.

Composites the four assets_k17f PNGs at the exact addImage rects from
build/slide_025.js (TL x85 y115 w180 h173; TR x616 y115 w263 h202;
BL x83 y290 w293 h237; BR x615 y344 w265 h187) onto a 960x540 white canvas
(PNGs are 300dpi at figsize=box_px/72, so downscaled to box_px here), then
vs unique_slides/slide_025.jpg:

  MD5    md5 of each k17f PNG vs the assets_k15 counterpart (must differ).
  CHECK1 BR bottom band slide x672..816 y472..517: total pixel diff%
         (sum|d|>60). PASS if < 50% (k15/k16 render was 97.9%).
  CHECK2 BL labels at the four task anchors: best 2-line glyph-template match:
           x236..278 y302..322 -> 'Global Minima'
           x325..350 y388..401 -> 'Local Minima'
           x138..205 y438..470 -> 'Local Minima'
           x300..346 y448..470 -> 'Global Minima'
  CHECK3 TR red segment (652,189)->(667,165): red-hit within 2px along the
         segment (orig 54%, k15 render 0%); BR winding ratio (~6.0);
         BL markers exactly 2 at (199,445),(270,482).

Writes the full report to pil_k17f_out.txt next to this script.
Does NOT touch any pptx/DB/deck/result file.
"""
import hashlib
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ASSETS = RJ + "/assets_k17f"
K15 = RJ + "/assets_k15"
OUT = RJ + "/pil_k17f_out.txt"

ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

# exact addImage rects from recreated_pptx/build/slide_025.js
PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
    "bl": dict(x0=83,  y0=290, w=293, h=237),
    "br": dict(x0=615, y0=344, w=265, h=187),
}

lines = []


def emit(s=""):
    lines.append(s)
    print(s)


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


emit("pil_k17f_out.txt — slide 025 assets_k17f vs unique_slides/slide_025.jpg")
emit("composite: 4 PNGs pasted at build/slide_025.js addImage rects on 960x540 white canvas")
emit("  rects: TL x85 y115 w180 h173 | TR x616 y115 w263 h202 | BL x83 y290 w293 h237 | BR x615 y344 w265 h187")
emit("")
emit("== 0. MD5: assets_k17f vs assets_k15 ==")
md5ok = True
for k in ("tl", "tr", "bl", "br"):
    m17 = md5(os.path.join(ASSETS, "plot_025_%s.png" % k))
    m15 = md5(os.path.join(K15, "plot_025_%s.png" % k))
    d = m17 != m15
    md5ok &= d
    emit("  %s: k17f=%s k15=%s differ=%s" % (k, m17, m15, d))
emit("  md5 all differ from k15: %s" % ("PASS" if md5ok else "FAIL"))

canvas = np.full((540, 960, 3), 255, np.int32)
for k, s in PLOTS.items():
    im = Image.open(os.path.join(ASSETS, "plot_025_%s.png" % k)).convert("RGB")
    emit("  %s png native size=%s -> pasted at (%d,%d) %dx%d" % (k, im.size, s["x0"], s["y0"], s["w"], s["h"]))
    im = im.resize((s["w"], s["h"]), Image.NEAREST)  # same filter as verify_k17f.py
    canvas[s["y0"]:s["y0"] + s["h"], s["x0"]:s["x0"] + s["w"]] = np.asarray(im).astype(np.int32)
REN = canvas


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
    return out


# ── CHECK1: BR bottom band ────────────────────────────────────────────────────
emit("")
emit("== CHECK1: BR bottom band slide x672..816 y472..517 diff vs orig ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = ORIG[by0:by1, bx0:bx1]
rb = REN[by0:by1, bx0:bx1]
diff = (np.abs(ob - rb).sum(2) > 60)
H, W = diff.shape
gx, gy = 12, 5
mx = 0
cell_area = (H // gy) * (W // gx)
for iy in range(gy):
    row = []
    for ix in range(gx):
        c = diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx]
        row.append(int(c.sum()))
        mx = max(mx, int(c.sum()))
    emit("  cell row: %s" % row)
band_pct = 100.0 * diff.mean()
c1 = band_pct < 50.0
emit("  band %dx%d total diff px=%d (%.1f%%), maxcell=%d/%d (%.1f%% solid)"
     % (W, H, diff.sum(), band_pct, mx, cell_area, 100.0 * mx / cell_area))
emit("  k15 render was 97.9%%; CHECK1 PASS if < 50%%: %s" % ("PASS" if c1 else "FAIL"))


def colmask(a):
    mx_, mn_ = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx_ - mn_) > 30) & (mx_ > 90) & ~red


op = 100.0 * colmask(ORIG[344:531, 615:880]).mean(1)
rp = 100.0 * colmask(REN[344:531, 615:880]).mean(1)
emit("  row colored%% y472..528 orig: " + " ".join("%d:%.0f" % (344 + i, op[i]) for i in range(472 - 344, 529 - 344)))
emit("  row colored%% y472..528 k17f: " + " ".join("%d:%.0f" % (344 + i, rp[i]) for i in range(472 - 344, 529 - 344)))

# ── CHECK2: BL labels at anchors ──────────────────────────────────────────────
emit("")
emit("== CHECK2: BL labels at task anchors (2-line glyph-template ID) ==")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]


def render_cand(s, fs, two_line):
    f = ImageFont.truetype(FONT, fs)
    parts = s.split(" ", 1) if two_line else [s]
    ims = []
    for p in parts:
        im = Image.new("L", (220, 40), 0)
        ImageDraw.Draw(im).text((4, 4), p, font=f, fill=255)
        a = np.array(im)
        ys, xs = np.nonzero(a > 128)
        ims.append(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    w = max(i.shape[1] for i in ims)
    h = sum(i.shape[0] for i in ims) + 2 * (len(ims) - 1)
    out = np.zeros((h, w), np.float32)
    y = 0
    for i in ims:
        out[y:y + i.shape[0], :i.shape[1]] = i
        y += i.shape[0] + 2
    return out


def iou(a, b):
    inter = np.logical_and(a > 0, b > 0).sum()
    union = np.logical_or(a > 0, b > 0).sum()
    return inter / max(union, 1)


def id_label(a, x0, y0, x1, y1):
    crop = a[y0:y1, x0:x1]
    L = lum(crop)
    med = np.median(L)
    ink = (L < med - 45) | (L < 90)
    ys, xs = np.nonzero(ink)
    if len(xs) < 6:
        return 0, "?", None
    ic = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = ic.shape
    best = (0.0, "?")
    for s in CANDS:
        for tl in (False, True):
            for fs in range(7, 14):
                c = render_cand(s, fs, tl)
                cr = np.array(Image.fromarray((c > 0).astype(np.uint8) * 255).resize((w, h), Image.BILINEAR))
                v = iou(ic, cr)
                if v > best[0]:
                    best = (v, s)
    return len(xs), best[1], round(best[0], 3)


ANCHORS = [
    ("top    x236..278 y302..322", 236, 302, 279, 323, "Global Minima"),
    ("right-m x325..350 y388..401", 325, 388, 351, 402, "Local Minima"),
    ("low-L  x138..205 y438..470", 138, 438, 206, 471, "Local Minima"),
    ("low-R  x300..346 y448..470", 300, 448, 347, 471, "Global Minima"),
]
ok2 = True
for name, x0, y0, x1, y1, want in ANCHORS:
    for tag, a in (("orig", ORIG), ("k17f", REN)):
        n, got, sc = id_label(a, max(0, x0 - 4), max(0, y0 - 4), min(960, x1 + 4), min(540, y1 + 4))
        mark = ""
        if tag == "k17f":
            mark = "OK" if got == want else "MISMATCH(want '%s')" % want
            if got != want:
                ok2 = False
        emit("  %s %-28s ink=%d -> '%s' iou=%s %s" % (tag, name, n, got, sc, mark))
emit("  CHECK2 (all four anchors read the expected string in k17f): %s" % ("PASS" if ok2 else "FAIL"))

# ── CHECK3: TR red segment ────────────────────────────────────────────────────
emit("")
emit("== CHECK3: TR red segment (652,189)->(667,165) red-hit within 2px ==")


def seg_cov(a, x0, y0, x1, y1):
    rm = redmask(a)
    n = 200
    hit = 0
    for i in range(n):
        t = i / (n - 1)
        x = int(round(x0 + (x1 - x0) * t))
        y = int(round(y0 + (y1 - y0) * t))
        win = rm[max(0, y - 2):y + 3, max(0, x - 2):x + 3]
        if win.any():
            hit += 1
    return hit, n


for tag, a in (("orig", ORIG), ("k17f", REN)):
    h, n = seg_cov(a, 652, 189, 667, 165)
    emit("  %s diag red-hit %d/%d = %.0f%%" % (tag, h, n, 100.0 * h / n))
h, n = seg_cov(REN, 652, 189, 667, 165)
ok3 = h / n >= 0.40
emit("  CHECK3 (k17f segment red-hit >= 40%%; orig 54%%, k15 render 0%%): %s" % ("PASS" if ok3 else "FAIL"))

# ── winding: BR largest dark comp ─────────────────────────────────────────────
emit("")
emit("== BR winding ratio (largest dark comp, BR panel; target ~6.0, k16 was 6.020) ==")


def wind_ratio(a):
    br = a[344 + 8:531 - 8, 615 + 8:880 - 8]
    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    best = None
    for area, x0, y0, x1, y1 in comps(dm, min_area=15):
        if best is None or area > best[0]:
            best = (area, x0, y0, x1, y1)
    if best is None:
        return None, None
    area, x0, y0, x1, y1 = best
    ys, xs = np.nonzero(dm[y0:y1 + 1, x0:x1 + 1])
    order = np.argsort(xs)
    px, py = xs[order].astype(float), ys[order].astype(float)
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    return seg / max(straight, 1.0), (area, 615 + x0, 344 + y0, 615 + x1, 344 + y1)


for tag, a in (("orig", ORIG), ("k17f", REN)):
    wr, bb = wind_ratio(a)
    emit("  %s wind-ratio=%s comp=%s" % (tag, ("%.3f" % wr) if wr else "?", bb))
wr, _ = wind_ratio(REN)
okA = wr is not None and 5.0 <= wr <= 7.0
emit("  winding (target ~6.0): %s" % ("PASS" if okA else "FAIL"))

# ── markers: BL red marker-like comps ─────────────────────────────────────────
emit("")
emit("== BL marker-like red comps (expect exactly 2 at (199,445),(270,482)) ==")


def markers(a):
    bl = a[290:528, 83:377]
    rm = redmask(bl)
    rm[:8, :] = False
    rm[-8:, :] = False
    rm[:, :8] = False
    rm[:, -8:] = False
    rm[413 - 290:423 - 290, :] = False
    out = []
    for area, x0, y0, x1, y1 in comps(rm, min_area=8):
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, (x0 + x1) // 2 + 83, (y0 + y1) // 2 + 290))
    return out


for tag, a in (("orig", ORIG), ("k17f", REN)):
    emit("  %s marker-like: %s" % (tag, markers(a)))
mk = markers(REN)
okB = (len(mk) == 2
       and any(abs(x - 199) <= 8 and abs(y - 445) <= 8 for _, x, y in mk)
       and any(abs(x - 270) <= 8 and abs(y - 482) <= 8 for _, x, y in mk))
emit("  markers exactly 2 at (199,445),(270,482) within 8px: %s" % ("PASS" if okB else "FAIL"))

emit("")
emit("SUMMARY: md5-differ=%s | CHECK1 band diff=%.1f%% (<50) %s | CHECK2 labels %s | "
     "CHECK3 TR red-hit=%.0f%% %s | winding=%.3f %s | markers=%s %s"
     % ("PASS" if md5ok else "FAIL", band_pct, "PASS" if c1 else "FAIL",
        "PASS" if ok2 else "FAIL", 100.0 * h / n, "PASS" if ok3 else "FAIL",
        wr if wr else -1, "PASS" if okA else "FAIL", mk, "PASS" if okB else "FAIL"))
emit("PROBE_K17F_DONE")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("wrote", OUT)
