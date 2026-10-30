import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = (0.299 * r + 0.587 * g + 0.114 * b)

S = 4
chars = ' .:-=+*%#@'


def dump(y0, y1, x0, x1, title):
    sub = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
    la = np.asarray(sub).astype(float)
    lu = 0.299 * la[:, :, 0] + 0.587 * la[:, :, 1] + 0.114 * la[:, :, 2]
    print(f"### {title}  ({S}x LANCZOS, y{y0}..{y1} x{x0}..{x1})")
    # print every S-th row and col => 2 chars per source px
    for y in range(0, lu.shape[0], S * 2):
        line = ''
        for x in range(0, lu.shape[1], S):
            blk = lu[y:y + S, x:x + S]
            v = blk.min()
            idx = int(np.clip((150 - v) / 150 * 9.99, 0, 9))
            line += chars[idx]
        print(f"{y0 + y//(S*2):4d}| {line}")
    print()


dump(132, 156, 130, 250, "B1 header cols (label,X1,X2,X3)")
dump(133, 157, 250, 375, "B1 header cols X4..X6")
dump(133, 157, 375, 465, "B1 header cols X7,X8")
