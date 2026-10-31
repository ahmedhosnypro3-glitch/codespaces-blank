#!/usr/bin/env python3
"""Probe 3: per ground-truth BL label box, extract text glyphs (opening 3x3,
area>=8), print row profile (line structure), identify vs 1-line AND 2-line
renderings of the 4 candidate strings. Read-only. Writes probe3_k17r_bl.txt +
probe3_k17r_bl_crops.png."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
ASSET = os.path.join(NS, "recreated_pptx/build/assets/plot_025_bl.png")
OUT = os.path.join(RJ, "probe3_k17r_bl.txt")

PX, PY, PW, PH = 83.0, 290.0, 293.0, 237.0

BOXES = [
    ("top",     "Global Maxima", 242, 304, 268, 319),
    ("mid-up",  "Local Maxima",  286, 337, 315, 352),
    ("mid-low", "Local Minima",  286, 390, 311, 399),
    ("low-L",   "Global Minima", 145, 439, 201, 465),
]
PAD = 12

L = []
def P(s=""):
    print(s)
    L.append(s)

img = Image.open(ASSET).convert("RGB")
W, H = img.size
sx, sy = W / PW, H / PH
a = np.asarray(img).astype(np.int32)
dark = (a.max(2) < 145) & ((a.max(2) - a.min(2)) < 80)
opened = ndimage.binary_opening(dark, structure=np.ones((3, 3)))

FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]

def render(s, fontpath, fs, two_line):
    f = ImageFont.truetype(fontpath, fs)
    parts = s.split(" ", 1) if two_line else [s]
    ims = []
    for p in parts:
        im = Image.new("L", (800, 300), 255)
        ImageDraw.Draw(im).text((10, 10), p, font=f, fill=0)
        ar = np.array(im)
        ys, xs = np.nonzero(ar < 128)
        ims.append(ar[ys.min():ys.max() + 1, xs.min():xs.max() + 1] < 128)
    w = max(i.shape[1] for i in ims)
    h = sum(i.shape[0] for i in ims) + 3 * (len(ims) - 1)
    out = np.zeros((h, w), bool)
    yy = 0
    for i in ims:
        out[yy:yy + i.shape[0], :i.shape[1]] = i
        yy += i.shape[0] + 3
    return out

def identify(crop):
    ys, xs = np.nonzero(crop)
    crop = crop[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2.0, "?", None, None)
    for s in CANDS:
        for fp in (FONT_R, FONT_B):
            for tl in (False, True):
                for fs in range(14, 150, 2):
                    c = render(s, fp, fs, tl)
                    cr = np.array(Image.fromarray((c * 255).astype(np.uint8))
                                  .resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
                    inter = (cr & crop).sum()
                    union = (cr | crop).sum()
                    v = float(inter) / union if union else -1.0
                    if v > best[0]:
                        best = (v, s, fs, tl)
    return best

crops = []
for tag, want, fx0, fy0, fx1, fy1 in BOXES:
    ax0 = int((fx0 - PAD - PX) * sx); ay0 = int((fy0 - PAD - PY) * sy)
    ax1 = int((fx1 + PAD - PX) * sx); ay1 = int((fy1 + PAD - PY) * sy)
    ax0, ay0 = max(0, ax0), max(0, ay0)
    ax1, ay1 = min(W - 1, ax1), min(H - 1, ay1)
    win = opened[ay0:ay1 + 1, ax0:ax1 + 1]
    lab, n = ndimage.label(win, structure=np.ones((3, 3)))
    keep = np.zeros_like(win)
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() >= 8:
            keep |= m
    ink = int(keep.sum())
    P("== %s want='%s' asset window x%d..%d y%d..%d glyph-ink=%d" % (tag, want, ax0, ax1, ay0, ay1, ink))
    if not ink:
        P("   NO glyph ink")
        continue
    ys, xs = np.nonzero(keep)
    bx0, bx1, by0, by1 = ax0 + xs.min(), ax0 + xs.max(), ay0 + ys.min(), ay0 + ys.max()
    P("   glyph bbox asset x%d..%d y%d..%d (%dx%d) slide x%.1f..%.1f y%.1f..%.1f"
      % (bx0, bx1, by0, by1, bx1 - bx0 + 1, by1 - by0 + 1,
         PX + bx0 / sx, PX + bx1 / sx, PY + by0 / sy, PY + by1 / sy))
    rows = keep[ys.min():ys.max() + 1].sum(1)
    prof = "".join("#" if r > 0 else "." for r in rows)
    P("   row profile: %s" % prof)
    v, got, fs, tl = identify(keep)
    P("   id='%s' IoU=%.3f fs=%s two_line=%s want='%s' -> %s"
      % (got, v, fs, tl, want, "MATCH" if got == want else "WRONG"))
    sub = a[by0:by1 + 1, bx0:bx1 + 1]
    crops.append((tag, got, Image.fromarray(sub.astype(np.uint8))
                  .resize(((bx1 - bx0 + 1) * 4, (by1 - by0 + 1) * 4), Image.LANCZOS)))

cw = max(c.width for _, _, c in crops) if crops else 100
ch = sum(c.height for _, _, c in crops) + 10 * max(1, len(crops))
sheet = Image.new("RGB", (cw + 240, ch), (255, 255, 0))
d = ImageDraw.Draw(sheet)
y = 0
for tag, got, c in crops:
    d.text((5, y + 5), "%s id='%s'" % (tag, got), fill=(255, 0, 0))
    sheet.paste(c, (240, y))
    y += c.height + 10
sheet.save(os.path.join(RJ, "probe3_k17r_bl_crops.png"))
P("\ncrops: probe3_k17r_bl_crops.png")

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT)
