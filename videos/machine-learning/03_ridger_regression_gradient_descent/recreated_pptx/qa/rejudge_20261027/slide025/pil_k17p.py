#!/usr/bin/env python3
"""k17p PIL probe: checks on the FRESH 150dpi render render_k17p.png of the
current slide_025_recreated.pptx (md5 banked in k17p_md5_at_render.txt) vs
unique_slides/slide_025.jpg. Render is downscaled to 960x540 slide space
(LANCZOS); all coordinates are slide px (1px=1pt).
  CHECK1: BR band x672..816 y472..517 diff-vs-orig % (k16 render was 97.9%)
  CHECK2: BL label anchors (IoU template ID + ink counts)
  CHECK3: TR red segment (652,189)->(667,165) red-hit%; BR winding ratio (~6.0);
          BL red-marker px in 11x11 windows at (199,445),(270,482)
Writes pil_k17p_out.txt.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
RENDER = RJ + "/render_k17p.png"
OUTFILE = RJ + "/pil_k17p_out.txt"

_lines = []


def P(s=""):
    print(s)
    _lines.append(s)


ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
rimg = Image.open(RENDER).convert("RGB")
P("render=%s size=%s" % (RENDER, rimg.size))
REN = np.asarray(rimg.resize((960, 540), Image.LANCZOS)).astype(np.int32)


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


# ── CHECK1: BR bottom band x672..816 y472..517 ──────────────────────────────
P("\n== CHECK1: BR band slide x672..816 y472..517 diff vs orig ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = ORIG[by0:by1, bx0:bx1]
rb = REN[by0:by1, bx0:bx1]
diff = (np.abs(ob - rb).sum(2) > 60)
H, W = diff.shape
band_pct = 100.0 * diff.mean()
# also colored% stats like pil_k15b check B
def colored(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mx = a.max(2); mn = a.min(2)
    return ((mx - mn > 40) & (mx > 90)).mean() * 100.0
P("  band %dx%d diff px=%d (%.2f%%) | orig colored%%=%.1f ren colored%%=%.1f" %
  (W, H, diff.sum(), band_pct, colored(ob), colored(rb)))
c1 = band_pct
P("  CHECK1 BR band diff%% = %.2f (was 97.9%% at k16; lower=closer to orig)" % band_pct)

# ── CHECK2: BL labels at anchors ─────────────────────────────────────────────
P("\n== CHECK2: BL label anchors (IoU template ID + ink) ==")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
_tc = {}


def render_cand_2l(s, fs):
    f = ImageFont.truetype(FONT, fs)
    parts = s.split(" ", 1)
    ims = []
    for p in parts:
        im = Image.new("L", (300, 60), 255)
        ImageDraw.Draw(im).text((4, 4), p, font=f, fill=0)
        a = np.array(im)
        ys, xs = np.nonzero(a < 128)
        ims.append(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    w = max(i.shape[1] for i in ims)
    h = sum(i.shape[0] for i in ims) + 2 * (len(ims) - 1)
    out = np.full((h, w), 255, np.uint8)
    yy = 0
    for i in ims:
        out[yy:yy + i.shape[0], :i.shape[1]] = i
        yy += i.shape[0] + 2
    return out < 128


def identify(win):
    dm = (win.max(2) < 145) & ((win.max(2) - win.min(2)) < 80)
    if not dm.any():
        return (-1.0, "?")
    ys, xs = np.nonzero(dm)
    crop = dm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2, "?")
    for s in CANDS:
        for fs in range(6, 17):
            c = render_cand_2l(s, fs)
            cr = np.array(Image.fromarray((c * 255).astype(np.uint8)).resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
            inter = (cr & crop).sum()
            union = (cr | crop).sum()
            v = float(inter) / union if union else -1.0
            if v > best[0]:
                best = (v, s)
    return best


ANCHORS = [
    ("top",     236, 302, 278, 322, "Global Minima"),
    ("right-m", 325, 388, 350, 401, "Local Minima"),
    ("low-L",   138, 438, 205, 470, "Local Minima"),
    ("low-R",   300, 448, 346, 470, "Global Minima"),
]
for tag, ax0, ay0, ax1, ay1, want in ANCHORS:
    ow = identify(ORIG[ay0:ay1, ax0:ax1])
    rw = identify(REN[ay0:ay1, ax0:ax1])
    win = REN[ay0:ay1, ax0:ax1]
    ink = int(((win.max(2) < 145) & ((win.max(2) - win.min(2)) < 80)).sum())
    ow_ink = int(((ORIG[ay0:ay1, ax0:ax1].max(2) < 145) & ((ORIG[ay0:ay1, ax0:ax1].max(2) - ORIG[ay0:ay1, ax0:ax1].min(2)) < 80)).sum())
    P("  %-7s x%d..%d y%d..%d want='%s' | orig='%s'(%.2f,ink=%d) render='%s'(%.2f,ink=%d)" %
      (tag, ax0, ax1, ay0, ay1, want, ow[1], ow[0], ow_ink, rw[1], rw[0], ink))
P("  CHECK2 BL label anchors listed (compare render IDs vs want; ink>30 expected)")

# ── CHECK3: TR red segment + winding + markers ───────────────────────────────
P("\n== CHECK3: TR red segment (652,189)->(667,165) red-hit within 2px ==")


def redhit(a, x0, y0, x1, y1, n=200):
    rm = redmask(a)
    hit = 0
    for i in range(n):
        t = i / (n - 1.0)
        xi, yi = int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t))
        if rm[max(0, yi - 2):yi + 3, max(0, xi - 2):xi + 3].any():
            hit += 1
    return 100.0 * hit / n


h_o = redhit(ORIG, 652, 189, 667, 165)
h_r = redhit(REN, 652, 189, 667, 165)
P("  orig red-hit=%.1f%%  render red-hit=%.1f%%" % (h_o, h_r))

P("\n== BR winding (largest dark comp in BR panel, target ~6.0) ==")
Bx0, By0, Bx1, By1 = 615, 344, 880, 531
P8 = 8
br = REN[By0 + P8:By1 - P8, Bx0 + P8:Bx1 - P8]
dmk = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
best = None
for area, xs, ys in comps(dmk, min_area=15):
    spanx = xs.max() - xs.min() + 1
    if best is None or area > best[0]:
        best = (area, spanx, xs, ys)
if best:
    aa, spanx, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    ratio = seg / max(straight, 1.0)
    P("  area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f" % (aa, spanx, seg, straight, ratio))
else:
    ratio = 0.0
    P("  no dark comp found")

P("\n== BL markers: red-px in 11x11 window at (199,445),(270,482) ==")
for (tx, ty) in [(199, 445), (270, 482)]:
    wo = redmask(ORIG[max(0, ty - 5):ty + 6, max(0, tx - 5):tx + 6]).sum()
    wr = redmask(REN[max(0, ty - 5):ty + 6, max(0, tx - 5):tx + 6]).sum()
    P("  (%d,%d): orig=%d render=%d" % (tx, ty, wo, wr))

P("\nPROBE_DONE")
with open(OUTFILE, "w") as f:
    f.write("\n".join(_lines) + "\n")
print("wrote", OUTFILE)
