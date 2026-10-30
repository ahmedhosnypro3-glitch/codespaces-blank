#!/usr/bin/env python3
"""Per-line glyph segmentation + font-size fit for slide_023 body text.
Prints original glyph geometry, then the Arial size whose advance span matches the
measured ink span, plus the predicted cap/x heights for that size."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
REG = '/usr/share/fonts/TTF/Arial.TTF'


def ink_mask(kind, y0, y1, x0, x1):
    if kind == 'red':
        return (R > 120) & (R - G > 60) & (R - B > 60)
    if kind == 'dark':
        return (R < 110) & (G < 110) & (B < 110)
    if kind == 'navy':
        return (B > R + 30) & (B > 90) & (G < 140)
    return (R < 130) & (G < 130) & (B < 130)


def seg(xs, gap=1):
    r = []; s = xs[0]; p = xs[0]
    for x in xs[1:]:
        if x > p + gap:
            r.append((s, p)); s = x
        p = x
    r.append((s, p)); return r


def glyphs(kind, y0, y1, x0, x1):
    m = ink_mask(kind, 0, 0, 0, 0)
    sub = m[y0:y1 + 1, x0:x1 + 1]
    xs = np.where(sub.any(axis=0))[0]
    if not len(xs):
        return []
    out = []
    for (s, e) in seg(xs, 1):
        g = sub[:, s:e + 1]
        ys = np.where(g.any(axis=1))[0]
        out.append((s + x0, e - s + 1, ys[0] + y0, ys[-1] + y0, ys[-1] - ys[0] + 1, int(g.sum())))
    return out


def adv(text, size, reg=REG):
    f = ImageFont.truetype(reg, size=size * 8)
    d = ImageDraw.Draw(Image.new('L', (10, 10)))
    return d.textlength(text, font=f) / 8.0


def fit_span(text, target, reg=REG, lo=8, hi=48):
    best = None
    for s in np.arange(lo, hi, 0.125):
        w = adv(text, s, reg)
        if best is None or abs(w - target) < abs(best[1] - target):
            best = (s, w)
    return best


LINES = [
    # (name, mask, y0,y1, x0,x1, text, style_hint)
    ("recall",     'dark', 110, 146,  95, 400, "Recall:", ''),
    ("dimnote1",   'dark', 191, 219,  95, 460, "if Feature vectors are of dimension d", ''),
    ("dimnote2",   'any',  191, 219, 460, 780, "(X^T X) is of size d+1 x d+1", ''),
    ("blueL1",     'navy', 238, 270,  90, 870, "The standard matrix inversion algorithm has a time", ''),
    ("blueL2",     'navy', 270, 304,  90, 870, "complexity of O(n^3), which means that the computation", ''),
    ("blueL3",     'navy', 304, 338,  90, 870, "time increases rapidly with the size of the matrix", ''),
    ("blueL4",     'navy', 304, 338,  90, 870, "time increases rapidly with the size of the matrix (increasing", ''),
    ("exL1",       'any',  360, 392,  90, 870, "For Example: if Features vector is of size 1000 then Inverse", ''),
    ("exL2",       'any',  392, 424,  90, 870, "calculation is or order 1,000,000,000 which is impractical", ''),
    ("solL1",      'navy', 470, 500, 240, 730, "Instead of using Least Squares with Matrix inversion,", ''),
    ("solL2",      'navy', 500, 528, 300, 670, "use Gradient Descent iterative solution", ''),
]
for name, kind, y0, y1, x0, x1, text, hint in LINES:
    g = glyphs(kind, y0, y1, x0, x1)
    if not g:
        print(f"{name}: EMPTY"); continue
    span = g[-1][0] + g[-1][1] - 1 - g[0][0] + 1
    caps = [t for t in g if t[2] <= g[0][2] + 2 and t[4] >= 15]
    s, w = fit_span(text, span)
    # predicted cap/x for size s
    f = ImageFont.truetype(REG, size=int(s * 8))
    d = ImageDraw.Draw(Image.new('L', (10, 10)))
    bb = d.textbbox((0, 0), 'H', font=f); cap = (bb[3] - bb[1]) / 8.0
    bb = d.textbbox((0, 0), 'x', font=f); xh = (bb[3] - bb[1]) / 8.0
    tops = sorted(set(t[2] for t in g))
    bots = sorted(set(t[3] for t in g))
    print(f"{name:9s} ng={len(g):2d} span={span:4d} fit={s:5.2f}pt adv={w:6.1f} "
          f"cap_pred={cap:4.1f} x_pred={xh:4.1f} | glyph tops={tops} bots={bots}")
    print("           glyphs: " + " ".join(f"x{t[0]}/w{t[1]}/y{t[2]}-{t[3]}" for t in g))
