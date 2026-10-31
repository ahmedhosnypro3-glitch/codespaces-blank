#!/usr/bin/env python3
"""PIL-verify assets_k17f vs unique_slides/slide_025.jpg at slide positions.

Composites the four k17f PNGs onto a 960x540 canvas at their exact slide
rects (from build/slide_025.js addImage calls) and compares panel-by-panel
against the original. Writes pil_k17f_out.txt with CHECK1/2/3 + winding +
markers. Does NOT touch any pptx/DB/deck/result file.
"""
import hashlib
import os
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
A = RJ + "/assets_k17f"
A15 = RJ + "/assets_k15"
OUT_TXT = RJ + "/pil_k17f_out.txt"

PANELS = {
    "tl": (85, 115, 266, 289),
    "tr": (616, 115, 880, 318),
    "bl": (83, 290, 377, 528),
    "br": (615, 344, 881, 532),
}

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
canvas = Image.new("RGB", (960, 540), (255, 255, 255))
md5s = {}
for name, (x0, y0, x1, y1) in PANELS.items():
    p = os.path.join(A, "plot_025_%s.png" % name)
    md5s[name] = hashlib.md5(open(p, "rb").read()).hexdigest()
    im = Image.open(p).convert("RGB")
    w, h = x1 - x0, y1 - y0
    canvas.paste(im.resize((w, h), Image.BILINEAR), (x0, y0))
ren = np.array(canvas).astype(np.int32)

JET = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255).astype(np.int32)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return m & ~pr


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def jet_hist(a, box):
    x0, y0, x1, y1 = box
    p = a[y0:y1, x0:x1]
    m = colmask(p)
    px = p[m]
    if len(px) == 0:
        return np.zeros(16), 0.0, None, None
    d = ((px[:, None, :] - JET[None, :, :]) ** 2).sum(2)
    t = d.argmin(1) / 255.0
    h, _ = np.histogram(t, bins=16, range=(0, 1))
    h = h.astype(np.float64)
    if h.sum() > 0:
        h /= h.sum()
    ys, xs = np.nonzero(m)
    bbox = (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())
    return h, 100.0 * m.mean(), bbox, m


lines = []
ok = True


def emit(s):
    lines.append(s)
    print(s)


emit("pil_k17f_out.txt — k17f assets vs unique_slides/slide_025.jpg (slide px 960x540)")
emit("assets_k17f md5: " + "  ".join("plot_025_%s.png=%s" % (k, v) for k, v in md5s.items()))
k15md5 = {n: hashlib.md5(open(os.path.join(A15, "plot_025_%s.png" % n), "rb").read()).hexdigest()
          for n in PANELS}
emit("assets_k15 md5: " + "  ".join("plot_025_%s.png=%s" % (k, v) for k, v in k15md5.items()))
alldiff = all(md5s[n] != k15md5[n] for n in PANELS)
ok &= alldiff
emit("md5 all differ from assets_k15: %s" % ("PASS" if alldiff else "FAIL"))

# ── CHECK1: per-panel colored% + surface bbox close to orig ──────────────────
emit("")
emit("CHECK1: per-panel colored%% and surface bbox vs orig (tol: col +-8pp, bbox +-8px)")
c1 = True
for name, box in PANELS.items():
    ho, co, bo, _ = jet_hist(orig, box)
    hr, cr, br_, _ = jet_hist(ren, box)
    dc = abs(co - cr)
    db = max(abs(bo[0] - br_[0]), abs(bo[1] - br_[1]), abs(bo[2] - br_[2]), abs(bo[3] - br_[3]))
    p = dc <= 8.0 and db <= 8
    c1 &= p
    emit("  %s: colored orig=%.1f%% k17f=%.1f%% (d=%.1f)  bbox orig x%d..%d y%d..%d  k17f x%d..%d y%d..%d (d=%d) -> %s"
          % (name, co, cr, dc, bo[0], bo[1], bo[2], bo[3], br_[0], br_[1], br_[2], br_[3], db,
             "PASS" if p else "FAIL"))
ok &= c1
emit("CHECK1: %s" % ("PASS" if c1 else "FAIL"))

