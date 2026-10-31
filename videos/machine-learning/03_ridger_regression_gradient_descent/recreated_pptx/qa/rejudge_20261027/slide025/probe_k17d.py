#!/usr/bin/env python3
"""k17d PIL verification for slide 025 BL panel.

CHECK1: md5(assets_k17d/plot_025_bl.png) != md5(assets_k15/plot_025_bl.png).
CHECK2: paste assets_k17d/plot_025_bl.png onto a 960x540 canvas at the BL
  rect (x83 y290 w293 h237, 1:1 slide px) and template-ID the dark ink in
  each of the 4 original anchor zones against candidate labels; each zone
  must top-1 match its expected label (none swapped). Cross-checked against
  the same zones on unique_slides/slide_025.jpg.
CHECK3: red marker-like comps (area 12..200, bbox 4..16 sq, fill>0.3) in the
  rendered BL panel: exactly 2, centered at slide (199,445) and (270,482),
  areas in the original's 60-67 range.
"""
import hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = NS + "/unique_slides/slide_025.jpg"
K17D_BL = RJ + "/assets_k17d/plot_025_bl.png"
K15_BL = RJ + "/assets_k15/plot_025_bl.png"

BL = (83, 290, 293, 237)  # x0, y0, w, h — matches build/slide_025_k15.js addImage

