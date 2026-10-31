#!/usr/bin/env python3
"""Probe k17l assets (build/assets_k17l) for slide 025. Writes pil_k17l_out.txt.

CHECK1: BR band x672..816 y472..517 diff% on the composited 960x540 canvas
        (need <50).
CHECK2: anchor-zone label ID on the native 300dpi BL png (strict ink +
        glyph filter + glyph-template match): each zone's best label must
        equal the original's anchor label.
CHECK3: red marker-like comps at (199,445) and (270,482), area 60-70.
Plus: BR GD-path winding (seg/straight) and TR segment red-hit.
"""
import hashlib
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
A = NS + "/recreated_pptx/build/assets_k17l"
OUT_TXT = os.path.join(RJ, "pil_k17l_out.txt")
ORIG = NS + "/unique_slides/slide_025.jpg"

BL = (83, 290, 293, 237)  # x0, y0, w, h — matches build/slide_025.js addImage

ANCHORS = [
    ("top     x236..278 y302..322", (236, 302, 279, 323), "Global Minima"),
    ("right-m x325..350 y388..401", (325, 388, 351, 402), "Local Minima"),
    ("low-L   x138..205 y438..470", (138, 438, 206, 471), "Local Minima"),
    ("low-R   x300..346 y448..470", (300, 448, 347, 471), "Global Minima"),
]
CANDS = ["Global Minima", "Local Minima", "Global Maxima", "Local Maxima"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
    "bl": dict(x0=83,  y0=290, w=293, h=237),
    "br": dict(x0=615, y0=344, w=265, h=187),
}
PANEL = np.array([233, 233, 231], np.int32)

lines = []
def P(s=""):
    print(s)
    lines.append(s)


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
        ink = (L < 70) & (sat < 40)
    else:
        med = np.median(L)
        ink = ((L < med - 45) | (L < 90)) & ~redmask(crop)
    if glyph_filter:
        lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
        keep = np.zeros_like(ink)
        for i in range(1, n + 1):
            ys, xs = np.nonzero(lab == i)
            h_sl = (ys.max() - ys.min() + 1) / sy
            w_sl = (xs.max() - xs.min() + 1) / sx
            if 4 <= h_sl <= 12 and 2 <= w_sl <= 45:
                keep[lab == i] = True
        ink = keep
    ys, xs = np.nonzero(ink)
    if len(xs) < 4:
        return None, 0
    return ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1], len(xs)


def best_label(ink):
    h, w = ink.shape
    scores = []
    for s in CANDS:
        for tl in (False, True):
            for fs in range(7, 14):
                c = render_cand(s, fs, tl)
                cr = np.array(Image.fromarray((c > 0).astype(np.uint8) * 255)
                              .resize((w, h), Image.BILINEAR)) > 0
                scores.append((iou(ink > 0, cr), s, tl, fs))
    scores.sort(reverse=True)
    return scores


