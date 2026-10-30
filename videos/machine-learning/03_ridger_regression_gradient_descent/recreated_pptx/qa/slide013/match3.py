import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

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


def best(t, pool, sizes=range(16, 50, 2)):
    res = []
    for c in pool:
        for bold in (True, False):
            sc = 0
            for sz in sizes:
                tt = tmpl(c, bold, sz)
                if tt is not None:
                    sc = max(sc, iou(tt, t))
            res.append((sc, c, bold))
    res.sort(reverse=True)
    return res[:3]


XG = [92, 133, 173, 213, 255, 296, 337, 377, 418, 459]
print("=== TRAIN HEADER row (band1 y126..157), label col first ===")
for ci in range(9):
    x0, x1 = XG[ci] + 3, XG[ci + 1] - 3
    t, bb = cell(x0, x1, 129, 154)
    if t is None:
        print(f"  col{ci}: empty")
        continue
    print(f"  col{ci}: x{bb[0]}..{bb[2]} -> " + ", ".join(f"{c}/{'B' if bd else 'R'}:{s:.2f}" for s, c, bd in best(t, ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'y', 'Test1', 'Test2', 'Test3'])))

# TEST tables: vlines measured 719/770/821/872 approx -> recompute per band
TG = [719, 770, 821, 872]
TB = [(126, 157, 188, 219, 249), (265, 296, 327, 358, 389), (402, 434, 465, 496, 527)]
NUMS = [str(i) for i in range(0, 200)]
for bi, (t0, t1, t2, t3, t4) in enumerate(TB, 1):
    print(f"=== TEST BAND{bi} (y{t0}..{t4}) ===")
    YB = [t0, t1, t2, t3, t4]
    for ri in range(4):
        y0, y1 = YB[ri] + 3, YB[ri + 1] - 3
        out = []
        for ci in range(3):
            x0, x1 = TG[ci] + 3, TG[ci + 1] - 3
            t, bb = cell(x0, x1, y0, y1)
            if t is None:
                out.append('(empty)')
                continue
            pool = ['Test1', 'Test2', 'Test3'] if ri == 0 else NUMS
            r = best(t, pool)
            out.append(f"{r[0][1]}:{r[0][0]:.2f}x{bb[0]}")
        print(f"  r{ri}: " + " ".join(out))
