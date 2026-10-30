# probe62_ascii_map.py — 1px-per-char ink-class map of the slide 009 annotation
# corridors, read directly off the ORIGINAL frame.
import sys
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def classify(y, x):
    R, G, B = r[y, x], g[y, x], b[y, x]
    if R > 200 and 25 < G < 75 and 45 < B < 95: return "D"   # big red disc
    if R > 150 and R - G > 70 and R - B > 55 and G < 75 and B < 75: return "R"  # red core
    if R > 120 and R - G > 45 and R - B > 30 and G < 110 and B < 110: return "r"  # red halo
    if R > 200 and 90 <= G < 185 and B < 80: return "O"      # orange
    if R > 195 and 140 < G < 230 and 140 < B < 235 and R - B > 10 and R - G > 10: return "p"  # rose
    if B > 110 and R < 100 and G < 100: return "B"           # blue
    if R < 130 and G < 130 and B < 130: return "#"           # dark ink / navy
    return "."

WINDOWS = {
    "LEFT":  (150, 300, 115, 310),   # x0,x1,y0,y1
    "RIGHT": (560, 720, 115, 350),
}

out = []
for name, (x0, x1, y0, y1) in WINDOWS.items():
    out.append(f"===== {name} cols x{x0}..{x1-1} rows y{y0}..{y1-1} =====")
    header = "     " + "".join(str((x0 + i) // 100 % 10) if (x0 + i) % 10 == 0 else ("|" if (x0 + i) % 5 == 0 else " ") for i in range(x1 - x0))
    header2 = "     " + "".join(str((x0 + i) // 10 % 10) if (x0 + i) % 10 == 0 else ("|" if (x0 + i) % 5 == 0 else " ") for i in range(x1 - x0))
    out.append(header)
    out.append(header2)
    for y in range(y0, y1):
        row = "".join(classify(y, x) for x in range(x0, x1))
        out.append(f"{y:4d} {row}")

text = "\n".join(out)
print(text)
with open("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/probe62_ascii_map.txt", "w") as f:
    f.write(text + "\n")
