import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
ro = np.asarray(O).astype(float)
lum = 0.299 * ro[:, :, 0] + 0.587 * ro[:, :, 1] + 0.114 * ro[:, :, 2]

for tag, cols, (y0, y1) in (
    ("B1", (564, 565, 566, 584, 585, 586, 587), (126, 252)),
    ("B2", (564, 565, 566, 611, 612, 613), (265, 390)),
    ("B3", (564, 565, 566, 610, 611, 612, 613), (402, 527)),
):
    print(f"=== {tag} bracket-column y-extents (lum<190) ===")
    for x in cols:
        ys = [y for y in range(y0, y1) if lum[y, x] < 190]
        if ys:
            # contiguous runs
            runs = []
            s = p = ys[0]
            for y in ys[1:]:
                if y == p + 1:
                    p = y
                else:
                    runs.append((s, p)); s = p = y
            runs.append((s, p))
            print(f"x{x:4d}: runs={runs}")
        else:
            print(f"x{x:4d}: none")
    print()
