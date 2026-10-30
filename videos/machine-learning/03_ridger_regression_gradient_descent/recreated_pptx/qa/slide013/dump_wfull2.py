import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
im = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

print("### B1 box interior x515..624, FULL band y126..252 (ink = lum<215)")
for y in range(126, 253, 2):
    row = "".join("#" if lum[y, x] < 215 else ("+" if lum[y, x] < 232 else ".") for x in range(515, 625))
    print(f"{y:4d}| {row}")

print()
print("### ink column census for B1 box interior x515..624 over y126..252")
for x in range(515, 625):
    n = int((lum[128:250, x] < 215).sum())
    if n > 2:
        print(f"  x{x}: {n}")
