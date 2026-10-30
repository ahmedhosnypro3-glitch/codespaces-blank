import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
ra = np.asarray(R).astype(int)
s = R.size[1] / 540.0


def px(x, y):
    return ra[int(y * s), int(x * s)]


x0, x1, y0, y1 = 505, 625, 265, 392
print("RENDER band-2 W box interior x505..624 y265..391 — R=red, K=black, .=other")
for y in range(y0, y1):
    row = []
    for x in range(x0, x1):
        r, g, b = px(x, y)
        if r > 110 and g < 80 and b < 80:
            row.append("R")
        elif r < 110 and g < 110 and b < 110:
            row.append("K")
        else:
            row.append(".")
    print(f"{y:4d}| " + "".join(row))
