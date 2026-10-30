import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
ro = np.asarray(O).astype(int)

x0, x1, y0, y1 = 505, 625, 265, 392


def runs(mask):
    out = []
    i = 0
    n = len(mask)
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


print("band-2 W box interior: exact ink runs (K=black, R=red), x505..624 y265..391")
for y in range(y0, y1):
    row = ro[y, x0:x1]
    k = (row[:, 0] < 110) & (row[:, 1] < 110) & (row[:, 2] < 110)
    r = (row[:, 0] > 110) & (row[:, 1] < 80) & (row[:, 2] < 80)
    kr = runs(k)
    rr = runs(r)
    # only interior (exclude border columns 505-506 and 623-624)
    kr = [t for t in kr if not (t[1] <= 506 or t[0] >= 622)]
    rr = [t for t in rr if not (t[1] <= 506 or t[0] >= 622)]
    if kr or rr:
        print(f"y{y:4d} K={kr} R={rr}")
