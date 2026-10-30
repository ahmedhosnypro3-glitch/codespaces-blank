import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
im = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

# bracket region only (x568..584) for each band: shows the stacked vector values
for (tag, y0, y1) in (("B1", 132, 214), ("B2", 271, 353), ("B3", 409, 491)):
    print(f"### {tag} vector digits x568..584, y{y0}..{y1}")
    for y in range(y0, y1):
        row = "".join("#" if lum[y, x] < 215 else ("+" if lum[y, x] < 232 else ".") for x in range(568, 585))
        print(f"{y:4d}| {row}")
    print()
