#!/usr/bin/env python3
"""Probe 4: per BL label region, drop the big wireframe comp, split remaining
dark comps into text lines, identify each line against single-word candidates
(Global/Local/Maxima/Minima). Prints exact baked-in words per line with slide
coords. Read-only. Writes probe4_k17r_bl.txt + probe4_k17r_bl_crops.png."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
ASSET = os.path.join(NS, "recreated_pptx/build/assets/plot_025_bl.png")
OUT = os.path.join(RJ, "probe4_k17r_bl.txt")

PX, PY, PW, PH = 83.0, 290.0, 293.0, 237.0

# generous regions around each ground-truth anchor (frame px)
REGIONS = [
    ("top",     225, 295, 290, 335),
    ("mid-up",  275, 325, 345, 370),
    ("mid-low", 270, 375, 345, 420),
    ("low-L",   130, 425, 215, 480),
    ("low-R",   290, 435, 360, 480),  # possible extra label lower-right
]

L = []
def P(s=""):
    print(s)
    L.append(s)

img = Image.open(ASSET).convert("RGB")
W, H = img.size
sx, sy = W / PW, H / PH
a = np.asarray(img).astype(np.int32)
dark = (a.max(2) < 145) & ((a.max(2) - a.min(2)) < 80)

FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
WORDS = ["Global", "Local", "Maxima", "Minima"]

def render(s, fontpath, fs):
    f = ImageFont.truetype(fontpath, fs)
    im = Image.new("L", (400, 200), 255)
    ImageDraw.Draw(im).text((10, 10), s, font=f, fill=0)
    ar = np.array(im)
    ys, xs = np.nonzero(ar < 128)
    return ar[ys.min():ys.max() + 1, xs.min():xs.max() + 1] < 128

def identify(crop):
    ys, xs = np.nonzero(crop)
    crop = crop[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2.0, "?", None)
    for s in WORDS:
        for fp in (FONT_R, FONT_B):
            for fs in range(14, 130, 2):
                c = render(s, fp, fs)
                cr = np.array(Image.fromarray((c * 255).astype(np.uint8))
                              .resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
                inter = (cr & crop).sum()
                union = (cr | crop).sum()
                v = float(inter) / union if union else -1.0
                if v > best[0]:
                    best = (v, s, fs)
    return best

crops = []
for tag, fx0, fy0, fx1, fy1 in REGIONS:
    ax0 = int((fx0 - PX) * sx); ay0 = int((fy0 - PY) * sy)
    ax1 = int((fx1 - PX) * sx); ay1 = int((fy1 - PY) * sy)
    ax0, ay0 = max(0, ax0), max(0, ay0)
    ax1, ay1 = min(W - 1, ax1), min(H - 1, ay1)
    win = dark[ay0:ay1 + 1, ax0:ax1 + 1]
    lab, n = ndimage.label(win, structure=np.ones((3, 3)))
    keep = np.zeros_like(win)
    for i in range(1, n + 1):
        m = lab == i
        if 8 <= m.sum() <= 1200:  # text glyphs; drop wireframe/leaders (big) and noise
            keep |= m
    P("== region %-6s frame x%d..%d y%d..%d  asset x%d..%d y%d..%d  glyph px=%d"
      % (tag, fx0, fx1, fy0, fy1, ax0, ax1, ay0, ay1, int(keep.sum())))
    if not keep.any():
        P("   (no glyph-size ink)")
        continue
    lab2, n2 = ndimage.label(keep, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n2 + 1):
        ys, xs = np.nonzero(lab2 == i)
        comps.append((ys.min(), ys.max(), xs.min(), xs.max(), len(xs)))
    # group into lines by vertical overlap
    comps.sort()
    lines = []
    for c in comps:
        placed = False
        for ln in lines:
            if not (c[1] < ln["y0"] or c[0] > ln["y1"]):
                ln["y0"] = min(ln["y0"], c[0]); ln["y1"] = max(ln["y1"], c[1])
                ln["x0"] = min(ln["x0"], c[2]); ln["x1"] = max(ln["x1"], c[3])
                ln["comps"].append(c)
                placed = True
                break
        if not placed:
            lines.append({"y0": c[0], "y1": c[1], "x0": c[2], "x1": c[3], "comps": [c]})
    lines.sort(key=lambda ln: ln["y0"])
    for ln in lines:
        if len(ln["comps"]) < 2:
            continue
        m = np.zeros_like(keep)
        for c in ln["comps"]:
            m[c[0]:c[1] + 1, c[2]:c[3] + 1] |= (lab2[c[0]:c[1] + 1, c[2]:c[3] + 1] > 0) & keep[c[0]:c[1] + 1, c[2]:c[3] + 1]
        ys, xs = np.nonzero(m)
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        sub = m[y0:y1 + 1, x0:x1 + 1]
        v, got, fs = identify(sub)
        P("   line asset x%d..%d y%d..%d (%dx%d) slide x%.1f..%.1f y%.1f..%.1f glyphs=%d id='%s' IoU=%.3f"
          % (ax0 + x0, ax0 + x1, ay0 + y0, ay0 + y1, x1 - x0 + 1, y1 - y0 + 1,
             PX + (ax0 + x0) / sx, PX + (ax0 + x1) / sx, PY + (ay0 + y0) / sy, PY + (ay0 + y1) / sy,
             len(ln["comps"]), got, v))
        imgc = Image.fromarray(a[ay0 + y0:ay0 + y1 + 1, ax0 + x0:ax0 + x1 + 1].astype(np.uint8))
        crops.append((tag, got, imgc.resize(((x1 - x0 + 1) * 5, (y1 - y0 + 1) * 5), Image.LANCZOS)))

cw = max(c.width for _, _, c in crops) if crops else 100
ch = sum(c.height for _, _, c in crops) + 10 * max(1, len(crops))
sheet = Image.new("RGB", (cw + 240, ch), (255, 255, 0))
d = ImageDraw.Draw(sheet)
y = 0
for tag, got, c in crops:
    d.text((5, y + 5), "%s '%s'" % (tag, got), fill=(255, 0, 0))
    sheet.paste(c, (240, y))
    y += c.height + 10
sheet.save(os.path.join(RJ, "probe4_k17r_bl_crops.png"))
P("\ncrops: probe4_k17r_bl_crops.png")

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT)
