import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

# numeric column only, inside the box, after the internal separator at x565/566
CASES = [("B1", 162, 181), ("B2", 300, 319), ("B3", 438, 457)]
for (tag, y0, y1) in CASES:
    print(f"### {tag}: numeric region x568..620, y{y0}..{y1} (1 char = 1 px)")
    for y in range(y0, y1):
        print(f"{y:4d}| " + ''.join('#' if lum[y, x] < 215 else ('+' if lum[y, x] < 232 else '.') for x in range(568, 621)))
    print()
