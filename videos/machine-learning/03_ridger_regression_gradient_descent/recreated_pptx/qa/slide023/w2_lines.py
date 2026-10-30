#!/usr/bin/env python3
"""w2 line analyser — word-level segmentation + Arial size/style fit per line.
Fits font size so the CUMULATIVE ADVANCE between consecutive word starts matches
the measured word-start positions (robust: uses spacing, not just total width).
READ-ONLY on unique_slides/slide_023.jpg."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

FONTS = {
    'r': '/usr/share/fonts/TTF/Arial.TTF',
    'b': '/usr/share/fonts/TTF/Arialbd.TTF',
    'i': '/usr/share/fonts/TTF/Ariali.TTF',
    'bi': '/usr/share/fonts/TTF/Arialbi.TTF',
}
SC = 8


def mask_of(kind):
    if kind == 'red':
        return (R > 120) & (R - G > 60) & (R - B > 60)
    if kind == 'navy':
        return (B > R + 30) & (B > 90) & (G < 140)
    if kind == 'dark':
        return (R < 115) & (G < 115) & (B < 115)
    return (R < 130) & (G < 130) & (B < 130)


def words(mask, y0, y1, x0, x1, gap=3):
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    cols = sub.any(axis=0)
    xi = np.where(cols)[0]
    if not len(xi):
        return []
    out = []
    s = p = int(xi[0])
    for x in xi[1:]:
        if x - p > gap:
            out.append((s + x0, p + x0))
            s = int(x)
        p = int(x)
    out.append((s + x0, p + x0))
    return out


def classify(y0, y1, x0, x1):
    sub = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    red = m_ = navy = dark = 0
    for px in sub:
        r, g, b = px
        if r > 120 and r - g > 60 and r - b > 60:
            red += 1
        elif b > r + 30 and b > 90 and g < 140:
            navy += 1
        elif r < 115 and g < 115 and b < 115:
            dark += 1
        else:
            m_ += 1
    tot = len(sub)
    return f"red{red} navy{navy} dark{dark} other{m_}"


def advance(text, size, path):
    f = ImageFont.truetype(path, int(size * SC))
    d = ImageDraw.Draw(Image.new('L', (10, 10)))
    return d.textlength(text, font=f) / SC


def fit(text, starts, path, sizes):
    """least-squares on predicted vs measured word-start offsets."""
    best = None
    for s in sizes:
        x = 0.0
        pred = []
        for w in text.split(' '):
            pred.append(x)
            x += advance(w, s, path) + advance(' ', s, path)
        meas = [st - starts[0] for st in starts]
        if len(pred) != len(meas):
            continue
        err = np.mean([abs(p - m) for p, m in zip(pred, meas)])
        if best is None or err < best[0]:
            best = (err, s, pred[-1] + advance(text.split(' ')[-1], s, path) - (pred[-1]))
    return best


LINES = [
    # name, maskkind, y0,y1, x0,x1, candidate full-line text (words in order)
    ("title",   'red',  74, 106, 60, 830,
     "Inverse of High Dimension Matrix"),
    ("recall",  'dark', 112, 146, 90, 300,
     "Recall:"),
    ("dim1",    'dark', 190, 217, 95, 420,
     "if Feature vectors are of dimension d"),
    ("dim2",    'red',  190, 217, 430, 770,
     "(X^T X) is of size d+1 x d+1"),
    ("blueL1",  'navy', 238, 268, 90, 870,
     "The standard matrix inversion algorithm has a time"),
    ("blueL1b", 'navy', 238, 268, 620, 870,
     "complexity of O(n^3),"),
    ("blueL2",  'navy', 270, 302, 90, 870,
     "which means that the computation time increases rapidly with the size of the matrix"),
    ("blueL3",  'navy', 302, 338, 90, 870,
     "(increasing cubically with the number of components)."),
    ("exL1",    'dark', 356, 390, 90, 870,
     "For Example: if Features vector is of size 1000 then Inverse"),
    ("exL2",    'dark', 392, 424, 90, 560,
     "calculation is or order 1,000,000,000 which is impractical"),
    ("solLab",  'navy', 444, 470, 90, 300,
     "Solution:"),
    ("solL1",   'navy', 470, 502, 230, 760,
     "Instead of using Least Squares with Matrix inversion,"),
    ("solL2",   'navy', 500, 534, 280, 680,
     "use Gradient Descent iterative solution"),
]

for name, kind, y0, y1, x0, x1, text in LINES:
    m = mask_of(kind)
    ws = words(m, y0, y1, x0, x1)
    if not ws:
        print(f"{name}: NO INK")
        continue
    span = ws[-1][1] - ws[0][0] + 1
    print(f"\n{name}: nwords={len(ws)} ink x{ws[0][0]}..{ws[-1][1]} w={span}")
    print("   words: " + " ".join(f"{s}-{e}" for s, e in ws))
    # colour census of the whole line
    mm = m[y0:y1 + 1, ws[0][0]:ws[-1][1] + 1]
    px = a[y0:y1 + 1, ws[0][0]:ws[-1][1] + 1][mm]
    redpx = int(sum(1 for p in px if p[0] > 120 and p[0] - p[1] > 60 and p[0] - p[2] > 60))
    print(f"   {classify(y0, y1, ws[0][0], ws[-1][1])}  redpx={redpx}")
    starts = [s for s, e in ws]
    for st, path in FONTS.items():
        r = fit(text, starts, path, np.arange(10, 44, 0.25))
        if r:
            err, s, tot = r
            print(f"   fit Arial-{st}: size={s:.2f}pt meanstart-err={err:.2f}px "
                  f"pred_total_adv={tot:.1f} (measured {span})")
    # y-extent
    sub = m[y0:y1 + 1, ws[0][0]:ws[-1][1] + 1]
    ys = np.where(sub.any(axis=1))[0]
    print(f"   ink y{ys.min()+y0}..{ys.max()+y0} h={ys.max()-ys.min()+1}")
