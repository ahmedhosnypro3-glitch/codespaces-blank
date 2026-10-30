import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

FONT_B = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'

NORM = (28, 34)


def render_template(text, bold, size):
    f = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    # generous box
    img = Image.new('L', (size * len(text) * 2 + 40, size * 3), 0)
    d = ImageDraw.Draw(img)
    d.text((20, 20), text, font=f, fill=255)
    arr = np.asarray(img)
    ys, xs = np.where(arr > 60)
    if not len(ys):
        return None
    crop = arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    t = Image.fromarray((crop > 60).astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
    return np.asarray(t) > 100


def cell_ink(x0, x1, y0, y1):
    sub = lum[y0:y1, x0:x1]
    # cell fill is white(254) or yellow(255,255,0)) -> ink is dark
    m = sub < 190
    if not m.any():
        return None
    ys, xs = np.where(m)
    crop = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    t = Image.fromarray(crop.astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
    return np.asarray(t) > 100, (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)


def iou(p, q):
    return (p & q).sum() / max((p | q).sum(), 1)


CANDS = [str(i) for i in range(0, 10)]
CANDS_B = ['X' + str(i) for i in range(1, 10)]

# train table cells band 1: boundaries
XG = [92, 133, 173, 213, 255, 296, 337, 377, 418, 459]
YB = [126, 157, 188, 219, 249]

print("=== TRAIN BAND1 cell matching (row 0 = header) ===")
for ri in range(4):
    y0, y1 = YB[ri] + 3, YB[ri + 1] - 3
    out = []
    for ci in range(9):
        x0, x1 = XG[ci] + 3, XG[ci + 1] - 3
        res = cell_ink(x0, x1, y0, y1)
        if res is None:
            out.append('(empty)')
            continue
        tmpl, bb = res
        if ri == 0:
            pool = CANDS_B if ci > 0 else ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'y']
            bold = True
        elif ci == 0:
            pool = ['X1', 'X2', 'y']
            bold = True
        else:
            pool = CANDS
            bold = False
        best = None
        for c in pool:
            sc = 0
            for sz in range(18, 46, 2):
                t = render_template(c, bold, sz)
                if t is None:
                    continue
                sc = max(sc, iou(t, tmpl))
            if best is None or sc > best[1]:
                best = (c, sc)
        out.append(f"{best[0]}:{best[1]:.2f}@x{bb[0]}")
    print(f" row{ri}: " + " | ".join(out))
