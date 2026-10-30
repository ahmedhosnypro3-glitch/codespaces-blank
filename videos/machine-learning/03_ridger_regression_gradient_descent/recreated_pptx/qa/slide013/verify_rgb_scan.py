import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
ro = np.asarray(O).astype(int)

print("B1 vertical-scan columns (RGB, lum) at y=150,160,170,180,190,200")
for x in range(560, 596):
    vals = []
    for y in (150, 160, 170, 180, 190, 200):
        r, g, b = ro[y, x, 0], ro[y, x, 1], ro[y, x, 2]
        lum = round(0.299 * r + 0.587 * g + 0.114 * b, 1)
        vals.append(f"{lum:6.1f}({r},{g},{b})")
    print(f"x{x:4d}: " + " ".join(vals))

print("\nB2 vertical-scan same columns at y=290,302,310,318,340")
for x in range(560, 596):
    vals = []
    for y in (290, 302, 310, 318, 340):
        r, g, b = ro[y, x, 0], ro[y, x, 1], ro[y, x, 2]
        lum = round(0.299 * r + 0.587 * g + 0.114 * b, 1)
        vals.append(f"{lum:6.1f}({r},{g},{b})")
    print(f"x{x:4d}: " + " ".join(vals))
