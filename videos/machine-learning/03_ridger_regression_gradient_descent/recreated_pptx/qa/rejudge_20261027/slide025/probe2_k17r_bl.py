#!/usr/bin/env python3
"""Probe 2: isolate TEXT glyphs (morphological opening removes thin leader
lines/wireframe) in each ground-truth BL label box of the live asset, identify
the baked-in string per box, and report asset-px bboxes to whiten.
Read-only. Writes probe2_k17r_bl.txt + probe2_k17r_bl_crops.png.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
ASSET = os.path.join(NS, "recreated_pptx/build/assets/plot_025_bl.png")
OUT = os.path.join(RJ, "probe2_k17r_bl.txt")

PX, PY, PW, PH = 83.0, 290.0, 293.0, 237.0  # addImage placement (slide px)

# authoritative ground-truth label bboxes (frame px, inclusive) + wanted text
BOXES = [
    ("top",     "Global Maxima", 242, 304, 268, 319),
    ("mid-up",  "Local Maxima",  286, 337, 315, 352),
    ("mid-low", "Local Minima",  286, 390, 311, 399),
    ("low-L",   "Global Minima", 145, 439, 201, 465),
]
PAD = 10  # frame px expansion

L = []
def P(s=""):
    print(s)
    L.append(s)

img = Image.open(ASSET).convert("RGB")
W, H = img.size
sx, sy = W / PW, H / PH
a = np.asarray(img).astype(np.int32)

dark = (a.max(2) < 145) & ((a.max(2) - a.min(2)) < 80)
opened = ndimage.binary_opening(dark, structure=np.ones((7, 7)))  # drop thin lines

FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]

def render(s, fontpath, fs):
    f = ImageFont.truetype(fontpath, fs)
    im = Image.new("L", (700, 200), 255)
    ImageDraw.Draw(im).text((10, 10), s, font=f, fill=0)
    ar = np.array(im)
    ys, xs = np.nonzero(ar < 128)
    return ar[ys.min():ys.max() + 1, xs.min():xs.max() + 1] < 128

def identify(crop_bool):
    ys, xs = np.nonzero(crop_bool)
    crop = crop_bool[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2.0, "?", None)
    for s in CANDS:
        for fp in (FONT_R, FONT_B):
            for fs in range(16, 140, 2):
                c = render(s, fp, fs)
                if abs(c.shape[0] - crop.shape[0]) > 8 or abs(c.shape[1] - crop.shape[1]) > 30:
                    continue
                cr = np.array(Image.fromarray((c * 255).astype(np.uint8))
                              .resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
                inter = (cr & crop).sum()
                union = (cr | crop).sum()
                v = float(inter) / union if union else -1.0
                if v > best[0]:
                    best = (v, s, fs)
    return best

crops = []
for tag, want, fx0, fy0, fx1, fy1 in BOXES:
    ax0 = int((fx0 - PAD - PX) * sx); ay0 = int((fy0 - PAD - PY) * sy)
    ax1 = int((fx1 + PAD - PX) * sx); ay1 = int((fy1 + PAD - PY) * sy)
    ax0, ay0 = max(0, ax0), max(0, ay0)
    ax1, ay1 = min(W - 1, ax1), min(H - 1, ay1)
    win = opened[ay0:ay1 + 1, ax0:ax1 + 1]
    ink = int(win.sum())
    P("== %s want='%s' frame box x%d..%d y%d..%d -> asset window x%d..%d y%d..%d text-ink=%d"
      % (tag, want, fx0, fx1, fy0, fy1, ax0, ax1, ay0, ay1, ink))
    if ink:
        lab, n = ndimage.label(win, structure=np.ones((3, 3)))
        keep = np.zeros_like(win)
        for i in range(1, n + 1):
            m = lab == i
            if m.sum() >= 25:
                keep |= m
        ys, xs = np.nonzero(keep)
        bx0, bx1, by0, by1 = ax0 + xs.min(), ax0 + xs.max(), ay0 + ys.min(), ay0 + ys.max()
        P("   text cluster asset bbox x%d..%d y%d..%d (%dx%d) -> slide x%.1f..%.1f y%.1f..%.1f"
          % (bx0, bx1, by0, by1, bx1 - bx0 + 1, by1 - by0 + 1,
             PX + bx0 / sx, PX + bx1 / sx, PY + by0 / sy, PY + by1 / sy))
        v, got, fs = identify(keep)
        P("   identified as '%s' IoU=%.3f (best fs=%s)  want='%s'  -> %s"
          % (got, v, fs, want, "MATCH" if got == want else "WRONG"))
        sub = a[by0:by1 + 1, bx0:bx1 + 1]
        crops.append((tag, got, Image.fromarray(sub.astype(np.uint8))
                      .resize(((bx1 - bx0 + 1) * 4, (by1 - by0 + 1) * 4), Image.LANCZOS)))
    else:
        P("   NO text ink found in window")

cw = max(c.width for _, _, c in crops) if crops else 100
ch = sum(c.height for _, _, c in crops) + 10 * max(1, len(crops))
sheet = Image.new("RGB", (cw + 220, ch), (255, 255, 0))
d = ImageDraw.Draw(sheet)
y = 0
for tag, got, c in crops:
    d.text((5, y + 5), "%s id='%s'" % (tag, got), fill=(255, 0, 0))
    sheet.paste(c, (220, y))
    y += c.height + 10
sheet.save(os.path.join(RJ, "probe2_k17r_bl_crops.png"))
P("\ncrops: probe2_k17r_bl_crops.png")

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT)
