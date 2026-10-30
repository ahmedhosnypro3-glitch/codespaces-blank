import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
RED = (r > g + 40) & (r > b + 40)


def dump(y0, y1, x0, x1, title, mask=None):
    if mask is None:
        mask = ~((abs(r - 254) < 6) & (abs(g - 255) < 6) & (abs(b - 253) < 6)) & \
               ~((abs(r - 233) < 8) & (abs(g - 233) < 8) & (abs(b - 231) < 10))
    print(f"### {title}")
    print("      " + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(x0, x1)))
    for y in range(y0, y1):
        line = ''
        for x in range(x0, x1):
            c = '#'
            if not mask[y, x]:
                c = '.'
            line += c
        print(f"{y:4d}| {line}")
    print()


print("### TRAIN BOX (blue fill removed -> white text only)")
notblue = ~BLUE
dump(92, 130, 88, 172, "Train label", notblue)
print("### TEST BOX (blue fill removed -> white text only)")
dump(92, 130, 792, 878, "Test label", notblue)

print("### bands 2/3 label-box check: ink in x88..175 and x792..878 per band")
for (y0, y1) in ((265, 390), (402, 528)):
    for (x0, x1, tag) in ((88, 175, "train-label x-band"), (792, 878, "test-label x-band")):
        seg = ~((abs(r[y0:y1, x0:x1] - 254) < 6) & (abs(g[y0:y1, x0:x1] - 255) < 6) & (abs(b[y0:y1, x0:x1] - 253) < 6)) & \
              ~((abs(r[y0:y1, x0:x1] - 233) < 8) & (abs(g[y0:y1, x0:x1] - 233) < 8) & (abs(b[y0:y1, x0:x1] - 231) < 10))
        print(f"  y{y0}..{y1} {tag}: non-bg px = {int(seg.sum())}")
