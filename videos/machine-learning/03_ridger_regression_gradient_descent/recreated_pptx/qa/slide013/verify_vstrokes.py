import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
ro = np.asarray(O).astype(float)
lum = 0.299 * ro[:, :, 0] + 0.587 * ro[:, :, 1] + 0.114 * ro[:, :, 2]

for tag, (y0, y1) in (("B1", (127, 251)), ("B2", (266, 389)), ("B3", (403, 527))):
    print(f"=== {tag}: columns with many mid-dark px (lum<175) inside W box x507..622 ===")
    for x in range(507, 623):
        col = lum[y0:y1, x]
        n = int((col < 175).sum())
        if n >= 8:
            ys = [y0 + i for i in range(y1 - y0) if col[i] < 175]
            print(f"x{x:4d} n={n:3d} y{ys[0]}..{ys[-1]}")
    print()
