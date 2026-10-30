import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

for (tag, y0, y1) in (("B1", 158, 186), ("B2", 298, 325), ("B3", 434, 462)):
    print(f"### {tag} content lines (red box interior x510..620)")
    for y in range(y0, y1):
        row = ''.join('#' if lum[y, x] < 200 else ('+' if lum[y, x] < 235 else '.') for x in range(510, 621))
        print(f"{y:4d}| {row}")
    print()
