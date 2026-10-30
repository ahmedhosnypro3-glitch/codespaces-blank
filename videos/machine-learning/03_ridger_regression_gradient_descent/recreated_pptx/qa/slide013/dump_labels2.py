import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (0.299 * r + 0.587 * g + 0.114 * b)

print("### gridline colour samples (train table)")
for (x, y) in ((133, 140), (133, 170), (173, 140), (459, 140), (92, 170)):
    print(f"  x{x} y{y}: {tuple(int(v) for v in im[y, x])}   neighbours: "
          + " ".join(str(tuple(int(v) for v in im[y, x + d])) for d in (-2, -1, 1, 2)))

chars = ' .:-=+*#%@'
print("\n### TRAIN label grayscale (blue box ~ lum 45, white text ~ lum 200+)")
for y in range(100, 122):
    line = ''
    for x in range(94, 165):
        v = lum[y, x]
        idx = min(int((v - 30) / 230 * 9.99), 9)
        line += chars[max(idx, 0)]
    print(f"{y:4d}| {line}")

print("\n### TEST label grayscale")
for y in range(100, 122):
    line = ''
    for x in range(798, 870):
        v = lum[y, x]
        idx = min(int((v - 30) / 230 * 9.99), 9)
        line += chars[max(idx, 0)]
    print(f"{y:4d}| {line}")