def main():
    orig = np.array(Image.open(ORIG).convert("RGB")).astype(np.int32)
    bl_img = Image.open(os.path.join(A, "plot_025_bl.png")).convert("RGB")
    ren = np.array(bl_img).astype(np.int32)
    sx = ren.shape[1] / float(BL[2])
    sy = ren.shape[0] / float(BL[3])

    def png_box(box):
        x0, y0, x1, y1 = box
        return (int((x0 - BL[0]) * sx), int((y0 - BL[1]) * sy),
                int(np.ceil((x1 - BL[0]) * sx)), int(np.ceil((y1 - BL[1]) * sy)))

    P("== md5s (assets_k17l vs k15) ==")
    for name in ["tl", "tr", "bl", "br"]:
        P("  plot_025_%s.png k17l=%s" % (name, md5(os.path.join(A, "plot_025_%s.png" % name))))
    k15 = RJ + "/assets_k15"
    for name in ["tl", "tr", "bl", "br"]:
        P("  plot_025_%s.png k15 =%s" % (name, md5(os.path.join(k15, "plot_025_%s.png" % name))))

    # composite canvas for CHECK1 / winding / TR segment
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[45:540, 54:904] = PANEL
    for name, s in PLOTS.items():
        im = Image.open(os.path.join(A, "plot_025_%s.png" % name)).convert("RGB")
        im = im.resize((s["w"], s["h"]), Image.BILINEAR)
        canvas[s["y0"]:s["y0"] + s["h"], s["x0"]:s["x0"] + s["w"]] = np.array(im).astype(np.int32)
    ren_c = canvas

    P("\n== CHECK1: BR band x672..816 y472..517 diff%% (composited) ==")
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    ob = orig[by0:by1, bx0:bx1]
    rb = ren_c[by0:by1, bx0:bx1]
    band = 100.0 * (np.abs(ob - rb).sum(2) > 60).mean()
    ob_col = 100.0 * ((ob.max(2) - ob.min(2)) > 60).mean()
    rb_col = 100.0 * ((rb.max(2) - rb.min(2)) > 60).mean()
    P("  diff%% = %.2f (need <50) | orig colored%%=%.1f ren colored%%=%.1f %s"
      % (band, ob_col, rb_col, "PASS" if band < 50 else "FAIL"))

    P("\n== CHECK2: anchor-zone label ID (k17l BL png native 300dpi vs orig) ==")
    P("  (png size %dx%d, scale %.4f png px per slide px)" % (ren.shape[1], ren.shape[0], sx))
    all_pass = True
    for name, box, expect in ANCHORS:
        r_ink, r_n = ink_of(ren, png_box(box), strict=True, sx=sx, sy=sy,
                            glyph_filter=True)
        o_ink, o_n = ink_of(orig, box)
        line = "  %s expect '%s'" % (name, expect)
        if r_ink is None:
            P(line + " -> render zone EMPTY ink (%d px) FAIL" % r_n)
            all_pass = False
            continue
        sc = best_label(r_ink)
        top = sc[0]
        ok = top[1] == expect
        all_pass &= ok
        osc = best_label(o_ink) if o_ink is not None else []
        otop = osc[0] if osc else (0, "?", 0, 0)
        P(line)
        P("    render ink w=%d h=%d n=%d (png px, = %.0fx%.1f slide px) -> best '%s'(2l=%d,fs=%d) iou=%.2f  %s"
          % (r_ink.shape[1], r_ink.shape[0], r_n, r_ink.shape[1] / sx, r_ink.shape[0] / sy,
             top[1], top[2], top[3], top[0], "PASS" if ok else "FAIL"))
        P("    runner-up: '%s' iou=%.2f | orig zone best '%s' iou=%.2f"
          % (sc[1][1], sc[1][0], otop[1], otop[0]))
    P("  CHECK2 %s" % ("PASS" if all_pass else "FAIL"))

    P("\n== CHECK3: red marker-like comps in k17l BL png (native) ==")
    rm = redmask(ren)
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        area = len(xs)
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        fill = area / float(w * h)
        a_sl = area / (sx * sy)
        w_sl, h_sl = w / sx, h / sy
        if 12 <= a_sl <= 200 and 4 <= w_sl <= 16 and 4 <= h_sl <= 16 and fill > 0.3:
            cx = BL[0] + xs.mean() / sx
            cy = BL[1] + ys.mean() / sy
            comps.append((a_sl, round(cx, 1), round(cy, 1), round(w_sl, 1), round(h_sl, 1)))
    exp = [(199, 445), (270, 482)]
    for c in sorted(comps):
        mark = " <-- expected marker" if any(abs(c[1] - ex) <= 6 and abs(c[2] - ey) <= 6
                                             for ex, ey in exp) else ""
        P("  area=%.0f slide-px^2 slide-center=(%s,%s) bbox %.0fx%.0f slide px%s" % (c + (mark,)))
    markers = [c for c in comps
               if any(abs(c[1] - ex) <= 6 and abs(c[2] - ey) <= 6 for ex, ey in exp)]
    ok3 = len(markers) == 2 and all(60 <= c[0] <= 70 for c in markers)
    P("  marker comps at expected centers: %d (areas %s)" %
      (len(markers), [round(c[0]) for c in markers]))
    P("  CHECK3 %s (expect exactly 2 at (199,445),(270,482), area 60-70 slide px^2)"
      % ("PASS" if ok3 else "FAIL"))

    P("\n== winding (BR GD path seg/straight, composited) ==")
    br = ren_c[344:344 + 187, 615:615 + 265]
    lum_b = lum(br)
    sat_b = br.max(2) - br.min(2)
    dm = (lum_b < 100) & (sat_b < 80)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    lab2, n2 = ndimage.label(dm, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n2 + 1):
        ys, xs = np.nonzero(lab2 == i)
        if len(xs) < 15:
            continue
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs, ys)
    if best is None:
        P("  winding = None")
    else:
        _, xs, ys = best
        order = np.argsort(xs)
        px, py = xs[order], ys[order]
        seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
        straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
        P("  winding = %.2f (target ~6.0), path px=%d" % (seg / max(straight, 1.0), len(px)))

    P("\n== TR segment (652,189)->(667,165) red-hit% (composited) ==")
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
    P("  orig=%.1f k17l=%.1f" % (seg_red_hit(orig), seg_red_hit(ren_c)))

    P("\nPROBE_DONE")
    with open(OUT_TXT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", OUT_TXT)


main()
