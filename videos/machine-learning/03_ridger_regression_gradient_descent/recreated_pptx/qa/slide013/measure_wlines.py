import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r > g + 40) & (r > b + 40)

F = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
NORM = (24, 30)
_c = {}


def tmpl(text, size, bold):
    k = (text, size, bold)
    if k in _c: return _c[k]
    f = ImageFont.truetype(FB if bold else F, size)
    img = Image.new('L', (size * len(text) * 2 + 40, size * 3), 0)
    ImageDraw.Draw(img).text((20, 20), text, font=f, fill=255)
    arr = np.asarray(img)
    ys, xs = np.where(arr > 60)
    out = None
    if len(ys):
        crop = arr[ys.min():ys.max()+1, xs.min():xs.max()+1]
        t = Image.fromarray((crop > 60).astype(np.uint8)*255).resize(NORM, Image.LANCZOS)
        out = np.asarray(t) > 100
    _c[k] = out
    return out


def iou(p, q): return (p & q).sum() / max((p | q).sum(), 1)


# each band: W-vector region red glyphs y163..180; the 3 value lines are at
# y163..180 (top), y186..211, y228..241 for band1 (rows of the vector)
# measure directly
print("### W-vector / equations red-ink line bands inside the white box (x508..621)")
for (y0, y1, tag) in ((126, 253, 'B1'), (265, 389, 'B2'), (402, 528, 'B3')):
    print(f"--- {tag}")
    for y in range(y0, y1):
        n = int(RED[y, 508:622].sum())
        if n:
            print(f"  y{y}: {n}")
