#!/usr/bin/env python3
"""Font-fit measurement for slide_023.js: find Arial size (pt) per text line so the
rendered glyph advance matches the original frame's measured ink width, and derive
cap/x-heights + baselines. 960x540 frame, 1px = 1pt = 1/72in.

Runs the SAME pipeline the build uses (pptxgenjs writes <a:latin typeface="Arial">;
LibreOffice substitutes Arial.TTF on this host)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
F = {
    'reg': '/usr/share/fonts/TTF/Arial.TTF',
    'bold': '/usr/share/fonts/TTF/Arialbd.TTF',
    'it': '/usr/share/fonts/TTF/Ariali.TTF',
    'bi': '/usr/share/fonts/TTF/Arialbi.TTF',
}


def ink_width(text, style, size_pt):
    """Advance width in px for Arial at size_pt (1px=1pt)."""
    f = ImageFont.truetype(F[style], size=size_pt * 4)   # 4x for precision
    d = ImageDraw.Draw(Image.new('L', (10, 10)))
    return d.textlength(text, font=f) / 4.0


def fit(text, style, target, lo=8, hi=60):
    best = None
    for s in np.arange(lo, hi, 0.25):
        w = ink_width(text, style, s)
        if best is None or abs(w - target) < abs(best[1] - target):
            best = (s, w)
    return best


# (label, text, style, measured ink x0,x1, measured ink y0,y1, note)
LINES = [
    ("title",      "Inverse of High Dimension Matrix", "bold", 220, 654, 78, 105, "no descenders -> cap h = 28"),
    ("recall_lbl", "Recall:",                          "reg",  104, 177, 117, 141, "italic+underline per spec"),
    # equation handled separately (image)
    # dimension note: 'if Feature vectors are of dimension d' then '(X^T X) is of size d+1 x d+1'
    ("dimnote1",   "if Feature vectors are of dimension d", "reg", 104, 394, 196, 215, "has 'd' asc + descenders? no desc"),
    ("dimnote1b",  "(X^T X) is of size d+1 x d+1",          "reg", 505, 746, 196, 215, "red 'd+1 x d+1'"),
    # blue box lines
    ("blueL1",  "The standard matrix inversion algorithm has a time complexity", "reg", 98, 768, 242, 266, "red tail O(n^3) at x775..834"),
    ("blueL2",  "of O(n^3), which means that the computation time increases", "reg", 97, 840, 276, 300, "O(n^3) red part of L1"),
    ("blueL3",  "rapidly with the size of the matrix (increasing cubically with the", "reg", 97, 760, 310, 333, "wraps"),
    ("blueL4",  "number of components).", "reg", 97, 760, 310, 333, "?"),
    # example lines
    ("exL1", "For Example: if Features vector is of size 1000 then Inverse", "reg", 96, 853, 364, 387, "red '1000' ~x530..577"),
    ("exL2", "calculation is or order 1,000,000,000 which is impractical", "reg", 96, 541, 398, 421, "red 1,000,000,000 x187..327"),
    # solution
    ("solL1", "Instead of using Least Squares with Matrix inversion,", "reg", 247, 709, 478, 496, "navy"),
    ("solL2", "use Gradient Descent iterative solution", "reg", 314, 648, 506, 520, "navy smaller"),
]

print(f"{'line':11s} {'style':5s} {'meas_w':>7s} {'fit_pt':>7s} {'fit_w':>7s} {'err':>6s}")
for name, text, style, x0, x1, y0, y1, note in LINES:
    tgt = x1 - x0 + 1
    s, w = fit(text, style, tgt)
    print(f"{name:11s} {style:5s} {tgt:7d} {s:7.2f} {w:7.1f} {w-tgt:+6.1f}")

print()
print("=== cap/x height per line (y extents) ===")
# measure per-line ink rows in the ORIGINAL to get cap/x height + baseline
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 120) & (R - G > 80) & (R - B > 80)
blk = (R < 110) & (G < 110) & (B < 110)
navy = (B > R + 30) & (B > 90) & (G < 140)
dark = blk | navy | red
BANDS = [
    ("title",      70, 112, 150, 800),
    ("recall",    112, 146,  95, 400),
    ("dimnote",   191, 219,  95, 780),
    ("blueL1",    238, 270,  90, 870),
    ("blueL2",    270, 304,  90, 870),
    ("blueL3",    304, 338,  90, 870),
    ("exL1",      360, 392,  90, 870),
    ("exL2",      392, 424,  90, 870),
    ("solL1",     470, 500, 240, 730),
    ("solL2",     500, 528, 300, 670),
]
for name, y0, y1, x0, x1 in BANDS:
    sub = dark[y0:y1 + 1, x0:x1 + 1]
    rows = np.where(sub.sum(axis=1) > 0)[0]
    if len(rows) == 0:
        print(f" {name:9s} EMPTY"); continue
    top, bot = rows[0] + y0, rows[-1] + y0
    # per-row counts to spot ascender/descender columns
    print(f" {name:9s} ink y {top}..{bot}  h={bot-top+1}  rows={len(rows)}")

print()
print("=== Arial cap/x/asc/desc heights at candidate sizes (px) ===")
for s in [14, 15, 16, 17, 18, 19, 20, 22, 24, 28, 32, 36, 40]:
    f = ImageFont.truetype(F['reg'], size=s * 4)
    asc, desc = f.getmetrics()
    # cap height via 'H', x-height via 'x', ascender via 'd'
    d = ImageDraw.Draw(Image.new('L', (10, 10)))
    def hgt(ch):
        bb = d.textbbox((0, 0), ch, font=f)
        return (bb[3] - bb[1]) / 4.0
    print(f"  {s:3d}pt: cap(H)={hgt('H'):5.1f} x(x)={hgt('x'):5.1f} asc(d)={hgt('d'):5.1f} "
          f"desc(p)={hgt('p'):5.1f} asc+desc={ (asc+desc)/4.0:5.1f}  adv('M')={ink_width('M','reg',s):5.1f}")
