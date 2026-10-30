import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

# B1 content y163..180 ; B2 y300..319 ; B3 y439..458 ; the RIGHT part (after the
# box's internal separator at x~563..570) holds the numbers.
for (tag, y0, y1) in (("B1", 161, 182), ("B2", 298, 321), ("B3", 437, 460)):
    print(f"### {tag}: x560..620 (numeric column) — 5x zoom")
    sub = np.asarray(im.crop((558, y0, 622, y1)).resize((64 * 2, (y1 - y0) * 10), Image.LANCZOS)).astype(float)
    lu = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    for y in range(0, lu.shape[0], 5):
        row = ''.join('#' if lu[y, x] < 200 else ('+' if lu[y, x] < 232 else '.') for x in range(0, lu.shape[1], 3))
        print(f"  {row}")
    print()
