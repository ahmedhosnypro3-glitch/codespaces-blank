import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

F = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
NORM = (30, 36)
_c = {}


def tmpl(text, size):
    k = (text, size)
    if k in _c: return _c[k]
    f = ImageFont.truetype(F, size)
    img = Image.new('L', (size * len(text) * 3 + 60, size * 4), 0)
    ImageDraw.Draw(img).text((30, 30), text, font=f, fill=255)
    arr = np.asarray(img)
    ys, xs = np.where(arr > 60)
    out = None
    if len(ys):
        crop = arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        t = Image.fromarray((crop > 60).astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
        out = np.asarray(t) > 100
    _c[k] = out
    return out


def iou(p, q): return (p & q).sum() / max((p | q).sum(), 1)


# interior content crop per band (measured red row groups)
CASES = [
    ("B1", 162, 181, ["W = [0; 2; 0]", "W=[0;2;0]", "W = [0, 2, 0]", "W = [0 2 0]",
                      "W = [0; 2; 0] ", "[0; 2; 0]", "W = [0; 20]", "W = [22; 20; 0]"]),
    ("B2", 300, 318, ["W = [2.7; 0.67; 0.64]", "W=[2.7;0.67;0.64]", "W = [2.7, 0.67, 0.64]",
                      "W = [2.7 0.67 0.64]", "[2.7; 0.67; 0.64]"]),
    ("B3", 438, 457, ["W = [4; 0.29; 0.78]", "W=[4;0.29;0.78]", "W = [4, 0.29, 0.78]",
                      "W = [4; 0.29; 0.78] ", "[4; 0.29; 0.78]"]),
]

for (tag, y0, y1, cands) in CASES:
    x0, x1 = 520, 622
    sub = lum[y0:y1, x0:x1]
    m = sub < 210
    if not m.any():
        print(f"{tag}: no ink")
        continue
    ys, xs = np.where(m)
    crop = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    t = Image.fromarray(crop.astype(np.uint8) * 255).resize(NORM, Image.LANCZOS)
    T = np.asarray(t) > 100
    print(f"### {tag}: ink bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} (w{xs.max()-xs.min()+1})")
    scores = []
    for c in cands:
        best = 0
        for sz in range(10, 30, 2):
            tt = tmpl(c, sz)
            if tt is not None:
                best = max(best, iou(tt, T))
        scores.append((best, c))
    scores.sort(reverse=True)
    for s, c in scores:
        print(f"   {s:.3f}  {c}")