# ── CHECK2: jet-t 16-bin histogram cosine sim + 8-band row-profile corr ──────
emit("")
emit("CHECK2: per-panel jet-t hist cosine-sim (>0.80) and row-profile Pearson (>0.75)")
c2 = True
for name, box in PANELS.items():
    x0, y0, x1, y1 = box
    ho, _, _, mo = jet_hist(orig, box)
    hr, _, _, mr = jet_hist(ren, box)
    cos = float((ho * hr).sum() / max(np.sqrt((ho * ho).sum() * (hr * hr).sum()), 1e-9))
    H = mo.shape[0]
    po = [100.0 * mo[i * H // 8:(i + 1) * H // 8].mean() for i in range(8)]
    pr = [100.0 * mr[i * H // 8:(i + 1) * H // 8].mean() for i in range(8)]
    corr = float(np.corrcoef(po, pr)[0, 1])
    p = cos > 0.80 and corr > 0.75
    c2 &= p
    emit("  %s: jet-t cosine=%.3f rowprof corr=%.3f -> %s" % (name, cos, corr, "PASS" if p else "FAIL"))
ok &= c2
emit("CHECK2: %s" % ("PASS" if c2 else "FAIL"))

# ── CHECK3a: BR bottom band taper y472..528 per-row colored% corr ─────────────
emit("")
emit("CHECK3: BR bottom band taper + TR diagonal red segment")
rows = list(range(472, 529, 2))
po, pr = [], []
for y in rows:
    mo = colmask(orig[y, 620:876][None, :, :])[0]
    mr = colmask(ren[y, 620:876][None, :, :])[0]
    po.append(100 * mo.mean()); pr.append(100 * mr.mean())
corr = float(np.corrcoef(po, pr)[0, 1])
p3a = corr > 0.80
ok &= p3a
emit("  3a. BR taper y472..528 row colored%% corr=%.3f (orig %s) -> %s"
     % (corr, " ".join("%.0f" % v for v in po), "PASS" if p3a else "FAIL"))
emit("      k17f %s" % " ".join("%.0f" % v for v in pr))

# ── CHECK3b: TR diagonal red segment (652,189)->(667,165) red-hit ~54% ────────
hits = tot = 0
for f in np.linspace(0, 1, 60):
    sx = 652 + 15 * f; sy = 189 - 24 * f
    w = redmask(ren[int(sy) - 2:int(sy) + 3, int(sx) - 2:int(sx) + 3])
    tot += 1
    if w.any():
        hits += 1
hit = 100.0 * hits / tot
p3b = 40.0 <= hit <= 70.0
ok &= p3b
emit("  3b. TR diagonal (652,189)->(667,165) red-hit=%.1f%% (orig 53.3%%) -> %s"
     % (hit, "PASS" if p3b else "FAIL"))
emit("CHECK3: %s" % ("PASS" if (p3a and p3b) else "FAIL"))

# ── winding: largest dark comp in BR panel, wind-ratio (verify_k15 metric) ───
emit("")
emit("winding: BR largest dark comp wind-ratio (target ~6.02, PASS >1.02)")
bx0, by0, bx1, by1 = 615 + 8, 344 + 8, 881 - 8, 532 - 8
br = ren[by0:by1, bx0:bx1]
dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
best = None
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 15:
        continue
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    ratio = seg / max(straight, 1.0)
    if best is None or len(xs) > best[0]:
        best = (len(xs), xs.max() - xs.min() + 1, seg, straight, ratio)
a, spanx, seg, straight, ratio = best
pw = ratio > 1.02 and spanx > 30
ok &= pw
emit("  area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f -> %s"
     % (a, spanx, seg, straight, ratio, "PASS" if pw else "FAIL"))

# ── markers: marker-like red comps in BL at (199,445),(270,482) ──────────────
emit("")
emit("markers: BL marker-like red comps (target 2 at (199,445),(270,482))")
bl = ren[290:528, 83:377]
rm = redmask(bl)
rm[:8] = False; rm[-8:] = False; rm[:, :8] = False; rm[:, -8:] = False
lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
mk = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 8:
        continue
    w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
    if 12 <= len(xs) <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and len(xs) / (w * h) > 0.3:
        mk.append(((xs.min() + xs.max()) // 2 + 83, (ys.min() + ys.max()) // 2 + 290, len(xs)))
pm = len(mk) == 2 and all(min(abs(m[0] - t[0]) + abs(m[1] - t[1]) for m in mk) <= 8
                           for t in ((199, 445), (270, 482)))
ok &= pm
emit("  k17f markers: %s -> %s" % (mk, "PASS" if pm else "FAIL"))

emit("")
emit("SUMMARY: %s" % ("ALL PASS" if ok else "FAILURES PRESENT"))
with open(OUT_TXT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("wrote", OUT_TXT)
