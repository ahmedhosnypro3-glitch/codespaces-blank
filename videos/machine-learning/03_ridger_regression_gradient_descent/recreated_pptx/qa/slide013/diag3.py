import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(float)
ro = np.asarray(O).astype(float)
lr = 0.299 * ra[:, :, 0] + 0.587 * ra[:, :, 1] + 0.114 * ra[:, :, 2]
lo = 0.299 * ro[:, :, 0] + 0.587 * ro[:, :, 1] + 0.114 * ro[:, :, 2]

print("### RENDER B1: values + W= region x526..586, y140..212 (every 2nd row)")
for y in range(140, 212, 2):
    print(f"{y:4d}| " + "".join(
        "#" if lr[int(y * s), int(x * s)] < 215
        else ("+" if lr[int(y * s), int(x * s)] < 232 else ".")
        for x in range(526, 586)))
print()
print("### ORIGINAL B1: same window")
for y in range(140, 212, 2):
    print(f"{y:4d}| " + "".join(
        "#" if lo[y, x] < 215 else ("+" if lo[y, x] < 232 else ".")
        for x in range(526, 586)))
