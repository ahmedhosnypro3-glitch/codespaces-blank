import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

# dwell: the box interior x508..621. Content occupies x513..570 (left) and
# x560..620 (right numbers). Dump the LEFT half x508..575 for each band.
for (tag, y0, y1) in (("B1", 158, 186), ("B2", 296, 322), ("B3", 435, 461)):
    print(f"### {tag}: x508..578 (left = 'W' + '=' + '[')")
    for y in range(y0, y1):
        row = ''.join('#' if lum[y, x] < 200 else ('+' if lum[y, x] < 232 else '.') for x in range(508, 578))
        print(f"{y:4d}| {row}")
    print()
