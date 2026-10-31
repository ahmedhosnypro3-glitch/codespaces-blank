#!/usr/bin/env python3
"""Focused ground truth: BL label string IDs, TR slanted-segment coverage, BR ASCII map + path."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ren_img = Image.open(RJ + "/slide025/render.png").convert("RGB")
SX, SY = ren_img.size[0] / 960.0, ren_img.size[1] / 540.0

def ren_box(x0, y0, x1, y1):
    c = ren_img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))
    return np.array(c.resize((x1 - x0, y1 - y0), Image.BILINEAR)).astype(np.int32)

def lum(a):
    return (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def colored(a, thr=50):
    return (a.max(2) - a.min(2)) > thr

# ── 1. BL label string ID: adaptive-binarized crop vs rendered candidates ────
print("== 1. BL label ID (orig) ==")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
REGIONS = {
    "top     (x236..278 y302..322)": (236, 302, 279, 323),
    "right-up(x318..352 y335..356)": (318, 335, 353, 357),
    "right-m (x325..350 y388..401)": (325, 388, 351, 402),
    "left-m  (x105..170 y388..410)": (105, 388, 170, 411),
    "low-L   (x138..205 y438..470)": (138, 438, 206, 471),
    "low-R   (x300..346 y448..470)": (300, 448, 347, 471),
}
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
    w = max(i.shape[1] for i in ims); h = sum(i.shape[0] for i in ims) + 2 * (len(ims) - 1)
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
for name, (x0, y0, x1, y1) in REGIONS.items():
    crop = orig[y0:y1, x0:x1]
    L = lum(crop)
    med = np.median(L)
    ink = (L < med - 45) | (L < 90)
    ys, xs = np.nonzero(ink)
    if len(xs) < 6:
        print("  %s: too little ink (%d px)" % (name, len(xs)))
        continue
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    ic = ink[by0:by1 + 1, bx0:bx1 + 1]
    h, w = ic.shape
    best = []
    for s in CANDS:
        for tl in (False, True):
            for fs in range(7, 14):
                c = render_cand(s, fs, tl)
                cr = np.array(Image.fromarray((c > 0).astype(np.uint8) * 255).resize((w, h), Image.BILINEAR))
                best.append((iou(ic, cr), s, tl, fs))
    best.sort(reverse=True)
    print("  %s ink w=%d h=%d -> %s" % (name, w, h, ", ".join("'%s'(2l=%d,fs=%d) iou=%.2f" % (b[1], b[2], b[3], b[0]) for b in best[:3])))

# ── 2. TR slanted red segment coverage in orig vs render ─────────────────────
print("\n== 2. TR red coverage along candidate slanted segments (within 2px) ==")
def seg_cov(a, x0, y0, x1, y1, box):
    rm = redmask(a)
    n = 200
    hit = 0; tot = 0
    for i in range(n):
        t = i / (n - 1)
        x = int(round(x0 + (x1 - x0) * t)); y = int(round(y0 + (y1 - y0) * t))
        loc_x, loc_y = x - box[0], y - box[1]
        if 0 <= loc_y < rm.shape[0] and 0 <= loc_x < rm.shape[1]:
            win = rm[max(0, loc_y - 2):loc_y + 3, max(0, loc_x - 2):loc_x + 3]
            tot += 1
            if win.any():
                hit += 1
    return hit, tot
trb = (616, 115, 880, 318)
SEGS = {
    "A build (655,189)->(860,209)": (655, 189, 860, 209),
    "B build (737,210)->(755,225)": (737, 210, 755, 225),
    "orig-diag (652,189)->(667,165)": (652, 189, 667, 165),
    "ctrl horizontal y226 x633..875": (633, 226, 875, 226),
}
for name, a in (("orig", orig[trb[1]:trb[3], trb[0]:trb[2]]),
                ("render", ren_box(*trb))):
    for sn, (sx0, sy0, sx1, sy1) in SEGS.items():
        h, t = seg_cov(a, sx0, sy0, sx1, sy1, (trb[0], trb[1]))  # box=(bx,by)
        print("  %s %-34s red-hit %d/%d = %.0f%%" % (name, sn, h, t, 100.0 * h / max(t, 1)))

# ── 1b. low-L vs low-R direct comparison + first-word ID ────────────────────
print("\n== 1b. low-L vs low-R ink cross-match (are the two labels the same string?) ==")
def ink_of(x0, y0, x1, y1):
    crop = orig[y0:y1, x0:x1]
    L = lum(crop)
    med = np.median(L)
    ink = ((L < med - 45) | (L < 90))
    ys, xs = np.nonzero(ink)
    return ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
lowL = ink_of(138, 438, 206, 471)
lowR = ink_of(300, 448, 347, 471)
h = max(lowL.shape[0], lowR.shape[0]); w = max(lowL.shape[1], lowR.shape[1])
a = np.array(Image.fromarray((lowL > 0).astype(np.uint8) * 255).resize((w, h), Image.BILINEAR)) > 0
b = np.array(Image.fromarray((lowR > 0).astype(np.uint8) * 255).resize((w, h), Image.BILINEAR)) > 0
print("  low-L w=%d h=%d, low-R w=%d h=%d, IoU(lowL,lowR)=%.2f" % (lowL.shape[1], lowL.shape[0], lowR.shape[1], lowR.shape[0], iou(a, b)))
# first line of each vs rendered 'Local'/'Global'
def line1(ink):
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    if n == 0:
        return None
    # topmost band: rows up to first empty row gap > 2
    rowsum = ink.sum(1)
    cuts = [i for i in range(1, len(rowsum)) if rowsum[i] == 0 and rowsum[i - 1] == 0]
    y1 = cuts[0] if cuts else len(rowsum)
    sub = ink[:y1]
    ys, xs = np.nonzero(sub)
    return sub[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
for nm, ink in (("low-L", lowL), ("low-R", lowR), ("top", ink_of(236, 302, 279, 323))):
    l1 = line1(ink)
    if l1 is None:
        continue
    hh, ww = l1.shape
    scores = []
    for w_ in ("Local", "Global"):
        best = 0
        for fs in range(6, 13):
            c = render_cand(w_, fs, False)
            cr = np.array(Image.fromarray((c > 0).astype(np.uint8) * 255).resize((ww, hh), Image.BILINEAR)) > 0
            best = max(best, iou(l1, cr))
        scores.append((best, w_))
    scores.sort(reverse=True)
    print("  %s line1 w=%d h=%d -> %s" % (nm, ww, hh, ", ".join("'%s' iou=%.2f" % (s[1], s[0]) for s in scores)))

# ── 3. BR ASCII map (orig) ───────────────────────────────────────────────────
print("\n== 3. BR panel ASCII map (orig), 3px cells, box x615..880 y344..531 ==")
x0, y0, x1, y1 = 615, 344, 881, 532
br = orig[y0:y1, x0:x1]
rm = redmask(br); cm = colored(br) & ~rm
L = lum(br)
dk = (L < 110) & ((br.max(2) - br.min(2)) < 70)
gr = (L >= 110) & (L < 200) & ((br.max(2) - br.min(2)) < 70)  # gray mesh/ticks
H, W = br.shape[:2]
for yy in range(0, H - 2, 3):
    row = ""
    for xx in range(0, W - 2, 3):
        sl = (slice(yy, yy + 3), slice(xx, xx + 3))
        if rm[sl].mean() > 0.2:
            row += "R"
        elif dk[sl].mean() > 0.25:
            row += "#"
        elif gr[sl].mean() > 0.3:
            row += "+"
        elif cm[sl].mean() > 0.3:
            row += "o"
        else:
            row += "."
    print("  y%03d %s" % (yy + y0, row))

# ── 4. BR path: relaxed dark mask comps with slide coords ────────────────────
print("\n== 4. BR dark comps (lum<150 sat<90, frame excluded) orig vs render ==")
for name, a in (("orig", br), ("render", ren_box(x0, y0, x1, y1))):
    L = lum(a)
    dm = (L < 150) & ((a.max(2) - a.min(2)) < 90)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= 8:
            out.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
    out.sort(reverse=True)
    print("  %s: %d comps; top:" % (name, len(out)))
    for c in out[:12]:
        print("    area=%d slide x%d..%d y%d..%d (w=%d h=%d)" % (c[0], c[1] + x0, c[3] + x0, c[2] + y0, c[4] + y0, c[3] - c[1] + 1, c[4] - c[2] + 1))
print("\nPROBE3_DONE")
