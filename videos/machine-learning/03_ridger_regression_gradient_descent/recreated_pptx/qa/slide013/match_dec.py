import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

FONT_R = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
NORM = (28, 34)
_cache = {}


def tmpl(text, size):
    key = (text, size)
    if key in _cache: return _cache[key]
    f = ImageFont.truetype(FONT_R, size)
    img = Image.new('L', (size * len(text) * 2 + 40, size * 3), 0)
    ImageDraw.Draw(img).text((20, 20), text, font=f, fill=255)
    arr = np.asarray(img)
    ys, xs = np.where(arr > 60)
    out = None
    if len(ys):
        crop = arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        t = Image.fromarray((crop > 60).astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
        out = np.asarray(t) > 100
    _cache[key] = out
    return out


def cell(x0, x1, y0, y1, thr=200):
    sub = lum[y0:y1, x0:x1]
    m = sub < thr
    if not m.any(): return None, None
    ys, xs = np.where(m)
    crop = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    t = Image.fromarray(crop.astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
    return np.asarray(t) > 100, (xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0)


def iou(p, q): return (p & q).sum() / max((p | q).sum(), 1)


TG = [719, 770, 821, 872]
DECS = ['24.4', '31.2', '38', '32.4', '42.3', '52.3', '60', '80', '100', '30', '40', '50',
        '15', '20', '25', '4', '8.11', '16.7', '0', '1', '2', '3', '2.7', '0.67', '0.64',
        '4', '0.29', '0.78', '2', '6', '11', '10', '9', '18', '16', '22', '5', '7']
bands = [(360, 385, 'B2'), (498, 523, 'B3')]
for (y0, y1, tag) in bands:
    for ci, (x0, x1) in enumerate(zip(TG[:-1], TG[1:]), 1):
        t, bb = cell(x0 + 3, x1 - 3, y0, y1)
        if t is None:
            print(f"{tag} col{ci}: empty"); continue
        scores = sorted(((iou(tmpl(c, s), t), c, s) for c in DECS for s in range(16, 46, 2)), reverse=True)
        print(f"{tag} col{ci} x{bb[0]}..{bb[2]} y{bb[1]}..{bb[3]} -> " +
              ", ".join(f"{c}@{sg}:{v:.2f}" for v, c, sg in scores[:4]))
