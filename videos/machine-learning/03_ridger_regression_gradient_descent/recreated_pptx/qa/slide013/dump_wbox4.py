import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

for (tag, y0, y1) in (("B2", 300, 320), ("B3", 438, 458)):
    print(f"### {tag} box interior x570..624")
    for y in range(y0, y1):
        print(f"{y:4d}| " + ''.join('#' if lum[y, x] < 205 else ('+' if lum[y, x] < 235 else '.') for x in range(570, 624)))
    print()
