import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

print("### B2 FULL box interior x515..624, y296..322")
for y in range(296, 323):
    print(f"{y:4d}| " + ''.join('#' if lum[y, x] < 215 else ('+' if lum[y, x] < 232 else '.') for x in range(515, 625)))
print()
print("### B1 FULL box interior x515..624, y158..184")
for y in range(158, 185):
    print(f"{y:4d}| " + ''.join('#' if lum[y, x] < 215 else ('+' if lum[y, x] < 232 else '.') for x in range(515, 625)))
