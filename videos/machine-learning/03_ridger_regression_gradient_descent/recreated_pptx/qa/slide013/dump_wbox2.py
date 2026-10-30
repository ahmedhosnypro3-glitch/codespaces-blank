import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

# band1 box interior: x508..622, y158..186. 6x LANCZOS, print every 2 zoom px.
Z = 6
sub = np.asarray(im.crop((508, 158, 622, 186)).resize((114 * Z, 28 * Z), Image.LANCZOS)).astype(float)
lu = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
print("### B1 W-box interior x508..622 y158..186 (6x zoom, 1 char = 1 source px)")
for y in range(0, lu.shape[0], 3):
    row = ''.join('#' if lu[y, x] < 205 else ('+' if lu[y, x] < 235 else '.') for x in range(0, lu.shape[1], 3))
    print(f"{158 + y//Z:4d}| {row}")
