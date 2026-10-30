import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)

bg = ((abs(im[:, :, 0] - 254) < 6) & (abs(im[:, :, 1] - 255) < 6) & (abs(im[:, :, 2] - 253) < 6)) | \
     ((abs(im[:, :, 0] - 233) < 8) & (abs(im[:, :, 1] - 233) < 8) & (abs(im[:, :, 2] - 231) < 10))
ink = ~bg

print("### column ink-row counts, x95..140, band y126..253 (gridline => ~128)")
for x in range(95, 141):
    n = int(ink[126:254, x].sum())
    if n:
        print(f"  x{x}: {n}")

print("\n### column ink-row counts, all x, y126..253; print columns with n>=120")
cols = [(x, int(ink[126:254, x].sum())) for x in range(90, 480)]
print([f"{x}" for x, n in cols if n >= 120])
print("with counts:", [(x, n) for x, n in cols if n >= 120])

print("\n### full-height-ish gridlines for band2 (y265..390) and band3 (y402..528)")
for (y0, y1) in ((265, 390), (402, 528)):
    h = y1 - y0
    res = [(x, int(ink[y0:y1, x].sum())) for x in range(90, 480)]
    print(f" band y{y0}..{y1}:", [(x, n) for x, n in res if n >= h * 0.9])
