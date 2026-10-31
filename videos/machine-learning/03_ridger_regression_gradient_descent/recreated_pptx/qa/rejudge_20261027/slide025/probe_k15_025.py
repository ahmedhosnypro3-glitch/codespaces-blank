#!/usr/bin/env python3
"""PIL ground-truth probe v2 of unique_slides/slide_025.jpg for the k15 fix."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ren_img = Image.open(RJ + "/slide025/render.png").convert("RGB")
SX, SY = ren_img.size[0] / 960.0, ren_img.size[1] / 540.0

def ren_box(x0, y0, x1, y1):
    c = ren_img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))
    return np.array(c.resize((x1 - x0, y1 - y0), Image.BILINEAR)).astype(np.int32)

PANELS = dict(tl=(85, 115, 266, 289), tr=(616, 115, 880, 318),
              bl=(83, 290, 377, 528), br=(615, 344, 881, 532))

def colored(a, thr=50):
    return (a.max(2) - a.min(2)) > thr

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def darkmask(a, thr=140, sat=75):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)

def lum(a):
    return (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])

def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append([len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), i, lab])
    return out

JETLUT = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255)
def jet_t(a, cm):
    px = a[cm].astype(np.float32)
    d2 = ((px[:, None, :] - JETLUT[None, :, :]) ** 2).sum(2)
    return d2.argmin(1) / 255.0

# ── A. BL label anchors via ink clusters + NCC template ID ───────────────────
print("== A. BL label anchors (orig) ==")
x0, y0, x1, y1 = PANELS["bl"]
bl = orig[y0:y1, x0:x1]
dm = darkmask(bl, thr=145, sat=80)
dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
dm[413 - y0:423 - y0, :] = False
cs = comps(dm, min_area=5)
words = []
for area, wx0, wy0, wx1, wy1, _, _ in cs:
    w, h = wx1 - wx0 + 1, wy1 - wy0 + 1
    if w > 25 and h <= 9:      # leader line
        continue
    if w > 40 and h < 3 * w // 4:
        continue
    words.append([wx0, wy0, wx1, wy1])
# cluster glyphs into words (x-gap<7, y-center<6), words into labels (x-gap<14, y-band<8; stack 2-line)
groups = []
for b in sorted(words, key=lambda b: (b[1], b[0])):
    hit = None
    for G in groups:
        if abs((b[1] + b[3]) / 2 - (G[1] + G[3]) / 2) < 6 and (b[0] - G[2] < 7 or G[0] - b[2] < 7):
            hit = G
            break
    if hit:
        hit[0] = min(hit[0], b[0]); hit[1] = min(hit[1], b[1]); hit[2] = max(hit[2], b[2]); hit[3] = max(hit[3], b[3])
    else:
        groups.append([b[0], b[1], b[2], b[3]])
labels = []
for G in sorted(groups, key=lambda g: (g[1], g[0])):
    hit = None
    for L in labels:
        yc = (L[1] + L[3]) / 2; gc = (G[1] + G[3]) / 2
        if abs(yc - gc) < 8 and (G[0] - L[2] < 16 or L[0] - G[2] < 16):
            hit = L
            break
    if hit is None:
        for L in labels:  # two-line stack: x-overlap, y-gap < 12
            if G[0] < L[2] and L[0] < G[2] and 0 <= G[1] - L[3] < 12:
                hit = L
                break
    if hit:
        hit[0] = min(hit[0], G[0]); hit[1] = min(hit[1], G[1]); hit[2] = max(hit[2], G[2]); hit[3] = max(hit[3], G[3])
    else:
        labels.append([G[0], G[1], G[2], G[3]])

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
def render_cand(s, fs, two_line):
    f = ImageFont.truetype(FONT, fs)
    parts = s.split(" ", 1) if two_line else [s]
    ims = []
    for p in parts:
        im = Image.new("L", (200, 40), 255)
        ImageDraw.Draw(im).text((4, 4), p, font=f, fill=0)
        a = np.array(im)
        ys, xs = np.nonzero(a < 128)
        ims.append(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    w = max(i.shape[1] for i in ims); h = sum(i.shape[0] for i in ims) + 2 * (len(ims) - 1)
    out = np.full((h, w), 255, np.float32)
    y = 0
    for i in ims:
        out[y:y + i.shape[0], :i.shape[1]] = i
        y += i.shape[0] + 2
    return out
def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den > 0 else -1.0
print("detected label boxes (slide px) + template ID:")
for L in sorted(labels, key=lambda l: l[1]):
    w = L[2] - L[0] + 1; h = L[3] - L[1] + 1
    if w < 14 or h < 5:
        continue
    crop = lum(bl[L[1]:L[3] + 1, L[0]:L[2] + 1]).astype(np.float32)
    best = (-2, "?", None)
    for s in CANDS:
        for tl in (False, True):
            for fs in range(7, 16):
                c = render_cand(s, fs, tl)
                cr = np.array(Image.fromarray(c.astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32)
                v = ncc(crop, cr)
                if v > best[0]:
                    best = (v, s, tl)
    print("  slide x%d..%d y%d..%d (w=%d h=%d) -> '%s' (2line=%s) ncc=%.3f"
          % (L[0] + x0, L[2] + x0, L[1] + y0, L[3] + y0, w, h, best[1], best[2], best[0]))

# ── B. BL red-x marker candidates ────────────────────────────────────────────
print("\n== B. BL red comps, marker-like (area 12..200, bbox 4..16 sq, fill>0.3) ==")
for name, a in (("orig", bl), ("render", ren_box(*PANELS["bl"]))):
    rm = redmask(a)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - y0:423 - y0, :] = False
    for area, rx0, ry0, rx1, ry1, _, _ in comps(rm, min_area=8):
        w, h = rx1 - rx0 + 1, ry1 - ry0 + 1
        tag = ""
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            tag = "  <-- MARKER-LIKE at slide (%d,%d)" % ((rx0 + rx1) // 2 + x0, (ry0 + ry1) // 2 + y0)
        if area > 300 or tag:
            print("  %s: area=%d local x%d..%d y%d..%d%s" % (name, area, rx0, rx1, ry0, ry1, tag))

# ── C. BR surface silhouette / jet-t diagonal roughness ─────────────────────
print("\n== C. BR surface (frame border 8px excluded) ==")
x0, y0, x1, y1 = PANELS["br"]
for name, a in (("orig", orig[y0:y1, x0:x1]), ("render", ren_box(*PANELS["br"]))):
    cm = colored(a)
    cm[:8, :] = False; cm[-8:, :] = False; cm[:, :8] = False; cm[:, -8:] = False
    ys, xs = np.nonzero(cm)
    print("  %s: surf bbox local x%d..%d y%d..%d (slide x%d..%d y%d..%d) colored%%=%.1f"
          % (name, xs.min(), xs.max(), ys.min(), ys.max(), xs.min() + x0, xs.max() + x0,
             ys.min() + y0, ys.max() + y0, 100.0 * cm.mean()))
    t = jet_t(a, cm)
    h16, _ = np.histogram(t, bins=16, range=(0, 1))
    print("  %s: jet-t hist/16: %s bins>8%%=%d" % (name, h16.tolist(), int((h16 > 0.08 * h16.sum()).sum())))
    # jet-t profile along main diagonal of surface bbox (z roughness)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    n = 100
    diag_t = []
    for i in range(n):
        xx = int(bx0 + (bx1 - bx0) * i / (n - 1)); yy = int(by0 + (by1 - by0) * i / (n - 1))
        if cm[yy, xx]:
            px = a[yy, xx].astype(np.float32)
            diag_t.append(float(((JETLUT - px) ** 2).sum(1).argmin()) / 255.0)
    diag_t = np.array(diag_t)
    if len(diag_t) > 10:
        sm = ndimage.uniform_filter1d(diag_t, 5)
        d = np.diff(sm)
        ext = int(np.sum(d[:-1] * d[1:] < 0))
        print("  %s: main-diag jet-t: mean=%.2f std=%.3f min=%.2f max=%.2f extrema=%d"
              % (name, diag_t.mean(), diag_t.std(), diag_t.min(), diag_t.max(), ext))

# ── A2. ASCII ink map of BL panel (orig): dark low-sat ink '#', red 'R' ─────
print("\n== A2. BL panel ASCII map (orig), 3px cells, box x83..376 y290..527 ==")
x0, y0, x1, y1 = PANELS["bl"]
bl = orig[y0:y1, x0:x1]
dm = darkmask(bl, thr=145, sat=80)
rm = redmask(bl)
cm = colored(bl) & ~rm
H, W = dm.shape
for yy in range(0, H - 2, 3):
    row = ""
    for xx in range(0, W - 2, 3):
        d = dm[yy:yy + 3, xx:xx + 3].mean()
        r = rm[yy:yy + 3, xx:xx + 3].mean()
        c = cm[yy:yy + 3, xx:xx + 3].mean()
        row += "#" if d > 0.25 else ("R" if r > 0.25 else ("o" if c > 0.3 else "."))
    print("  y%03d %s" % (yy + y0, row))

# ── D. BR bottom margin ─────────────────────────────────────────────────────
print("\n== D. BR bottom margin: per-row colored%% rows y455..540 (BR cols x615..880) ==")
for name, a in (("orig", orig), ("render", ren_box(0, 0, 960, 540))):
    line = []
    for yy in range(455, 540):
        row = a[yy:yy + 1, 615:881, :]
        line.append("%d:%.0f" % (yy, 100.0 * colored(row).mean()))
    print("  %s: %s" % (name, " ".join(line)))
for name, a in (("orig", orig), ("render", ren_box(0, 0, 960, 540))):
    rows = [100.0 * colored(a[yy:yy + 1, 615:881, :]).mean() for yy in range(344, 532)]
    hot = [344 + i for i, v in enumerate(rows) if v > 20]
    print("  %s: BR rows>20%% colored: y%d..%d (box y344..531); rows>20%% below y500: %s"
          % (name, min(hot), max(hot), [344 + i for i, v in enumerate(rows) if v > 20 and 344 + i > 500]))

# ── E. BR black GD path ──────────────────────────────────────────────────────
print("\n== E. BR black path (lum<100, low-sat, frame excluded) ==")
for name, a in (("orig", orig[y0:y1, x0:x1]), ("render", ren_box(*PANELS["br"]))):
    L = lum(a)
    dm = (L < 100) & ((a.max(2) - a.min(2)) < 60)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    cs = comps(dm, min_area=8)
    cs.sort(key=lambda c: -c[0])
    print("  %s: top dark comps:" % name, [(c[0], c[1], c[2], c[3], c[4]) for c in cs[:8]])
    if cs:
        c = cs[0]
        lab = c[6]
        ys, xs = np.nonzero(lab == c[5])
        ux = np.unique(xs)
        my = np.array([ys[xs == u].mean() for u in ux])
        d = np.diff(my)
        wind = int(np.sum(d[:-1] * d[1:] < 0)) if len(d) > 2 else 0
        plen = float(np.sum(np.hypot(np.diff(ux), np.diff(my))))
        span = float(np.hypot(ux[-1] - ux[0], my[-1] - my[0]))
        print("  %s: largest: area=%d slide-x %d..%d slide-y %d..%d | x-span=%d winding=%d len=%.1f straight=%.1f wind-ratio=%.2f"
              % (name, c[0], xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0,
                 ux[-1] - ux[0], wind, plen, span, plen / max(span, 1e-9)))

# ── F. TR red geometry ───────────────────────────────────────────────────────
print("\n== F. TR red ink: horizontal runs vs residual (frame excluded) ==")
x0, y0, x1, y1 = PANELS["tr"]
for name, a in (("orig", orig[y0:y1, x0:x1]), ("render", ren_box(*PANELS["tr"]))):
    rm = redmask(a)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    H, W = rm.shape
    horiz = np.zeros_like(rm)
    for r in range(H):
        row = rm[r]; x = 0
        while x < W:
            if row[x]:
                x2 = x
                while x2 + 1 < W and row[x2 + 1]:
                    x2 += 1
                if x2 - x + 1 >= 12:
                    horiz[r, x:x2 + 1] = True
                x = x2 + 1
            else:
                x += 1
    resid = rm & ~horiz
    print("  %s: red=%d horiz=%d resid=%d" % (name, rm.sum(), horiz.sum(), resid.sum()))
    for area, rx0, ry0, rx1, ry1, _, lab in comps(resid, min_area=6):
        if area < 20:
            continue
        ys, xs = np.nonzero(lab == ry0 * 0 + 0)  # placeholder
        sub = (lab[ry0:ry1 + 1, rx0:rx1 + 1] == lab[ry0, rx0]) if lab[ry0, rx0] else None
        yy, xx = np.nonzero(resid[ry0:ry1 + 1, rx0:rx1 + 1])
        xx = xx + rx0; yy = yy + ry0
        slope = float(np.cov(xx, yy)[0, 1] / xx.var()) if len(xx) > 2 and xx.var() > 1 else float("nan")
        print("    resid area=%d slide x%d..%d y%d..%d slope=%.3f" % (area, rx0 + x0, rx1 + x0, ry0 + y0, ry1 + y0, slope))

# ── G. TR bowl profile ───────────────────────────────────────────────────────
print("\n== G. TR surface: bbox, top-silhouette bowl sign, jet-t center vs rim ==")
for name, a in (("orig", orig[y0:y1, x0:x1]), ("render", ren_box(*PANELS["tr"]))):
    cm = colored(a)
    cm[:8, :] = False; cm[-8:, :] = False; cm[:, :8] = False; cm[:, -8:] = False
    ys, xs = np.nonzero(cm)
    print("  %s: surf bbox slide x%d..%d y%d..%d colored%%=%.1f" % (name, xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0, 100 * cm.mean()))
    top = np.full(cm.shape[1], -1, np.int32)
    for x in range(cm.shape[1]):
        yy = np.nonzero(cm[:, x])[0]
        if len(yy):
            top[x] = yy[0]
    v = top >= 0
    xsv = np.nonzero(v)[0]
    prof = top[xsv].astype(float)
    n = len(prof)
    c = prof[n // 2]
    edges = np.concatenate([prof[:max(1, n // 6)], prof[-max(1, n // 6):]])
    print("  %s: top-silhouette center=%.1f edges=%.1f center-minus-edges=%+.2f" % (name, c, edges.mean(), c - edges.mean()))
    t = jet_t(a, cm)
    tt = np.full(cm.shape, np.nan)
    tt[cm] = t
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    ccx0, ccx1 = bx0 + (bx1 - bx0) // 3, bx1 - (bx1 - bx0) // 3
    ccy0, ccy1 = by0 + (by1 - by0) // 3, by1 - (by1 - by0) // 3
    ctr = tt[ccy0:ccy1, ccx0:ccx1]
    rim = tt[by0:by1, bx0:bx1]
    rim = rim[~np.isnan(rim)]
    ctr = ctr[~np.isnan(ctr)]
    print("  %s: jet-t center=%.2f rim=%.2f (low t = blue floor)" % (name, np.nanmean(ctr), np.nanmean(rim)))

print("\nPROBE_DONE")
