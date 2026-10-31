"""Fine structure of the bottom-left equation box: strict ink classification."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
a = np.asarray(Image.open(P).convert("RGB")).astype(int)


def strict(c):
    r, g, b = c
    if r - max(g, b) > 55 and r > 130:
        return "R"
    if r < 120 and g < 120 and b < 120:
        return "#"
    if r > 225 and r - b > 6:
        return "."
    if abs(r - g) < 25 and abs(g - b) < 25:
        return "-"   # neutral gray (bg or fill)
    return " "


def amap(x0, x1, y0, y1, step=1, label=""):
    print(f"--- {label} x{x0}-{x1} y{y0}-{y1} (step {step}) ---")
    for y in range(y0, y1, step):
        line = "".join(strict(tuple(a[y, x])) for x in range(x0, x1, step))
        print(f"{y:4d} {line}")


amap(300, 420, 455, 510, 1, "BL box right half")
print()
for lbl, pt in [("band", (330, 460)), ("band2", (330, 470)), ("band3", (330, 500)),
                ("row1 text", (360, 468)), ("row2 text", (360, 486)),
                ("box fill", (200, 463)), ("box fill2", (410, 500)),
                ("prefix", (150, 480)), ("outside bg", (95, 480))]:
    print(lbl, pt, tuple(a[pt[1], pt[0]]))
