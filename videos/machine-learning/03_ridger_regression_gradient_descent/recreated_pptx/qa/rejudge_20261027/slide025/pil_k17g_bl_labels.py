#!/usr/bin/env python3
"""PIL pixel-verify of the BL plot in promoted asset set k17g (deck 03 slide 25).

Compares recreated_pptx/qa/rejudge_20261027/slide025/assets_k17g/plot_025_bl.png
against the BL panel crop of videos/.../unique_slides/slide_025.jpg at matching
scale (BL placement on slide: x83 y290 w293 h237; 1 slide px = 1 pt).

Ground-truth anchors (slide coords, from pil_k15_labels.txt):
  top     x236..278 y302..322 'Global Minima'
  right-m x325..350 y388..401 'Local Minima'
  low-L   x138..205 y438..470 'Local Minima'
  low-R   x300..346 y448..470 'Global Minima'

Checks, per label: dark-text pixel cluster inside the anchor box in the k17g
asset (at slide scale and full asset scale), 2-line glyph IoU identity vs the
expected string, and a whole-panel scan for extra label-like dark clusters.
Writes pil_k17g_bl_labels.txt. Read-only wrt build files.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ASSET = os.path.join(RJ, "assets_k17g", "plot_025_bl.png")
OUTFILE = os.path.join(RJ, "pil_k17g_bl_labels.txt")
CROPS = os.path.join(RJ, "pil_k17g_bl_labels_crops.png")

X0, Y0, W, H = 83, 290, 293, 237  # BL placement in slide coords

ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
AIMG = Image.open(ASSET).convert("RGB")
A = np.asarray(AIMG).astype(np.int32)
sx, sy = AIMG.size[0] / W, AIMG.size[1] / H
# slide-scale view of the asset (1 slide px = 1 sample), same as k17g_verify.py
REN = np.asarray(AIMG.resize((W, H), Image.NEAREST)).astype(np.int32)
ORIG_BL = ORIG[Y0:Y0 + H, X0:X0 + W]

_lines = []


def P(s=""):
    print(s)
    _lines.append(s)


def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)


def comps(mask, min_area=1):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
    return out


# 2-line glyph-template identity (pil_k15_labels.py / k17g_verify.py method)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]
_tc = {}


def render_cand_2l(s, fs):
    if (s, fs) in _tc:
        return _tc[(s, fs)]
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
    _tc[(s, fs)] = out < 128
    return _tc[(s, fs)]


def identify(win):
    dm = darkmask(win)
    if not dm.any():
        return (-1.0, "?")
    ys, xs = np.nonzero(dm)
    crop = dm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2.0, "?")
    for s in CANDS:
        for fs in range(6, 17):
            c = render_cand_2l(s, fs)
            cr = np.array(Image.fromarray((c * 255).astype(np.uint8))
                          .resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
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

P("pil_k17g_bl_labels: asset=%s" % ASSET)
P("asset size=%dx%d  slide-scale sx=%.4f sy=%.4f  BL panel slide x%d..%d y%d..%d (%dx%d)"
  % (AIMG.size[0], AIMG.size[1], sx, sy, X0, X0 + W, Y0, Y0 + H, W, H))
P("orig slide_025.jpg 960x540; BL crop orig[%d:%d, %d:%d] vs asset resized %dx%d NEAREST (matching scale)"
  % (Y0, Y0 + H, X0, X0 + W, W, H))

# side-by-side crop evidence (orig BL panel vs k17g asset at slide scale), anchors drawn
ov = Image.fromarray(ORIG_BL.astype(np.uint8))
rv = Image.fromarray(REN.astype(np.uint8))
d = ImageDraw.Draw(ov)
for tag, ax0, ay0, ax1, ay1, want in ANCHORS:
    d.rectangle([ax0 - X0, ay0 - Y0, ax1 - X0, ay1 - Y0], outline=(255, 0, 0))
d2 = ImageDraw.Draw(rv)
for tag, ax0, ay0, ax1, ay1, want in ANCHORS:
    d2.rectangle([ax0 - X0, ay0 - Y0, ax1 - X0, ay1 - Y0], outline=(255, 0, 0))
combo = Image.new("RGB", (W * 2 + 10, H), (255, 255, 0))
combo.paste(ov, (0, 0))
combo.paste(rv, (W + 10, 0))
combo = combo.resize((combo.width * 2, combo.height * 2), Image.NEAREST)
combo.save(CROPS)
P("crop evidence: %s (left=orig BL crop, right=k17g asset at slide scale, red=anchor boxes)" % CROPS)

P("\n== per-label anchor check (dark-text clusters in anchor boxes) ==")
results = []
for tag, ax0, ay0, ax1, ay1, want in ANCHORS:
    # slide-scale windows
    ow = ORIG[ay0:ay1 + 1, ax0:ax1 + 1]
    rw = REN[(ay0 - Y0):(ay1 - Y0) + 1, (ax0 - X0):(ax1 - X0) + 1]
    o_ink = int(darkmask(ow).sum())
    r_ink = int(darkmask(rw).sum())
    o_id = identify(ow)
    r_id = identify(rw)
    # comps inside the anchor window (slide scale), area>=5; window origin (ax0,ay0)
    r_comps = comps(darkmask(rw), min_area=5)
    r_big = max((c for c in r_comps), key=lambda c: c[0]) if r_comps else None
    # full-res asset window
    lx0, ly0 = int((ax0 - X0) * sx), int((ay0 - Y0) * sy)
    lx1, ly1 = int((ax1 - X0 + 1) * sx), int((ay1 - Y0 + 1) * sy)
    aw = A[ly0:ly1, lx0:lx1]
    a_ink = int(darkmask(aw).sum())
    a_comps = comps(darkmask(aw), min_area=20)
    a_big = max((c for c in a_comps), key=lambda c: c[0]) if a_comps else None
    a_bbox_slide = None
    if a_big:
        _, bx0, by0, bx1, by1 = a_big
        a_bbox_slide = (X0 + (lx0 + bx0) / sx, Y0 + (ly0 + by0) / sy,
                        X0 + (lx0 + bx1) / sx, Y0 + (ly0 + by1) / sy)
    present = r_ink >= 30 and r_big is not None
    ident_ok = r_id[1] == want
    ok = present and ident_ok
    results.append(ok)
    P("  %-7s anchor slide x%d..%d y%d..%d want='%s'" % (tag, ax0, ax1, ay0, ay1, want))
    P("    orig : ink=%d id='%s'(%.2f)" % (o_ink, o_id[1], o_id[0]))
    P("    k17g : ink(slide-scale)=%d ink(asset-res)=%d comps(slide)=%d biggest=%s"
      % (r_ink, a_ink, len(r_comps),
         ("area=%d slide x%.0f..%.0f y%.0f..%.0f" % (r_big[0], ax0 + r_big[1], ax0 + r_big[3], ay0 + r_big[2], ay0 + r_big[4])) if r_big else None))
    if a_bbox_slide:
        P("    k17g biggest comp (asset-res) slide bbox x%.1f..%.1f y%.1f..%.1f"
          % a_bbox_slide)
    P("    k17g id='%s'(%.2f) present=%s -> %s"
      % (r_id[1], r_id[0], present, "PASS" if ok else "FAIL"))

# count: exactly 4 labels, one per anchor (per-anchor ink check above), and no
# extra text-like clusters elsewhere in the panel. Wireframe lines connect
# everything at dilation, so scan raw comps and require text-like shape.
P("\n== whole-BL-panel scan (slide scale): label-cluster count / extras ==")
rm_all = darkmask(REN)
om_all = darkmask(ORIG_BL)
anchor_slide = [(a[1], a[2], a[3], a[4]) for a in ANCHORS]
PAD = 12


def hits_anchor(c, pad=PAD):
    for ax0, ay0, ax1, ay1 in anchor_slide:
        if not (c[3] + pad < ax0 or ax1 + pad < c[1] or
                c[4] + pad < ay0 or ay1 + pad < c[2]):
            return True
    return False


def overlaps_any(c, others, pad=PAD):
    return any(not (c[3] + pad < o[1] or o[3] + pad < c[1] or
                    c[4] + pad < o[2] or o[4] + pad < c[2]) for o in others)


def text_like(c):
    w, h = c[3] - c[1] + 1, c[4] - c[2] + 1
    return w <= 90 and h <= 45 and c[0] / float(w * h) > 0.12


r_panel = [(c[0], c[1] + X0, c[2] + Y0, c[3] + X0, c[4] + Y0) for c in comps(rm_all, min_area=25)]
o_panel = [(c[0], c[1] + X0, c[2] + Y0, c[3] + X0, c[4] + Y0) for c in comps(om_all, min_area=25)]
P("  k17g BL panel dark comps area>=25 (slide coords): %d" % len(r_panel))
for c in sorted(r_panel, key=lambda c: -c[0]):
    P("    area=%d x%d..%d y%d..%d%s%s" % (c[0], c[1], c[3], c[2], c[4],
      " ANCHOR" if hits_anchor(c) else "", " TEXT" if text_like(c) else ""))
P("  orig BL panel dark comps area>=25 (slide coords): %d" % len(o_panel))
for c in sorted(o_panel, key=lambda c: -c[0]):
    P("    area=%d x%d..%d y%d..%d%s%s" % (c[0], c[1], c[3], c[2], c[4],
      " ANCHOR" if hits_anchor(c) else "", " TEXT" if text_like(c) else ""))

covered = set()
for i, (tag, ax0, ay0, ax1, ay1, want) in enumerate(ANCHORS):
    win = darkmask(REN[(ay0 - Y0):(ay1 - Y0) + 1, (ax0 - X0):(ax1 - X0) + 1])
    if win.sum() >= 30:
        covered.add(i)
P("  anchors with >=30 dark px (label present): %d/4 (%s)" % (len(covered), sorted(covered)))

extras = [c for c in r_panel if not hits_anchor(c) and text_like(c) and not overlaps_any(c, o_panel)]
P("  extra text-like clusters in k17g BL panel outside anchors (no orig counterpart): %d" % len(extras))
for c in extras:
    P("    EXTRA area=%d x%d..%d y%d..%d" % (c[0], c[1], c[3], c[2], c[4]))

count_ok = len(covered) == 4 and len(extras) == 0
P("  count check (4 anchors covered, no extra labels): %s" % ("PASS" if count_ok else "FAIL"))

P("\n== SUMMARY ==")
for (tag, ax0, ay0, ax1, ay1, want), ok in zip(ANCHORS, results):
    P("  %-7s x%d..%d y%d..%d '%s': %s" % (tag, ax0, ax1, ay0, ay1, want, "PASS" if ok else "FAIL"))
P("  label count / no-extra-labels: %s" % ("PASS" if count_ok else "FAIL"))
overall = all(results) and count_ok
P("OVERALL: %s" % ("PASS" if overall else "FAIL"))

with open(OUTFILE, "w") as f:
    f.write("\n".join(_lines) + "\n")
print("wrote", OUTFILE)
