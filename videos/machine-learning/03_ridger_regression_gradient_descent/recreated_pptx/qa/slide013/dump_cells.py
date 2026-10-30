import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# glyph separation for band1 rows
REGS = [
    ("B1 label row1 'X1'", 88, 135, 160, 191),
    ("B1 label row2 'X2'", 88, 135, 190, 221),
    ("B1 label row3 'y'", 88, 135, 221, 252),
    ("B1 col1 header", 133, 175, 132, 155),
    ("B1 col2 header", 173, 215, 132, 155),
    ("B1 col1 row1 val", 133, 175, 157, 189),
    ("B1 col2 row1 val", 173, 215, 157, 189),
    ("B1 col3 row1 val", 213, 255, 157, 189),
    ("B2 col X8 row1 val (yellow)", 418, 462, 292, 328),
]
S = 4
chars = ' .:-=+*%#@'
for (title, x0, x1, y0, y1) in REGS:
    sub = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
    la = np.asarray(sub).astype(float)
    lu = 0.299 * la[:, :, 0] + 0.587 * la[:, :, 1] + 0.114 * la[:, :, 2]
    print(f"### {title}  x{x0}..{x1} y{y0}..{y1}")
    for y in range(0, lu.shape[0], S * 2):
        line = ''
        for x in range(0, lu.shape[1], S):
            blk = lu[y:y + S, x:x + S]
            v = blk.min()
            idx = int(np.clip((150 - v) / 150 * 9.99, 0, 9))
            line += chars[idx]
        print("    " + line)
    print()