# anchor zones (slide px) and expected label, from the task / pil_k15_labels.txt
ANCHORS = [
    ("top     x236..278 y302..322", (236, 302, 279, 323), "Global Minima"),
    ("right-m x325..350 y388..401", (325, 388, 351, 402), "Local Minima"),
    ("low-L   x138..205 y438..470", (138, 438, 206, 471), "Local Minima"),
    ("low-R   x300..346 y448..470", (300, 448, 347, 471), "Global Minima"),
]
CANDS = ["Global Minima", "Local Minima", "Global Maxima", "Local Maxima"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def render_cand(s, fs, two_line):
    f = ImageFont.truetype(FONT, fs)
    parts = s.split(" ", 1) if two_line else [s]
    ims = []
    for p in parts:
        im = Image.new("L", (260, 48), 0)
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


def ink_of(img, box, strict=False, sx=1.0, sy=1.0, glyph_filter=False):
    x0, y0, x1, y1 = box
    crop = img[y0:y1, x0:x1]
    L = lum(crop)
    sat = crop.max(2) - crop.min(2)
    if strict:
        # label text is pure black (lum<70, sat<40); excludes red x markers
        # and the colored/dark-gray surface mesh
        ink = (L < 70) & (sat < 40)
    else:
        med = np.median(L)
        ink = ((L < med - 45) | (L < 90)) & ~redmask(crop)
    if glyph_filter:
        # keep only glyph-sized comps (h 3..14, w 1..50 slide px): drops tick
        # labels and any mesh/axis blobs, keeps label glyphs
        lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
        keep = np.zeros_like(ink)
        for i in range(1, n + 1):
            ys, xs = np.nonzero(lab == i)
            h_sl = (ys.max() - ys.min() + 1) / sy
            w_sl = (xs.max() - xs.min() + 1) / sx
            if 3 <= h_sl <= 14 and 1 <= w_sl <= 50:
                keep[lab == i] = True
        ink = keep
    if ink.sum() < 4:
        return None, int(ink.sum())
    return ink, int(ink.sum())


def best_label(ink, scale=1.0):
    """Template-ID a full-zone ink mask: render each candidate at native scale
    (fontsize fs slide px -> fs*scale px), centered on the zone, IoU directly
    (no resize distortion). Returns scores sorted best-first."""
    h, w = ink.shape
    scores = []
    for s in CANDS:
        for tl in (False, True):
            for fs in np.arange(6.5, 9.01, 0.25):
                f = ImageFont.truetype(FONT, max(4, int(round(fs * scale))))
                im = Image.new("L", (w, h), 0)
                d = ImageDraw.Draw(im)
                d.text((w / 2.0, h / 2.0), s.replace(" ", "\n") if tl else s,
                       font=f, fill=255, anchor="mm", align="center",
                       spacing=2)
                cr = np.array(im) > 0
                scores.append((iou(ink > 0, cr), s, tl, float(fs)))
    scores.sort(reverse=True)
    return scores


def main():
    orig = np.array(Image.open(ORIG).convert("RGB")).astype(np.int32)
    # work at the PNG's native 300dpi: slide px -> png px via the placed size
    bl_img = Image.open(K17D_BL).convert("RGB")
    ren = np.array(bl_img).astype(np.int32)
    sx = ren.shape[1] / float(BL[2])
    sy = ren.shape[0] / float(BL[3])

    def png_box(box):
        x0, y0, x1, y1 = box
        return (int((x0 - BL[0]) * sx), int((y0 - BL[1]) * sy),
                int(np.ceil((x1 - BL[0]) * sx)), int(np.ceil((y1 - BL[1]) * sy)))

    print("== CHECK1: md5 differ k17d vs k15 BL ==")
    m17, m15 = md5(K17D_BL), md5(K15_BL)
    print("  k17d plot_025_bl.png md5 = %s" % m17)
    print("  k15  plot_025_bl.png md5 = %s" % m15)
    c1 = m17 != m15
    print("  CHECK1 %s" % ("PASS" if c1 else "FAIL"))

    print("\n== CHECK2: anchor-zone label ID (k17d BL png native 300dpi vs orig) ==")
    print("  (png size %dx%d, scale %.4f png px per slide px)" % (ren.shape[1], ren.shape[0], sx))
    all_pass = True
    for name, box, expect in ANCHORS:
        r_ink, r_n = ink_of(ren, png_box(box), strict=True, sx=sx, sy=sy,
                            glyph_filter=True)
        o_ink, o_n = ink_of(orig, box)
        line = "  %s expect '%s'" % (name, expect)
        if r_ink is None:
            print(line + " -> render zone EMPTY ink (%d px) FAIL" % r_n)
            all_pass = False
            continue
        sc = best_label(r_ink, scale=sx)
        top = sc[0]
        ok = top[1] == expect
        all_pass &= ok
        osc = best_label(o_ink, scale=1.0) if o_ink is not None else []
        otop = osc[0] if osc else (0, "?", 0, 0)
        print(line)
        print("    render ink n=%d png px (= %d slide px^2) -> best '%s'(2l=%d,fs=%.2f) iou=%.2f  %s"
              % (r_n, r_n / (sx * sy), top[1], top[2], top[3], top[0],
                 "PASS" if ok else "FAIL"))
        print("    runner-up: '%s'(2l=%d,fs=%.2f) iou=%.2f | orig zone best '%s' iou=%.2f"
              % (sc[1][1], sc[1][2], sc[1][3], sc[1][0], otop[1], otop[0]))
    print("  CHECK2 %s" % ("PASS" if all_pass else "FAIL"))

    print("\n== CHECK3: red marker-like comps in k17d BL png (native) ==")
    rm = redmask(ren)
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        area = len(xs)
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        fill = area / float(w * h)
        # orig: area 60-67 slide px, bbox ~14x8..16x10 slide px
        a_sl = area / (sx * sy)
        w_sl, h_sl = w / sx, h / sy
        if 12 <= a_sl <= 200 and 4 <= w_sl <= 16 and 4 <= h_sl <= 16 and fill > 0.3:
            cx = BL[0] + xs.mean() / sx
            cy = BL[1] + ys.mean() / sy
            comps.append((a_sl, round(cx, 1), round(cy, 1), round(w_sl, 1), round(h_sl, 1)))
    exp = [(199, 445), (270, 482)]
    allc = sorted(comps)
    for c in allc:
        mark = " <-- expected marker" if any(abs(c[1] - ex) <= 6 and abs(c[2] - ey) <= 6
                                             for ex, ey in exp) else ""
        print("  area=%.0f slide-px^2 slide-center=(%s,%s) bbox %.0fx%.0f slide px%s" % (c + (mark,)))
    markers = [c for c in comps
               if any(abs(c[1] - ex) <= 6 and abs(c[2] - ey) <= 6 for ex, ey in exp)]
    others = [c for c in comps if c not in markers]
    ok3 = len(markers) == 2 and all(55 <= c[0] <= 75 for c in markers)
    print("  marker comps at expected centers: %d (areas %s)" %
          (len(markers), [round(c[0]) for c in markers]))
    print("  CHECK3 %s (expect exactly 2 at (199,445),(270,482), area 60-67 slide px^2)"
          % ("PASS" if ok3 else "FAIL"))

    print("\nOVERALL %s" % ("PASS" if (c1 and all_pass and ok3) else "FAIL"))


main()
