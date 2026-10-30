import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

REGIONS = [("ELL1", 216, 248, 512, 600), ("ELL2", 354, 387, 512, 604), ("ELL3", 492, 525, 516, 606)]
for (name, y0, y1, x0, x1) in REGIONS:
    print(f"### {name}: dark-ink map x{x0}..{x1} y{y0}..{y1} (# lum<150, + lum<185)")
    for y in range(y0, y1):
        line = ''.join('#' if lum[y, x] < 150 else ('+' if lum[y, x] < 185 else '.') for x in range(x0, x1))
        print(f"{y:4d}| {line}")
    print()
