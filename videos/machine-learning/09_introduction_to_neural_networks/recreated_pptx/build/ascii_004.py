"""ASCII colour maps of the ORIGINAL slide_004.jpg for structural reading."""
from PIL import Image
import numpy as np

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
P = 72.0


def cls(px):
    r, g, b = px
    if r > 238 and g > 238 and b > 225:
        return "."
    if r > 90 and r - g > 45 and r - b > 45:
        return "R"
    if g > 80 and g - r > 35 and g - b > 35:
        return "G"
    if b > 90 and b - r > 45 and b - g > 35:
        return "B"
    if r > 150 and g > 120 and b < 120:
        return "r"
    if max(r, g, b) < 140:
        return "#"
    return "+"


def amap(tag, x0, x1, y0, y1, sx=2, sy=2):
    print(f"--- {tag}: x {x0:.2f}-{x1:.2f} y {y0:.2f}-{y1:.2f} (sample {sx}px) ---")
    header = "     " + "".join(str(int((x0 + i * sx / P) * 10) % 10) for i in range(0, max(1, (int((x1 - x0) * P) - sx + 1)//sx + 1)))
    print(header)
    nx = int((x1 - x0) * P)
    for j in range(0, int((y1 - y0) * P), sy):
        y = int(round(y0 * P)) + j
        xs = [min(int(round(x0 * P)) + i * sx, nx - 1) for i in range(0, nx, sx)]
        line = "".join(cls(a[y, x]) for x in xs)
        print(f"{y0 + j/P:5.2f} {line}")
    print()


amap("P2 Error equation + limit", 1.00, 5.10, 3.40, 4.12, 2, 2)
amap("P3 gradient equation + limit", 6.95, 10.70, 5.30, 6.10, 2, 2)
amap("mint box equation + limit", 1.05, 6.75, 6.15, 6.95, 3, 2)
amap("centre arrow + rule", 6.35, 8.00, 6.38, 6.70, 2, 1)
amap("P2 clause start (underline?)", 4.95, 7.05, 3.40, 4.02, 2, 2)
