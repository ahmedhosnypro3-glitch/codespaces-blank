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
_cache = {}


def tmpl(text, bold, size):
    key = (text, bold, size)
    if key in _cache:
        return _cache[key]
    f = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    img = Image.new('L', (size * len(text) * 2 + 40, size * 3), 0)
    d = ImageDraw.Draw(img)
    d.text((20, 20), text, font=f, fill=255)
    arr = np.asarray(img)
    ys, xs = np.where(arr > 60)
    out = None
    if len(ys):
        crop = arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        t = Image.fromarray((crop > 60).astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
        out = np.asarray(t) > 100
    _cache[key] = out
    return out


def cell(x0, x1, y0, y1, thr=190):
    sub = lum[y0:y1, x0:x1]
    m = sub < thr
    if not m.any():
        return None, None
    ys, xs = np.where(m)
    crop = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    t = Image.fromarray(crop.astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
    return np.asarray(t) > 100, (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)


def iou(p, q):
    return (p & q).sum() / max((p | q).sum(), 1)


def best_match(tmpl_img, pool, bold, sizes=range(16, 48, 2)):
    best = None
    for c in pool:
        sc = 0
        for sz in sizes:
            t = tmpl(c, bold, sz)
            if t is not None:
                sc = max(sc, iou(t, tmpl_img))
        if best is None or sc > best[1]:
            best = (c, sc)
    return best


NUMS = [str(i) for i in range(0, 200)]
XG = [92, 133, 173, 213, 255, 296, 337, 377, 418, 459]
BANDS = [("BAND1", 126, 157, 188, 219, 249),
         ("BAND2", 265, 296, 327, 358, 389),
         ("BAND3", 402, 434, 465, 496, 527)]

for (name, t0, t1, t2, t3, t4) in BANDS:
    YB = [t0, t1, t2, t3, t4]
    print(f"===== {name} TRAIN (rows y{t0}..{t4}) =====")
    for ri in range(4):
        y0, y1 = YB[ri] + 3, YB[ri + 1] - 3
        out = []
        for ci in range(9):
            x0, x1 = XG[ci] + 3, XG[ci + 1] - 3
            ti, bb = cell(x0, x1, y0, y1)
            if ti is None:
                out.append('(empty)')
                continue
            if ri == 0:
                pool = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8'] if ci > 0 else ['X1', 'X2', 'y']
                bold = True
            elif ci == 0:
                pool = ['X1', 'X2', 'y']
                bold = True
            else:
                pool = NUMS
                bold = False
            bm = best_match(ti, pool, bold)
            out.append(f"{bm[0]}({bm[1]:.2f})x{bb[0]}")
        print(f" r{ri}: " + " ".join(out))
