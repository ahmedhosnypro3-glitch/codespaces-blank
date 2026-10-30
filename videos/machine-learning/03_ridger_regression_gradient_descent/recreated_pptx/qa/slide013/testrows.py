import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

print("=== TEST table ink row profile (x722..870) — glyph bands ===")
for y in range(120, 535):
    n = int((lum[y, 722:870] < 200).sum())
    if n:
        print(f"  y{y}: {n}")
