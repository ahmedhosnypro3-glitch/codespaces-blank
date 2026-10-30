import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (0.299 * r + 0.587 * g + 0.114 * b)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)

chars = ' .:-=+*#%@'


def dump(y0, y1, x0, x1, title, marks=()):
    print(f"### {title}  (Y=yellow fill)")
    for y in range(y0, y1):
        line = ''
        for x in range(x0, x1):
            if YEL[y, x]:
                line += 'Y'
            else:
                v = lum[y, x]
                idx = min(int((v - 30) / 230 * 9.99), 9)
                line += chars[max(idx, 0)]
        mk = ' <-- ' + ', '.join(marks) if y in marks else ''
        print(f"{y:4d}| {line}{mk}")
    print()


BANDS = [("BAND1 train", 126, 256), ("BAND2 train", 265, 391), ("BAND3 train", 402, 529)]
for name, y0, y1 in BANDS:
    dump(y0 + 9, y0 + 33, 88, 462, f"{name} HEADER row (y{y0+9}..{y0+33})")
for name, y0, y1 in BANDS:
    dump(y0 + 33, y0 + 64, 88, 462, f"{name} DATA ROW 1 (X1) y{y0+33}..{y0+64}")
for name, y0, y1 in BANDS:
    dump(y0 + 64, y0 + 95, 88, 462, f"{name} DATA ROW 2 (X2) y{y0+64}..{y0+95}")
for name, y0, y1 in BANDS:
    dump(y0 + 95, y0 + 128, 88, 462, f"{name} DATA ROW 3 (y) y{y0+95}..{y0+128}")
