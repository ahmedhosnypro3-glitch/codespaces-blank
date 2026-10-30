#!/usr/bin/env python3
"""Pass-6 (resume worker w4-s026): decisive font/size/wrap identification.

1. TITLE: rasterize 'Gradient Descent Solution' in EVERY available bold TTF at a
   range of sizes; match the measured ink band (x 294..639 w=346, y 60..82 h=23,
   center 466.5) — ink bbox from the raster, halo-free.
2. BODY/NOTES: for each measured line, enumerate every prefix of the source text
   as the line content at sizes 15..19 (Arial reg/bold mixes ignored — all-reg
   approximation) and rank |predicted ink extent - measured|. Then check greedy
   wrap consistency across the lines of one block to pin the text-box width.
"""
import glob
import numpy as np
from PIL import Image, ImageFont, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

TITLE = "Gradient Descent Solution"
T_MEAS = {"x0": 294, "x1": 639, "y0": 60, "y1": 82}  # ink, incl ~1px halo

def ink_bbox(text, fontpath, size):
    """Rasterize the text large, return (ink_w, ink_h, left_ink, top_ink) in px at 4x, /4."""
    S = 4
    f = ImageFont.truetype(fontpath, int(round(size * S)))
    img = Image.new("L", (int(size * S * len(text) * 1.5) + 200, size * S * 3), 0)
    d = ImageDraw.Draw(img)
    d.text((100, 100), text, font=f, fill=255)
    a = np.asarray(img)
    ys, xs = np.where(a > 40)
    if not len(xs):
        return None
    return ((xs.max() - xs.min() + 1) / S, (ys.max() - ys.min() + 1) / S,
            (xs.min() - 100) / S, (ys.min() - 100) / S)

print("== TITLE FONT SCAN (target ink w=346, h=23) ==")
fonts = sorted(glob.glob("/usr/share/fonts/**/*.ttf", recursive=True))
bold_like = [p for p in fonts if any(k in p.lower() for k in ("bd", "bold", "black", "blk"))]
best = []
for p in bold_like:
    for s in range(22, 40):
        r = ink_bbox(TITLE, p, s)
        if r is None:
            continue
        w, h, li, ti = r
        score = abs(w - 346) + abs(h - 23) * 4
        best.append((score, w, h, s, p.split("/")[-1]))
best.sort()
for score, w, h, s, name in best[:15]:
    print(f"  {name:28s} s={s:2d} ink_w={w:6.1f} ink_h={h:5.1f} score={score:.1f}")

print("\n== BODY LINE ID: prefix match, sizes 15..19 (Arial) ==")
AR = "/usr/share/fonts/TTF/Arial.TTF"
ARB = "/usr/share/fonts/TTF/Arialbd.TTF"

def ink_extent(text, size, bold=False):
    r = ink_bbox(text, ARB if bold else AR, size)
    return None if r is None else (r[0], r[1])

# measured line ink extents (text only, bullet disc excluded; halo ~2px total)
LINES = [
    # (name, source text (full bullet), measured ink width px)
    ("rowA", "[1] Start with initial Random Weights (W)", 324),
    ("rowB", "[2] Update the weights by moving along the direction of negative gradient of Loss function", 701),
    ("rowC", "(w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)", 544),
    ("rowD", "[3] Stop when the gradient is almost zero (this is at the minimum value of the function)", 685),
    ("N1", "Least Squares Linear regression objective function is a convex function (even with regularizer). This means it has ONE Minimum (good news ).", 660),
    ("N2", "Least Squares Linear regression objective function is a convex function (even with regularizer). This means it has ONE Minimum (good news ).", 467),
    ("N3", "GD will approximately find this minimum value but at a variable number of steps depending on the used Learning Rate", 727),
    ("N4", "GD will approximately find this minimum value but at a variable number of steps depending on the used Learning Rate", 184),
]
for name, full, meas in LINES:
    words = full.split(" ")
    cands = []
    for s in (15, 16, 17, 18, 19):
        for k in range(1, len(words) + 1):
            line = " ".join(words[:k])
            r = ink_extent(line, s)
            if r is None:
                continue
            w, h = r
            if abs(w - meas) <= max(6, 0.02 * meas):
                cands.append((abs(w - meas), s, k, line, w, h))
    cands.sort()
    print(f" -- {name} (measured {meas}) --")
    for d, s, k, line, w, h in cands[:6]:
        print(f"    s={s} w={w:.1f} d={d:.1f} :: {line[:95]}")

print("\n== GREEDY WRAP WIDTH CHECK: for the winning size, max line ink that still fits ==")
# (filled after seeing results)
