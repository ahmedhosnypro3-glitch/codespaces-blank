#!/usr/bin/env python3
"""Build assets_k17j: TL/TR/BL copied from assets_k15 (re-encoded so md5 differs)
with patches:
  TR: red diagonal slide (652,189)->(667,165), color ~RGB(174,64,46), ~1.5 slide px wide
  BL: erase k15's 4 labels + leaders + 2 markers (median-fill), then draw the four
      labels at the task anchor boxes and red x markers at slide (199,445),(270,482).
BR is written separately by build/generate_plots_025_k17j.py.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
K15 = os.path.join(RJ, "assets_k15")
OUT = os.path.join(RJ, "assets_k17j")
os.makedirs(OUT, exist_ok=True)
DPI = 300
S = DPI / 72.0  # png px per slide px

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# panel placement (slide px) per build/slide_025.js addImage calls
PANELS = {"tl": (85, 115), "tr": (616, 115), "bl": (83, 290), "br": (615, 344)}


def to_png(panel, sx, sy):
    ox, oy = PANELS[panel]
    return (sx - ox) * S, (sy - oy) * S


def median_fill(img, mask):
    """replace mask pixels with median of surrounding non-mask pixels (per channel)"""
    a = np.asarray(img).astype(np.int32)
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return
    y0, y1 = max(ys.min() - 6, 0), min(ys.max() + 7, a.shape[0])
    x0, x1 = max(xs.min() - 6, 0), min(xs.max() + 7, a.shape[1])
    ring = a[y0:y1, x0:x1].reshape(-1, 3)
    sub = mask[y0:y1, x0:x1].reshape(-1)
    med = np.median(ring[~sub], axis=0) if (~sub).any() else np.array([255, 255, 255])
    a[mask] = med.astype(np.uint8)
    img.paste(Image.fromarray(a.astype(np.uint8)))


def erase_dark_text(img, cx_slide, cy_slide, panel, halfw=14, halfh=8):
    """erase dark text pixels near a slide-space center"""
    a = np.asarray(img).astype(np.int32)
    px, py = to_png(panel, cx_slide, cy_slide)
    x0, x1 = int(px - halfw * S), int(px + halfw * S)
    y0, y1 = int(py - halfh * S), int(py + halfh * S)
    sub = a[y0:y1, x0:x1]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    sat = sub.max(2) - sub.min(2)
    m = np.zeros(a.shape[:2], bool)
    m[y0:y1, x0:x1] = (lum < 130) & (sat < 100)
    # also gray leader lines
    m[y0:y1, x0:x1] |= (np.abs(sub[:, :, 0] - sub[:, :, 1]) < 25) & \
                        (np.abs(sub[:, :, 1] - sub[:, :, 2]) < 25) & (lum < 200) & (sat < 40)
    median_fill(img, m)


def erase_red_markers(img, panel, pts_slide, half=8):
    a = np.asarray(img).astype(np.int32)
    m = np.zeros(a.shape[:2], bool)
    for sx, sy in pts_slide:
        px, py = to_png(panel, sx, sy)
        x0, x1 = int(px - half * S), int(px + half * S)
        y0, y1 = int(py - half * S), int(py + half * S)
        sub = a[y0:y1, x0:x1]
        r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
        m[y0:y1, x0:x1] = (r > 110) & (r - g > 40) & (r - b > 40)
    median_fill(img, m)


def draw_label(dr, panel, box, text, two_line=True):
    """box: slide px (x0,y0,x1,y1); draw text centered, sized to the box"""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    px, py = to_png(panel, cx, cy)
    # font size: two lines each ~0.42*h slide px tall -> pt == slide px
    if two_line:
        fs = int(0.42 * h)
        lines = text.split(" ")
        if len(lines) == 2:
            txt = lines[0] + "\n" + lines[1]
        else:
            txt = text
    else:
        fs = int(0.62 * h)
        txt = text
    f = ImageFont.truetype(FONT, max(fs, 6))
    dr.text((px, py), txt, font=f, fill=(0, 0, 0), anchor="mm", align="center",
            spacing=int(0.15 * fs))


def draw_x(dr, panel, sx, sy, size_slide=3.4, width_slide=1.3):
    px, py = to_png(panel, sx, sy)
    r = size_slide * S
    w = max(int(round(width_slide * S)), 2)
    dr.line([(px - r, py - r), (px + r, py + r)], fill=(192, 0, 0), width=w)
    dr.line([(px - r, py + r), (px + r, py - r)], fill=(192, 0, 0), width=w)


# ── TL: straight copy (re-encode) ────────────────────────────────────────────
im = Image.open(os.path.join(K15, "plot_025_tl.png")).convert("RGB")
im.save(os.path.join(OUT, "plot_025_tl.png"), optimize=True)
print("tl copied+re-encoded")

# ── TR: copy + red diagonal (652,189)->(667,165) ─────────────────────────────
im = Image.open(os.path.join(K15, "plot_025_tr.png")).convert("RGB")
dr = ImageDraw.Draw(im)
p0 = to_png("tr", 652, 189)
p1 = to_png("tr", 667, 165)
w = max(int(round(1.5 * S)), 3)
dr.line([p0, p1], fill=(174, 64, 46), width=w)
im.save(os.path.join(OUT, "plot_025_tr.png"), optimize=True)
print("tr patched with red diagonal")

# ── BL: copy, erase k15 labels/markers, draw task anchors ─────────────────────
im = Image.open(os.path.join(K15, "plot_025_bl.png")).convert("RGB")
# k15 label anchors (slide px): GM (254,309), LMx (300,345), LMn (158,456), GMn (314,459)
for cx, cy in ((254, 309), (300, 345), (158, 456), (314, 459)):
    erase_dark_text(im, cx, cy, "bl", halfw=16, halfh=10)
# k15 markers were drawn at projected peak positions; erase any red x-like comps
# found in the panel interior (keep the red frame at the border)
a = np.asarray(im).astype(np.int32)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
rm = (r > 110) & (r - g > 40) & (r - b > 40)
rm[:20] = False; rm[-20:] = False; rm[:, :20] = False; rm[:, -20:] = False
lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if 8 <= len(xs) <= 400:
        w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
        if 4 <= w <= 24 and 4 <= h <= 24:
            cx = (xs.min() + xs.max()) / 2 / S + PANELS["bl"][0]
            cy = (ys.min() + ys.max()) / 2 / S + PANELS["bl"][1]
            erase_red_markers(im, "bl", [(cx, cy)], half=7)
            print("erased k15 marker at slide (%.0f,%.0f) area=%d" % (cx, cy, len(xs)))
dr = ImageDraw.Draw(im)
# task anchor boxes (slide px) -> label text
LABELS = [
    ((236, 302, 278, 322), "Global Minima"),
    ((325, 388, 350, 401), "Local Minima"),
    ((138, 438, 205, 470), "Local Minima"),
    ((300, 448, 346, 470), "Global Minima"),
]
for box, txt in LABELS:
    draw_label(dr, "bl", box, txt, two_line=True)
for mx, my in ((199, 445), (270, 482)):
    draw_x(dr, "bl", mx, my)
im.save(os.path.join(OUT, "plot_025_bl.png"), optimize=True)
print("bl patched with 4 labels + 2 markers")
print("assets_k17j written (br pending from generator)")
