#!/usr/bin/env python3
"""Font fit for slide 027 (frame 960x540, 1px = 1pt = 1/72in).

Fits family+size for the 2-line title and the 6 text labels from the banked
measured-geometry dossier (qa/slide027/measured_geometry.md, worker_zcode
2026-10-19 — TRUSTED rows; this script only settles FONT/SIZE, not geometry):

  Title (bold, color 8B0000):
    L1 "Follow Negative Direction of Gradient with"  ink x 191..744 (553), cap band 73..93 (cap 21)
    L2 "Selected Learning Rate"                       ink x 321..621 (300), rows 108..135 (cap ~21)
  Labels (black, regular):
    "Cost"           x 200..238  (w 39),  rows 176..189 (band 14, no descenders -> cap 14)
    "Learning step"  x 297..404 (w 107),  L cap 272..284 (cap ~13), g descender 289
    "Minimum"        x 428..497  (w 69),  rows 364..376 (cap ~13)
    "Random"         x 230..295  (w 65),  rows 444..457 (cap ~13)
    "initial value"  x 219..306  (w 87),  rows 466..479 (i-dot to baseline ~13)
    "\u03b8" (axis)  x 697..709  (w 12),  rows 427..444 (h 17)
    "\u03b8\u0302"   body x 439..449 (w 10), rows 488..504 (h 16), hat 484..485

Method: PIL (FreeType) ink metrics of the candidate TTFs == the metrics LO uses
when rendering, so a width/cap fit here transfers to the render. We pick the
family+size minimizing width error while keeping cap error small.
"""
from PIL import ImageFont

FONTS = {
    "Calibri": "/usr/share/fonts/TTF/calibri.ttf",
    "CalibriBold": "/usr/share/fonts/TTF/calibrib.ttf",
    "Carlito": "/usr/share/fonts/carlito/Carlito-Regular.ttf",
    "CarlitoBold": "/usr/share/fonts/carlito/Carlito-Bold.ttf",
    "LibSans": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "LibSansBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
}

def ink_w(font, text):
    x0, y0, x1, y1 = font.getbbox(text)
    return x1 - x0

def ink_h(font, text):
    x0, y0, x1, y1 = font.getbbox(text)
    return y1 - y0

def cap_h(font, ch="H"):
    return ink_h(font, ch)

def fit_size(path, text, target_w):
    """size (float px) whose rendered ink width == target_w (bisection)."""
    lo, hi = 4.0, 80.0
    for _ in range(60):
        mid = (lo + hi) / 2
        f = ImageFont.truetype(path, int(round(mid * 4)))  # 4x for sub-px precision
        w = ink_w(f, text) / 4.0
        if w < target_w:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def report(path, name, text, target_w):
    s = fit_size(path, text, target_w)
    f = ImageFont.truetype(path, int(round(s * 4)))
    w = ink_w(f, text) / 4.0
    c = cap_h(f) / 4.0
    asc, desc = [m / 4.0 for m in f.getmetrics()]
    print(f"    {name:14s} S={s:6.2f}pt  w={w:6.1f} (target {target_w})  cap={c:5.2f}  asc={asc:5.2f} desc={desc:5.2f} extent={asc+desc:5.2f}")
    return s

TITLE = [
    ("L1", "Follow Negative Direction of Gradient with", 553),
    ("L2", "Selected Learning Rate", 300),
]
LABELS = [
    ("Cost", "Cost", 39, 14),
    ("Learning step", "Learning step", 107, 13),
    ("Minimum", "Minimum", 69, 13),
    ("Random", "Random", 65, 13),
    ("initial value", "initial value", 87, 13),
]
THETA = [("\u03b8 axis", "\u03b8", 12, 17), ("\u03b8hat body", "\u03b8", 10, 16)]

print("== TITLE fit (bold faces) ==")
for fam in ("CalibriBold", "CarlitoBold", "LibSansBold"):
    print(f"  {fam}:")
    for name, text, tw in TITLE:
        report(FONTS[fam], name, text, tw)

print("\n== LABELS joint fit (regular faces) ==")
for fam in ("Calibri", "Carlito", "LibSans"):
    print(f"  {fam}:")
    sizes = []
    for name, text, tw, cap in LABELS:
        s = report(FONTS[fam], name, text, tw)
        sizes.append((name, s, cap))
    joint = sum(s for _, s, _ in sizes) / len(sizes)
    print(f"    -> joint mean S={joint:.2f}; per-label cap targets:")
    for name, s, cap in sizes:
        f = ImageFont.truetype(FONTS[fam], int(round(s * 4)))
        c = cap_h(f) / 4.0
        print(f"       {name:14s} at joint S would need w-scale; own-fit cap={c:.2f} vs target {cap}")

print("\n== \u03b8 glyphs (fit at the label size chosen later; info only) ==")
for fam in ("Calibri", "Carlito", "LibSans"):
    print(f"  {fam}:")
    for name, text, tw, th in THETA:
        s = fit_size(FONTS[fam], text, tw)
        f = ImageFont.truetype(FONTS[fam], int(round(s * 4)))
        print(f"    {name:12s} S={s:6.2f}pt  w={ink_w(f, text)/4.0:5.1f}  h={ink_h(f, text)/4.0:5.1f} (targets w {tw}, h {th})")
        # also height-fit
        lo, hi = 4.0, 80.0
        for _ in range(60):
            mid = (lo + hi) / 2
            f2 = ImageFont.truetype(FONTS[fam], int(round(mid * 4)))
            if ink_h(f2, text) / 4.0 < th:
                lo = mid
            else:
                hi = mid
        s2 = (lo + hi) / 2
        f2 = ImageFont.truetype(FONTS[fam], int(round(s2 * 4)))
        print(f"    {name:12s} height-fit S={s2:6.2f}pt  w={ink_w(f2, text)/4.0:5.1f}  h={ink_h(f2, text)/4.0:5.1f}")
