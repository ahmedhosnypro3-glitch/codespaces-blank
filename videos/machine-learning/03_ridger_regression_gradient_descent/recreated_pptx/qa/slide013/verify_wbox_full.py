import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
ro = np.asarray(O).astype(int)

# band-2 W box interior: x505..624 y265..390. R = red mask, K = black mask.
x0, x1, y0, y1 = 505, 625, 265, 390
print("orig band-2 W box interior x505..624 y265..389 — R=red ink, K=black ink")
for y in range(y0, y1):
    row = []
    for x in range(x0, x1):
        r, g, b = ro[y, x]
        if r > 110 and g < 80 and b < 80:
            row.append("R")
        elif r < 110 and g < 110 and b < 110:
            row.append("K")
        else:
            row.append(".")
    print(f"{y:4d}| " + "".join(row))
