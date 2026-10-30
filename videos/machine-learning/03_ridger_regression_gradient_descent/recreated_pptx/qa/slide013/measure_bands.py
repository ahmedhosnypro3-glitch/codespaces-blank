import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

bg = ((abs(r - 254) < 8) & (abs(g - 255) < 8) & (abs(b - 253) < 8)) | \
     ((abs(r - 233) < 10) & (abs(g - 233) < 10) & (abs(b - 231) < 12))
ink = ~bg

print("=== per-row ink count in x60..900 (5-row blocks) ===")
for y in range(0, H, 5):
    n = int(ink[y:y + 5, 60:900].sum())
    print(f"{y:4d} {n:6d}")
