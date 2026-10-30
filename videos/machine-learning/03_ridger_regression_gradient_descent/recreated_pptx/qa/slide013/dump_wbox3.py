import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

print("### B1 interior LEFT x508..570")
for y in range(158, 188):
    print(f"{y:4d}| " + ''.join('#' if lum[y, x] < 205 else ('+' if lum[y, x] < 235 else '.') for x in range(508, 571)))
print()
print("### B1 interior RIGHT x570..624")
for y in range(158, 188):
    print(f"{y:4d}| " + ''.join('#' if lum[y, x] < 205 else ('+' if lum[y, x] < 235 else '.') for x in range(570, 624)))
