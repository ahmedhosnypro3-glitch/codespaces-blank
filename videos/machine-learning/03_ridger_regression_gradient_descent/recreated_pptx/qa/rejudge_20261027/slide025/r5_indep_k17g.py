#!/usr/bin/env python3
"""r5 independent PIL re-check of assets_k17g (own code, not the promoter's
verify script). Composites the 4 PNGs at slide_025.js placements and checks
vs unique_slides/slide_025.jpg: CHECK1 BR band diff, CHECK2 label anchors
(ink presence), CHECK3 TR red segment, winding wind-ratio in [4,7],
markers at (199,445),(270,482). Writes pil_r5_indep_k17g.txt.
"""
import hashlib
import os
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ASSETS = os.path.join(RJ, "assets_k17g")
K15 = os.path.join(RJ, "assets_k15")
OUT = os.path.join(RJ, "pil_r5_indep_k17g.txt")
L = []
def P(s=""):
    print(s); L.append(s)

ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
PLACEMENTS = [("tl", 85, 115, 180, 173), ("tr", 616, 115, 263, 202),
              ("bl", 83, 290, 293, 237), ("br", 615, 344, 265, 187)]
canvas = np.full((540, 960, 3), 255, np.int32)
canvas[45:540, 54:904] = np.array([233, 233, 231], np.int32)
for name, x, y, w, h in PLACEMENTS:
    p = os.path.join(ASSETS, "plot_025_%s.png" % name)
    im = Image.open(p).convert("RGB").resize((w, h), Image.NEAREST)
    canvas[y:y+h, x:x+w] = np.asarray(im).astype(np.int32)
REN = canvas

P("r5 independent check assets_k17g")
for name, *_ in PLACEMENTS:
    a = hashlib.md5(open(os.path.join(ASSETS, "plot_025_%s.png" % name), "rb").read()).hexdigest()
    b = hashlib.md5(open(os.path.join(K15, "plot_025_%s.png" % name), "rb").read()).hexdigest()
    P("  %s md5=%s k15=%s differ=%s" % (name, a[:12], b[:12], a != b))

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

# CHECK1: BR band x672..816 y472..528 diff vs orig
d = np.abs(REN[472:529, 672:817] - ORIG[472:529, 672:817]).sum(axis=2)
P("CHECK1 BR band x672..816 y472..528: diff px=%d (%.1f%%) -> %s"
  % (int((d > 60).sum()), 100.0 * (d > 60).sum() / d.size, "PASS" if (d > 60).mean() < 0.5 else "FAIL"))

# CHECK2: dark ink present in each BL label anchor box (render side)
for tag, (x0, y0, x1, y1) in {
    "top(Global Minima)": (236, 302, 278, 322), "right-m(Local Minima)": (325, 388, 350, 401),
    "low-L(Local Minima)": (138, 438, 205, 470), "low-R(Global Minima)": (300, 448, 346, 470)}.items():
    ink = int(((REN[y0:y1, x0:x1].mean(axis=2) < 120)).sum())
    P("CHECK2 anchor %-22s render ink=%d -> %s" % (tag, ink, "OK" if ink > 20 else "MISS"))

# CHECK3: TR red segment (652,189)->(667,165), red-hit within 2px
seg = np.array([(652 + 15 * t / 24.0, 189 - 24 * t / 24.0) for t in range(25)])
def redhit(a):
    hits = 0
    for x, y in seg:
        x, y = int(round(x)), int(round(y))
        win = redmask(a[max(0, y-2):y+3, max(0, x-2):x+3])
        hits += int(win.any())
    return 100.0 * hits / len(seg)
P("CHECK3 TR segment red-hit: orig=%.0f%% ren=%.0f%% -> %s"
  % (redhit(ORIG), redhit(REN), "PASS" if redhit(REN) >= 20 else "FAIL"))

# winding: largest dark comp in BR panel region (exclude red frame)
br = REN[344:532, 615:881]
lum = br.mean(axis=2)
dark = (lum < 100)
lab, n = ndimage.label(dark, structure=np.ones((3, 3)))
best = None
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 50:
        continue
    pts = np.stack([xs, ys], 1).astype(float)
    # path length: order by x, sum consecutive distances (approx)
    order = np.argsort(pts[:, 0])
    p = pts[order]
    seglen = np.hypot(np.diff(p[:, 0]), np.diff(p[:, 1])).sum()
    straight = np.hypot(p[-1, 0] - p[0, 0], p[-1, 1] - p[0, 1])
    wr = seglen / max(straight, 1e-6)
    if best is None or len(xs) > best[0]:
        best = (len(xs), p[:, 0].max() - p[:, 0].min(), seglen, straight, wr)
if best:
    P("winding BR largest dark comp: area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f -> %s"
      % (best[0], best[1], best[2], best[3], best[4], "PASS" if 4 <= best[4] <= 7 else "FAIL"))
else:
    P("winding: no comp found -> FAIL")

# markers: red comps centered within 6px of targets
def markers(a):
    lab, n = ndimage.label(redmask(a), structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 12:
            continue
        cx, cy = xs.mean(), ys.mean()
        out.append((len(xs), round(cx, 1), round(cy, 1)))
    return out
mo = markers(ORIG[290:528, 83:377])
mr = markers(REN[290:528, 83:377])
def near(ms, tx, ty):
    return [(a, x + 83, y + 290) for a, x, y in ms if abs(x + 83 - tx) <= 6 and abs(y + 290 - ty) <= 6]
P("markers orig (panel-local): %s" % mo)
P("markers ren  (panel-local): %s" % mr)
t1 = near(mr, 199, 445); t2 = near(mr, 270, 482)
P("markers at (199,445): %s  at (270,482): %s -> %s"
  % (t1, t2, "PASS" if t1 and t2 else "FAIL"))

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
