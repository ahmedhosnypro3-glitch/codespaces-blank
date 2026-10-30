import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
ro = np.asarray(O).astype(int)


def runs(mask, x0):
    out = []
    i, n = 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            out.append((i + x0, j + x0))
            i = j + 1
        else:
            i += 1
    return out


for tag, (y0, y1) in (("B1", (126, 254)), ("B3", (402, 530))):
    print(f"=== {tag} W box interior runs ===")
    for y in range(y0, y1):
        row = ro[y, 505:625]
        k = (row[:, 0] < 110) & (row[:, 1] < 110) & (row[:, 2] < 110)
        r = (row[:, 0] > 110) & (row[:, 1] < 80) & (row[:, 2] < 80)
        kr = [t for t in runs(k, 505) if not (t[1] <= 506 or t[0] >= 622)]
        rr = [t for t in runs(r, 505) if not (t[1] <= 506 or t[0] >= 622)]
        if kr or rr:
            print(f"y{y:4d} K={kr} R={rr}")
    print()
