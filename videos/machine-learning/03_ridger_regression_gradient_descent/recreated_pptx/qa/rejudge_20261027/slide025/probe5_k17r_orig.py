#!/usr/bin/env python3
"""Probe 5: same line-splitting analysis on the ORIGINAL frame
unique_slides/slide_025.jpg BL area — gives the ground-truth label geometry
(line structure, ink bbox per label, words per line) to replicate.
Read-only. Writes probe5_k17r_orig.txt."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
ORIG = os.path.join(NS, "unique_slides/slide_025.jpg")
OUT = os.path.join(RJ, "probe5_k17r_orig.txt")

REGIONS = [
    ("top",     225, 295, 290, 335),
    ("mid-up",  275, 325, 345, 370),
    ("mid-low", 270, 375, 345, 420),
    ("low-L",   130, 425, 215, 480),
    ("low-R",   290, 435, 360, 480),
]

L = []
def P(s=""):
    print(s)
    L.append(s)

a = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int32)
dark = (a.max(2) < 145) & ((a.max(2) - a.min(2)) < 80)

FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
WORDS = ["Global", "Local", "Maxima", "Minima"]

def render(s, fontpath, fs):
    f = ImageFont.truetype(fontpath, fs)
    im = Image.new("L", (200, 100), 255)
    ImageDraw.Draw(im).text((5, 5), s, font=f, fill=0)
    ar = np.array(im)
    ys, xs = np.nonzero(ar < 128)
    return ar[ys.min():ys.max() + 1, xs.min():xs.max() + 1] < 128

def identify(crop):
    ys, xs = np.nonzero(crop)
    crop = crop[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2.0, "?", None)
    for s in WORDS:
        for fp in (FONT_R, FONT_B):
            for fs in range(4, 30, 1):
                c = render(s, fp, fs)
                cr = np.array(Image.fromarray((c * 255).astype(np.uint8))
                              .resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
                inter = (cr & crop).sum()
                union = (cr | crop).sum()
                v = float(inter) / union if union else -1.0
                if v > best[0]:
                    best = (v, s, fs)
    return best

for tag, fx0, fy0, fx1, fy1 in REGIONS:
    win = dark[fy0:fy1 + 1, fx0:fx1 + 1]
    lab, n = ndimage.label(win, structure=np.ones((3, 3)))
    keep = np.zeros_like(win)
    for i in range(1, n + 1):
        m = lab == i
        if 3 <= m.sum() <= 400:
            keep |= m
    P("== ORIG region %-6s x%d..%d y%d..%d glyph px=%d" % (tag, fx0, fx1, fy0, fy1, int(keep.sum())))
    if not keep.any():
        P("   (no glyph ink)")
        continue
    lab2, n2 = ndimage.label(keep, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n2 + 1):
        ys, xs = np.nonzero(lab2 == i)
        comps.append((ys.min(), ys.max(), xs.min(), xs.max(), len(xs)))
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
            m[c[0]:c[1] + 1, c[2]:c[3] + 1] |= keep[c[0]:c[1] + 1, c[2]:c[3] + 1]
        ys, xs = np.nonzero(m)
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        sub = m[y0:y1 + 1, x0:x1 + 1]
        v, got, fs = identify(sub)
        P("   line frame x%d..%d y%d..%d (%dx%d) glyphs=%d id='%s' IoU=%.3f fs~%s"
          % (fx0 + x0, fx0 + x1, fy0 + y0, fy0 + y1, x1 - x0 + 1, y1 - y0 + 1,
             len(ln["comps"]), got, v, fs))

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT)
