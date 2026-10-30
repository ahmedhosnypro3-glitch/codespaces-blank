"""Identify slide 030's right-endpoint label by matching rendered serif/sans italic
type against the original frame's ink.

Calibration: the known labels "(2, 10)" and "(5, 1)" are matched against their own
text in each candidate font family and size; the family/size that reproduces the
knowns is then used to score hypotheses for the ambiguous label.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_030.jpg"
g = np.array(Image.open(ORIG).convert("RGB")).astype(float).sum(axis=2) / 3.0

FONTS = {
    "sans-italic": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "serif-italic": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
}


def render(s, size, blur=0.8, ss=4):
    f = ImageFont.truetype(FONTS[fam], int(size * ss))
    im = Image.new("L", (int(len(s) * size * ss * 1.6) + 40, int(size * ss * 2.2) + 40), 0)
    d = ImageDraw.Draw(im)
    d.text((20, 20), s, font=f, fill=255)
    im = im.resize((max(1, im.width // ss), max(1, im.height // ss)), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(float) / 255.0
    m = a > 0.3
    ys, xs = np.nonzero(m)
    if len(xs) < 2:
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def orig_mask(x0, x1, y0, y1, thr):
    m = g[y0:y1, x0:x1] < thr
    ys, xs = np.nonzero(m)
    if len(xs) < 2:
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b):
    a = np.asarray(a, bool); b = np.asarray(b, bool)
    u = np.logical_or(a, b).sum()
    return np.logical_and(a, b).sum() / u if u else 0.0


def score(mask, cand):
    """Best IoU of cand placed on a canvas around mask."""
    if cand is None:
        return 0.0
    H, W = mask.shape
    ch, cw = cand.shape
    best = 0.0
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            y0, x0 = 3 + dy, 3 + dx
            if y0 < 0 or x0 < 0 or y0 + ch > H + 6 or x0 + cw > W + 6:
                continue
            c = np.zeros((H + 6, W + 6), bool)
            c[y0:y0 + ch, x0:x0 + cw] = cand
            m2 = np.zeros((H + 6, W + 6), bool)
            m2[3:3 + H, 3:3 + W] = mask
            best = max(best, iou(m2, c))
    return best


KNOWN = {
    "(2, 10)": (628, 662, 148, 161),
    "(5, 1)": (692, 728, 244, 260),
}
AMBIG = (724, 760, 140, 155)
CANDS = ["(7, 7)", "(7, 1)", "(8, 10)", "(?, ?)", "(x, y)", "(8, 8)", "(0, 0)", "(2, 10)",
         "(5, 1)", "(9, 9)", "(6, 2)", "(8, 2)", "(2, 8)", "(?, 10)", "(10, 10)"]

for fam in FONTS:
    print(f"########## family {fam}")
    print("=== calibration on known labels ===")
    bestcal = {}
    for text, box in KNOWN.items():
        rows = []
        for thr in (180, 190, 200):
            m = orig_mask(*box, thr)
            if m is None:
                continue
            for size in range(8, 16):
                v = score(m, render(text, size))
                rows.append((v, size, thr))
        rows.sort(reverse=True)
        bestcal[text] = rows[0]
        print(f"  {text}: best IoU={rows[0][0]:.3f} at size {rows[0][1]} thr {rows[0][2]}   "
              f"top5: " + " ".join(f"{v:.2f}/sz{s}" for v, s, t in rows[:5]))
    sizes = sorted({s for _, s, _ in bestcal.values()})
    print("=== AMBIG scored against candidates ===")
    for size in sizes:
        for thr in (185, 195):
            m = orig_mask(*AMBIG, thr)
            if m is None:
                continue
            sc = []
            for c in CANDS:
                sc.append((score(m, render(c, size)), c))
            sc.sort(reverse=True)
            print(f"  size {size} thr {thr}: " + "  ".join(f"{c}={v:.2f}" for v, c in sc[:8]))
    print()
