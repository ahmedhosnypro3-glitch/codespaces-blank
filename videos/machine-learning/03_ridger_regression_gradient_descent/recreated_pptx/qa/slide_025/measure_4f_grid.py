import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(axis=2); mn = a.min(axis=2)

def cls(y, x):
    r, g, b = R[y, x], G[y, x], B[y, x]
    if r > 245 and g > 245 and b > 245:
        return "W"
    if abs(r-233) < 12 and abs(g-233) < 12 and abs(b-231) < 12:
        return "."
    if r - g > 60 and r - b > 60:
        return "R"
    if b - r > 100 and b - g > 80:
        return "B"
    if mx[y,x] - mn[y,x] > 45:
        if r >= b:
            return "#"          # warm jet (red/yellow)
        return "o"              # cool jet (cyan/blue/green)
    if mx[y,x] < 90:
        return "K"
    return "-"

QUADS = {"TL": (55, 105, 412, 305), "TR": (468, 105, 905, 305),
         "BL": (52, 295, 475, 540), "BR": (465, 295, 905, 540)}
step = 4
for name, (x0, y0, x1, y1) in QUADS.items():
    print("=== %s  x%d..%d y%d..%d  (each char = %dx%d px block) ===" % (name, x0, x1, y0, y1, step, step))
    print("     " + "".join(str((x//step) % 10) if x % (step*5) == 0 else " " for x in range(x0, x1)))
    for y in range(y0, y1, step):
        print("%4d %s" % (y, "".join(cls(y, x) for x in range(x0, x1, step))))
