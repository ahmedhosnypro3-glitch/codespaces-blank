import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

RED = (r > g + 40) & (r > b + 40)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
BLK = (r < 120) & (g < 120) & (b < 120)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)
syms = ['R', 'B', 'K', 'Y']
masks = [RED, BLUE, BLK, YEL]

step = 3
y0, y1, x0, x1 = 126, 256, 90, 890
print("legend R=red B=blue K=black Y=yellow .=panel/white; every 3rd px, x0=90")
print("      " + ''.join('|' if ((x0 + i * step) % 50 < step) else ('+' if ((x0 + i * step) % 25 < step) else ' ') for i in range((x1 - x0) // step + 1)))
for y in range(y0, y1, step):
    line = ''
    for x in range(x0, x1, step):
        c = '.'
        for m, s in zip(masks, syms):
            if m[y, x]:
                c = s
                break
        line += c
    print(f"{y:4d}| {line}")
