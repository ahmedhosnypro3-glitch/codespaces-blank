import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

RED = (r > g + 40) & (r > b + 40)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
BLK = (r < 120) & (g < 120) & (b < 120)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)


def ascii_map(y0, y1, x0, x1, step=1):
    syms = ['R', 'B', 'K', 'Y']
    masks = [RED, BLUE, BLK, YEL]
    print(f"=== y{y0}..{y1} x{x0}..{x1} ===")
    for y in range(y0, y1, step):
        line = ''
        for x in range(x0, x1, step):
            c = '.'
            for m, s in zip(masks, syms):
                if m[y, x]:
                    c = s
                    break
            line += c
        print(f"{y:4d}|{line}")


print("###### BRACKET REGION band1 (x455..510) ######")
ascii_map(158, 215, 455, 512, 1)
print()
print("###### ARROW REGION band1 (x655..730) ######")
ascii_map(126, 255, 655, 732, 2)
