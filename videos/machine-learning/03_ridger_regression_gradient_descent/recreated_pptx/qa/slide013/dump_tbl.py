import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)

bg = ((abs(im[:, :, 0] - 254) < 6) & (abs(im[:, :, 1] - 255) < 6) & (abs(im[:, :, 2] - 253) < 6)) | \
     ((abs(im[:, :, 0] - 233) < 8) & (abs(im[:, :, 1] - 233) < 8) & (abs(im[:, :, 2] - 231) < 10))
ink = ~bg
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
RED = (r > g + 40) & (r > b + 40)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)


def dump(y0, y1, x0, x1, title):
    print(f"### {title}: y{y0}..{y1} x{x0}..{x1}")
    print("      " + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(x0, x1)))
    for y in range(y0, y1):
        line = ''
        for x in range(x0, x1):
            c = '#' if ink[y, x] else '.'
            if c == '#':
                if YEL[y, x]:
                    c = 'Y'
                elif RED[y, x]:
                    c = 'R'
                elif BLUE[y, x]:
                    c = 'B'
                else:
                    c = 'K'
            line += c
        print(f"{y:4d}| {line}")
    print()


dump(130, 140, 88, 135, "TRAIN1 top border + label-col header area")
dump(133, 156, 88, 215, "TRAIN1 header row")
dump(156, 192, 88, 215, "TRAIN1 data row 1")
dump(192, 224, 88, 215, "TRAIN1 data row 2")
dump(224, 256, 88, 215, "TRAIN1 data row 3")
