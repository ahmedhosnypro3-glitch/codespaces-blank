import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

S = 5
chars = ' .:-=+*%#@'


def dump(y0, y1, x0, x1, title):
    sub = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
    la = np.asarray(sub).astype(float)
    lu = 0.299 * la[:, :, 0] + 0.587 * la[:, :, 1] + 0.114 * la[:, :, 2]
    print(f"### {title} x{x0}..{x1} y{y0}..{y1}")
    for y in range(0, lu.shape[0], S * 2):
        line = ''
        for x in range(0, lu.shape[1], S):
            blk = lu[y:y + S, x:x + S]
            v = blk.min()
            idx = int(np.clip((190 - v) / 190 * 9.99, 0, 9))
            line += chars[idx]
        print("    " + line)
    print()


dump(216, 248, 510, 602, "ELLIPSE 1 text")
dump(354, 387, 512, 604, "ELLIPSE 2 text")
dump(492, 525, 516, 606, "ELLIPSE 3 text")
