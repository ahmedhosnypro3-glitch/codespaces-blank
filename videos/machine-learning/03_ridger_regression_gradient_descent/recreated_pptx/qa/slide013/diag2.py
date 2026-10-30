import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_1-1.png").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(int)
lum = 0.299 * ra[:, :, 0] + 0.587 * ra[:, :, 1] + 0.114 * ra[:, :, 2]
r_, g_, b_ = ra[:, :, 0], ra[:, :, 1], ra[:, :, 2]
BLUE = (b_ > r_ + 60) & (b_ > 100) & (g_ < r_ + 30)
YEL = (r_ > 235) & (g_ > 200) & (b_ < 170) & (r_ - b_ > 90)


def dump(fy0, fy1, fx0, fx1, title, extra=None):
    y0, y1, x0, x1 = int(fy0 * s), int(fy1 * s), int(fx0 * s), int(fx1 * s)
    print(f"### {title} (frame y{fy0}..{fy1} x{fx0}..{fx1})")
    for y in range(y0, y1):
        line = ''
        for x in range(x0, x1):
            c = '#'
            if BLUE[y, x]:
                c = 'B'
            elif YEL[y, x]:
                c = 'Y'
            elif lum[y, x] < 205:
                c = '#'
            elif lum[y, x] < 232:
                c = '+'
            else:
                c = '.'
            line += c
        print(f"{int(y/s):4d}| {line}")
    print()


dump(126, 252, 505, 626, "RENDER W BOX B1")
dump(296, 330, 505, 626, "RENDER W BOX B2 top")
