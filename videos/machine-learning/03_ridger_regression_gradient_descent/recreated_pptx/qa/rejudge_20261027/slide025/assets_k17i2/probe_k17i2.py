#!/usr/bin/env python3
"""Probe k17i2 assets composited onto 960x540 vs unique_slides/slide_025.jpg.
Writes pil_k17i2_out.txt next to this script's parent (slide025/).
CHECK1 BR band x672..816 y472..517 diff% | CHECK2 4 BL label anchors |
CHECK3 TR red segment (652,189)->(667,165) red-hit% | winding | markers.
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
A = os.path.join(RJ, "assets_k17i2")
OUT_TXT = os.path.join(RJ, "pil_k17i2_out.txt")

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
    "bl": dict(x0=83,  y0=290, w=293, h=237),
    "br": dict(x0=615, y0=344, w=265, h=187),
}
PANEL = np.array([233, 233, 231], np.int32)

canvas = np.full((540, 960, 3), 255, np.int32)
canvas[45:540, 54:904] = PANEL
for name, s in PLOTS.items():
    im = Image.open(os.path.join(A, "plot_025_%s.png" % name)).convert("RGB")
    im = im.resize((s["w"], s["h"]), Image.BILINEAR)
    canvas[s["y0"]:s["y0"] + s["h"], s["x0"]:s["x0"] + s["w"]] = np.array(im).astype(np.int32)
ren = canvas

lines = []
def P(s=""):
    print(s)
    lines.append(s)

def redmask(a):
    return (a[:, :, 0] > 140) & (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 60)

def darkmask(a):
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    return (lum < 100) & ((a.max(2) - a.min(2)) < 80)

# ── CHECK1: BR bottom band diff % ──
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = orig[by0:by1, bx0:bx1]
rb = ren[by0:by1, bx0:bx1]
band = 100.0 * (np.abs(ob - rb).sum(2) > 60).mean()
ob_col = 100.0 * ((ob.max(2) - ob.min(2)) > 60).mean()
rb_col = 100.0 * ((rb.max(2) - rb.min(2)) > 60).mean()
P("CHECK1 BR band x672..816 y472..517 diff%% = %.2f (need <50) | orig colored%%=%.1f ren colored%%=%.1f"
  % (band, ob_col, rb_col))

# ── CHECK2: 4 BL label anchors (dark ink count in each box, orig vs ren) ──
ANCHORS = [
    ("top   Global Minima", 236, 302, 278, 322),
    ("r-mid Local Minima ", 325, 388, 350, 401),
    ("low-L Local Minima ", 138, 438, 205, 470),
    ("low-R Global Minima", 300, 448, 346, 470),
]
P("CHECK2 BL label anchors (dark-ink px, orig vs k17i2):")
for name, x0, y0, x1, y1 in ANCHORS:
    do = int(darkmask(orig[y0:y1 + 1, x0:x1 + 1]).sum())
    dr = int(darkmask(ren[y0:y1 + 1, x0:x1 + 1]).sum())
    P("  %s box x%d..%d y%d..%d : orig=%d ren=%d" % (name, x0, x1, y0, y1, do, dr))

# ── CHECK3: TR red segment (652,189)->(667,165) red-hit % ──
def seg_red_hit(a):
    x0, y0, x1, y1 = 652, 189, 667, 165
    n = 60
    hits = 0
    for i in range(n + 1):
        t = i / n
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        xi, yi = int(round(cx)), int(round(cy))
        win = a[max(0, yi - 2):yi + 3, max(0, xi - 2):xi + 3]
        if redmask(win).any():
            hits += 1
    return 100.0 * hits / (n + 1)
P("CHECK3 TR segment (652,189)->(667,165) red-hit%%: orig=%.1f k17i2=%.1f"
  % (seg_red_hit(orig), seg_red_hit(ren)))

# ── winding of the GD path inside the BR box ──
bl = ren[344:344 + 187, 615:615 + 265]
lum = 0.299 * bl[:, :, 0] + 0.587 * bl[:, :, 1] + 0.114 * bl[:, :, 2]
sat = bl.max(2) - bl.min(2)
dm = (lum < 100) & (sat < 80)
dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
best = None
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 15:
        continue
    if best is None or len(xs) > best[0]:
        best = (len(xs), xs, ys)
if best is None:
    P("winding = None")
else:
    _, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    P("winding (BR GD path seg/straight) = %.2f (target ~6.0), path px=%d" % (seg / max(straight, 1.0), len(px)))

# ── markers at (199,445) and (270,482): red px in 11x11 window ──
P("markers red-px in 11x11 window (orig vs k17i2):")
for (mx, my) in ((199, 445), (270, 482)):
    ro = int(redmask(orig[my - 5:my + 6, mx - 5:mx + 6]).sum())
    rr = int(redmask(ren[my - 5:my + 6, mx - 5:mx + 6]).sum())
    P("  (%d,%d): orig=%d k17i2=%d" % (mx, my, ro, rr))

P("PROBE_DONE")
with open(OUT_TXT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("wrote", OUT_TXT)
