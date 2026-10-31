#!/usr/bin/env python3
"""r5 PIL re-verify on the actual 150dpi render_k17z.png (2001x1125),
downscaled to slide space 960x540, vs unique_slides/slide_025.jpg:
CHECK1 BR band diff, CHECK2 label-anchor ink, CHECK3 TR red segment,
winding wind-ratio (dark low-sat comp, verify_k15 metric), BL markers.
Writes pil_r5_render_k17z.txt.
"""
import numpy as np, os
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
OUT = os.path.join(RJ, "pil_r5_render_k17z.txt")
L = []
def P(s=""):
    print(s); L.append(s)

r = Image.open(os.path.join(RJ, "render_k17z.png")).convert("RGB")
P("render_k17z.png size=%s" % (r.size,))
REN = np.asarray(r.resize((960, 540), Image.LANCZOS)).astype(np.int32)
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

def redmask(a):
    rr, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (rr > 110) & (rr - g > 50) & (rr - b > 50)

d = np.abs(REN[472:529, 672:817] - ORIG[472:529, 672:817]).sum(axis=2)
P("CHECK1 BR band x672..816 y472..528 diff px=%d (%.1f%%) -> %s"
  % (int((d > 60).sum()), 100.0 * (d > 60).sum() / d.size, "PASS" if (d > 60).mean() < 0.5 else "FAIL"))

for tag, (x0, y0, x1, y1) in {
    "top(Global Minima)": (236, 302, 278, 322), "right-m(Local Minima)": (325, 388, 350, 401),
    "low-L(Local Minima)": (138, 438, 205, 470), "low-R(Global Minima)": (300, 448, 346, 470)}.items():
    ink = int((REN[y0:y1, x0:x1].mean(axis=2) < 120).sum())
    P("CHECK2 anchor %-22s render ink=%d -> %s" % (tag, ink, "OK" if ink > 20 else "MISS"))

seg = [(652 + 15 * t / 24.0, 189 - 24 * t / 24.0) for t in range(25)]
def redhit(a):
    hits = 0
    for x, y in seg:
        x, y = int(round(x)), int(round(y))
        hits += int(redmask(a[max(0, y-2):y+3, max(0, x-2):x+3]).any())
    return 100.0 * hits / len(seg)
P("CHECK3 TR segment red-hit: orig=%.0f%% render=%.0f%% -> %s"
  % (redhit(ORIG), redhit(REN), "PASS" if redhit(REN) >= 20 else "FAIL"))

def wind(A):
    Bx0, By0, Bx1, By1, P8 = 615, 344, 880, 531, 8
    br = A[By0+P8:By1-P8, Bx0+P8:Bx1-P8]
    dmk = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    lab, n = ndimage.label(dmk, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 15:
            continue
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs, ys)
    if not best:
        return None
    aa, xs, ys = best
    o = np.argsort(xs)
    px, py = xs[o].astype(float), ys[o].astype(float)
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    st = float(np.hypot(px[-1]-px[0], py[-1]-py[0]))
    return aa, seg, st, seg / max(st, 1.0)
wr = wind(REN)
P("winding render BR: %s -> %s" % (
    "area=%d len=%.1f straight=%.1f wind-ratio=%.3f" % wr if wr else "none",
    "PASS" if wr and 4 <= wr[3] <= 7 else "FAIL"))

def markers(a, ox, oy):
    lab, n = ndimage.label(redmask(a), structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 12:
            continue
        out.append((len(xs), xs.mean() + ox, ys.mean() + oy))
    return out
mr = markers(REN[290:528, 83:377], 83, 290)
t1 = [(a, x, y) for a, x, y in mr if abs(x-199) <= 6 and abs(y-445) <= 6]
t2 = [(a, x, y) for a, x, y in mr if abs(x-270) <= 6 and abs(y-482) <= 6]
P("render markers near targets: (199,445)=%s (270,482)=%s -> %s"
  % (t1, t2, "PASS" if t1 and t2 else "FAIL"))

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
