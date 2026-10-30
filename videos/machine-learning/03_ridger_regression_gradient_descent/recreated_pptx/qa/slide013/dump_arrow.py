import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)

for (tag, y0, y1, x0, x1) in (("LEFT-1", 184, 214, 462, 506), ("RIGHT-1", 184, 214, 625, 670)):
    print(f"### {tag} blue ink map x{x0}..{x1} y{y0}..{y1}")
    for y in range(y0, y1):
        print(f"{y:4d}| " + ''.join('#' if BLUE[y, x] else '.' for x in range(x0, x1)))
    print()

# arrow colour core sample
ys, xs = np.where(BLUE[186:212, 466:502])
print("left-arrow blue core samples:",
      [tuple(int(v) for v in a[y, x]) for y, x in list(zip(ys[:5], xs[:5]))])
